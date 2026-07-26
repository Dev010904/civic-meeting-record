"""Generate benchmark/VERIFY.md — the hand-verification checklist.

Seeded random sample of 25 motions from the live-format subset (documents
dated 2025-02-01 or later, plus Audit Committee documents from 2024-12-01
or later — the format-era boundaries established in step 5), forced to
include every truncated_outcome case, spread across as many distinct
documents as possible, sorted by document then page.

Reads benchmark/results.json; re-parses only the sampled documents (from
cache/) to attach the media timestamps recorded on each motion's page.

Usage: python scripts/make_verify.py
"""

from __future__ import annotations

import json
import random
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

import parse_minutes  # noqa: E402

SEED = 20260726
SAMPLE_SIZE = 25
BENCH_DIR = REPO_ROOT / "benchmark"
CACHE_DIR = REPO_ROOT / "cache"

CRITERIA = (
    "documents dated 2025-02-01 or later, plus Audit Committee documents "
    "dated 2024-12-01 or later (the format-era boundaries: the structured "
    "Board era begins February 2025; the structured Audit era begins "
    "December 2024). All truncated_outcome motions are force-included; the "
    "rest are drawn round-robin across shuffled documents so the sample "
    "spans as many distinct PDFs as possible."
)


def in_subset(doc: dict[str, Any]) -> bool:
    if "audit" in doc["event_name"].lower():
        return doc["event_date"] >= "2024-12-01"
    return doc["event_date"] >= "2025-02-01"


def pick_sample(documents: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rng = random.Random(SEED)
    docs = [d for d in documents if in_subset(d) and d["motions"]]

    def entry(doc: dict[str, Any], motion: dict[str, Any]) -> dict[str, Any]:
        return {"file_id": doc["file_id"], "event_date": doc["event_date"][:10],
                "event_name": doc["event_name"].strip(), **motion}

    # Force-include every truncated_outcome case.
    sample = [
        entry(d, m)
        for d in docs
        for m in d["motions"]
        if "truncated_outcome" in m["flags"]
    ]
    taken = {(s["file_id"], s["page"], s["text"]) for s in sample}

    rng.shuffle(docs)
    queues = [
        (d, rng.sample(range(len(d["motions"])), len(d["motions"]))) for d in docs
    ]
    round_index = 0
    while len(sample) < SAMPLE_SIZE and any(
        round_index < len(q) for _, q in queues
    ):
        for doc, queue in queues:
            if len(sample) >= SAMPLE_SIZE:
                break
            if round_index < len(queue):
                motion = doc["motions"][queue[round_index]]
                key = (doc["file_id"], motion["page"], motion["text"])
                if key not in taken:
                    taken.add(key)
                    sample.append(entry(doc, motion))
        round_index += 1
    sample.sort(key=lambda s: (s["event_date"], s["file_id"], s["page"]))
    return sample


def page_timestamps(sample: list[dict[str, Any]]) -> dict[tuple[int, int], list[str]]:
    """Media timestamps per (file_id, page), for the sampled documents only."""
    out: dict[tuple[int, int], list[str]] = {}
    for file_id in sorted({s["file_id"] for s in sample}):
        parsed = parse_minutes.parse_minutes(
            (CACHE_DIR / f"{file_id}.pdf").read_bytes(), file_id=file_id
        )
        for ts in parsed.media_timestamps:
            rendered = ts.start if ts.end is None else f"{ts.start} - {ts.end}"
            out.setdefault((file_id, ts.provenance.page), []).append(rendered)
    return out


def render(sample: list[dict[str, Any]], stamps: dict) -> str:
    lines: list[str] = []
    add = lines.append
    distinct = len({s["file_id"] for s in sample})
    add("# Hand-verification checklist — Stage A parser")
    add("")
    add(f"Seed: **{SEED}** (random.Random, scripts/make_verify.py — rerun it "
        "to reproduce this exact sample).")
    add("")
    add(f"Selection criteria: {CRITERIA}")
    add("")
    add(f"Sample: **{len(sample)} motions across {distinct} documents**, "
        "sorted by document then page. Every field below is parser output; "
        "compare each against the PDF at the fetch URL. Coverage is not "
        "accuracy — this checklist is what separates the two.")
    add("")
    for i, s in enumerate(sample, 1):
        url = (f"https://ivgid.api.civicclerk.com/v1/Meetings/"
               f"GetMeetingFileStream(fileId={s['file_id']},plainText=false)")
        text = s["text"] if len(s["text"]) <= 110 else s["text"][:110] + "..."
        add(f"### {i} of {len(sample)}")
        add(f"Document: {s['event_date']} {s['event_name']} "
            f"(file {s['file_id']}, page {s['page']})")
        add(f"Open: {url}")
        add("")
        add("Parser says:")
        add(f"  Motion:    {text}")
        mover = s["mover"] or (
            "— (not recorded in minutes)" if "mover_not_recorded" in s.get("notes", [])
            else "— (NOT FOUND)"
        )
        if s["seconder"]:
            seconder = s["seconder"]
        elif "no_seconder" in s.get("notes", []):
            seconder = "— (no second recorded)"
        elif "mover_not_recorded" in s.get("notes", []):
            seconder = "— (not recorded in minutes)"
        else:
            seconder = "— (NOT FOUND)"
        add(f"  Mover:     {mover}")
        add(f"  Seconder:  {seconder}")
        if s["yeas"] or s["nays"] or "no_recorded_vote" not in s.get("notes", []):
            add(f"  YEAS ({s['tally']['aye']}):  {', '.join(s['yeas']) or '—'}")
            add(f"  NAYS ({s['tally']['nay']}):  {', '.join(s['nays']) or '—'}")
            if s["abstain"]:
                add(f"  ABSTAIN ({s['tally']['abstain']}): {', '.join(s['abstain'])}")
            if s["absent"]:
                add(f"  ABSENT ({s['tally']['absent']}): {', '.join(s['absent'])}")
        else:
            add("  Vote:      — (no roll call recorded — normal per "
                "NRS 241.035(1)(c))")
        if s["outcome"]:
            add(f"  Outcome:   {s['outcome'].upper()}")
        elif "truncated_outcome" in s["flags"]:
            add("  Outcome:   UNKNOWN — bare 'MOTION' terminator, outcome "
                "word missing in minutes (flagged truncated_outcome)")
        else:
            add("  Outcome:   UNKNOWN")
        page_ts = stamps.get((s["file_id"], s["page"]), [])
        add(f"  Timestamp: {'; '.join(page_ts) if page_ts else '— (none on this page)'}")
        if s["kind"] != "motion":
            add(f"  Kind:      {s['kind']}")
        if s["flags"]:
            add(f"  Flags:     {', '.join(s['flags'])}")
        add("")
        add("Correct? [ ] yes  [ ] no — what's wrong: ________________")
        add("")
    return "\n".join(lines)


def main() -> None:
    results = json.loads((BENCH_DIR / "results.json").read_text(encoding="utf-8"))
    sample = pick_sample(results["documents"])
    truncated = sum(1 for s in sample if "truncated_outcome" in s["flags"])
    stamps = page_timestamps(sample)
    out = BENCH_DIR / "VERIFY.md"
    out.write_text(render(sample, stamps), encoding="utf-8")
    print(f"wrote {out}: {len(sample)} motions, "
          f"{len({s['file_id'] for s in sample})} documents, "
          f"{truncated} truncated_outcome cases included")


if __name__ == "__main__":
    main()
