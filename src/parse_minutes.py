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

# Safety bound when assembling a vote block that never terminates.
MAX_MOTION_BLOCK_LINES = 30

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
# "Moved By X, Seconded by Y" — tolerates the kerning-damaged "B y" form
# (page 8 of ivgid_minutes_2778.pdf reads "B y Trustee Chair Tonking, …").
_MOVER_RE = re.compile(
    r"(?:Moved\s*)?B\s*y\s+(.+?),\s*Second(?:ed)?\s+by\s+(.+)$", re.IGNORECASE
)
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
            if text:
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
        if dk.startswith("MOTION:"):
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
        token = token.strip(" .")
        if not token or token.lower() == "none":
            continue
        names.append(token)
    return names, stated


def _parse_motion_block(
    block: list[_BodyLine], file_id: int
) -> Motion:
    """Parse one fully reassembled motion block. The block must already span
    all its lines (across page breaks) — votes are never parsed from a
    single line, which is what makes wrapped tallies safe."""
    flags: list[str] = []
    raw = "\n".join(bl.text for bl in block)
    start_page = block[0].page

    mover: Optional[str] = None
    seconder: Optional[str] = None
    mover_idx: Optional[int] = None
    for idx, bl in enumerate(block):
        match = _MOVER_RE.search(bl.text)
        if match:
            mover, seconder = match.group(1).strip(), match.group(2).strip()
            mover_idx = idx
            break

    # Locate vote-section label lines and the outcome line.
    outcome: Optional[str] = None
    section_starts: list[tuple[int, str]] = []
    end_idx = len(block)
    for idx, bl in enumerate(block):
        dk = _dekern(bl.text)
        if dk.startswith("MOTIONPASSED"):
            outcome, end_idx = "passed", idx
            break
        if dk.startswith("MOTIONFAILED"):
            outcome, end_idx = "failed", idx
            break
        for label in _VOTE_SECTIONS:
            if dk.startswith(label):
                section_starts.append((idx, label))
                break
    if outcome is None:
        flags.append("missing_outcome")

    # Motion text: everything between "MOTION:" and the mover line (or the
    # first vote section when the mover line is missing).
    text_end = mover_idx if mover_idx is not None else (
        section_starts[0][0] if section_starts else end_idx
    )
    text = _dehyphenate_join([bl.text for bl in block[:text_end]])
    text = re.sub(r"^\s*MOTION\s*:\s*", "", text, flags=re.IGNORECASE).strip()
    if mover is None:
        flags.append("missing_mover")

    # Reassemble each vote section across its full line span, then parse.
    names_by_section: dict[str, list[str]] = {s: [] for s in _VOTE_SECTIONS}
    stated_by_section: dict[str, list[int]] = {s: [] for s in _VOTE_SECTIONS}
    tally: dict[str, Optional[int]] = {v: 0 for v in _SECTION_TO_TALLY_KEY.values()}
    for pos, (idx, label) in enumerate(section_starts):
        next_idx = (
            section_starts[pos + 1][0] if pos + 1 < len(section_starts) else end_idx
        )
        section_text = " ".join(bl.text for bl in block[idx:next_idx])
        section_text = re.sub(
            rf"^\s*{label[0]}\s*{''.join(c + r'\s*' for c in label[1:])}:?",
            "",
            section_text,
            flags=re.IGNORECASE,
        )
        names, stated = _parse_vote_section(section_text)
        names_by_section[label] = names
        stated_by_section[label] = stated
        key = _SECTION_TO_TALLY_KEY[label]
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
        flags.append("missing_vote_sections")
        tally = {v: None for v in _SECTION_TO_TALLY_KEY.values()}

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
        if _dekern(scan[i].text).startswith("MOTION:"):
            block = [scan[i]]
            j = i + 1
            while j < len(scan) and len(block) < MAX_MOTION_BLOCK_LINES:
                dk = _dekern(scan[j].text)
                if dk.startswith("MOTION:"):
                    break
                block.append(scan[j])
                if dk.startswith("MOTIONPASSED") or dk.startswith("MOTIONFAILED"):
                    break
                j += 1
            motions.append(_parse_motion_block(block, file_id))
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
