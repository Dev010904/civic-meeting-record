"""Build the committed cross-meeting findings under data/tracking/ (step 6b).

    python scripts/build_tracking.py

Reads data/meetings/ only — the live-format published records — and writes
one file per spec §2.5 pattern plus an index. Every finding is validated
against §2.7 before it is written; a finding missing provenance at either
end of its link is rejected and recorded, never published with a caveat.

Output is deterministic: sorted keys, fixed order, no timestamps in any
payload. These files are committed and diffed.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

import tracking  # noqa: E402

MEETINGS_DIR = REPO_ROOT / "data" / "meetings"
TRACKING_DIR = REPO_ROOT / "data" / "tracking"

# Spec §2.5 patterns this build cannot detect from the available data.
# Recorded in the index rather than approximated, because every available
# proxy would require guessing (see the note on each).
NOT_DETECTED = {
    "contract_value_changed_between_agenda_and_minutes": (
        "Not detected: requires the agenda's stated value, and no agenda "
        "layer exists. Records carry source.agenda_file_id but agenda and "
        "agenda-packet PDFs are never fetched or parsed (spec §2.2 lists "
        "them as a separate extraction target). Comparing two minutes "
        "figures would answer a different question, so nothing is reported."
    ),
    "item_appeared_on_agenda_then_vanished": (
        "Not detected: the record layer carries only items that produced a "
        "motion, because items[] is built by grouping motions. An item that "
        "appeared on an agenda and produced no motion is therefore absent "
        "from the records by construction, and cannot be distinguished from "
        "an item that was never on the agenda. Detecting this needs either "
        "the agenda layer above, or 6a extended to emit motion-free items."
    ),
}


def load_records() -> list[dict[str, Any]]:
    paths = sorted(MEETINGS_DIR.glob("*.json"))
    if not paths:
        raise SystemExit(f"no records in {MEETINGS_DIR} — run build_records.py first")
    return [json.loads(p.read_text(encoding="utf-8")) for p in paths]


def main() -> None:
    records = load_records()
    findings = tracking.detect_all(records)

    written: dict[str, list[dict[str, Any]]] = {p: [] for p in tracking.PATTERNS}
    rejected: list[dict[str, Any]] = []
    for finding in findings:
        payload = finding.to_dict()
        violations = tracking.validate_finding(payload)
        if violations:
            rejected.append({
                "pattern": payload.get("pattern"),
                "summary": payload.get("summary", "")[:200],
                "violations": violations,
            })
            continue
        written[payload["pattern"]].append(payload)

    TRACKING_DIR.mkdir(parents=True, exist_ok=True)
    for pattern, entries in written.items():
        (TRACKING_DIR / f"{pattern}.json").write_text(
            tracking.serialise({
                "schema_version": tracking.SCHEMA_VERSION,
                "jurisdiction": tracking.JURISDICTION,
                "pattern": pattern,
                "description": tracking.PATTERNS[pattern],
                "count": len(entries),
                "asserted": sum(
                    1 for e in entries if e["confidence"] == tracking.CONFIDENCE_ASSERTED
                ),
                "candidates": sum(
                    1 for e in entries if e["confidence"] == tracking.CONFIDENCE_CANDIDATE
                ),
                "findings": entries,
            }),
            encoding="utf-8",
        )

    counts = {p: len(e) for p, e in written.items()}
    confidence = Counter(
        e["confidence"] for entries in written.values() for e in entries
    )
    (TRACKING_DIR / "index.json").write_text(
        tracking.serialise({
            "schema_version": tracking.SCHEMA_VERSION,
            "jurisdiction": tracking.JURISDICTION,
            "built_by": "scripts/build_tracking.py",
            "source": "data/meetings/ (live-format published records only)",
            "meetings_scanned": len(records),
            "date_range": [records[0]["date"], records[-1]["date"]] if records else None,
            "counts": counts,
            "confidence": dict(confidence),
            "rejected": rejected,
            "not_detected": NOT_DETECTED,
            "note": (
                "Findings report what the published records show. An absence "
                "is an absence from the published set of "
                f"{len(records)} meetings, not from the district's record."
            ),
        }),
        encoding="utf-8",
    )

    # Remove stale pattern files so the published set is exactly this build.
    pruned = []
    for path in sorted(TRACKING_DIR.glob("*.json")):
        if path.stem != "index" and path.stem not in tracking.PATTERNS:
            path.unlink()
            pruned.append(path.name)

    print(f"meetings scanned: {len(records)}")
    for pattern, count in sorted(counts.items()):
        entries = written[pattern]
        a = sum(1 for e in entries if e["confidence"] == tracking.CONFIDENCE_ASSERTED)
        print(f"  {pattern}: {count} ({a} asserted, {count - a} candidate)")
    print(f"rejected (failed §2.7 validation): {len(rejected)}")
    for entry in rejected:
        print(f"    {entry['pattern']}: {entry['violations']}")
    print(f"not detected: {', '.join(sorted(NOT_DETECTED))}")
    if pruned:
        print(f"pruned stale files: {pruned}")
    print(f"wrote {TRACKING_DIR}")


if __name__ == "__main__":
    main()
