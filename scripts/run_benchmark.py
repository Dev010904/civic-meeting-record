"""Run the Stage A benchmark over the full IVGID minutes archive.

Produces benchmark/results.json (machine-readable, committed for regression
diffing) and benchmark/REPORT.md (human-readable, with the hand-verification
checklist). Usage: python scripts/run_benchmark.py
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

import benchmark  # noqa: E402

BENCH_DIR = REPO_ROOT / "benchmark"
CACHE_DIR = REPO_ROOT / "cache"

# Previous milestone, kept for the before/after comparison in the report.
# (Step 4 pre-hardening was 149/183 = 81.4%; step 5 hardening reached the
# numbers below; the current run adds the hand-verification round's recall
# fixes — QUESTION:-labelled and narrative vote blocks — so the motion
# count rises and percentages are NOT comparable across denominators.)
BASELINE = {
    "date": "2026-07-26 (step 5, pre-verification-round)",
    "motions": 197,
    "motions_clean": 189,
    "coverage_pct": 95.9,
    "flags": {"missing_outcome": 5, "missing_mover": 5,
              "missing_vote_sections": 5, "truncated_outcome": 3},
}


def write_report(results: dict, sample: list[dict]) -> str:
    t = results["totals"]
    c = results["corpus"]
    lines: list[str] = []
    add = lines.append
    add("# Stage A benchmark report — IVGID minutes archive")
    add("")
    add(f"Generated {date.today().isoformat()} by scripts/run_benchmark.py.")
    add("")
    add("## Spec correction")
    add("")
    add(results["spec_correction"])
    add("")
    add("## Corpus")
    add("")
    add(f"- Minutes PDFs: **{c['minutes_files']}**")
    add(f"- Date range: **{c['date_range'][0]} to {c['date_range'][1]}**")
    add(f"- Slug: `{c['slug']}`, events before {c['before_date']}")
    add("")
    add("## Automated metrics (not accuracy)")
    add("")
    add(f"- Motions found: **{t['motions']}**")
    add(f"- Motions parsed clean (coverage): **{t['motions_clean']} "
        f"({t['coverage_pct']}%)**")
    add(f"- Documents crashed: **{t['crashes']}**")
    add("")
    add(f"### Before/after (baseline: {BASELINE['date']})")
    add("")
    add("Recall fixes change the denominator — the motion counts differ, so "
        "the two coverage percentages are rates over different populations "
        "and must not be read as a like-for-like delta.")
    add("")
    add("| | baseline | current |")
    add("|---|---|---|")
    add(f"| motions found | {BASELINE['motions']} | {t['motions']} |")
    add(f"| motions clean | {BASELINE['motions_clean']} | {t['motions_clean']} |")
    add(f"| coverage | {BASELINE['coverage_pct']}% | {t['coverage_pct']}% |")
    add(f"| flags | {BASELINE['flags']} | {t['flags']} |")
    add("")
    live = results.get("live")
    if live:
        add("## Live-format subset (docs ≥ 2025-01-01 + all Audit Committee)")
        add("")
        add("This is the subset the live pipeline will meet, and the number "
            "for the published /accuracy page. Reported separately from the "
            "full archive; the archive includes deferred format eras.")
        add("")
        add(f"- Documents: **{live['documents']}**")
        add(f"- Motions: **{live['motions']}**, clean **{live['motions_clean']}"
            f"** (**{live['coverage_pct']}%**)")
        add(f"- Flags: {live['flags'] or 'none'}")
        add(f"- Zero-motion documents (recall): **{len(live['zero_motion_documents'])}**")
        investigations = {}
        inv_path = BENCH_DIR / "investigations.json"
        if inv_path.exists():
            investigations = {
                int(k): v
                for k, v in json.loads(inv_path.read_text(encoding="utf-8")).items()
            }
        for z in live["zero_motion_documents"]:
            note = investigations.get(
                z["file_id"], "NOT YET INVESTIGATED — do not publish until it is"
            )
            add(f"  - file {z['file_id']} ({z['event_date']} {z['event_name']}): {note}")
        add("")
    add("### Flag breakdown")
    add("")
    if t["flags"]:
        for flag, count in sorted(t["flags"].items(), key=lambda kv: -kv[1]):
            locs = [
                f"file {d['file_id']} p{f['page']}"
                for d in results["documents"]
                for f in d["failures"]
                if flag in f["flags"]
            ][:5]
            add(f"- `{flag}`: {count} — e.g. {', '.join(locs)}")
    else:
        add("- none")
    add("")
    add("### Per-document anomalies")
    add("")
    for d in results["documents"]:
        notes = []
        if d["error"]:
            notes.append("CRASHED")
        if d["unparseable_pages"]:
            notes.append(f"unparseable pages {d['unparseable_pages']}")
        if d.get("doc_flags"):
            notes.append(f"doc flags {d['doc_flags']}")
        if not d["motions"] and not d["error"]:
            notes.append("zero motions found")
        if notes:
            add(f"- file {d['file_id']} ({d['event_date'][:10]} "
                f"{d['event_name']}): {'; '.join(notes)}")
    add("")
    add("## Hand-verified accuracy — **PENDING HUMAN VERIFICATION**")
    add("")
    add("Coverage is not accuracy. The following seeded random sample of "
        f"{len(sample)} motions across "
        f"{len({s['file_id'] for s in sample})} documents must be checked "
        "by eye against the PDFs (cache/<file_id>.pdf, page as listed). "
        "Tick each box only after comparing every field.")
    add("")
    for i, s in enumerate(sample, 1):
        add(f"### [ ] {i}. file {s['file_id']}, page {s['page']} "
            f"({s['event_date']} {s['event_name']})")
        add("")
        add(f"- text: {s['text']}")
        add(f"- mover: {s['mover']} | seconder: {s['seconder']}")
        add(f"- yeas ({s['tally']['aye']}): {', '.join(s['yeas']) or '—'}")
        add(f"- nays ({s['tally']['nay']}): {', '.join(s['nays']) or '—'}")
        if s["abstain"] or s["absent"]:
            add(f"- abstain: {s['abstain']} | absent: {s['absent']}")
        add(f"- outcome: {s['outcome']} | flags: {s['flags'] or 'none'}")
        add("")
    add("## Failure catalogue (specification for Stage B)")
    add("")
    grouped: dict[str, list[dict]] = defaultdict(list)
    for d in results["documents"]:
        for f in d["failures"]:
            grouped[",".join(f["flags"])].append(f)
    if not grouped:
        add("No flagged motions in the corpus.")
    for cause, failures in sorted(grouped.items(), key=lambda kv: -len(kv[1])):
        add(f"### `{cause}` — {len(failures)} occurrence(s)")
        add("")
        for f in failures:
            add(f"**file {f['file_id']}, page {f['page']} ({f['event_date'][:10]})**")
            add("")
            add("```")
            add(f["raw"])
            add("```")
            add("")
    return "\n".join(lines)


def main() -> None:
    if "--render-only" in sys.argv:
        # Re-render REPORT.md from the existing results.json (e.g. after
        # curating benchmark/investigations.json) without re-parsing.
        results = json.loads(
            (BENCH_DIR / "results.json").read_text(encoding="utf-8")
        )
        sample = benchmark.sample_for_verification(results)
        (BENCH_DIR / "REPORT.md").write_text(
            write_report(results, sample), encoding="utf-8"
        )
        print(f"re-rendered {BENCH_DIR / 'REPORT.md'}")
        return
    results = benchmark.run_benchmark(cache_dir=CACHE_DIR)
    sample = benchmark.sample_for_verification(results)

    BENCH_DIR.mkdir(exist_ok=True)
    (BENCH_DIR / "results.json").write_text(
        json.dumps(results, indent=2), encoding="utf-8"
    )
    (BENCH_DIR / "REPORT.md").write_text(write_report(results, sample), encoding="utf-8")

    t = results["totals"]
    print()
    print(f"corpus: {results['corpus']['minutes_files']} minutes PDFs, "
          f"{results['corpus']['date_range']}")
    print(f"motions: {t['motions']}  clean: {t['motions_clean']} "
          f"({t['coverage_pct']}%)  crashes: {t['crashes']}")
    print(f"flags: {t['flags']}")
    print(f"wrote {BENCH_DIR / 'results.json'} and {BENCH_DIR / 'REPORT.md'}")


if __name__ == "__main__":
    main()
