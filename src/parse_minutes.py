"""Stage A deterministic parser for IVGID Board of Trustees minutes.

Extracts motions, vote tallies, media timestamps and public-comment metadata
from minutes PDFs using structural parsing only — no LLM calls anywhere in
this module (Stage B, the LLM fallback for lines Stage A misses, is a later
step and must never silently overwrite these results; spec §2.3).

Contract with the spec:
- Every emitted record carries ``provenance: {type: "pdf", file_id, page}``
  (spec §2.4, §2.7 rule 7). Records cannot be constructed without it, and
  :func:`validate` re-checks the whole output.
- Contradictions are detected, never resolved (spec §2.6). A vote block
  whose stated count disagrees with the parsed name list is emitted with
  ``flags: ["tally_mismatch"]`` and both values; a motion with no
  ``Moved By`` line is flagged ``missing_mover``. Nothing is inferred.
- Public comment (legal-footing-v2 §3, §4d; spec §2.7 rule 4): commenters
  have no defamation privilege under NRS 241.0353(3), so comment regions are
  segmented and excluded from all parsing. Output carries only
  ``{topic, commenter_type}`` per comment — never the verbatim text, never a
  private commenter's name. Officials in motion records are named in full
  (absolutely privileged under NRS 241.0353(1)).

Structural hazards handled (observed in the real fixtures):
- Wrapped tallies: counts are right-aligned and merge into the name list;
  when the list wraps, the count lands mid-block. Vote blocks are fully
  reassembled across lines and pages before any parsing.
- Kerning splits ("B y Trustee", "G ENERAL BUSINESS") — labels are matched
  space-insensitively; raw text is kept verbatim for provenance.
- Repeated per-page header/footer boilerplate is stripped before parsing;
  the printed ``-N-`` header number is asserted against the PDF page and
  mismatches are flagged.
- Scanned pages (no text layer) are reported in ``unparseable_pages``,
  never silently skipped.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field, asdict
from typing import Any, Optional

import pdftext

# Pages with fewer characters than this cannot be parsed (scanned or empty).
MIN_PARSEABLE_CHARS = 20

# Safety bound when assembling a vote block that never terminates. Amendment
# motions carry embedded revision text and legitimately run past 30 lines
# (observed: ~32 body lines), so the guard is generous; a runaway block is
# still cut off and flagged rather than swallowing the document.
MAX_MOTION_BLOCK_LINES = 60

# Outcome terminator variants observed across eras: the structured era
# writes "MOTION PASSED"/"MOTION FAILED", some 2025 clerks write "MOTION
# PASSES", the Audit Committee writes "MOTION CARRIED". A bare "MOTION"
# line (outcome word lost, seen in Audit Committee minutes) terminates the
# block but yields no outcome — flagged `truncated_outcome`, never guessed.
_OUTCOME_TERMINATORS = (
    ("MOTIONPASSED", "passed"),
    ("MOTIONPASSES", "passed"),
    ("MOTIONCARRIED", "passed"),
    ("MOTIONFAILED", "failed"),
    ("MOTIONFAILS", "failed"),
)

_VOTE_SECTIONS = ("YEAS", "NAYS", "ABSTAIN", "ABSENT")
_SECTION_TO_TALLY_KEY = {
    "YEAS": "aye",
    "NAYS": "nay",
    "ABSTAIN": "abstain",
    "ABSENT": "absent",
}

# One general rule, not an enumeration of variants: the words "media" and
# "time stamp"/"timestamp" in either order (media optional), any case,
# optionally space-separated or fused, an optional -/–/: separator, then one
# or two H:MM:SS or HH:MM:SS values, with or without parentheses. Observed
# clerk forms include "Media Timestamp (00:12:15 - 00:31:03)",
# "Media Timestamp 02:00:34", "Timestamp Media 00:18:58",
# "MEDIA TIMESTAMP 00:43:15", "Time Stamp 00:13:59",
# "Media Timestamp - 02:45:36", "(Media Timestamp 1:20:55 - 1:21:03)" and
# the fused "Media Timestamp1:21:05". `end` is None for rangeless forms.
_MEDIA_TIMESTAMP_RE = re.compile(
    r"\b(?:media\s*)?time\s*stamp(?:s)?(?:\s*media)?"
    r"\s*[-–—:]?\s*"
    r"\(?\s*(\d{1,2}:\d{2}:\d{2})"
    r"(?:\s*[-–—]\s*(\d{1,2}:\d{2}:\d{2}))?\s*\)?",
    re.IGNORECASE,
)
_HEADER_RE = re.compile(
    r"IVGID\s*Board\s*of\s*Trustees\s*-\s*(\d+)\s*-\s*Meeting\s*Minutes", re.IGNORECASE
)
def _kt(word: str) -> str:
    """Kerning-tolerant regex for a keyword: extraction sometimes splits a
    word after its first letter ("B y", "M oved"), so allow whitespace
    between every character."""
    return r"\s*".join(re.escape(c) for c in word)


# Mover/seconder attribution, searched over the reassembled pre-vote segment
# (never a single line — clauses wrap across lines and pages). Name captures
# are bounded at 45 characters: attribution names are short role+surname
# strings, and the bound stops a match from swallowing sentence text.
#
# Full clause: "Moved By X, Seconded by Y" with observed separator variants
# "," / ";" / none, optional colon after "by", optional "Moved" (a kerned
# line can open with bare "B y"), and "Second by" for "Seconded by".
_FULL_MOVER_RE = re.compile(
    rf"(?<![A-Za-z])(?:{_kt('Motion')}\s+)?(?:{_kt('Moved')}\s+)?{_kt('By')}\s*:?\s+"
    rf"([^,;:.]{{1,45}}?)[,;]?\s+"
    rf"{_kt('Second')}(?:{_kt('ed')})?\s+{_kt('by')}\s*:?\s+([^,;]{{1,45}}?)(?=[.;,]|$)",
    re.IGNORECASE,
)
# Mover alone (no seconder clause). Requires the literal "Moved" so prose
# like "was moved to a future meeting" cannot match; the name stays on the
# mover's own line (searched per line) so a following sentence is not
# swallowed.
_MOVED_BY_RE = re.compile(
    rf"(?<![A-Za-z]){_kt('Moved')}\s+{_kt('By')}\s*:?\s+([^,;:.]{{1,45}})",
    re.IGNORECASE,
)
# Seconder recorded on its own, possibly in prose ("The motion was seconded
# by Trustee Jezycki." / "Motion Seconded by X") or wrapped onto the next
# line. The prose lead-in is part of the match so excision leaves no debris.
_SECONDED_RE = re.compile(
    rf"(?<![A-Za-z])(?:(?:the\s+)?motion\s+was\s+|motion\s+)?"
    rf"{_kt('Second')}(?:{_kt('ed')})?\s+{_kt('by')}\s*:?\s+"
    r"([^,;.]{1,45}?)(?=[.;,]|$)",
    re.IGNORECASE,
)


def _kti(word: str) -> str:
    """Kerning-tolerant AND case-insensitive keyword regex, for patterns
    whose name capture must stay case-sensitive (so re.IGNORECASE on the
    whole pattern is not an option)."""
    return r"\s*".join(f"[{c.upper()}{c.lower()}]" for c in word if c.isalpha())


# The "MOTION By <name> to <verb>…" label form (2025 transitional): the name
# is the run of capitalised words after "By".
_LEADING_BY_RE = re.compile(
    rf"^\s*(?:{_kti('Moved')}\s+)?{_kti('By')}\s*:?\s+"
    r"((?:[A-Z][\w.'’-]*\s+)*[A-Z][\w.'’-]*)"
)
# An amendment motion announces itself with parliamentary language.
_AMENDMENT_RE = re.compile(r"^\s*to\s+(?:modify|amend)\s+the\s+motion", re.IGNORECASE)
# An arbitrary labelled introducer for an orphan vote block ("QUESTION: All
# in favor of…"). A decision block is defined by its vote structure, not by
# its opening word — any word+colon line can introduce one.
_INTRODUCER_RE = re.compile(r"^\s*([A-Z][A-Za-z ]{1,24}):")
_NON_INTRODUCER_WORDS = {"YEAS", "NAYS", "ABSTAIN", "ABSENT", "MOTION"}
# Narrative motion inside a structured-era document: "Trustee Noble made a
# Motion to approve …". Only captured when a real vote block follows, so
# agenda headings are never mistaken for motions.
_NARRATIVE_RE = re.compile(
    r"((?:[A-Z][\w.'’-]*\s+)+)[Mm]ade\s+a\s+[Mm]otion\s+"
)


# Agenda-item association (spec §2.4 `items[]`). Numbered items look like
# "E.1 (For Possible Action) Approve and Authorize …"; lettered sections like
# "G. MEETING MINUTES (For possible Action)". Audit Committee minutes carry
# no numbered items at all, so a motion there associates with its section —
# both forms are verbatim document structure, never inferred.
# "E.1", "E.1.2" and the lettered sub-item form "E.1.A" the clerks use for
# a public hearing's parts. Without the trailing letter, "E.1.A Review …"
# reads as item E.1 with a title beginning "A Review …", colliding with the
# real E.1 in the same meeting.
_ITEM_NUMBER_RE = re.compile(r"^\s*([A-Z]\.\d+(?:\.\d+)*(?:\.[A-Z])?)[.)]?\s*(.*)$")
# The minutes body ends at adjournment; everything after it is appended
# correspondence and staff attachments, whose lines can look exactly like
# item headings ("H.1. Employee Beach Access — Supportive" is a line from an
# emailed talking-points note, not an agenda item). The skeleton stops there.
_ADJOURNMENT_RE = re.compile(r"\badjourn", re.IGNORECASE)
# A line left dangling mid-item-reference: ends on "Item"/"Items" or on an
# item number. The next line continuing that list is not a heading.
_ITEM_LIST_TAIL_RE = re.compile(
    r"(?:\bitems?|\b[A-Z]\.\d+)\s*[.,;]*\s*(?:and\s*)?[.,;]*\s*$", re.IGNORECASE
)
_SECTION_NUMBER_RE = re.compile(r"^\s*([A-Z])[.)]\s*(.*)$")
# The procedural action marker is a Nevada open-meeting annotation on the
# heading, not part of the item's title.
_ACTION_MARKER_RE = re.compile(r"\((?:not\s+)?for\s+possible\s+action\)", re.IGNORECASE)
_URL_RE = re.compile(r"https?://", re.IGNORECASE)
# A wrapped item title runs over several lines; the bound stops a heading
# with no following structural boundary from swallowing the meeting.
MAX_ITEM_TITLE_LINES = 12


# After the item's title the clerk writes a separate sentence pointing at the
# recording ("Item E.3. Board and Staff discussion can be viewed in its
# entirety at", "Full staff report and Board discussion for Item E.1. can be
# viewed/heard at:", "…is available to be viewed/heard at:"). Title assembly
# already stops at the URL itself, but the sentence introducing it is not a
# title. The invariant across every observed phrasing is the clause "be" +
# a media verb; the rule is that one, not the phrasings.
_MEDIA_REFERENCE_RE = re.compile(
    r"\bbe\s+(?:viewed|heard|watched|listened)"
    r"(?:\s*/\s*(?:viewed|heard|watched|listened))*\b",
    re.IGNORECASE,
)
# The same sentence, truncated wherever title assembly stopped: with the URL
# on the following line the title can end "… can be", "… is available to be"
# or "… is available", the verb never reaching it. Recognised by the last
# sentence of the title reading like a media reference rather than by
# enumerating the points it can be cut at. "Available" needs corroboration
# because it occurs in ordinary titles ("Capital Funds Available for …");
# a bare trailing auxiliary never does.
_TRUNCATED_MEDIA_RE = re.compile(
    r"\b(?:viewed|heard|watched|listened)\b"
    r"|\bavailable\b(?=[\s\S]*\b(?:at|to|be)\b)"
    r"|\bavailable\s*$"
    r"|\bbe\s*$",
    re.IGNORECASE,
)
# A sentence boundary is a period or close-paren before whitespace — except
# the period ending an item reference ("Item E.3."), which is mid-sentence.
_SENTENCE_BOUNDARY_RE = re.compile(r"(?:(?<!\b[A-Z]\.\d)\.|\))(?=\s)")


def _trim_media_reference(text: str) -> str:
    """Cut a title at the sentence boundary before a media-reference clause.

    The title ends where the sentence pointing at the recording begins, so
    the whole of that sentence is dropped however it is worded.
    """
    boundaries = [b.end() for b in _SENTENCE_BOUNDARY_RE.finditer(text)]
    match = _MEDIA_REFERENCE_RE.search(text)
    if match:
        target = match.start()
    else:
        # No complete clause: check whether the title's last sentence is a
        # truncated one.
        last = boundaries[-1] if boundaries else 0
        if not _TRUNCATED_MEDIA_RE.search(text[last:]):
            return text
        target = last
    cut = 0
    for boundary in boundaries:
        if boundary <= target:
            cut = boundary
    trimmed = text[:cut].strip() if cut else text[:target].strip()
    # Never trade a real title for an empty one.
    return trimmed or text


def _clean_title(text: str) -> str:
    """Normalise a heading into a title: drop the "(For possible Action)"
    annotation, cut any trailing media-reference sentence, squeeze
    whitespace, rejoin wrap-hyphenated words and strip separator debris.
    Words, punctuation and case are otherwise untouched."""
    text = _ACTION_MARKER_RE.sub(" ", text)
    text = re.sub(r"\s+", " ", text)
    text = _fix_wrap_hyphens(text)
    text = _trim_media_reference(text)
    text = re.sub(r"\s+([,;:.])", r"\1", text)  # excising the marker leaves " ."
    return text.strip(" -–—.,;:")


def _clean_name(name: str) -> str:
    """Normalise an extracted attribution name: squeeze whitespace, strip
    stray separators, and repair kerning splits inside the name — a lone
    uppercase letter glued back onto its lowercase continuation
    ("H oman" -> "Homan", "T rustee" -> "Trustee"). "A" and "I" are excluded
    because they are legitimate one-letter words."""
    name = re.sub(r"\s+", " ", name).strip(" .,:;")
    return re.sub(r"\b([B-HJ-Z])\s+([a-z]{2,})", r"\1\2", name)
# The clerk's line announcing that a named member of the public spoke. The
# continuation varies by clerk and by year — "is transcribed below:", "is as
# follows:", "are as follows:", "regarding <subject>.", "did not respond
# when called upon." — so only the invariant opening is matched. Requiring
# any one continuation (as this did) segmented one document in the archive
# and left the rest of the verbatim comment text in the parsing stream.
# The name after "by" is deliberately never captured.
_COMMENT_MARKER_RE = re.compile(
    r"Public\s+comments?\s+provided\s+by\b",
    re.IGNORECASE,
)
_FOOTER_PATTERNS = (
    "fiscally responsible community partner",
    "oriented recreation programs and facilities",
    "893 Southwood Boulevard",
    "www.yourtahoeplace.com",
)
_INT_RE = re.compile(r"\b\d+\b")


# A pure attribution line — "Motion by X, Seconded by Y." with nothing else
# on the line — belongs to the block above it and must not start a new one.
_ATTRIBUTION_LINE_RE = re.compile(
    rf"^\s*{_kt('Motion')}\s+(?:{_kt('Moved')}\s+)?{_kt('by')}\s*:?\s+[^,;:]{{1,45}}[,;]?\s+"
    rf"{_kt('Second')}(?:{_kt('ed')})?\s+{_kt('by')}\s*:?\s+[^,;:]{{1,45}}\.?\s*$",
    re.IGNORECASE,
)


def _label_kind(text: str) -> Optional[str]:
    """Which motion-label form starts at this line, if any.

    - "colon":       MOTION: to Approve …        (structured era)
    - "passive":     MOTION WAS MADE TO approve … (Audit Committee)
    - "mover_label": MOTION By X … / MOTION Moved by X: … (2025 transitional)

    A full-line attribution clause ("Motion by X, Seconded by Y.") is not a
    label — it is the mover line of the block above it.
    """
    dk = _dekern(text)
    if _terminator(dk) is not None:
        return None
    if dk.startswith("MOTION:"):
        return "colon"
    if dk.startswith("MOTIONWASMADE"):
        return "passive"
    if dk.startswith("MOTIONBY") or dk.startswith("MOTIONMOVEDBY"):
        if _ATTRIBUTION_LINE_RE.match(text):
            return None
        return "mover_label"
    return None


def _terminator(dk: str) -> Optional[tuple[Optional[str], bool]]:
    """Is this de-kerned line an outcome terminator?

    Returns (outcome, truncated): a known variant maps to "passed"/"failed";
    a line that is exactly "MOTION" is a truncated terminator (outcome None,
    truncated True). Returns None when the line is not a terminator.
    """
    # Tolerate one stray leading letter — margin noise sometimes glues onto
    # the terminator line ("D MOTION PASSED" -> "DMOTIONPASSED").
    for candidate in (dk, dk[1:] if dk[:1].isalpha() else dk):
        for prefix, outcome in _OUTCOME_TERMINATORS:
            if candidate.startswith(prefix):
                return outcome, False
        if candidate == "MOTION":
            return None, True
    return None


def _dekern(text: str) -> str:
    """Space-stripped uppercase copy for label matching. Kerning splits
    ("B y", "G ENERAL") and merges ("THEIVGIDBOARD") both collapse to the
    same form. Raw text is never altered — this copy is for matching only."""
    return re.sub(r"\s+", "", text).upper()


@dataclass(frozen=True)
class Provenance:
    """Where a claim came from. Required on every record (spec §2.7 rule 7)."""

    file_id: int
    page: int
    type: str = "pdf"

    def __post_init__(self) -> None:
        if self.type != "pdf":
            raise ValueError(f"unsupported provenance type: {self.type!r}")
        if not isinstance(self.file_id, int) or self.file_id <= 0:
            raise ValueError(f"invalid file_id: {self.file_id!r}")
        if not isinstance(self.page, int) or self.page < 1:
            raise ValueError(f"invalid page: {self.page!r}")


@dataclass
class Motion:
    """One motion block. Name lists are verbatim from the minutes; officials
    are named in full (NRS 241.0353(1) privilege). ``tally`` holds validated
    counts only — where the stated count disagrees with the parsed names the
    entry is None, ``stated`` keeps the printed numbers, and
    ``flags`` carries ``tally_mismatch`` (spec §2.6: detect, don't resolve)."""

    text: str
    mover: Optional[str]
    seconder: Optional[str]
    yeas: list[str]
    nays: list[str]
    abstain: list[str]
    absent: list[str]
    tally: dict[str, Optional[int]]
    stated: dict[str, list[int]]
    outcome: Optional[str]
    provenance: Provenance
    flags: list[str] = field(default_factory=list)
    raw: str = ""
    # "motion" | "amendment" (a motion to modify the motion on the floor) |
    # "amended" (a motion superseded by a following amendment; the recorded
    # vote belongs to its successor).
    kind: str = "motion"
    # Non-failure annotations, kept separate from ``flags`` (which mark
    # parse failures and count against coverage):
    # - no_seconder: mover found; the minutes record no second (procedural
    #   motions, motions that die for lack of a second).
    # - mover_not_recorded: passive "MOTION WAS MADE" style; the minutes do
    #   not name a mover at all.
    # - no_recorded_vote: terminated block with no YEAS/NAYS sections —
    #   normal under NRS 241.035(1)(c), which requires per-member records
    #   only at a member's request (spec §2.2).
    # - superseded_by_amendment: see kind="amended".
    notes: list[str] = field(default_factory=list)
    # The agenda item (or, where the body numbers no items, the lettered
    # section) this motion sits under — verbatim document structure, used to
    # group motions into spec §2.4 ``items[]``. None when the motion appears
    # before any heading.
    item_number: Optional[str] = None
    item_title: Optional[str] = None


@dataclass
class AgendaItem:
    """One heading in the document's agenda skeleton, whether or not it
    produced a motion (spec §2.2: item number, title, disposition).

    Emitted for every heading so a record can say that an item was on the
    agenda and produced nothing — which is a different fact from the item
    not being there at all, and the one spec §2.5's vanishing-item pattern
    depends on. ``number`` is a lettered section ("G") or a numbered item
    ("H.5"); ``page`` is where the heading appears.
    """

    number: Optional[str]
    title: Optional[str]
    page: int


@dataclass
class MediaTimestamp:
    """A clerk-written ``Media Timestamp (HH:MM:SS - HH:MM:SS)`` range —
    human-verified alignment ground truth (spec §2.2). Draft minutes also
    use a single-timestamp form, in which case ``end`` is None."""

    start: str
    end: Optional[str]
    provenance: Provenance
    item_number: Optional[str] = None
    item_title: Optional[str] = None


@dataclass
class PublicComment:
    """Metadata only. By design this record has no field for the commenter's
    name or the comment text: NRS 241.0353(3) withholds privilege from
    public comment, and spec §2.7 rule 4 forbids naming private commenters.
    ``topic`` is the containing agenda-item heading where identifiable."""

    topic: Optional[str]
    commenter_type: str
    provenance: Provenance
    flags: list[str] = field(default_factory=list)


@dataclass
class ParsedMinutes:
    motions: list[Motion]
    media_timestamps: list[MediaTimestamp]
    public_comments: list[PublicComment]
    unparseable_pages: list[int]
    flags: list[str]
    # The agenda skeleton in document order — every heading, including ones
    # that produced no motion.
    items: list[AgendaItem] = field(default_factory=list)
    # Spec §2.7 rule 2: pages built from unapproved minutes must be labelled
    # draft. "draft" | "approved" | None (undetermined — treat as draft
    # downstream rather than assuming approval).
    minutes_status: Optional[str] = None
    # Which signal produced ``minutes_status``: "file_name" (the clerk's own
    # naming, uncorroborated by the document), "document_text" (an extracted
    # DRAFT line), "watermark_noise" (the vertical watermark leaking as
    # single-letter noise), or None when undetermined. Published so a page
    # can show what the status claim rests on.
    minutes_status_basis: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class _BodyLine:
    page: int
    line: int
    text: str
    in_comment: bool = False


def _strip_page_furniture(
    pages: list[pdftext.Page], doc_flags: list[str]
) -> tuple[list[_BodyLine], list[str]]:
    """Remove per-page header/footer boilerplate; verify the printed page
    number in the ``-N-`` header against the PDF page (provenance check).

    Also returns the dropped single-letter noise lines: on draft-watermarked
    documents those stray letters are the vertical DRAFT watermark leaking
    into extraction, which :func:`_minutes_status` uses as a draft signal."""
    body: list[_BodyLine] = []
    noise_letters: list[str] = []
    for page in pages:
        lines = page.text.split("\n")
        # Footer: drop matching lines in the final 6, plus the bare district
        # name line that precedes them (only there — motions mention the
        # district name inline and must not lose it).
        tail_start = max(0, len(lines) - 6)
        keep = []
        for idx, text in enumerate(lines):
            if idx >= tail_start:
                if any(pat in text for pat in _FOOTER_PATTERNS):
                    continue
                if text.strip() == "Incline Village General Improvement District":
                    continue
            keep.append((idx + 1, text))
        # Header: first kept line on pages 2+.
        if keep and page.page_number >= 2:
            match = _HEADER_RE.search(keep[0][1])
            if match:
                printed = int(match.group(1))
                if printed != page.page_number:
                    doc_flags.append(
                        f"header_page_mismatch:pdf_page={page.page_number},"
                        f"printed={printed}"
                    )
                keep = keep[1:]
        for line_number, text in keep:
            # A line consisting of exactly one letter is page-margin noise
            # from extraction (observed as orphan "r"/"a"/"D" lines that
            # corrupt names and vote sections — on draft documents these are
            # the vertical DRAFT watermark). Lone digits are kept — a
            # wrapped tally count could in principle land alone.
            if not text:
                continue
            if len(text.strip()) == 1 and text.strip().isalpha():
                noise_letters.append(text.strip())
                continue
            body.append(_BodyLine(page.page_number, line_number, text))
    return body, noise_letters


def _is_heading(text: str) -> tuple[bool, bool]:
    """(is_heading, is_item). Section headings look like ``C. INITIAL PUBLIC
    COMMENTS``; item headings like ``H.1 (For Possible Action) …``. Matched
    on the de-kerned copy so ``L. G ENERAL BUSINESS`` still matches."""
    dk = _dekern(text)
    if re.match(r"^[A-Z]\.\d", dk):
        return True, True
    if re.match(r"^[A-Z]\.[A-Z]", dk):
        # Section headings are set in capitals. A sentence opening with an
        # initialism ("U.S. as key reasons for the price difference") has the
        # same shape once de-kerned, so the raw text is checked for lowercase
        # up to any trailing annotation — the de-kerned copy is uppercased and
        # cannot answer this.
        head = re.split(r"[(\-–—]", text, maxsplit=1)[0]
        return not re.search(r"[a-z]", head), False
    return False, False


def _mark_comment_regions(
    body: list[_BodyLine], file_id: int
) -> tuple[list[_BodyLine], list[PublicComment]]:
    """Segment public-comment text and emit metadata-only records.

    Two triggers: a section heading containing PUBLIC COMMENT(S), and the
    clerk's marker line "Public comment provided by <name> is transcribed
    below:". Everything inside a region or after a marker (up to the next
    structural boundary) is marked ``in_comment`` and excluded from all
    later parsing, so verbatim comment text cannot leak into any output.
    The name in the marker line is deliberately never captured."""
    comments: list[PublicComment] = []
    marked: list[_BodyLine] = []
    in_region = False
    in_marker_block = False
    current_item_heading: Optional[str] = None

    for bl in body:
        heading, is_item = _is_heading(bl.text)
        dk = _dekern(bl.text)
        if heading:
            in_region = "PUBLICCOMMENT" in dk
            in_marker_block = False
            if is_item:
                current_item_heading = bl.text
            marked.append(bl)
            continue
        # The marker is tested before the timestamp check because clerks
        # routinely write both on one line ("MEDIA TIMESTAMP 00:05:14 -
        # Public Comment provided by Judith …"). Testing the timestamp first
        # treated those as structural and left the commenter's name in the
        # parsing stream. Marking the line as comment does not lose the
        # timestamp: media timestamps are harvested from the whole body,
        # comment regions included.
        if _COMMENT_MARKER_RE.search(bl.text):
            in_marker_block = True
            flags = []
            topic = current_item_heading if not in_region else None
            if topic is None:
                flags.append("topic_unknown")
            comments.append(
                PublicComment(
                    topic=topic,
                    commenter_type="resident",
                    provenance=Provenance(file_id=file_id, page=bl.page),
                    flags=flags,
                )
            )
            marked.append(_BodyLine(bl.page, bl.line, bl.text, in_comment=True))
            continue
        if _MEDIA_TIMESTAMP_RE.search(bl.text):
            # A timestamp line carrying no comment marker is structural, not
            # comment text, and ends the block above it.
            in_marker_block = False
            marked.append(bl)
            continue
        if _label_kind(bl.text) is not None:
            in_marker_block = False
            marked.append(bl)
            continue
        marked.append(
            _BodyLine(bl.page, bl.line, bl.text, in_comment=in_region or in_marker_block)
        )
    return marked, comments


def _title_continues(bl: _BodyLine) -> bool:
    """May this line be part of the item title started above it?

    A title stops at the next structural thing in the document: another
    heading, a motion label, a vote section or outcome line, the clerk's
    media-timestamp/URL pointer lines, or any public-comment text (which
    must never reach output).
    """
    if bl.in_comment:
        return False
    if _is_heading(bl.text)[0] or _label_kind(bl.text) is not None:
        return False
    if _URL_RE.search(bl.text) or _MEDIA_TIMESTAMP_RE.search(bl.text):
        return False
    dk = _dekern(bl.text)
    if _terminator(dk) is not None:
        return False
    return not any(dk.startswith(section) for section in _VOTE_SECTIONS)


def _item_context(
    body: list[_BodyLine],
) -> tuple[
    dict[tuple[int, int], tuple[Optional[str], Optional[str]]],
    list["AgendaItem"],
]:
    """Map every body line to the agenda item it sits under, and return the
    agenda skeleton in document order.

    A numbered item heading ("E.1 …") wins over the lettered section it sits
    in, and a new section clears the current item. Where a body numbers no
    items at all — the Audit Committee format — every motion associates with
    its section heading instead. Both are read verbatim from the document;
    nothing is inferred, and a motion appearing before any heading maps to
    ``(None, None)``.

    The second return value is every heading the document carries, whether
    or not it produced a motion. Without it a record cannot distinguish
    "this item produced no motion" from "this item was never on the agenda"
    — the two look identical, which is a silent inaccuracy and hides the
    spec §2.5 pattern of an item appearing and then not returning.
    """
    context: dict[tuple[int, int], tuple[Optional[str], Optional[str]]] = {}
    section: tuple[Optional[str], Optional[str]] = (None, None)
    item: Optional[tuple[Optional[str], Optional[str]]] = None
    items: list[AgendaItem] = []
    seen: set[tuple[Optional[str], Optional[str]]] = set()

    adjourned = False

    def record(key: tuple[Optional[str], Optional[str]], page: int) -> None:
        if adjourned:
            return
        if key != (None, None) and key not in seen:
            seen.add(key)
            items.append(
                AgendaItem(number=key[0], title=key[1], page=page)
            )

    for index, bl in enumerate(body):
        heading, is_item = _is_heading(bl.text)
        # A consent calendar lists its members inline ("… and Item F.3.
        # Approval of a Donation …", "Items F.1., F.2., F.3., F.4., F.5 /
        # F.6., as submitted."). When that sentence wraps so a number lands
        # at the start of a line it looks exactly like a heading. What marks
        # it as a continuation is the line above ending mid-reference — on
        # the word "Item(s)" or on another item number. A real heading never
        # follows either.
        if is_item and index and _ITEM_LIST_TAIL_RE.search(body[index - 1].text):
            heading = False
        if heading:
            pattern = _ITEM_NUMBER_RE if is_item else _SECTION_NUMBER_RE
            match = pattern.match(bl.text)
            number = match.group(1) if match else None
            remainder = match.group(2) if match else bl.text
            if is_item:
                # Item titles wrap across lines; sections are single-line.
                parts = [remainder]
                for following in body[index + 1 : index + MAX_ITEM_TITLE_LINES]:
                    if not _title_continues(following):
                        break
                    parts.append(following.text)
                item = (number, _clean_title(" ".join(parts)) or None)
                record(item, bl.page)
            else:
                section = (number, _clean_title(remainder) or None)
                item = None
                record(section, bl.page)
                if _ADJOURNMENT_RE.search(section[1] or ""):
                    adjourned = True
        context[(bl.page, bl.line)] = item if item is not None else section
    return context, items


def _fix_wrap_hyphens(text: str) -> str:
    """Rejoin hyphenated tokens split by a line break: after joining lines,
    a wrap leaves the hyphen glued to the preceding word with a space after
    it ("At- Large" -> "At-Large", "Non- Profit" -> "Non-Profit"). Genuinely
    separate hyphen-delimited words ("Items G.1 - G.5") keep a space on
    both sides of the hyphen and are untouched."""
    return re.sub(r"(\w-)\s+(?=\w)", r"\1", text)


def _clean_motion_text(text: str) -> str:
    """Tidy motion text after attribution clauses are excised: no stranded
    colons or semicolons, no duplicated separators, no space before
    punctuation, no leading/trailing separator debris. Words, punctuation
    inside the text, currency and case are untouched."""
    text = re.sub(r"\s+", " ", text)
    text = _fix_wrap_hyphens(text)
    text = re.sub(r"\s+([,;:.])", r"\1", text)  # excision leaves " ;" etc.
    text = re.sub(r"([,;:.])(?:\s*[,;:])+", r"\1", text)  # "; :" -> ";"
    text = re.sub(r"[;,]\s*(?=\.)", "", text)  # ";." -> "."
    text = re.sub(r"\.\s*\.", ".", text)  # ". ." -> "."
    return text.strip().lstrip(";:,. ").strip()


def _strip_block_label(first_line: str, label: str) -> str:
    """Remove the block's opening label from its first line."""
    if label == "colon":
        return re.sub(rf"^\s*{_kt('MOTION')}\s*:\s*", "", first_line, flags=re.IGNORECASE)
    if label == "passive":
        return re.sub(
            rf"^\s*{_kt('MOTION')}\s+{_kt('WAS')}\s+{_kt('MADE')}(?:\s+{_kt('TO')})?:?\s*",
            "",
            first_line,
            flags=re.IGNORECASE,
        )
    if label == "mover_label":
        return re.sub(rf"^\s*{_kt('MOTION')}\s+", "", first_line, flags=re.IGNORECASE)
    if label == "variant":
        return _INTRODUCER_RE.sub("", first_line, count=1).strip()
    return first_line  # narrative: the attribution regex handles the prefix


def _is_name_continuation(line: str) -> bool:
    """Does this line look like the continuation of a wrapped vote name
    list? Name lists are capitalised tokens (plus counts and "and"); a
    prose sentence ("The vote was 1/4 …") is not, and must not leak into a
    vote section."""
    cleaned = _INT_RE.sub("", line)
    words = re.findall(r"[A-Za-z][\w.'’-]*", cleaned)
    if not words:
        return True  # bare count line
    return all(w[0].isupper() or w.lower() == "and" for w in words)


def _parse_vote_section(text: str) -> tuple[list[str], list[int]]:
    """Parse one reassembled vote section ("YEAS: A, B, C 3", possibly
    wrapped with the count mid-list). Returns (names, stated_counts).
    Integers are stripped from name tokens; "None" yields no names."""
    stated = [int(m) for m in _INT_RE.findall(text)]
    cleaned = _INT_RE.sub("", text)
    # Rejoin wrap-hyphenated names AFTER count removal: the right-aligned
    # count can land between the fragment and its continuation
    # ("…, At- 5" / "Large Audit Committee Member Kelly").
    cleaned = _fix_wrap_hyphens(cleaned)
    names: list[str] = []
    for token in cleaned.split(","):
        token = re.sub(r"\s+", " ", token).strip(" .")
        # "None" with up to two stray non-digit characters is a clerk typo
        # ("None t 0" observed); anything that could change a number is not
        # tolerated — digits were already extracted above.
        if not token or re.fullmatch(r"None(?:\s*[^\d\s]{1,2})?", token, re.IGNORECASE):
            continue
        # Clerks write "and" before the final name of a list.
        token = re.sub(r"^and\s+", "", token, flags=re.IGNORECASE)
        names.append(token)
    return names, stated


def _parse_motion_block(
    block: list[_BodyLine],
    file_id: int,
    successor_text: Optional[str] = None,
    intro: Optional[str] = None,
    intro_word: Optional[str] = None,
    item: tuple[Optional[str], Optional[str]] = (None, None),
    prefix: Optional[str] = None,
) -> Motion:
    """Parse one fully reassembled motion block. The block must already span
    all its lines (across page breaks) — votes are never parsed from a
    single line, which is what makes wrapped tallies safe.

    ``successor_text`` is the first line of the next motion block when this
    block was interrupted by one; it identifies amendment chains (a motion
    superseded on the floor by "Motion: To modify the motion …").

    ``intro`` marks blocks captured by their vote structure rather than a
    MOTION label: "variant" (an arbitrary labelled introducer such as
    ``QUESTION:``, with ``intro_word`` carrying the label word) or
    "narrative" ("Trustee X made a motion to …")."""
    flags: list[str] = []
    notes: list[str] = []
    raw = "\n".join(bl.text for bl in block)
    start_page = block[0].page
    label = intro if intro is not None else (_label_kind(block[0].text) or "colon")
    if intro == "variant":
        notes.append(f"label_variant:{intro_word or 'UNKNOWN'}")
    elif intro == "narrative":
        notes.append("narrative_motion")

    # Locate vote-section label lines and the outcome line.
    outcome: Optional[str] = None
    terminated = False
    section_starts: list[tuple[int, str]] = []
    end_idx = len(block)
    for idx, bl in enumerate(block):
        dk = _dekern(bl.text)
        term = _terminator(dk)
        if term is not None:
            outcome, truncated = term
            end_idx = idx
            terminated = True
            if truncated:
                flags.append("truncated_outcome")
            break
        for lab in _VOTE_SECTIONS:
            if dk.startswith(lab):
                section_starts.append((idx, lab))
                break

    # The pre-vote segment: label line through the last line before the
    # first vote section (or the whole block when votes are absent).
    seg_end = section_starts[0][0] if section_starts else end_idx
    seg_lines = [bl.text for bl in block[:seg_end]]
    if seg_lines:
        seg_lines = [_strip_block_label(seg_lines[0], label), *seg_lines[1:]]
        if prefix:
            # The introducing phrase began mid-sentence; restore its subject
            # so the motion text does not open with a bare predicate.
            seg_lines[0] = f"{prefix} {seg_lines[0].lstrip()}"
    # Join with known offsets so per-line matches map to segment positions.
    offsets: list[int] = []
    pos = 0
    for line in seg_lines:
        offsets.append(pos)
        pos += len(line) + 1
    segment = " ".join(seg_lines)

    # Attribution: the clause is the EARLIEST attribution-shaped text in the
    # block — quoted attribution deep inside item-list text must never win
    # over the clause at the block head. Chosen spans are excised from the
    # motion text afterwards.
    mover: Optional[str] = None
    seconder: Optional[str] = None
    spans: list[tuple[int, int]] = []
    if label == "narrative":
        nm = _NARRATIVE_RE.search(segment)
        if nm:
            mover = _clean_name(nm.group(1))
            spans.append(nm.span())
    else:
        candidates: list[tuple[int, str, Optional[str], tuple[int, int]]] = []
        for m in _FULL_MOVER_RE.finditer(segment):
            candidates.append(
                (m.start(), _clean_name(m.group(1)), _clean_name(m.group(2)), m.span())
            )
        if label == "mover_label":
            lead = _LEADING_BY_RE.match(segment)
            if lead:
                candidates.append(
                    (lead.start(), _clean_name(lead.group(1)), None, lead.span())
                )
        for offset, line in zip(offsets, seg_lines):
            # Per line, so a mover's name cannot swallow a following
            # sentence: the name ends on the mover's own line.
            by = _MOVED_BY_RE.search(line)
            if by:
                candidates.append(
                    (
                        offset + by.start(),
                        _clean_name(by.group(1)),
                        None,
                        (offset + by.start(), offset + by.end()),
                    )
                )
        if candidates:
            candidates.sort(key=lambda c: (c[0], c[2] is None))
            _, mover, seconder, span = candidates[0]
            spans.append(span)
    if seconder is None:
        sec = _SECONDED_RE.search(segment)
        if sec and not any(s <= sec.start() < e for s, e in spans):
            seconder = _clean_name(sec.group(1))
            spans.append(sec.span())

    # Motion text = segment minus the excised spans, tidied. A single-word
    # fragment left in front of the attribution ("MOTION: Approve; Moved By
    # X: to Approve …") is a label echo, not motion text — drop it.
    spans.sort()
    pieces: list[str] = []
    cursor = 0
    for s, e in spans:
        if s < cursor:
            continue
        pieces.append(segment[cursor:s])
        cursor = e
    pieces.append(segment[cursor:])
    if spans:
        lead_fragment = pieces[0].strip()
        if len(lead_fragment) <= 15 and re.fullmatch(r"\W*[\w$]+\W*", lead_fragment):
            pieces[0] = ""
    text = _clean_motion_text(" ".join(pieces))

    kind = "motion"
    if _AMENDMENT_RE.match(text):
        kind = "amendment"
    if (
        not terminated
        and not section_starts
        and successor_text is not None
        and _AMENDMENT_RE.match(
            re.sub(
                rf"^\s*{_kt('MOTION')}\s*:?\s*",
                "",
                successor_text,
                flags=re.IGNORECASE,
            )
        )
    ):
        # Superseded on the floor: the following amendment (and the vote
        # recorded after it) replaces this block. Not a parse failure.
        kind = "amended"
        notes.append("superseded_by_amendment")
    elif not terminated:
        flags.append("missing_outcome")

    if mover is None:
        if label in ("passive", "variant"):
            # Passive "MOTION WAS MADE" style and labelled variants like
            # "QUESTION:" (a chair-called vote) name no mover; nothing to
            # extract, so absence is not a parse failure.
            notes.append("mover_not_recorded")
        else:
            flags.append("missing_mover")
    elif seconder is None:
        # Mover found, no second recorded — legitimate for procedural
        # motions and motions that die for lack of a second.
        notes.append("no_seconder")

    # Reassemble each vote section across its full line span, then parse.
    names_by_section: dict[str, list[str]] = {s: [] for s in _VOTE_SECTIONS}
    stated_by_section: dict[str, list[int]] = {s: [] for s in _VOTE_SECTIONS}
    tally: dict[str, Optional[int]] = {v: 0 for v in _SECTION_TO_TALLY_KEY.values()}
    for pos, (idx, section) in enumerate(section_starts):
        next_idx = (
            section_starts[pos + 1][0] if pos + 1 < len(section_starts) else end_idx
        )
        # Wrapped name lists continue across lines, but only lines shaped
        # like name lists — prose after the last section (an outcome
        # narrated in a sentence) must not contaminate the tally.
        section_lines = [block[idx].text]
        for bl in block[idx + 1 : next_idx]:
            if not _is_name_continuation(bl.text):
                break
            section_lines.append(bl.text)
        section_text = " ".join(section_lines)
        section_text = re.sub(
            rf"^\s*{_kt(section)}:?", "", section_text, flags=re.IGNORECASE
        )
        names, stated = _parse_vote_section(section_text)
        names_by_section[section] = names
        stated_by_section[section] = stated
        key = _SECTION_TO_TALLY_KEY[section]
        # Validate, never guess: the parsed name count must match exactly one
        # stated number (or "None" with no/zero stated count). Otherwise the
        # tally stays None and the record is flagged (spec §2.6).
        if not stated:
            tally[key] = len(names)
        elif stated.count(len(names)) == 1:
            tally[key] = len(names)
        else:
            tally[key] = None
            if "tally_mismatch" not in flags:
                flags.append("tally_mismatch")
    if not section_starts:
        tally = {v: None for v in _SECTION_TO_TALLY_KEY.values()}
        if terminated:
            # A terminated motion with no recorded roll call is normal:
            # NRS 241.035(1)(c) requires per-member vote records only at a
            # member's request (spec §2.2 — absence is not a failure).
            notes.append("no_recorded_vote")
        elif kind != "amended":
            flags.append("missing_vote_sections")

    return Motion(
        text=text,
        mover=mover,
        seconder=seconder,
        yeas=names_by_section["YEAS"],
        nays=names_by_section["NAYS"],
        abstain=names_by_section["ABSTAIN"],
        absent=names_by_section["ABSENT"],
        tally=tally,
        stated=stated_by_section,
        outcome=outcome,
        provenance=Provenance(file_id=file_id, page=start_page),
        flags=flags,
        raw=raw,
        kind=kind,
        notes=notes,
        item_number=item[0],
        item_title=item[1],
    )


def _minutes_status(
    minutes_name: Optional[str],
    pages: list[pdftext.Page],
    noise_letters: list[str],
) -> tuple[Optional[str], Optional[str]]:
    """Draft/approved status (spec §2.7 rule 2) and the signal it came from,
    as ``(status, basis)``.

    The basis matters as much as the status. A status read from the clerk's
    file name is uncorroborated by the document itself, and files 1341 and
    1342 show why that is worth publishing: both are named as approved while
    the page carries a visible DRAFT watermark that leaves no extractable
    text and no distinguishing image or vector content. Recording the basis
    lets a page show the reader what the claim rests on instead of asserting
    a status the source appears to contradict.

    Document signals for draft: a standalone uppercase DRAFT (or spaced
    D R A F T) line — the watermark, when it extracts as text — or the
    stray single-letter noise spelling out the vertical DRAFT watermark.
    Prose mentions ("the draft letter") are deliberately not a signal.
    Caveat: a purely image-based watermark leaves no text at all; with no
    file-name signal either, the status stays None (undetermined)."""
    if minutes_name:
        name = minutes_name.lower()
        if "draft" in name:
            return "draft", "file_name"
        if "approved" in name:
            return "approved", "file_name"
    for page in pages:
        for line in page.text.split("\n"):
            if re.fullmatch(r"\s*D\s*R\s*A\s*F\s*T\s*", line):
                return "draft", "document_text"
    if {"d", "r", "a", "f", "t"} <= {c.lower() for c in noise_letters}:
        return "draft", "watermark_noise"
    return None, None


def _subject_prefix(scan: list[_BodyLine], idx: int, match_start: int) -> Optional[str]:
    """The sentence subject preceding a predicate-shaped introducer.

    "Chair Tonking called for a vote …" wraps so that the line the phrase was
    matched on begins mid-sentence, leaving the subject at the end of the
    line above. When nothing precedes the phrase on its own line, the tail of
    the previous line after its last sentence boundary is returned — but only
    when that tail is a short capitalised fragment, which is what a subject
    looks like. Anything longer is prose and is left alone.
    """
    if scan[idx].text[:match_start].strip():
        return None
    if idx == 0:
        return None
    tail = re.split(r"(?<=[.;!?])\s", scan[idx - 1].text)[-1].strip()
    if not tail or len(tail) > 60 or not tail[:1].isupper():
        return None
    return tail


def _find_introducer(
    scan: list[_BodyLine], yeas_idx: int, consumed: set[int]
) -> tuple[int, str, Optional[str], Optional[str]]:
    """Walk back from an orphan YEAS line to the line that introduced the
    decision block: either an arbitrary labelled introducer ("QUESTION: All
    in favor of …") or a narrative motion ("Trustee X made a motion to …").
    Falls back to the YEAS line itself when nothing qualifies. The walk is
    bounded by structural boundaries (headings, consumed blocks, vote
    sections) rather than a short line budget — narrative motion sentences
    legitimately run long. The NEAREST introducer of any form wins: the
    line closest above the vote is the one that called it."""
    for back in range(1, 21):
        idx = yeas_idx - back
        if idx < 0 or idx in consumed:
            break
        text = scan[idx].text
        if _is_heading(text)[0]:
            break
        dk = _dekern(text)
        if _terminator(dk) is not None or any(
            dk.startswith(v) for v in _VOTE_SECTIONS
        ):
            break
        if _NARRATIVE_RE.search(text):
            return idx, "narrative", None, None
        called = re.search(r"called\s+for\s+a\s+vote", text, re.IGNORECASE)
        if called:
            # Chair-called votes ("Chair Tonking called for a vote on the
            # request to remove this item") — recurring clerk phrasing for
            # votes with no formal motion. Unlike a label, this phrase is a
            # predicate, so the subject can sit on the line above it.
            return (
                idx,
                "variant",
                "CALLED FOR A VOTE",
                _subject_prefix(scan, idx, called.start()),
            )
        match = _INTRODUCER_RE.match(text)
        if match and match.group(1).strip().upper() not in _NON_INTRODUCER_WORDS:
            return idx, "variant", match.group(1).strip(), None
    return yeas_idx, "variant", None, None


def parse_minutes(
    pdf_bytes: bytes, file_id: int, minutes_name: Optional[str] = None
) -> ParsedMinutes:
    """Parse an IVGID minutes PDF into structured, provenance-carrying
    records. Deterministic only; anything this misses is Stage B's input.

    ``minutes_name`` is the publishedFiles[] entry name from the CivicClerk
    event, used for draft/approved detection (spec §2.7 rule 2)."""
    doc_flags: list[str] = []
    pages = pdftext.extract_pages(pdf_bytes)
    unparseable = [p.page_number for p in pages if p.char_count < MIN_PARSEABLE_CHARS]
    for page in pages:
        if page.raw_fallback:
            doc_flags.append(f"raw_fallback_page:{page.page_number}")

    parseable = [p for p in pages if p.page_number not in unparseable]
    body, noise_letters = _strip_page_furniture(parseable, doc_flags)
    body, comments = _mark_comment_regions(body, file_id)
    # Agenda-item association, computed after comment segmentation so a
    # title can never absorb public-comment text.
    item_context, agenda_items = _item_context(body)

    def item_at(bl: _BodyLine) -> tuple[Optional[str], Optional[str]]:
        return item_context.get((bl.page, bl.line), (None, None))

    # Media timestamps: collected everywhere, including comment regions —
    # the timestamp itself is structural clerk text, not comment content.
    # A range whose separator dangles at a line break ("… (03:19:07 -")
    # continues on the next line; join before matching. The continuation
    # line alone (bare digits) can never match, so nothing double-counts.
    media = []
    for idx, bl in enumerate(body):
        text = bl.text
        if re.search(r"[-–—]\s*$", text) and idx + 1 < len(body):
            text = text + " " + body[idx + 1].text
        m = _MEDIA_TIMESTAMP_RE.search(text)
        if m:
            media.append(
                MediaTimestamp(
                    start=m.group(1),
                    end=m.group(2),
                    provenance=Provenance(file_id=file_id, page=bl.page),
                    item_number=item_at(bl)[0],
                    item_title=item_at(bl)[1],
                )
            )

    # Motion blocks: assembled only from non-comment lines, from "MOTION:"
    # to the outcome line, across page breaks.
    # Pass 1 — blocks opened by a recognised MOTION label.
    entries: list[tuple[int, Motion]] = []
    consumed: set[int] = set()
    scan = [bl for bl in body if not bl.in_comment]
    i = 0
    while i < len(scan):
        if _label_kind(scan[i].text) is not None:
            block = [scan[i]]
            j = i + 1
            while j < len(scan) and len(block) < MAX_MOTION_BLOCK_LINES:
                if _label_kind(scan[j].text) is not None:
                    break
                block.append(scan[j])
                if _terminator(_dekern(scan[j].text)) is not None:
                    break
                j += 1
            successor = (
                scan[j].text
                if j < len(scan) and _label_kind(scan[j].text) is not None
                else None
            )
            consumed.update(range(i, i + len(block)))
            entries.append(
                (i, _parse_motion_block(block, file_id, successor, item=item_at(scan[i])))
            )
            i = j
        else:
            i += 1

    # Pass 2 — decision blocks defined by their vote structure alone: a
    # YEAS section outside every captured block is a vote the label pass
    # could not see (clerk labelled it QUESTION:, wrote the motion as
    # narrative, etc.). A block that has a vote is captured whatever word
    # introduces it.
    for k, bl in enumerate(scan):
        if k in consumed or not _dekern(bl.text).startswith("YEAS"):
            continue
        start, intro, intro_word, prefix = _find_introducer(scan, k, consumed)
        block = [scan[start]]
        j = start + 1
        while j < len(scan) and len(block) < MAX_MOTION_BLOCK_LINES:
            if j in consumed or _label_kind(scan[j].text) is not None:
                break
            block.append(scan[j])
            if _terminator(_dekern(scan[j].text)) is not None:
                break
            j += 1
        consumed.update(range(start, start + len(block)))
        entries.append(
            (
                start,
                _parse_motion_block(
                    block,
                    file_id,
                    intro=intro,
                    intro_word=intro_word,
                    item=item_at(scan[start]),
                    prefix=prefix,
                ),
            )
        )

    entries.sort(key=lambda e: e[0])
    motions = [m for _, m in entries]

    status, basis = _minutes_status(minutes_name, parseable, noise_letters)
    parsed = ParsedMinutes(
        motions=motions,
        media_timestamps=media,
        public_comments=comments,
        unparseable_pages=unparseable,
        flags=doc_flags,
        items=agenda_items,
        minutes_status=status,
        minutes_status_basis=basis,
    )
    validate(parsed)
    return parsed


def validate(parsed: ParsedMinutes) -> None:
    """Fail hard on any record without valid provenance (spec §2.7 rule 7:
    a claim without provenance fails validation — it never publishes with a
    caveat) and on any public-comment record carrying prose or a name."""
    records: list[Any] = [*parsed.motions, *parsed.media_timestamps, *parsed.public_comments]
    for record in records:
        prov = getattr(record, "provenance", None)
        if not isinstance(prov, Provenance):
            raise ValueError(f"record without provenance: {record!r}")
    for comment in parsed.public_comments:
        payload = set(vars(comment)) - {"topic", "commenter_type", "provenance", "flags"}
        if payload:
            raise ValueError(f"public comment carries extra fields: {payload}")
