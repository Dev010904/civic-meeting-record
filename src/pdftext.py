"""PDF text extraction with positional data.

Every piece of text this module emits carries a page number (and, for lines,
a line number within the page). This is not a convenience: spec §2.7 rule 7
requires provenance on every published claim, and the §2.4 data model records
``{"type": "pdf", "file_id": …, "page": …}``. Text without a page number
cannot satisfy that requirement, so no function here returns bare text.

Extraction uses pdfplumber (installs cleanly on Python 3.14). Reading order
is pdfplumber's positional ordering; pages that look multi-column — where
positional ordering would interleave columns into scrambled text — fall back
to raw content-stream order and are flagged via ``Page.raw_fallback`` rather
than silently producing scrambled output.

Whitespace is normalised conservatively: runs of spaces/tabs collapse to one
space, line edges are stripped, runs of blank lines collapse to a single
blank line (preserving paragraph breaks). Punctuation, currency symbols and
case are untouched — the step-3 parser needs them verbatim.

This module makes no network requests and no LLM calls.
"""

from __future__ import annotations

import io
import re
from dataclasses import dataclass
from typing import Any

import pdfplumber

# A page with fewer extracted characters than this, alongside at least one
# image, is treated as a scanned page with no usable text layer.
MIN_TEXT_CHARS_PER_PAGE = 20

# Multi-column heuristic thresholds (see _looks_multi_column).
_ROW_BUCKET_PT = 4.0
_MIN_ELIGIBLE_ROWS = 8
_GUTTER_MIN_FRACTION = 0.12
_GUTTER_ROW_RATIO = 0.7


@dataclass(frozen=True)
class Page:
    """One page of extracted text. ``page_number`` is 1-indexed."""

    page_number: int
    text: str
    char_count: int
    # True when the page looked multi-column and positional ordering was
    # abandoned for raw content-stream order. Downstream parsers should
    # treat flagged pages with suspicion rather than trusting line order.
    raw_fallback: bool = False


@dataclass(frozen=True)
class Line:
    """One non-empty line. ``line_number`` is 1-indexed within its page and
    counts physical lines of ``Page.text`` (blank lines occupy a number but
    are not emitted), so it cross-references ``Page.text`` exactly."""

    page_number: int
    line_number: int
    text: str


def _normalise(text: str) -> str:
    """Conservative whitespace normalisation.

    Collapses runs of spaces/tabs to one space and strips line edges;
    collapses runs of blank lines to a single blank line so paragraph breaks
    survive. Nothing else is altered — no punctuation, currency or case
    changes, which step 3 parses.
    """
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.split("\n")]
    out: list[str] = []
    for line in lines:
        if line == "" and (not out or out[-1] == ""):
            continue
        out.append(line)
    while out and out[-1] == "":
        out.pop()
    return "\n".join(out)


def _looks_multi_column(words: list[dict[str, Any]], page_width: float) -> bool:
    """Heuristic: does this page have a persistent vertical gutter?

    Words are bucketed into rows by vertical position; a row votes for
    multi-column when its widest inter-word gap falls in the middle band of
    the page and spans at least 12% of the page width. If 70% of multi-word
    rows vote yes (and there are at least 8 such rows), positional ordering
    would likely interleave the columns, so the caller falls back to raw
    extraction. Single-column minutes and agendas do not trip this.
    """
    rows: dict[int, list[dict[str, Any]]] = {}
    for word in words:
        rows.setdefault(int(word["top"] / _ROW_BUCKET_PT), []).append(word)

    mid_lo, mid_hi = 0.30 * page_width, 0.70 * page_width
    eligible = 0
    gutter_rows = 0
    for row in rows.values():
        if len(row) < 2:
            continue
        eligible += 1
        row.sort(key=lambda w: w["x0"])
        for prev, nxt in zip(row, row[1:]):
            gap = nxt["x0"] - prev["x1"]
            centre = (prev["x1"] + nxt["x0"]) / 2
            if gap >= _GUTTER_MIN_FRACTION * page_width and mid_lo <= centre <= mid_hi:
                gutter_rows += 1
                break
    return eligible >= _MIN_ELIGIBLE_ROWS and gutter_rows / eligible >= _GUTTER_ROW_RATIO


def _raw_text(page: pdfplumber.page.Page) -> str:
    """Text in raw content-stream order (the order the PDF was written).

    Used only as the multi-column fallback: column-by-column writing order is
    usually the true reading order, whereas positional sorting interleaves
    columns. A newline is inserted whenever the baseline moves.
    """
    parts: list[str] = []
    last_top: float | None = None
    for char in page.chars:
        if last_top is not None and abs(char["top"] - last_top) > 3.0:
            parts.append("\n")
        parts.append(char["text"])
        last_top = char["top"]
    return "".join(parts)


def extract_pages(pdf_bytes: bytes) -> list[Page]:
    """Extract normalised text per page, 1-indexed, preserving reading order.

    Pages suspected of multi-column layout are extracted in raw
    content-stream order and flagged (``raw_fallback=True``) instead of
    silently returning interleaved text.

    Per-page caches are flushed as pages are processed, so memory stays
    bounded by the largest single page rather than the whole document —
    agenda packets run to tens of MB.
    """
    pages: list[Page] = []
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for number, page in enumerate(pdf.pages, start=1):
            try:
                words = page.extract_words()
                raw_fallback = _looks_multi_column(words, page.width)
                text = _raw_text(page) if raw_fallback else (page.extract_text() or "")
            finally:
                page.flush_cache()
                page.get_textmap.cache_clear()
            text = _normalise(text)
            pages.append(
                Page(
                    page_number=number,
                    text=text,
                    char_count=len(text),
                    raw_fallback=raw_fallback,
                )
            )
    return pages


def extract_lines(pdf_bytes: bytes) -> list[Line]:
    """Extract non-empty lines, each carrying page and in-page line numbers.

    ``line_number`` counts physical lines of the page's normalised text
    (blank lines consume a number but are not emitted), so a ``Line`` can be
    located in ``Page.text`` and, from there, in the source PDF page —
    the provenance chain spec §2.7 rule 7 requires.
    """
    lines: list[Line] = []
    for page in extract_pages(pdf_bytes):
        for index, text in enumerate(page.text.split("\n"), start=1):
            if text:
                lines.append(
                    Line(page_number=page.page_number, line_number=index, text=text)
                )
    return lines


def pages_without_text(pdf_bytes: bytes) -> list[int]:
    """1-indexed pages that appear scanned: an image but no usable text layer.

    A page counts as lacking text when it extracts fewer than
    ``MIN_TEXT_CHARS_PER_PAGE`` characters *and* contains at least one image.
    Genuinely blank pages (no text, no images) are not reported — there is
    nothing on them to extract.
    """
    suspect: list[int] = []
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for number, page in enumerate(pdf.pages, start=1):
            try:
                char_count = len(page.chars)
                has_images = bool(page.images)
            finally:
                page.flush_cache()
            if char_count < MIN_TEXT_CHARS_PER_PAGE and has_images:
                suspect.append(number)
    return suspect


def is_text_extractable(pdf_bytes: bytes) -> bool:
    """True only when every page with content has a real text layer.

    Honest about partial cases: a mixed PDF where some pages are scanned
    images returns False — use :func:`pages_without_text` to see which pages
    are the problem. A document with no text at all returns False.
    """
    if pages_without_text(pdf_bytes):
        return False
    return any(page.char_count >= MIN_TEXT_CHARS_PER_PAGE for page in extract_pages(pdf_bytes))
