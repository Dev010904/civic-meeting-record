"""Regression protection for the Stage A benchmark.

benchmark/results.json is committed so parser changes can be diffed against
it. These tests pin the coverage achieved on the first full-archive run
(26 July 2026): future changes must not push coverage below that floor.
The number may only move up — Stage B work (step 5) is expected to raise
it, at which point the floor should be raised to match.
"""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RESULTS = REPO_ROOT / "benchmark" / "results.json"

# Achieved on the full 153-document IVGID corpus after the hand-verification
# round's recall fixes, 26 July 2026. These floors are LOWER than step 5's
# (95.9 / 98.4) because the denominators grew: the recall fixes surfaced 5
# previously invisible decision blocks (QUESTION:-labelled, chair-called and
# narrative votes), of which one carries an honest missing_outcome flag.
# 193 clean motions vs step 5's 189 — strictly more correct records; the
# percentages are rates over different populations and not comparable.
COVERAGE_FLOOR_PCT = 95.5
MOTIONS_FLOOR = 202  # recall floor: the denominator itself must not shrink
# Live-format subset (docs >= 2025-01-01 plus all Audit Committee docs) —
# the published /accuracy number.
LIVE_COVERAGE_FLOOR_PCT = 98.0
CORPUS_FLOOR_DOCS = 153
PARSER_CRASH_CEILING = 0


def test_results_json_exists_and_is_committed_shape():
    results = json.loads(RESULTS.read_text(encoding="utf-8"))
    assert results["corpus"]["minutes_files"] >= CORPUS_FLOOR_DOCS
    # Recall floor: coverage percentages can hide recall loss, so the motion
    # count itself is pinned — a change that makes motions invisible again
    # must fail even if the survivors all parse clean.
    assert results["totals"]["motions"] >= MOTIONS_FLOOR


def test_coverage_does_not_regress():
    results = json.loads(RESULTS.read_text(encoding="utf-8"))
    coverage = results["totals"]["coverage_pct"]
    assert coverage >= COVERAGE_FLOOR_PCT, (
        f"Stage A coverage regressed: {coverage}% < {COVERAGE_FLOOR_PCT}% floor. "
        "If a parser change legitimately reclassifies motions, re-run "
        "scripts/run_benchmark.py, inspect the diff of benchmark/results.json, "
        "and only then adjust the floor."
    )


def test_live_format_coverage_does_not_regress():
    results = json.loads(RESULTS.read_text(encoding="utf-8"))
    live = results["live"]
    assert live["coverage_pct"] >= LIVE_COVERAGE_FLOOR_PCT, (
        f"live-format coverage regressed: {live['coverage_pct']}% < "
        f"{LIVE_COVERAGE_FLOOR_PCT}% floor — this is the published number."
    )


def test_no_parser_crashes():
    """Fetch failures are network noise; parser exceptions are defects.
    The committed results must contain zero documents whose error is a
    parse-time exception (errors, if any, must be fetch failures)."""
    results = json.loads(RESULTS.read_text(encoding="utf-8"))
    parse_crashes = [
        d for d in results["documents"]
        if d["error"] and not d["error"].startswith("FETCH FAILED")
    ]
    assert len(parse_crashes) <= PARSER_CRASH_CEILING, parse_crashes
