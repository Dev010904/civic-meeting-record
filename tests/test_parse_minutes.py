"""Tests for the Stage A deterministic minutes parser.

Expected values were hand-verified by reading the raw extracted text of the
two real fixtures (see the motion-block dump in scripts/inspect_minutes.py
output): 11 motions in ivgid_minutes_2778.pdf (approved, 29 Apr 2026) and
1 in ivgid_minutes_draft_2783.pdf (draft, 20 May 2026).
"""

from __future__ import annotations

import json
import re

import pytest

import parse_minutes as pm
import pdftext
from conftest import FIXTURES

TRUSTEES_FULL = [
    "Trustee Chair Tonking",
    "Trustee Jezycki",
    "Trustee Noble",
    "Trustee Homan",
    "Trustee Tulloch",
]


@pytest.fixture(scope="module")
def approved() -> pm.ParsedMinutes:
    return pm.parse_minutes(
        (FIXTURES / "ivgid_minutes_2778.pdf").read_bytes(), file_id=2778
    )


@pytest.fixture(scope="module")
def draft() -> pm.ParsedMinutes:
    return pm.parse_minutes(
        (FIXTURES / "ivgid_minutes_draft_2783.pdf").read_bytes(), file_id=2783
    )


def _bl(page: int, line: int, text: str) -> pm._BodyLine:
    return pm._BodyLine(page, line, text)


# --- Motion inventory ----------------------------------------------------


def test_motion_counts(approved, draft):
    assert len(approved.motions) == 11
    assert len(draft.motions) == 1


def test_all_fixture_motions_parse_clean(approved, draft):
    for motion in [*approved.motions, *draft.motions]:
        assert motion.flags == [], (motion.provenance.page, motion.flags)
        assert motion.outcome == "passed"


# --- The wrapped-tally hazard (page 8, hand-verified) --------------------


def test_page8_wrapped_tally_parses_complete_name_list(approved):
    """'YEAS: … Trustee Homan, 5' with 'Trustee Tulloch 0' on the next line:
    four names then the count, fifth name wrapped. The reassembled block
    must yield all five names and the validated count."""
    motion = approved.motions[0]
    assert motion.provenance.page == 8
    assert motion.yeas == TRUSTEES_FULL
    assert motion.tally == {"aye": 5, "nay": 0, "abstain": 0, "absent": 0}
    assert motion.nays == []
    assert motion.stated["YEAS"] == [5, 0]  # the orphan 0 is kept as evidence
    # Kerning-damaged mover line "B y Trustee Chair Tonking, Seconded by …"
    assert motion.mover == "Trustee Chair Tonking"
    assert motion.seconder == "Trustee Homan"
    assert "Steven Phillips" in motion.text


def test_wrapped_tallies_across_all_unanimous_motions(approved):
    # Motions 2, 3, 5 and 9 (indexes 1, 2, 4, 8) share the wrapped 5-0 form.
    for index in (1, 2, 4, 8):
        motion = approved.motions[index]
        assert motion.yeas == TRUSTEES_FULL, index
        assert motion.tally["aye"] == 5


# --- Blocks that span a page break ---------------------------------------


def test_consent_calendar_block_survives_page_break(approved):
    """Motion 3 starts on page 11; its vote lines are on page 12 with the
    footer and header in between. Provenance anchors to the MOTION: line."""
    motion = approved.motions[2]
    assert motion.provenance.page == 11
    assert "Consent Calendar" in motion.text
    assert motion.mover == "Trustee Homan"
    assert motion.seconder == "Trustee Jezycki"
    assert motion.yeas == TRUSTEES_FULL
    assert motion.tally == {"aye": 5, "nay": 0, "abstain": 0, "absent": 0}


def test_punch_card_block_survives_page_break_with_name_variant(approved):
    motion = approved.motions[7]
    assert motion.provenance.page == 17
    assert "$865" in motion.text
    # The clerk wrote "Chair Tonking" here, not "Trustee Chair Tonking" —
    # names are verbatim, not normalised.
    assert motion.yeas == [
        "Trustee Jezycki",
        "Trustee Noble",
        "Trustee Homan",
        "Chair Tonking",
    ]
    assert motion.nays == ["Trustee Tulloch"]
    assert motion.tally == {"aye": 4, "nay": 1, "abstain": 0, "absent": 0}


# --- Hand-verified split and 4-1 votes -----------------------------------


def test_facility_fee_split_vote(approved):
    motion = approved.motions[6]
    assert motion.provenance.page == 17
    assert "Facility Fee for Fiscal Year 2027" in motion.text
    assert motion.mover == "Trustee Homan"
    assert motion.seconder == "Trustee Noble"
    assert motion.yeas == ["Trustee Jezycki", "Trustee Noble", "Trustee Homan"]
    assert motion.nays == ["Trustee Chair Tonking", "Trustee Tulloch"]
    assert motion.tally == {"aye": 3, "nay": 2, "abstain": 0, "absent": 0}


def test_ordinance7_first_reading(approved):
    motion = approved.motions[3]
    assert motion.provenance.page == 13
    assert "First Reading of Ordinance 7" in motion.text
    assert "4:00 p.m. on Wednesday, May 13, 2026" in motion.text
    assert motion.mover == "Trustee Jezycki"
    assert motion.seconder == "Trustee Homan"
    assert motion.nays == ["Trustee Tulloch"]
    assert motion.tally == {"aye": 4, "nay": 1, "abstain": 0, "absent": 0}


def test_cmar_contract_motion_preserves_currency_and_vendor(approved):
    motion = approved.motions[9]
    assert motion.provenance.page == 20
    assert "$2,230,662.28" in motion.text  # currency untouched (step-3 input)
    assert "Advanced Companies, Inc." in motion.text
    assert motion.mover == "Trustee Homan"
    assert motion.tally == {"aye": 4, "nay": 1, "abstain": 0, "absent": 0}


def test_reclassification_motion(approved):
    motion = approved.motions[10]
    assert motion.provenance.page == 21
    assert motion.mover == "Trustee Noble"
    assert motion.seconder == "Trustee Homan"
    assert motion.tally == {"aye": 4, "nay": 1, "abstain": 0, "absent": 0}


def test_dehyphenation_of_wrapped_motion_text(approved):
    motion = approved.motions[4]
    assert "Youth Non-Profit" in motion.text  # "Non-\nProfit" rejoined
    assert "$30 per hour" in motion.text and "$38" in motion.text


def test_draft_minutes_motion_with_absent_trustee(draft):
    """Only four trustees voted (no Noble, no ABSENT line): 4 names,
    stated 4, NAYS 'None 0' — validates clean."""
    motion = draft.motions[0]
    assert motion.provenance.page == 2
    assert "$199,000.00" in motion.text
    assert "Olympus" in motion.text
    assert motion.mover == "Trustee Homan"
    assert motion.seconder == "Trustee Jezycki"
    assert motion.yeas == [
        "Trustee Chair Tonking",
        "Trustee Jezycki",
        "Trustee Homan",
        "Trustee Tulloch",
    ]
    assert motion.tally == {"aye": 4, "nay": 0, "abstain": 0, "absent": 0}


# --- Media timestamps ----------------------------------------------------


def test_media_timestamps_including_url_sharing_line(approved):
    assert len(approved.media_timestamps) == 26
    pairs = {(m.start, m.end, m.provenance.page) for m in approved.media_timestamps}
    # Shares a line with the portal URL on page 1:
    assert ("00:04:17", "00:32:19", 1) in pairs
    assert ("00:34:22", "00:41:14", 8) in pairs


def test_draft_media_timestamp_variants(draft):
    """Draft minutes use an en-dash separator and a single-timestamp form."""
    entries = {(m.start, m.end) for m in draft.media_timestamps}
    assert ("00:16:31", None) in entries  # no range at all
    assert ("00:16:46", "00:18:18") in entries  # en-dash separated
    assert ("00:18:20", "01:13:00") in entries  # en-dash, shares URL line
    assert len(draft.media_timestamps) == 3


# --- Public comment: metadata only, never text, never names --------------


def test_public_comment_records_are_metadata_only(approved):
    assert len(approved.public_comments) == 10
    for comment in approved.public_comments:
        assert comment.commenter_type == "resident"
        assert isinstance(comment.provenance, pm.Provenance)
        assert set(vars(comment)) == {"topic", "commenter_type", "provenance", "flags"}
    assert [c.provenance.page for c in approved.public_comments] == [
        1, 2, 2, 3, 3, 4, 5, 5, 6, 6,
    ]


def test_no_verbatim_comment_text_or_names_in_output(approved):
    """Harvest every commenter name and the first line of every verbatim
    comment straight from the PDF, then prove none of it reaches output."""
    output = json.dumps(approved.to_dict())
    lines = pdftext.extract_lines((FIXTURES / "ivgid_minutes_2778.pdf").read_bytes())
    marker = re.compile(
        r"Public\s+comments?\s+provided\s+by\s+(.+?)\s+is\s+transcribed\s+below",
        re.IGNORECASE,
    )
    names_found = 0
    for i, line in enumerate(lines):
        match = marker.search(line.text)
        if not match:
            continue
        names_found += 1
        commenter = match.group(1)
        assert commenter not in output, f"commenter name leaked: {commenter}"
        first_comment_line = lines[i + 1].text
        assert first_comment_line not in output, "verbatim comment text leaked"
    assert names_found == 10  # the harvest itself found every marker
    # Spot-check distinctive verbatim phrases read from the PDF by hand:
    assert "pickleball" not in output
    assert "I have been told that you guys" not in output


# --- Contradictions are flagged, never resolved --------------------------


def test_deliberate_tally_mismatch_is_flagged_not_resolved():
    block = [
        _bl(4, 1, "MOTION: to Approve the Test Item."),
        _bl(4, 2, "Moved By Trustee A, Seconded by Trustee B"),
        _bl(4, 3, "YEAS: Trustee A, Trustee B 3"),  # two names, stated 3
        _bl(4, 4, "NAYS: None"),
        _bl(4, 5, "MOTION PASSED"),
    ]
    motion = pm._parse_motion_block(block, file_id=999)
    assert "tally_mismatch" in motion.flags
    assert motion.tally["aye"] is None  # not resolved to either value
    assert motion.yeas == ["Trustee A", "Trustee B"]  # parsed evidence kept
    assert motion.stated["YEAS"] == [3]  # stated evidence kept
    assert motion.tally["nay"] == 0  # unaffected section still validates


def test_missing_mover_is_flagged_not_inferred():
    block = [
        _bl(7, 1, "MOTION: to Approve the Test Item."),
        _bl(7, 2, "YEAS: Trustee A, Trustee B 2"),
        _bl(7, 3, "NAYS: None"),
        _bl(7, 4, "MOTION PASSED"),
    ]
    motion = pm._parse_motion_block(block, file_id=999)
    assert "missing_mover" in motion.flags
    assert motion.mover is None and motion.seconder is None
    assert motion.tally["aye"] == 2  # votes still parse


def test_abstain_absent_and_failed_outcome():
    block = [
        _bl(3, 1, "MOTION: to Approve the Test Item."),
        _bl(3, 2, "Moved By Trustee A, Seconded by Trustee B"),
        _bl(3, 3, "YEAS: Trustee A, Trustee B 2"),
        _bl(3, 4, "NAYS: Trustee C 1"),
        _bl(3, 5, "ABSTAIN: Trustee D 1"),
        _bl(3, 6, "ABSENT: Trustee E 1"),
        _bl(3, 7, "MOTION FAILED"),
    ]
    motion = pm._parse_motion_block(block, file_id=999)
    assert motion.outcome == "failed"
    assert motion.abstain == ["Trustee D"]
    assert motion.absent == ["Trustee E"]
    assert motion.tally == {"aye": 2, "nay": 1, "abstain": 1, "absent": 1}
    assert motion.flags == []


def test_missing_outcome_is_flagged():
    block = [
        _bl(5, 1, "MOTION: to Approve the Test Item."),
        _bl(5, 2, "Moved By Trustee A, Seconded by Trustee B"),
        _bl(5, 3, "YEAS: Trustee A, Trustee B 2"),
    ]
    motion = pm._parse_motion_block(block, file_id=999)
    assert "missing_outcome" in motion.flags
    assert motion.outcome is None


# --- Page furniture and provenance checks --------------------------------


def test_scanned_tail_reported_not_skipped(approved):
    assert approved.unparseable_pages == [25, 26, 27, 28, 29]


def test_no_header_page_mismatches_in_real_fixtures(approved, draft):
    assert [f for f in approved.flags if f.startswith("header_page_mismatch")] == []
    assert [f for f in draft.flags if f.startswith("header_page_mismatch")] == []


def test_header_page_mismatch_is_flagged():
    page = pdftext.Page(
        page_number=2,
        text="IVGID Board of Trustees -3- Meeting Minutes April 29, 2026\nBody text here",
        char_count=70,
    )
    doc_flags: list[str] = []
    body = pm._strip_page_furniture([page], doc_flags)
    assert doc_flags == ["header_page_mismatch:pdf_page=2,printed=3"]
    assert [bl.text for bl in body] == ["Body text here"]  # header stripped


# --- Provenance is mandatory ---------------------------------------------


def test_provenance_validation():
    with pytest.raises(ValueError):
        pm.Provenance(file_id=0, page=1)
    with pytest.raises(ValueError):
        pm.Provenance(file_id=2778, page=0)
    with pytest.raises(ValueError):
        pm.Provenance(file_id=2778, page=1, type="url")
    with pytest.raises(TypeError):
        pm.Motion(  # no provenance argument at all
            text="x", mover=None, seconder=None, yeas=[], nays=[],
            abstain=[], absent=[], tally={}, stated={}, outcome=None,
        )


def test_validate_rejects_record_stripped_of_provenance(approved):
    import copy

    broken = copy.deepcopy(approved)
    broken.motions[0].provenance = None  # type: ignore[assignment]
    with pytest.raises(ValueError, match="without provenance"):
        pm.validate(broken)
