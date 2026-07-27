"""Tests for cross-meeting item tracking (spec §2.5, step 6b).

The central risk here is not a missed link but a wrong one: linking two
unrelated items produces a false claim about a public body. The
similar-but-distinct tests below are the ones that matter most — IVGID
procurement titles share twenty-odd words of boilerplate, so a naive title
comparison would link almost any two contracts.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

import tracking  # noqa: E402

TRACKING_DIR = REPO_ROOT / "data" / "tracking"
MEETINGS_DIR = REPO_ROOT / "data" / "meetings"


# --- Fixtures built by hand, so the shapes under test are explicit -------


def _motion(text, file_id, page, outcome="passed"):
    return {
        "text": text, "mover": "Trustee A", "seconder": "Trustee B",
        "yeas": ["Trustee A"], "nays": [], "abstain": [], "absent": [],
        "tally": {"aye": 1, "nay": 0, "abstain": 0, "absent": 0},
        "outcome": outcome, "kind": "motion", "flags": [], "notes": [],
        "provenance": {"type": "pdf", "file_id": file_id, "page": page},
    }


def _money(raw, usd, vendor, purpose, ref, file_id, page, role="amount"):
    return {
        "amount_usd": usd, "amount_raw": raw, "role": role, "vendor": vendor,
        "purpose": purpose, "contract_ref": ref, "contingency": False,
        "approximate": False, "flags": [],
        "provenance": {"type": "pdf", "file_id": file_id, "page": page},
    }


def _item(number, title, motions, money, page=1):
    return {
        "number": number, "title": title, "page": page,
        "disposition": "passed" if motions else None,
        "motions": motions, "money": money, "media_timestamp": None,
        "media_timestamps": [],
        "extraction": {"stage": "A", "confidence": "exact", "flags": []},
    }


def _record(meeting_id, date, file_id, items):
    return {
        "schema_version": 1, "meeting_id": meeting_id, "jurisdiction": "ivgid",
        "body": "Board of Trustees", "date": date, "minutes_status": "approved",
        "minutes_status_basis": "file_name", "visual_draft_watermark": None,
        "source": {"event_id": 1, "agenda_file_id": None,
                   "minutes_file_id": file_id, "media_url": None},
        "document": {"unparseable_pages": [], "flags": []},
        "items": items,
    }


BOILERPLATE_HEAD = (
    "Approve and Authorize the Board Chair and Board Secretary to Sign and "
    "Execute an Agreement between Incline Village General Improvement "
    "District and "
)


@pytest.fixture(scope="module")
def committed():
    paths = sorted(p for p in TRACKING_DIR.glob("*.json") if p.stem != "index")
    assert paths, "no tracking output — run scripts/build_tracking.py first"
    return {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in paths}


# --- The wrong-link risk -------------------------------------------------


def test_similar_but_distinct_items_are_not_matched():
    """Two unrelated contracts sharing IVGID's procurement boilerplate.

    Every word of the opening clause is identical; only the vendor, the
    purpose and the project code differ. The later item carries change-order
    language, so the only thing standing between these two and a false link
    is the matching rule.
    """
    earlier = _record("ivgid-2025-03-12-bot", "2025-03-12", 1262, [
        _item(
            "G.2",
            BOILERPLATE_HEAD + "Olympus & Associates, Inc. for Exterior "
            "Re-coating of Water Reservoir R6C-1",
            [_motion("to Approve an Agreement in the Amount of $199,000.", 1262, 5)],
            [_money("$199,000", 199000.0, "Olympus & Associates, Inc",
                    "Exterior Re-coating of Water Reservoir R6C-1",
                    "CIP #2221WS22601", 1262, 5)],
        ),
    ])
    later = _record("ivgid-2025-12-10-bot", "2025-12-10", 1570, [
        _item(
            "H.1",
            BOILERPLATE_HEAD + "Miles Construction Incorporated for Removal "
            "and Replacement of the Existing Recreation Center HVAC System",
            [_motion("to Approve the Change Order for additional work; $3,154,402.",
                     1570, 16)],
            [_money("$3,154,402", 3154402.0, "Miles Construction Incorporated",
                    "Removal and Replacement of the Existing Recreation Center "
                    "HVAC System", "CIP #4899BD2502", 1570, 16)],
        ),
    ])

    findings = tracking.detect_all([earlier, later])
    assert findings == [], [f.summary for f in findings]


def test_boilerplate_alone_never_reaches_the_candidate_threshold():
    left = BOILERPLATE_HEAD + "Olympus & Associates, Inc. for Exterior Re-coating"
    right = BOILERPLATE_HEAD + "Miles Construction Incorporated for HVAC Replacement"
    assert tracking.similarity(left, right) < tracking.CANDIDATE_SIMILARITY
    # The boilerplate really is shared — this is not passing by accident.
    assert tracking.normalise_title(left).split()[:6] == \
        tracking.normalise_title(right).split()[:6]


def test_a_thin_title_matches_nothing():
    """A title with too few distinctive words must never link, however much
    of it happens to overlap."""
    assert tracking.similarity("Approval of the Agenda", "Approval of the Agenda") == 0.0
    assert tracking.distinctive_tokens("Review and Discuss") == frozenset()


def test_different_project_codes_do_not_link():
    assert tracking.contract_key("CIP #2221WS22601") != tracking.contract_key(
        "CIP #2299DI1707"
    )
    # …but formatting differences in the same code do.
    assert tracking.contract_key("CIP #2299DI1707") == tracking.contract_key(
        "CIP#2299DI1707"
    )


# --- Positive controls: the matcher does still fire ----------------------


def _linked_pair(later_ref, later_vendor, later_title_tail):
    earlier = _record("ivgid-2025-01-29-bot", "2025-01-29", 1140, [
        _item("E.1", BOILERPLATE_HEAD + "American Ramp Company for Construction "
              "of the Incline Bike Park Phase II",
              [_motion("to Approve an Agreement in the Amount of $297,000.", 1140, 4)],
              [_money("$297,000", 297000.0, "American Ramp Company",
                      "Construction of the Incline Bike Park - Phase II",
                      "Project #4378LI2601", 1140, 4)]),
    ])
    later = _record("ivgid-2026-03-11-bot", "2026-03-11", 2665, [
        _item("H.1", BOILERPLATE_HEAD + later_title_tail,
              [_motion("to Approve a Change Order to Pave the Existing Pump Tracks "
                       "in the Amount of $112,000.", 2665, 11)],
              [_money("$112,000", 112000.0, later_vendor,
                      "Change Order to Pave the Pump Tracks", later_ref, 2665, 11)]),
    ])
    return [earlier, later]


def test_shared_project_code_is_asserted():
    findings = tracking.detect_all(
        _linked_pair("Project #4378LI2601", "American Ramp Company",
                     "American Ramp Company for Construction of the Incline "
                     "Bike Park Phase II")
    )
    increases = [f for f in findings
                 if f.pattern == "amount_increase_after_prior_approval"]
    assert increases, "shared project code should link the two meetings"
    assert all(f.confidence == tracking.CONFIDENCE_ASSERTED for f in increases)
    assert len(increases[0].endpoints) == 2


def test_shared_vendor_without_project_code_is_only_a_candidate():
    """The same firm can hold several unrelated contracts, so a vendor name
    is never identity on its own."""
    findings = tracking.detect_all(
        _linked_pair(None, "American Ramp Company",
                     "American Ramp Company for Construction of the Incline "
                     "Bike Park Phase II")
    )
    increases = [f for f in findings
                 if f.pattern == "amount_increase_after_prior_approval"]
    assert increases, "shared vendor plus overlapping title should be offered"
    assert all(f.confidence == tracking.CONFIDENCE_CANDIDATE for f in increases)


def test_shared_vendor_with_unrelated_title_does_not_link():
    findings = tracking.detect_all(
        _linked_pair(None, "American Ramp Company",
                     "American Ramp Company for Replacement of the Burnt Cedar "
                     "Backup Generator Fuel Tank at the Water Treatment Plant")
    )
    assert [f for f in findings
            if f.pattern == "amount_increase_after_prior_approval"] == []


# --- Motion-free items and the vanishing pattern -------------------------


def _removal_meeting(target_has_motion: bool):
    target_motions = (
        [_motion("to Approve the Employee Pass Program.", 1428, 15)]
        if target_has_motion else []
    )
    return _record("ivgid-2025-05-14-bot", "2025-05-14", 1428, [
        _item("D", "APPROVAL OF AGENDA",
              [_motion('All in favor of Removing Item H.1. Review, discuss, and '
                       'possibly approve the Employee Pass Program for Beach '
                       'access; From the Agenda, please vote by saying "Yea".',
                       1428, 8, outcome="failed")], [], page=7),
        _item("H.1", "Review, Discuss, and Approve the Employee Pass Program "
                     "for Beach Access at District Beaches",
              target_motions, [], page=15),
    ])


def test_a_removal_vote_links_to_the_item_it_named():
    """The target sits in the same meeting. Before records carried
    motion-free items it was invisible, so the vote could not be linked to
    what it was aimed at."""
    findings = tracking.detect_all([_removal_meeting(target_has_motion=False)])
    vote = next(f for f in findings if f.pattern == "agenda_removal_vote")
    assert len(vote.endpoints) == 2
    assert vote.endpoints[1].item_number == "H.1"
    assert vote.endpoints[1].page == 15
    assert "Item H.1 appears on the agenda of the same meeting" in vote.summary


def test_a_named_item_that_produced_no_motion_is_reported_as_vanished():
    findings = tracking.detect_all([_removal_meeting(target_has_motion=False)])
    vanished = [f for f in findings if f.pattern == "item_vanished_from_agenda"]
    assert len(vanished) == 1
    assert vanished[0].confidence == tracking.CONFIDENCE_CANDIDATE
    assert vanished[0].endpoints[0].item_number == "H.1"


def test_a_named_item_that_was_acted_on_is_not_reported_as_vanished():
    """Removed-but-still-acted-on is not a vanishing item."""
    findings = tracking.detect_all([_removal_meeting(target_has_motion=True)])
    assert [f for f in findings if f.pattern == "item_vanished_from_agenda"] == []


def test_an_explicit_removal_note_is_asserted_not_a_candidate():
    record = _record("ivgid-2025-03-05-bot", "2025-03-05", 1229, [
        _item("E.1", "Review and Discuss Fiscal Year 2024/2025 Mid-Year Budget; "
                     "Discussion, Direction, and Possible Action - This Item was "
                     "removed by staff", [], [], page=2),
    ])
    findings = tracking.detect_all([record])
    vanished = [f for f in findings if f.pattern == "item_vanished_from_agenda"]
    assert len(vanished) == 1
    assert vanished[0].confidence == tracking.CONFIDENCE_ASSERTED
    assert "removal recorded in the item heading" == vanished[0].match_basis


def test_an_ordinary_motion_free_item_is_not_reported_as_vanished():
    """A verbal update that appears once and does not recur is the ordinary
    shape of a report item, not a finding."""
    record = _record("ivgid-2025-02-12-bot", "2025-02-12", 1171, [
        _item("E.3", "Verbal Update on the Tyler Enterprises ERP Implementation "
                     "and the Committee Structure", [], [], page=2),
    ])
    assert tracking.detect_all([record]) == []


# --- Provenance is required at every end ---------------------------------


def _valid_finding():
    findings = tracking.detect_all(
        _linked_pair("Project #4378LI2601", "American Ramp Company",
                     "American Ramp Company for Construction of the Incline "
                     "Bike Park Phase II")
    )
    finding = next(f for f in findings
                   if f.pattern == "amount_increase_after_prior_approval")
    return finding.to_dict()


def test_valid_finding_passes_validation():
    assert tracking.validate_finding(_valid_finding()) == []


@pytest.mark.parametrize("end", [0, 1])
def test_finding_missing_either_ends_provenance_is_rejected(end):
    """Both ends of a link must be traceable. A finding a reader can only
    verify at one end is not a verifiable claim."""
    finding = _valid_finding()
    del finding["endpoints"][end]["provenance"]
    violations = tracking.validate_finding(finding)
    assert any("without provenance" in v for v in violations), violations


@pytest.mark.parametrize("field,bad", [("file_id", 0), ("page", 0), ("type", "video")])
def test_invalid_provenance_at_the_far_end_is_rejected(field, bad):
    finding = _valid_finding()
    finding["endpoints"][1]["provenance"][field] = bad
    assert tracking.validate_finding(finding)


def test_a_link_with_only_one_endpoint_is_rejected():
    finding = _valid_finding()
    finding["endpoints"] = finding["endpoints"][:1]
    violations = tracking.validate_finding(finding)
    assert any("every end needs provenance" in v for v in violations), violations


def test_a_link_whose_endpoints_are_the_same_meeting_is_rejected():
    finding = _valid_finding()
    finding["endpoints"][1]["meeting_id"] = finding["endpoints"][0]["meeting_id"]
    violations = tracking.validate_finding(finding)
    assert any("same meeting" in v for v in violations), violations


def test_a_rejected_finding_is_not_written(tmp_path):
    finding = _valid_finding()
    del finding["endpoints"][1]["provenance"]
    out = tmp_path / "findings.json"
    if not tracking.validate_finding(finding):
        out.write_text(tracking.serialise(finding), encoding="utf-8")
    assert not out.exists()


# --- The committed output -------------------------------------------------


def test_every_committed_finding_validates(committed):
    total = 0
    for payload in committed.values():
        for finding in payload["findings"]:
            total += 1
            assert tracking.validate_finding(finding) == [], finding["summary"]
    assert total > 0


def test_every_committed_finding_traces_to_a_real_meeting_record(committed):
    known = {
        json.loads(p.read_text(encoding="utf-8"))["meeting_id"]:
            json.loads(p.read_text(encoding="utf-8"))["source"]["minutes_file_id"]
        for p in MEETINGS_DIR.glob("*.json")
    }
    for payload in committed.values():
        for finding in payload["findings"]:
            for endpoint in finding["endpoints"]:
                assert endpoint["meeting_id"] in known
                assert endpoint["provenance"]["file_id"] == known[endpoint["meeting_id"]]


def test_findings_are_reports_not_assertions(committed):
    """Spec §2.7 and §5: the site reports what a meeting recorded; it does
    not assert facts of its own. Every summary is framed as a report, and
    none of them editorialises."""
    editorial = (
        "quietly", "secretly", "buried", "hid", "hidden", "sneak", "failed to",
        "refused to", "should have", "apparently", "seems", "suggests",
        "controversial", "raises questions",
    )
    for payload in committed.values():
        for finding in payload["findings"]:
            summary = finding["summary"]
            assert summary.startswith("The minutes of"), summary
            lowered = summary.lower()
            for word in editorial:
                assert word not in lowered, f"{word!r} in: {summary}"


def test_absence_claims_are_scoped_to_the_published_set(committed):
    """An item missing from 39 meetings is missing from the published set,
    not from the district's record. Any absence claim must say so."""
    for payload in committed.values():
        for finding in payload["findings"]:
            if "no later meeting" in finding["summary"]:
                assert "published set" in finding["summary"], finding["summary"]


def test_index_records_the_undetectable_patterns():
    index = json.loads((TRACKING_DIR / "index.json").read_text(encoding="utf-8"))
    assert index["not_detected"], "patterns that cannot be detected must be recorded"
    for reason in index["not_detected"].values():
        assert reason.startswith("Not detected:")
    assert index["meetings_scanned"] > 0
    assert index["rejected"] == []


# --- Determinism ----------------------------------------------------------


def test_detection_is_byte_identical_across_two_builds():
    records = [json.loads(p.read_text(encoding="utf-8"))
               for p in sorted(MEETINGS_DIR.glob("*.json"))]
    first = tracking.serialise([f.to_dict() for f in tracking.detect_all(records)])
    second = tracking.serialise([f.to_dict() for f in tracking.detect_all(records)])
    assert first == second


def test_detection_does_not_depend_on_input_order():
    """Records arrive in filename order; findings must not."""
    records = [json.loads(p.read_text(encoding="utf-8"))
               for p in sorted(MEETINGS_DIR.glob("*.json"))]
    forward = tracking.serialise([f.to_dict() for f in tracking.detect_all(records)])
    reverse = tracking.serialise(
        [f.to_dict() for f in tracking.detect_all(list(reversed(records)))]
    )
    assert forward == reverse


def test_rebuilding_reproduces_the_committed_files(committed):
    records = [json.loads(p.read_text(encoding="utf-8"))
               for p in sorted(MEETINGS_DIR.glob("*.json"))]
    rebuilt: dict[str, list] = {p: [] for p in tracking.PATTERNS}
    for finding in tracking.detect_all(records):
        payload = finding.to_dict()
        if not tracking.validate_finding(payload):
            rebuilt[payload["pattern"]].append(payload)
    for pattern, entries in rebuilt.items():
        assert tracking.serialise(entries) == tracking.serialise(
            committed[pattern]["findings"]
        ), f"{pattern} is not reproducible"


def test_no_timestamp_fields_in_tracking_payloads(committed):
    banned = {"generated", "generated_at", "built_at", "timestamp", "run_date", "now"}

    def keys(payload):
        if isinstance(payload, dict):
            for key, value in payload.items():
                yield key
                yield from keys(value)
        elif isinstance(payload, list):
            for value in payload:
                yield from keys(value)

    for payload in committed.values():
        assert not (set(k.lower() for k in keys(payload)) & banned)
