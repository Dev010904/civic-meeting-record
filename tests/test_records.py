"""Tests for the per-meeting published records (spec §2.4, step 6a).

Schema and gate tests run against every record actually committed under
data/meetings/ — not a synthetic sample — because those files are the
published product. Money extraction is tested against motion text copied
verbatim from IVGID minutes, including the two real clerical defects in the
archive ("$359,97", "$307,9250") and the settlement clause that is shaped
like a procurement but names a private individual.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

import parse_minutes as pm  # noqa: E402
import records  # noqa: E402

DATA_DIR = REPO_ROOT / "data"
MEETINGS_DIR = DATA_DIR / "meetings"
FIXTURES = Path(__file__).resolve().parent / "fixtures"

PROV = pm.Provenance(file_id=2783, page=2)


def _record_paths() -> list[Path]:
    return sorted(MEETINGS_DIR.glob("*.json"))


@pytest.fixture(scope="module")
def built() -> list[dict]:
    paths = _record_paths()
    assert paths, (
        "no records under data/meetings/ — run scripts/build_records.py first"
    )
    return [json.loads(p.read_text(encoding="utf-8")) for p in paths]


# --- Schema (spec §2.4) ---------------------------------------------------


def test_every_record_has_the_spec_2_4_shape(built):
    for record in built:
        for key in (
            "meeting_id", "jurisdiction", "body", "date", "source", "items",
            "minutes_status",
        ):
            assert key in record, f"{record.get('meeting_id')}: missing {key}"
        assert record["jurisdiction"] == records.JURISDICTION
        assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", record["date"])
        assert record["meeting_id"].startswith(f"ivgid-{record['date']}-")
        source = record["source"]
        assert set(source) == {
            "event_id", "agenda_file_id", "minutes_file_id", "media_url"
        }
        assert isinstance(source["event_id"], int)
        assert isinstance(source["minutes_file_id"], int)
        for item in record["items"]:
            assert set(item) == {
                "number", "title", "disposition", "motions", "money",
                "media_timestamp", "media_timestamps", "extraction",
            }
            assert item["extraction"]["stage"] == "A"
            assert item["extraction"]["confidence"] in ("exact", "flagged")
            assert item["disposition"] in (
                None, "passed", "failed", "tabled", "continued"
            )


def test_meeting_ids_are_unique(built):
    ids = [r["meeting_id"] for r in built]
    assert len(ids) == len(set(ids))


def test_every_record_passes_its_own_validation_gate(built):
    for record in built:
        assert records.validate_record(record) == [], record["meeting_id"]


def test_minutes_status_is_present_and_valid_on_every_record(built):
    """Spec §2.7 rule 2. None is legitimate (undetermined, treated as draft
    downstream); a missing field is not."""
    for record in built:
        assert "minutes_status" in record
        assert record["minutes_status"] in (None, "draft", "approved")


def test_every_claim_carries_provenance(built):
    """Spec §2.7 rule 7 — and rule 1: a vote's provenance must be this
    meeting's minutes file, never anything else."""
    seen = 0
    for record in built:
        minutes_file_id = record["source"]["minutes_file_id"]
        for item in record["items"]:
            claims = (
                item["motions"] + item["money"] + item["media_timestamps"]
            )
            for claim in claims:
                seen += 1
                provenance = claim["provenance"]
                assert provenance["type"] == "pdf"
                assert provenance["file_id"] == minutes_file_id
                assert provenance["page"] >= 1
    assert seen > 0


# --- The validation gate rejects rather than publishing with a caveat ----


def _valid_record() -> dict:
    return records.build_record(
        file_id=2783,
        event_id=755,
        event_name="Board of Trustees Meeting",
        event_date="2026-05-20T16:00:00Z",
        parsed=pm.ParsedMinutes(
            motions=[
                pm.Motion(
                    text="to Approve the thing in the Amount of $199,000.00",
                    mover="Trustee Homan", seconder="Trustee Jezycki",
                    yeas=["Trustee Homan"], nays=[], abstain=[], absent=[],
                    tally={"aye": 1, "nay": 0, "abstain": 0, "absent": 0},
                    stated={}, outcome="passed", provenance=PROV,
                    item_number="E.1", item_title="Approve the thing",
                )
            ],
            media_timestamps=[],
            public_comments=[],
            unparseable_pages=[],
            flags=[],
            minutes_status="approved",
        ),
    )


def test_a_record_missing_provenance_is_rejected_not_written(tmp_path):
    record = _valid_record()
    assert records.validate_record(record) == []

    del record["items"][0]["motions"][0]["provenance"]
    violations = records.validate_record(record)
    assert violations and "without provenance" in violations[0]

    # The builder's contract: violations mean the file is never written.
    written = tmp_path / f"{record['meeting_id']}.json"
    if not records.validate_record(record):
        written.write_text(records.serialise(record), encoding="utf-8")
    assert not written.exists()


def test_provenance_from_a_foreign_file_is_rejected():
    """Spec §2.7 rule 1 — votes come only from this meeting's minutes."""
    record = _valid_record()
    record["items"][0]["motions"][0]["provenance"]["file_id"] = 9999
    violations = records.validate_record(record)
    assert any("is not this meeting's minutes file" in v for v in violations)


def test_non_document_provenance_is_rejected():
    """Spec §2.7 rule 3 — the no-name-from-audio gate stands before audio
    exists, so a transcript-sourced claim can never slip in later."""
    record = _valid_record()
    record["items"][0]["motions"][0]["provenance"]["type"] = "video"
    violations = records.validate_record(record)
    assert any("is not a document" in v for v in violations)


def test_missing_minutes_status_is_rejected():
    record = _valid_record()
    del record["minutes_status"]
    assert any("minutes_status" in v for v in records.validate_record(record))


def test_commenter_derived_field_is_rejected():
    """Spec §2.7 rule 4 — private commenters are excluded entirely."""
    record = _valid_record()
    record["items"][0]["commenter"] = "a name"
    violations = records.validate_record(record)
    assert any("forbidden commenter-derived field" in v for v in violations)


# --- No public-comment content reaches data/ -----------------------------


def test_no_public_comment_text_or_names_anywhere_in_data():
    """Harvest every commenter name and the opening line of every verbatim
    comment straight from a real minutes PDF, then prove none of it appears
    in any committed record. The record type has no field for it; this
    proves the segmentation upstream holds too."""
    import pdftext

    blob = "\n".join(
        p.read_text(encoding="utf-8") for p in _record_paths()
    ) + (DATA_DIR / "skipped.json").read_text(encoding="utf-8")

    marker = re.compile(
        r"Public\s+comments?\s+provided\s+by\s+(.+?)\s+is\s+transcribed\s+below",
        re.IGNORECASE,
    )
    checked = 0
    for pdf in ("ivgid_minutes_2778.pdf", "ivgid_minutes_draft_2783.pdf"):
        lines = pdftext.extract_lines((FIXTURES / pdf).read_bytes())
        for i, line in enumerate(lines):
            match = marker.search(line.text)
            if not match:
                continue
            name = match.group(1).strip()
            checked += 1
            assert name not in blob, f"commenter name {name!r} leaked into data/"
            # The first substantial line of the comment itself.
            for following in lines[i + 1 : i + 4]:
                text = following.text.strip()
                if len(text) > 40:
                    assert text not in blob, f"comment text leaked: {text[:60]!r}"
                    break
    assert checked > 0, "fixture yielded no commenter names to check"


def test_records_carry_no_commenter_fields(built):
    for record in built:
        keys = {k.lower() for k in records._find_keys(record)}
        assert not (keys & records._FORBIDDEN_KEYS)
        # The aggregate count is the only comment-derived value permitted.
        assert isinstance(record["public_comment_count"], int)


# --- Determinism ---------------------------------------------------------


def test_serialisation_is_byte_identical_across_builds():
    """Records are committed and diffed; a noisy diff destroys the audit
    trail. Building the same input twice must produce identical bytes."""
    first = records.serialise(_valid_record())
    second = records.serialise(_valid_record())
    assert first == second


@pytest.mark.parametrize("file_id", [2783, 2670, 1559, 2649])
def test_building_the_same_document_twice_is_byte_identical(file_id):
    """Build twice from the same PDF through the whole path — parse, build,
    serialise — and compare the bytes. Catches nondeterministic iteration
    order and any timestamp that crept into the payload."""
    pdf = REPO_ROOT / "cache" / f"{file_id}.pdf"
    if not pdf.exists():
        pytest.skip(f"cache/{file_id}.pdf not present")

    def build() -> str:
        parsed = pm.parse_minutes(
            pdf.read_bytes(), file_id=file_id, minutes_name="Minutes"
        )
        return records.serialise(
            records.build_record(
                file_id=file_id,
                event_id=1,
                event_name="Board of Trustees Meeting",
                event_date="2026-05-20T16:00:00Z",
                parsed=parsed,
            )
        )

    first, second = build(), build()
    assert first == second
    assert json.loads(first)  # and it is still valid JSON


def test_rebuilding_every_committed_record_reproduces_it_byte_for_byte():
    """The strong form: re-parse each cached PDF, rebuild the record and
    compare against what is committed. If the committed files were not
    reproducible, the git diff would stop being an audit trail."""
    skipped_meta = json.loads(
        (DATA_DIR / "skipped.json").read_text(encoding="utf-8")
    )
    assert skipped_meta["scope"]["board_from"] == records.LIVE_BOARD_FROM

    checked = 0
    for path in _record_paths():
        committed = json.loads(path.read_text(encoding="utf-8"))
        pdf = REPO_ROOT / "cache" / f"{committed['source']['minutes_file_id']}.pdf"
        if not pdf.exists():
            continue
        parsed = pm.parse_minutes(
            pdf.read_bytes(), file_id=committed["source"]["minutes_file_id"]
        )
        rebuilt = records.build_record(
            file_id=committed["source"]["minutes_file_id"],
            event_id=committed["source"]["event_id"],
            event_name=committed["body"],
            event_date=committed["date"],
            parsed=parsed,
            agenda_file_id=committed["source"]["agenda_file_id"],
            media_url=committed["source"]["media_url"],
        )
        # minutes_name is not replayed here, so compare everything the PDF
        # alone determines.
        assert records.serialise(rebuilt["items"]) == records.serialise(
            committed["items"]
        ), f"{path.name}: items are not reproducible"
        checked += 1
    assert checked > 0


def test_no_timestamp_fields_in_any_payload(built):
    for record in built:
        for key in records._find_keys(record):
            assert key.lower() not in {"generated", "generated_at", "built_at",
                                       "timestamp", "now", "run_date"}


# --- Scope ---------------------------------------------------------------


def test_scope_boundaries_match_the_format_eras():
    assert records.scope_decision("2026-05-20T00:00:00Z", "Board of Trustees Meeting")[0]
    assert records.scope_decision("2025-02-12T00:00:00Z", "Regular Meeting of the Board of Trustees")[0]
    # The structured Audit Committee format begins December 2024.
    assert records.scope_decision("2024-12-19T00:00:00Z", "Regular Meeting of the Audit Committee")[0]
    assert not records.scope_decision("2024-11-18T00:00:00Z", "Regular Meeting of the Audit Committee")[0]
    # Deferred eras, each with a recorded reason.
    for date, name in (
        ("2025-01-08T00:00:00Z", "Regular Meeting of the Board of Trustees"),
        ("2023-09-27T00:00:00Z", "Regular Meeting of the Board of Trustees"),
        ("2021-05-12T00:00:00Z", "Board of Trustees Meeting"),
    ):
        in_scope, reason = records.scope_decision(date, name)
        assert not in_scope
        assert reason


def test_every_skipped_document_records_a_reason():
    skipped = json.loads((DATA_DIR / "skipped.json").read_text(encoding="utf-8"))
    assert skipped["skipped"], "expected deferred-era documents to be recorded"
    for entry in skipped["skipped"]:
        assert entry["reason"], entry
        assert entry["file_id"] and entry["date"]
    for entry in skipped["rejected"]:
        assert entry["reason"], entry


def test_body_identification():
    assert records.identify_body("Regular Meeting of the Audit Committee") == (
        "Audit Committee", "audit"
    )
    assert records.identify_body("Board of Trustees Meeting") == (
        "Board of Trustees", "bot"
    )
    assert records.identify_body("Regular Meeting of the Capitol Investment Committee") == (
        "Capital Investment Committee", "cic"
    )


# --- Money extraction (spec §2.2) ----------------------------------------


def _money(text):
    return records.extract_money(text, PROV)


def test_contract_amount_vendor_purpose_and_reference():
    text = (
        "to Approve and Authorize the Board Chair and Board Secretary to Sign "
        "and Execute an Agreement between Incline Village General Improvement "
        "District and Olympus & Associates, Inc. for Exterior Re-coating of "
        "Water Reservoir R6C-1; FY2025/26 Utilities: Water: CIP #2221WS22601; "
        "in the Amount of $199,000.00; and Authorize staff to Execute Change "
        "Orders for Additional Work if required, of Approximately 5% of the "
        "Construction Contract Value not to Exceed $10,000."
    )
    entries = _money(text)
    assert [e.amount_usd for e in entries] == [199000.0, 10000.0]
    principal, contingency = entries
    assert principal.role == "amount"
    assert principal.vendor == "Olympus & Associates, Inc"
    assert principal.purpose == "Exterior Re-coating of Water Reservoir R6C-1"
    assert principal.contract_ref == "CIP #2221WS22601"
    # Spec §2.2 asks whether a contingency was attached.
    assert principal.contingency is True
    assert principal.flags == []
    assert contingency.role == "not_to_exceed"


def test_every_amount_carries_its_own_provenance():
    entries = _money("in the Amount of $1,000 and not to Exceed $200")
    assert entries
    for entry in entries:
        assert entry.provenance is PROV
        assert entry.provenance.file_id == 2783


def test_malformed_amounts_are_flagged_never_repaired():
    """Real clerical defects in the archive. The intended value cannot be
    recovered without guessing, so no value is recorded."""
    for raw, text in (
        ("$359,97", "Carollo Engineers for a SCADA Master Plan; in the Amount of $359,97;"),
        ("$307,9250", "for not to exceed a total of $307,9250 cash and $53,000 trade."),
    ):
        entry = next(e for e in _money(text) if e.amount_raw == raw)
        assert entry.amount_usd is None
        assert "malformed_amount" in entry.flags
        assert entry.amount_raw == raw


def test_a_list_comma_is_not_read_as_a_thousands_group():
    entries = _money("in the Amount of $112,000; IVGID Portion of $56,000, Private Donor")
    assert [e.amount_raw for e in entries] == ["$112,000", "$56,000"]
    assert [e.amount_usd for e in entries] == [112000.0, 56000.0]
    assert all(e.flags == [] or "malformed_amount" not in e.flags for e in entries)


def test_missing_vendor_is_null_and_flagged_never_guessed():
    entries = _money("to Approve the Recreation Facility Fee totaling $1,375;")
    assert len(entries) == 1
    assert entries[0].vendor is None
    assert entries[0].purpose is None
    assert "vendor_not_extracted" in entries[0].flags
    assert "purpose_not_extracted" in entries[0].flags


def test_settlement_counterparty_is_not_recorded_as_a_vendor():
    """"Settlement Agreement with <name>" is shaped exactly like a
    procurement clause but names a private individual in litigation, not a
    vendor. The field stays null and flagged rather than naming them."""
    text = (
        "to Approval of Settlement Agreement with Sheila A. Leijon in Amount "
        "of $105,000 Relating to Leijon v. Incline Village General "
        "Improvement District, Employee-Management Relations Board Case No. "
        "2024-022."
    )
    entries = _money(text)
    assert len(entries) == 1
    assert entries[0].amount_usd == 105000.0
    assert entries[0].vendor is None
    assert "vendor_not_extracted" in entries[0].flags
    assert "Leijon" not in str(entries[0].vendor)


def test_consent_calendar_attributes_each_amount_to_its_own_vendor():
    """One motion, several items, several vendors — each amount takes the
    vendor clause above it, and a fund reference belonging to an earlier
    item is not borrowed by a later one."""
    text = (
        "to approve the Consent Calendar as documented. Item F.3. Approve an "
        "Agreement between Incline Village General Improvement District and "
        "Construction Material Engineers, Inc. to provide Professional "
        "Services, for an Amount Not to Exceed $553,925 Effluent Export Line "
        "Project; Fund: Utilities; Project #2524SS1010; and, Item F.4. "
        "Approve a Purchase Agreement between the District and American "
        "Hazmat Rentals (AHR) for Procurement of a Hazardous Waste Storage "
        "Container; Fund: Utilities; in the amount of $100,301."
    )
    first, second = _money(text)
    assert first.amount_usd == 553925.0
    assert first.vendor == "Construction Material Engineers, Inc"
    assert first.contract_ref == "Project #2524SS1010"
    assert second.amount_usd == 100301.0
    assert second.vendor == "American Hazmat Rentals (AHR)"
    assert second.purpose == "Procurement of a Hazardous Waste Storage Container"
    # The earlier item's project number must not leak onto this amount.
    assert second.contract_ref is None


def test_the_district_is_never_its_own_vendor():
    text = (
        "to Approve an Agreement between Incline Village General Improvement "
        "District and the District in the Amount of $500."
    )
    for entry in _money(text):
        assert entry.vendor != "Incline Village General Improvement District"


def test_multiplier_and_approximate_amounts():
    entry = _money("allocating Approximately $4.05 Million in the General Fund")[0]
    assert entry.amount_usd == 4_050_000.0
    assert entry.approximate is True


def test_money_is_extracted_from_the_real_corpus(built):
    """Coverage sanity on the committed records: money exists, every entry
    carries provenance, and nothing claims a vendor without a value."""
    total = 0
    for record in built:
        for item in record["items"]:
            for entry in item["money"]:
                total += 1
                assert entry["provenance"]["file_id"] == record["source"]["minutes_file_id"]
                assert entry["amount_raw"].startswith("$")
                if entry["amount_usd"] is None:
                    assert "malformed_amount" in entry["flags"]
                if entry["vendor"] is None:
                    assert "vendor_not_extracted" in entry["flags"]
    assert total > 0
