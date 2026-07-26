"""Build the committed per-meeting records under data/meetings/ (step 6a).

Reads the IVGID minutes archive, runs Stage A over the live-format subset,
and writes one spec §2.4 JSON record per meeting. Nothing here matches items
across meetings — that is step 6b.

    python scripts/build_records.py

Event metadata (agenda file id, media URL) comes from the CivicClerk API;
the PDFs come from cache/ and are only fetched when missing. Output is
deterministic: sorted keys, no timestamps in any payload, documents
processed in a fixed order. Rebuilding an unchanged archive produces
byte-identical files, so the git diff of data/ is a real audit trail.

A document that is out of scope, or whose record fails the spec §2.7
validation gate, is recorded in data/skipped.json with its reason. Nothing
is dropped silently and nothing publishes with a caveat.
"""

from __future__ import annotations

import json
import sys
import traceback
from collections import Counter
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

import benchmark  # noqa: E402
import civicclerk  # noqa: E402
import parse_minutes  # noqa: E402
import records  # noqa: E402

DATA_DIR = REPO_ROOT / "data"
MEETINGS_DIR = DATA_DIR / "meetings"
CACHE_DIR = REPO_ROOT / "cache"
SLUG = "ivgid"
BEFORE_DATE = "2026-07-26"


def assemble(slug: str, before_date: str) -> list[dict[str, Any]]:
    """Every Minutes PDF in the archive, with the event fields spec §2.4's
    ``source`` block needs. Sorted by file id so the build order is fixed."""
    docs: list[dict[str, Any]] = []
    for event in civicclerk.list_events(slug, before_date):
        agendas = civicclerk.published_files(event, "Agenda")
        media = civicclerk.media_stream(event)
        for entry in civicclerk.published_files(event, "Minutes"):
            docs.append(
                {
                    "file_id": entry["fileId"],
                    "event_id": event["id"],
                    "event_name": event.get("eventName", ""),
                    "event_date": event.get("startDateTime", ""),
                    "minutes_name": entry.get("name", ""),
                    "agenda_file_id": agendas[0]["fileId"] if agendas else None,
                    # A relative mediaStreamPath has no established base URL
                    # (see civicclerk.media_stream); an unresolvable URL is
                    # not a source, so it is left null rather than guessed.
                    "media_url": (
                        media.path if media and not media.is_relative else None
                    ),
                }
            )
    docs.sort(key=lambda d: d["file_id"])
    return docs


def main() -> None:
    docs = assemble(SLUG, BEFORE_DATE)

    in_scope: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    for doc in docs:
        ok, reason = records.scope_decision(doc["event_date"], doc["event_name"])
        (in_scope if ok else skipped).append(
            doc if ok else {**doc, "reason": reason}
        )

    # meeting_id collides when one body meets twice on a date (IVGID's
    # continued public hearings do). Every member of a colliding group gets
    # the file id appended, so an id never depends on processing order.
    bases: Counter[str] = Counter()
    for doc in in_scope:
        _, code = records.identify_body(doc["event_name"])
        bases[records.meeting_id(doc["event_date"][:10], code)] += 1

    written: dict[str, str] = {}
    rejected: list[dict[str, Any]] = []
    money_total = 0
    money_flagged = 0
    status_counts: Counter[str] = Counter()
    violation_causes: Counter[str] = Counter()

    for i, doc in enumerate(in_scope, 1):
        file_id = doc["file_id"]
        print(f"[{i}/{len(in_scope)}] file {file_id} — "
              f"{doc['event_date'][:10]} {doc['event_name'][:52]}")
        try:
            pdf_bytes = benchmark.fetch_cached(SLUG, file_id, CACHE_DIR)
            parsed = parse_minutes.parse_minutes(
                pdf_bytes, file_id=file_id, minutes_name=doc["minutes_name"]
            )
        except Exception:
            rejected.append(
                {**doc, "reason": "parse or fetch failed",
                 "detail": traceback.format_exc(limit=3)}
            )
            continue

        _, code = records.identify_body(doc["event_name"])
        base = records.meeting_id(doc["event_date"][:10], code)
        record = records.build_record(
            file_id=file_id,
            event_id=doc["event_id"],
            event_name=doc["event_name"],
            event_date=doc["event_date"],
            parsed=parsed,
            agenda_file_id=doc["agenda_file_id"],
            media_url=doc["media_url"],
            disambiguate=bases[base] > 1,
        )

        violations = records.validate_record(record)
        if violations:
            # Spec §2.7 rule 7 — this does not publish with a caveat.
            for violation in violations:
                violation_causes[violation.split(":", 1)[-1].strip()] += 1
            rejected.append({**doc, "reason": "failed §2.7 validation",
                             "violations": violations})
            continue

        written[record["meeting_id"]] = records.serialise(record)
        status_counts[str(record["minutes_status"])] += 1
        for item in record["items"]:
            for money in item["money"]:
                money_total += 1
                if money["flags"]:
                    money_flagged += 1

    MEETINGS_DIR.mkdir(parents=True, exist_ok=True)
    for meeting_id, payload in sorted(written.items()):
        (MEETINGS_DIR / f"{meeting_id}.json").write_text(payload, encoding="utf-8")

    # A record whose id changed would otherwise leave an orphan behind; the
    # published set must be exactly what this build produced.
    pruned = []
    for path in sorted(MEETINGS_DIR.glob("*.json")):
        if path.stem not in written:
            path.unlink()
            pruned.append(path.name)

    (DATA_DIR / "skipped.json").write_text(
        json.dumps(
            {
                "built_by": "scripts/build_records.py",
                "scope": {
                    "board_from": records.LIVE_BOARD_FROM,
                    "audit_committee_from": records.LIVE_AUDIT_FROM,
                    "note": (
                        "Spec §2.6: v1 publishes new meetings only. The "
                        "deferred stenographic-transcript and narrative-prose "
                        "eras are the archive phase."
                    ),
                },
                "skipped": sorted(
                    (
                        {
                            "file_id": d["file_id"],
                            "event_id": d["event_id"],
                            "date": d["event_date"][:10],
                            "event_name": d["event_name"],
                            "reason": d["reason"],
                        }
                        for d in skipped
                    ),
                    key=lambda d: d["file_id"],
                ),
                "rejected": sorted(
                    (
                        {
                            "file_id": d["file_id"],
                            "date": d["event_date"][:10],
                            "event_name": d["event_name"],
                            "reason": d["reason"],
                            "violations": d.get("violations", []),
                        }
                        for d in rejected
                    ),
                    key=lambda d: d["file_id"],
                ),
            },
            indent=2,
            sort_keys=True,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    by_body: Counter[str] = Counter()
    for payload in written.values():
        by_body[json.loads(payload)["body"]] += 1

    print()
    print(f"corpus:      {len(docs)} minutes documents")
    print(f"in scope:    {len(in_scope)}")
    print(f"records:     {len(written)} written to {MEETINGS_DIR}")
    print(f"  by body:   {dict(by_body)}")
    print(f"skipped:     {len(skipped)} out of scope")
    for reason, count in sorted(Counter(d["reason"] for d in skipped).items()):
        print(f"    {count:>3}  {reason[:96]}")
    print(f"rejected:    {len(rejected)}")
    for entry in rejected:
        print(f"    file {entry['file_id']}: {entry['reason']}")
    if violation_causes:
        print(f"  causes:    {dict(violation_causes)}")
    print(f"minutes_status: {dict(status_counts)}")
    print(f"money:       {money_total} amounts, {money_flagged} flagged incomplete")
    if pruned:
        print(f"pruned stale records: {pruned}")


if __name__ == "__main__":
    main()
