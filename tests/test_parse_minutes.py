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


# --- Stage A hardening: format variants (step 5) -------------------------


def test_motion_passes_and_carried_terminators():
    for terminator, expected in (
        ("MOTION PASSES", "passed"),
        ("MOTION CARRIED", "passed"),
        ("MOTION FAILS", "failed"),
    ):
        block = [
            _bl(2, 1, "MOTION: to Approve the Test Item."),
            _bl(2, 2, "Moved By Trustee A, Seconded by Trustee B"),
            _bl(2, 3, "YEAS: Trustee A, Trustee B 2"),
            _bl(2, 4, "NAYS: None"),
            _bl(2, 5, terminator),
        ]
        motion = pm._parse_motion_block(block, file_id=999)
        assert motion.outcome == expected, terminator
        assert motion.flags == []


def test_bare_motion_terminator_is_truncated_not_overrun():
    block = [
        _bl(1, 1, "MOTION: to Approve and Follow the Agenda as Submitted."),
        _bl(1, 2, "Moved By Committee Chair A"),
        _bl(1, 3, "YEAS: Committee Chair A, Trustee B, Member C 3"),
        _bl(1, 4, "NAYS: None 0"),
        _bl(1, 5, "MOTION"),
        _bl(1, 6, "D. REPORTS TO THE COMMITTEE - pages 3 - 8"),  # stray numbers
    ]
    motion = pm._parse_motion_block(block, file_id=999)
    assert motion.flags == ["truncated_outcome"]  # outcome unknown, flagged
    assert motion.outcome is None
    assert motion.tally["aye"] == 3  # the overrun no longer poisons the tally
    assert motion.notes == ["no_seconder"]
    assert motion.mover == "Committee Chair A"


def test_audit_passive_label_and_carried():
    block = [
        _bl(3, 1, "MOTION WAS MADE TO approve the 2nd Extension of the Audit."),
        _bl(3, 2, "YEAS: Committee Members Brandle, Schmitz, and Tulloch 3"),
        _bl(3, 3, "NAYS: None 0"),
        _bl(3, 4, "MOTION CARRIED"),
    ]
    motion = pm._parse_motion_block(block, file_id=999)
    assert motion.flags == []
    assert motion.notes == ["mover_not_recorded"]  # passive style, not a failure
    assert motion.outcome == "passed"
    assert motion.yeas == ["Committee Members Brandle", "Schmitz", "Tulloch"]
    assert motion.tally["aye"] == 3


def test_mover_variants_semicolon_colon_and_missing_separator():
    for mover_line in (
        "Moved by Trustee A; Seconded by Trustee B",
        "Moved by Trustee A Seconded by Trustee B",
        "Moved by: Trustee A, Seconded by: Trustee B",
    ):
        block = [
            _bl(4, 1, "MOTION: to Approve the Test Item."),
            _bl(4, 2, mover_line),
            _bl(4, 3, "YEAS: Trustee A, Trustee B 2"),
            _bl(4, 4, "NAYS: None"),
            _bl(4, 5, "MOTION PASSED"),
        ]
        motion = pm._parse_motion_block(block, file_id=999)
        assert motion.mover == "Trustee A", mover_line
        assert motion.seconder == "Trustee B", mover_line
        assert motion.flags == []


def test_mid_text_mover_clause_and_kerned_names():
    block = [
        _bl(5, 1, "MOTION: to Approve the Big Contract in the amount of"),
        _bl(5, 2, "$755,000. Moved by Trustee"),
        _bl(5, 3, "H oman, Seconded by"),
        _bl(5, 4, "T rustee Noble"),
        _bl(5, 5, "YEAS: Trustee Homan, Trustee Noble 2"),
        _bl(5, 6, "NAYS: None"),
        _bl(5, 7, "MOTION PASSED"),
    ]
    motion = pm._parse_motion_block(block, file_id=999)
    assert motion.mover == "Trustee Homan"  # kerning "H oman" repaired
    assert motion.seconder == "Trustee Noble"
    assert "$755,000." in motion.text
    assert motion.flags == []


def test_no_seconder_is_note_not_flag():
    block = [
        _bl(9, 1, "MOTION: To remove Item H.5. from the Agenda"),
        _bl(9, 2, "Moved by Trustee Tulloch, Trustee Chair T called for a Vote."),
        _bl(9, 3, "YEAS: Trustee Tulloch 1"),
        _bl(9, 4, "NAYS: Trustee A, Trustee B, Trustee C, Trustee D 4"),
        _bl(9, 5, "MOTION FAILED"),
    ]
    motion = pm._parse_motion_block(block, file_id=999)
    assert motion.mover == "Trustee Tulloch"
    assert motion.seconder is None
    assert motion.notes == ["no_seconder"]
    assert motion.flags == []
    assert motion.outcome == "failed"


def test_no_recorded_vote_is_normal_per_nrs():
    """NRS 241.035(1)(c): per-member vote records only at a member's
    request. A terminated motion with no roll call is not a failure."""
    block = [
        _bl(2, 1, "MOTION By Trustee Noble to approve the recommendation"),
        _bl(2, 2, "as contained in the staff report."),
        _bl(2, 3, "The motion was seconded by Trustee Jezycki."),
        _bl(2, 4, "MOTION PASSED"),
    ]
    motion = pm._parse_motion_block(block, file_id=999)
    assert motion.flags == []
    assert "no_recorded_vote" in motion.notes
    assert motion.mover == "Trustee Noble"
    assert motion.seconder == "Trustee Jezycki"
    assert motion.tally == {"aye": None, "nay": None, "abstain": None, "absent": None}


def test_amendment_chain_supersedes_without_flags():
    first = [
        _bl(16, 1, "MOTION: to Approve the draft letter with revisions:"),
        _bl(16, 2, "Line 5: strike this and insert that; strike the other."),
        _bl(16, 3, "Moved by: Trustee Noble"),
    ]
    successor = "Motion: To modify the motion on the floor by adding a revision"
    motion = pm._parse_motion_block(first, file_id=999, successor_text=successor)
    assert motion.kind == "amended"
    assert motion.flags == []
    assert "superseded_by_amendment" in motion.notes
    assert motion.mover == "Trustee Noble"
    assert motion.outcome is None  # the vote belongs to the successor

    # Without an amendment successor, the same interrupted block is broken.
    broken = pm._parse_motion_block(
        first, file_id=999, successor_text="MOTION: to Approve something else."
    )
    assert broken.kind == "motion"
    assert "missing_outcome" in broken.flags


def test_none_with_stray_chars_tolerated_but_not_digits():
    names, stated = pm._parse_vote_section(" Trustee A, Trustee B 2")
    assert (names, stated) == (["Trustee A", "Trustee B"], [2])
    names, stated = pm._parse_vote_section(" None t 0")  # clerk typo, observed
    assert (names, stated) == ([], [0])
    # A full word after None is NOT dismissed as a typo.
    names, _ = pm._parse_vote_section(" None Trustee")
    assert names == ["None Trustee"]


def test_single_letter_noise_lines_dropped():
    page = pdftext.Page(
        page_number=3,
        text="IVGID Board of Trustees -3- Meeting Minutes May 30, 2025\n"
             "Real content line\nr\nAnother real line\n7",
        char_count=100,
    )
    body = pm._strip_page_furniture([page], [])
    texts = [bl.text for bl in body]
    assert "r" not in texts  # letter noise dropped
    assert "7" in texts  # lone digits kept (could be a wrapped count)


def test_attribution_line_does_not_split_block():
    """'Motion by X, Seconded by Y.' on its own line is the mover line of
    the block above it, not a new motion label."""
    block_lines = [
        _bl(15, 1, "MOTION: Approve the following consent matters: Item G.1."),
        _bl(15, 2, "and Item G.2. as submitted."),
        _bl(16, 1, "Motion by Trustee Secretary Noble, Seconded by Trustee Treasurer Homan."),
        _bl(16, 2, "YEAS: Trustee Secretary Noble, Trustee Tulloch 2"),
        _bl(16, 3, "NAYS: None 0"),
        _bl(16, 4, "MOTION PASSED"),
    ]
    assert pm._label_kind(block_lines[2].text) is None  # attribution, not label
    assert pm._label_kind("MOTION By Trustee Noble to approve the plan") == "mover_label"
    motion = pm._parse_motion_block(block_lines, file_id=999)
    assert motion.flags == []
    assert motion.mover == "Trustee Secretary Noble"
    assert motion.seconder == "Trustee Treasurer Homan"
    assert motion.tally["aye"] == 2


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
