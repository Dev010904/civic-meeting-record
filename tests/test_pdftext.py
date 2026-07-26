"""Tests for src/pdftext.py against real recorded IVGID PDFs.

Fixtures (all captured live from the CivicClerk API by
scripts/record_fixtures.py):

- ivgid_file_2800.pdf      — Agenda, 6 pages, fully text-extractable
- ivgid_minutes_2778.pdf   — approved Minutes, 29 pages, MIXED: pages 25-29
                             are scanned images with no text layer
- ivgid_minutes_draft_2783.pdf — draft Minutes, 3 pages, fully extractable
- ivgid_packet_2805.pdf    — Agenda Packet, 436 pages, ~42 MB, mixed

The mixed minutes PDF is a real-world specimen of the partial-scan case, so
is_text_extractable's honesty is tested against reality, not a synthetic.
"""

from __future__ import annotations

import tracemalloc

import pytest

import pdftext
from conftest import FIXTURES


def _load(name: str) -> bytes:
    return (FIXTURES / name).read_bytes()


@pytest.fixture(scope="module")
def agenda_pages() -> list[pdftext.Page]:
    return pdftext.extract_pages(_load("ivgid_file_2800.pdf"))


@pytest.fixture(scope="module")
def minutes_pages() -> list[pdftext.Page]:
    return pdftext.extract_pages(_load("ivgid_minutes_2778.pdf"))


@pytest.fixture(scope="module")
def packet_extraction() -> tuple[list[pdftext.Page], int]:
    """Extract the 436-page packet once, under tracemalloc, for all
    packet tests (extraction takes ~2 minutes)."""
    data = _load("ivgid_packet_2805.pdf")
    tracemalloc.start()
    pages = pdftext.extract_pages(data)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return pages, peak


# --- Page counts match the actual PDFs -----------------------------------


def test_agenda_page_count(agenda_pages):
    assert len(agenda_pages) == 6
    assert [p.page_number for p in agenda_pages] == list(range(1, 7))


def test_minutes_page_count(minutes_pages):
    assert len(minutes_pages) == 29


def test_packet_page_count(packet_extraction):
    pages, _ = packet_extraction
    assert len(pages) == 436


# --- Every line carries positional data ----------------------------------


def test_every_line_carries_page_and_line_numbers():
    lines = pdftext.extract_lines(_load("ivgid_minutes_draft_2783.pdf"))
    assert lines
    assert all(line.page_number >= 1 for line in lines)
    assert all(line.line_number >= 1 for line in lines)
    assert all(line.text for line in lines)  # no empty lines emitted


def test_line_numbers_cross_reference_page_text(minutes_pages):
    """Line.line_number indexes physical lines of Page.text exactly."""
    lines = pdftext.extract_lines(_load("ivgid_minutes_2778.pdf"))
    by_page = {p.page_number: p.text.split("\n") for p in minutes_pages}
    for line in lines:
        assert by_page[line.page_number][line.line_number - 1] == line.text


# --- Known text lands on the right page, not a neighbour -----------------


def test_known_text_found_on_its_page_only(minutes_pages):
    needle = "Ms. Sanford provided a comprehensive update on federal legislative"
    hits = [p.page_number for p in minutes_pages if needle in p.text]
    assert hits == [10]
    # The clerk's printed page header confirms PDF page = document page.
    assert "-10-" in minutes_pages[9].text
    assert needle not in minutes_pages[8].text
    assert needle not in minutes_pages[10].text


def test_media_timestamp_line_present_on_page_1(minutes_pages):
    # The clerk's hand-written alignment key (spec §2.2) survives extraction.
    assert "Media Timestamp (00:04:17 - 00:32:19)" in minutes_pages[0].text


# --- is_text_extractable: honest, including the real mixed PDF -----------


def test_agenda_is_text_extractable():
    assert pdftext.is_text_extractable(_load("ivgid_file_2800.pdf")) is True


def test_draft_minutes_are_text_extractable():
    assert pdftext.is_text_extractable(_load("ivgid_minutes_draft_2783.pdf")) is True


def test_mixed_minutes_return_false_and_name_the_scanned_pages():
    """ivgid_minutes_2778.pdf is a real mixed PDF: pages 25-29 are scanned
    images (signature/attachment pages) with no text layer."""
    data = _load("ivgid_minutes_2778.pdf")
    assert pdftext.is_text_extractable(data) is False
    assert pdftext.pages_without_text(data) == [25, 26, 27, 28, 29]


def test_no_text_at_all_is_not_extractable():
    # A structurally valid PDF with a single empty page.
    empty_page_pdf = (
        b"%PDF-1.4\n"
        b"1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
        b"2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
        b"3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]>>endobj\n"
        b"trailer<</Root 1 0 R>>\n"
    )
    assert pdftext.is_text_extractable(empty_page_pdf) is False


# --- Multi-column fallback flags rather than scrambles -------------------


def test_prose_pages_are_not_flagged(minutes_pages, agenda_pages):
    assert not any(p.raw_fallback for p in minutes_pages)
    assert not any(p.raw_fallback for p in agenda_pages)


def test_packet_columnar_pages_are_flagged(packet_extraction):
    pages, _ = packet_extraction
    flagged = [p.page_number for p in pages if p.raw_fallback]
    # Page 43 is a two-column vendor/amount table; positional ordering would
    # interleave it, so it must be flagged and fall back to raw order.
    assert 43 in flagged
    assert pages[42].text  # flagged pages still return text
    assert "Acushnet Company" in pages[42].text


# --- Whitespace normalisation: conservative ------------------------------


def test_normalise_collapses_spaces_and_preserves_breaks():
    raw = "Line  one \t here \nLine two\n\n\n\nLine three   \n\n"
    assert pdftext._normalise(raw) == "Line one here\nLine two\n\nLine three"


def test_normalise_leaves_punctuation_currency_case_alone():
    raw = "Amount:  $350,236.00  (Trillium Pumps USA);  Vote 4-1"
    assert (
        pdftext._normalise(raw)
        == "Amount: $350,236.00 (Trillium Pumps USA); Vote 4-1"
    )


# --- Large packet: bounded memory ----------------------------------------


def test_packet_extracts_with_bounded_memory(packet_extraction):
    """42 MB, 436 pages. With per-page cache flushing the observed peak is
    ~92 MB; an unbounded cache across pages would run to many hundreds of
    MB. 300 MB is the tripwire."""
    pages, peak = packet_extraction
    assert len(pages) == 436
    assert peak < 300 * 1024 * 1024
