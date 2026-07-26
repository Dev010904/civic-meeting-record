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

# Observed separator is an ASCII hyphen in approved minutes but an en-dash
# in draft minutes; drafts also use a single-timestamp form with no range,
# e.g. "Media Timestamp (00:16:31)" — then `end` is None.
_MEDIA_TIMESTAMP_RE = re.compile(
    r"Media\s*Timestamp\s*\(\s*(\d{2}:\d{2}:\d{2})"
    r"(?:\s*[-–—]\s*(\d{2}:\d{2}:\d{2}))?\s*\)",
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
# by Trustee Jezycki.") or wrapped onto the next line.
_SECONDED_RE = re.compile(
    rf"(?<![A-Za-z]){_kt('Second')}(?:{_kt('ed')})?\s+{_kt('by')}\s*:?\s+"
    r"([^,;.]{1,45}?)(?=[.;,]|$)",
    re.IGNORECASE,
)
# The "MOTION By <name> to <verb>…" label form (2025 transitional): the name
# is the run of capitalised words after "By".
_LEADING_BY_RE = re.compile(
    rf"^\s*(?:{_kt('Moved')}\s+)?{_kt('By')}\s*:?\s+"
    r"((?:[A-Z][\w.'’-]*\s+)*[A-Z][\w.'’-]*)"
)
# An amendment motion announces itself with parliamentary language.
_AMENDMENT_RE = re.compile(r"^\s*to\s+(?:modify|amend)\s+the\s+motion", re.IGNORECASE)


def _clean_name(name: str) -> str:
    """Normalise an extracted attribution name: squeeze whitespace, strip
    stray separators, and repair kerning splits inside the name — a lone
    uppercase letter glued back onto its lowercase continuation
    ("H oman" -> "Homan", "T rustee" -> "Trustee"). "A" and "I" are excluded
    because they are legitimate one-letter words."""
    name = re.sub(r"\s+", " ", name).strip(" .,:;")
    return re.sub(r"\b([B-HJ-Z])\s+([a-z]{2,})", r"\1\2", name)
_COMMENT_MARKER_RE = re.compile(
    r"Public\s+comments?\s+provided\s+by\s+.+?\s+is\s+transcribed\s+below",
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


@dataclass
class MediaTimestamp:
    """A clerk-written ``Media Timestamp (HH:MM:SS - HH:MM:SS)`` range —
    human-verified alignment ground truth (spec §2.2). Draft minutes also
    use a single-timestamp form, in which case ``end`` is None."""

    start: str
    end: Optional[str]
    provenance: Provenance


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
) -> list[_BodyLine]:
    """Remove per-page header/footer boilerplate; verify the printed page
    number in the ``-N-`` header against the PDF page (provenance check)."""
    body: list[_BodyLine] = []
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
            # corrupt names and vote sections). Lone digits are kept — a
            # wrapped tally count could in principle land alone.
            if text and not (len(text.strip()) == 1 and text.strip().isalpha()):
                body.append(_BodyLine(page.page_number, line_number, text))
    return body


def _is_heading(text: str) -> tuple[bool, bool]:
    """(is_heading, is_item). Section headings look like ``C. INITIAL PUBLIC
    COMMENTS``; item headings like ``H.1 (For Possible Action) …``. Matched
    on the de-kerned copy so ``L. G ENERAL BUSINESS`` still matches."""
    dk = _dekern(text)
    if re.match(r"^[A-Z]\.\d", dk):
        return True, True
    if re.match(r"^[A-Z]\.[A-Z]", dk):
        return True, False
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
        if _MEDIA_TIMESTAMP_RE.search(bl.text):
            # Timestamp lines are structural, not comment text.
            in_marker_block = False
            marked.append(bl)
            continue
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
        if _label_kind(bl.text) is not None:
            in_marker_block = False
            marked.append(bl)
            continue
        marked.append(
            _BodyLine(bl.page, bl.line, bl.text, in_comment=in_region or in_marker_block)
        )
    return marked, comments


def _dehyphenate_join(lines: list[str]) -> str:
    """Join wrapped lines, rejoining hyphenated word breaks ("Non-\\nProfit"
    -> "Non-Profit"). No other text alteration."""
    out = ""
    for line in lines:
        if not out:
            out = line
        elif out.endswith("-"):
            out += line
        else:
            out += " " + line
    return out


def _parse_vote_section(text: str) -> tuple[list[str], list[int]]:
    """Parse one reassembled vote section ("YEAS: A, B, C 3", possibly
    wrapped with the count mid-list). Returns (names, stated_counts).
    Integers are stripped from name tokens; "None" yields no names."""
    stated = [int(m) for m in _INT_RE.findall(text)]
    cleaned = _INT_RE.sub("", text)
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
) -> Motion:
    """Parse one fully reassembled motion block. The block must already span
    all its lines (across page breaks) — votes are never parsed from a
    single line, which is what makes wrapped tallies safe.

    ``successor_text`` is the first line of the next motion block when this
    block was interrupted by one; it identifies amendment chains (a motion
    superseded on the floor by "Motion: To modify the motion …")."""
    flags: list[str] = []
    notes: list[str] = []
    raw = "\n".join(bl.text for bl in block)
    start_page = block[0].page
    label = _label_kind(block[0].text) or "colon"

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
    segment = _dehyphenate_join(seg_lines)
    if label == "colon":
        segment = re.sub(
            rf"^\s*{_kt('MOTION')}\s*:\s*", "", segment, flags=re.IGNORECASE
        )
    elif label == "passive":
        segment = re.sub(
            rf"^\s*{_kt('MOTION')}\s+{_kt('WAS')}\s+{_kt('MADE')}(?:\s+{_kt('TO')})?:?\s*",
            "",
            segment,
            flags=re.IGNORECASE,
        )
    else:  # mover_label: keep the By-clause for mover extraction
        segment = re.sub(
            rf"^\s*{_kt('MOTION')}\s+", "", segment, flags=re.IGNORECASE
        )

    # Mover and seconder, from the reassembled segment. Matched clause text
    # is excised from the motion text afterwards.
    mover: Optional[str] = None
    seconder: Optional[str] = None
    excise: list[str] = []
    full = _FULL_MOVER_RE.search(segment)
    if full:
        mover, seconder = _clean_name(full.group(1)), _clean_name(full.group(2))
        excise.append(full.group(0))
    else:
        if label == "mover_label":
            lead = _LEADING_BY_RE.search(segment)
            if lead:
                mover = _clean_name(lead.group(1))
                excise.append(lead.group(0))
        if mover is None:
            # Search line-by-line so a name cannot swallow a following
            # sentence: the mover's name ends on the mover's own line.
            for line in seg_lines:
                by = _MOVED_BY_RE.search(line)
                if by:
                    mover = _clean_name(by.group(1))
                    excise.append(by.group(0))
                    break
        sec = _SECONDED_RE.search(segment)
        if sec:
            seconder = _clean_name(sec.group(1))
            excise.append(sec.group(0))

    text = segment
    for clause in excise:
        text = text.replace(clause, " ", 1)
    text = re.sub(r"\s+", " ", text).strip(" ;,").strip()

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
        if label == "passive":
            # "MOTION WAS MADE" style names no mover; nothing to extract.
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
        section_text = " ".join(bl.text for bl in block[idx:next_idx])
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
    )


def parse_minutes(pdf_bytes: bytes, file_id: int) -> ParsedMinutes:
    """Parse an IVGID minutes PDF into structured, provenance-carrying
    records. Deterministic only; anything this misses is Stage B's input."""
    doc_flags: list[str] = []
    pages = pdftext.extract_pages(pdf_bytes)
    unparseable = [p.page_number for p in pages if p.char_count < MIN_PARSEABLE_CHARS]
    for page in pages:
        if page.raw_fallback:
            doc_flags.append(f"raw_fallback_page:{page.page_number}")

    parseable = [p for p in pages if p.page_number not in unparseable]
    body = _strip_page_furniture(parseable, doc_flags)
    body, comments = _mark_comment_regions(body, file_id)

    # Media timestamps: collected everywhere, including comment regions —
    # the timestamp itself is structural clerk text, not comment content.
    media = [
        MediaTimestamp(
            start=m.group(1),
            end=m.group(2),
            provenance=Provenance(file_id=file_id, page=bl.page),
        )
        for bl in body
        for m in [_MEDIA_TIMESTAMP_RE.search(bl.text)]
        if m
    ]

    # Motion blocks: assembled only from non-comment lines, from "MOTION:"
    # to the outcome line, across page breaks.
    motions: list[Motion] = []
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
            motions.append(_parse_motion_block(block, file_id, successor))
            i = j
        else:
            i += 1

    parsed = ParsedMinutes(
        motions=motions,
        media_timestamps=media,
        public_comments=comments,
        unparseable_pages=unparseable,
        flags=doc_flags,
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
