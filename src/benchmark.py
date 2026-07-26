"""Benchmark harness: Stage A accuracy over the full IVGID minutes archive.

Spec correction (applied here, noted in the report): spec §2.6 names Augusta
Charter Township's 146 minutes PDFs as the benchmark corpus. That predates
the switch to IVGID — Augusta is a different jurisdiction and format, so
testing an IVGID parser against it measures nothing. The benchmark corpus
is the full IVGID minutes archive; Augusta is deferred to phase two as a
generalisation test.

What this measures, kept separate and never blended:
- Coverage: motions parsed without flags, as a percentage. Automated.
- Flag breakdown: every flag type with counts and locations.
- Crash rate: documents that raised an exception.
- Hand-verified accuracy: a seeded random sample of motions rendered as a
  checklist for human verification against the PDFs. Coverage is not
  accuracy — only human checking separates them — so that section stays
  "pending" until a person has ticked it.

PDFs are cached in cache/ by file_id (gitignored, never committed); the
1 req/s courtesy throttle in src/civicclerk.py applies to every fetch.
"""

from __future__ import annotations

import random
import traceback
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Optional

import civicclerk
import parse_minutes

VERIFICATION_SAMPLE_SIZE = 25
VERIFICATION_MIN_DOCUMENTS = 8
VERIFICATION_SEED = 20260726  # fixed so the sample is reproducible


@dataclass(frozen=True)
class CorpusDoc:
    """One Minutes PDF in the benchmark corpus."""

    file_id: int
    event_id: int
    event_name: str
    event_date: str
    minutes_name: str


def assemble_corpus(
    slug: str = "ivgid", before_date: str = "2026-07-26"
) -> list[CorpusDoc]:
    """Paginate the full event archive and collect every Minutes file.

    Events can in principle carry more than one Minutes entry in
    publishedFiles[]; every one becomes a corpus document.
    """
    events = civicclerk.list_events(slug, before_date)
    docs: list[CorpusDoc] = []
    for event in events:
        for entry in civicclerk.published_files(event, "Minutes"):
            docs.append(
                CorpusDoc(
                    file_id=entry["fileId"],
                    event_id=event["id"],
                    event_name=event.get("eventName", ""),
                    event_date=event.get("startDateTime", ""),
                    minutes_name=entry.get("name", ""),
                )
            )
    return docs


def fetch_cached(slug: str, file_id: int, cache_dir: Path) -> bytes:
    """Fetch a PDF by file_id, caching on disk so reruns don't refetch."""
    path = cache_dir / f"{file_id}.pdf"
    if path.exists():
        return path.read_bytes()
    data = civicclerk.fetch_file(slug, file_id)
    cache_dir.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return data


def _motion_summary(motion: parse_minutes.Motion) -> dict[str, Any]:
    return {
        "page": motion.provenance.page,
        "text": motion.text[:300],
        "mover": motion.mover,
        "seconder": motion.seconder,
        "yeas": motion.yeas,
        "nays": motion.nays,
        "abstain": motion.abstain,
        "absent": motion.absent,
        "tally": motion.tally,
        "outcome": motion.outcome,
        "flags": motion.flags,
        "kind": motion.kind,
        "notes": motion.notes,
    }


def run_document(doc: CorpusDoc, pdf_bytes: bytes) -> dict[str, Any]:
    """Run Stage A over one document; capture rather than raise exceptions."""
    result: dict[str, Any] = {**asdict(doc), "error": None}
    try:
        parsed = parse_minutes.parse_minutes(pdf_bytes, file_id=doc.file_id)
    except Exception:
        result["error"] = traceback.format_exc(limit=3)
        result.update(
            motions=[], flag_counts={}, unparseable_pages=[],
            public_comments=0, media_timestamps=0, failures=[],
        )
        return result

    flag_counts: dict[str, int] = {}
    failures: list[dict[str, Any]] = []
    for motion in parsed.motions:
        for flag in motion.flags:
            flag_counts[flag] = flag_counts.get(flag, 0) + 1
        if motion.flags:
            failures.append(
                {
                    "file_id": doc.file_id,
                    "event_date": doc.event_date,
                    "page": motion.provenance.page,
                    "flags": motion.flags,
                    "raw": motion.raw,
                }
            )
    result.update(
        motions=[_motion_summary(m) for m in parsed.motions],
        flag_counts=flag_counts,
        unparseable_pages=parsed.unparseable_pages,
        public_comments=len(parsed.public_comments),
        media_timestamps=len(parsed.media_timestamps),
        doc_flags=parsed.flags,
        failures=failures,
    )
    return result


def run_benchmark(
    slug: str = "ivgid",
    cache_dir: Path = Path("cache"),
    before_date: str = "2026-07-26",
    progress: bool = True,
) -> dict[str, Any]:
    """Assemble the corpus, run Stage A everywhere, aggregate the metrics."""
    corpus = assemble_corpus(slug, before_date)
    dates = sorted(d.event_date for d in corpus if d.event_date)

    documents: list[dict[str, Any]] = []
    for i, doc in enumerate(corpus, 1):
        if progress:
            print(f"[{i}/{len(corpus)}] file {doc.file_id} — "
                  f"{doc.event_date[:10]} {doc.event_name[:50]}")
        try:
            pdf_bytes = fetch_cached(slug, doc.file_id, cache_dir)
        except Exception:
            documents.append(
                {**asdict(doc), "error": "FETCH FAILED:\n" + traceback.format_exc(limit=2),
                 "motions": [], "flag_counts": {}, "unparseable_pages": [],
                 "public_comments": 0, "media_timestamps": 0, "failures": []}
            )
            continue
        documents.append(run_document(doc, pdf_bytes))

    total_motions = sum(len(d["motions"]) for d in documents)
    clean = sum(
        1 for d in documents for m in d["motions"] if not m["flags"]
    )
    flags: dict[str, int] = {}
    for d in documents:
        for flag, count in d["flag_counts"].items():
            flags[flag] = flags.get(flag, 0) + count
    crashes = [d for d in documents if d["error"]]
    live = live_metrics(documents)

    return {
        "spec_correction": (
            "Spec §2.6 names Augusta Charter Township (146 PDFs) as the "
            "benchmark corpus; that is stale — it predates the switch to "
            "IVGID. The benchmark is the full IVGID minutes archive. "
            "Augusta is deferred to phase two as a generalisation test."
        ),
        "corpus": {
            "slug": slug,
            "before_date": before_date,
            "minutes_files": len(corpus),
            "date_range": [dates[0][:10], dates[-1][:10]] if dates else None,
        },
        "totals": {
            "documents": len(documents),
            "motions": total_motions,
            "motions_clean": clean,
            "coverage_pct": round(100 * clean / total_motions, 1)
            if total_motions
            else None,
            "crashes": len(crashes),
            "flags": flags,
        },
        "live": live,
        "documents": documents,
    }


def is_live_format(doc: dict[str, Any]) -> bool:
    """The subset the live pipeline will actually meet: documents dated
    2025-01-01 or later, plus all Audit Committee documents (that committee
    still meets and has used its own format for years)."""
    return doc["event_date"] >= "2025-01-01" or "audit" in doc["event_name"].lower()


def live_metrics(documents: list[dict[str, Any]]) -> dict[str, Any]:
    """Coverage and recall over the live-format subset — the numbers for the
    published /accuracy page. Recall is reported as the list of subset
    documents that yielded zero motions; each needs individual
    investigation, because a genuinely motion-free meeting is a different
    thing from a document the parser cannot see."""
    subset = [d for d in documents if is_live_format(d)]
    motions = sum(len(d["motions"]) for d in subset)
    clean = sum(1 for d in subset for m in d["motions"] if not m["flags"])
    zero = [
        {"file_id": d["file_id"], "event_date": d["event_date"][:10],
         "event_name": d["event_name"]}
        for d in subset
        if not d["motions"] and not d["error"]
    ]
    flags: dict[str, int] = {}
    for d in subset:
        for flag, count in d["flag_counts"].items():
            flags[flag] = flags.get(flag, 0) + count
    return {
        "documents": len(subset),
        "motions": motions,
        "motions_clean": clean,
        "coverage_pct": round(100 * clean / motions, 1) if motions else None,
        "flags": flags,
        "zero_motion_documents": zero,
    }


def sample_for_verification(
    results: dict[str, Any],
    sample_size: int = VERIFICATION_SAMPLE_SIZE,
    min_documents: int = VERIFICATION_MIN_DOCUMENTS,
    seed: int = VERIFICATION_SEED,
) -> list[dict[str, Any]]:
    """Seeded random sample of motions, spread across documents.

    Documents are shuffled and motions taken round-robin so the sample
    spans at least ``min_documents`` distinct PDFs (or every document with
    motions, if fewer exist).
    """
    rng = random.Random(seed)
    docs = [d for d in results["documents"] if d["motions"]]
    rng.shuffle(docs)
    queues = [
        (d, rng.sample(range(len(d["motions"])), len(d["motions"]))) for d in docs
    ]
    sample: list[dict[str, Any]] = []
    round_index = 0
    while len(sample) < sample_size and any(q for _, q in queues):
        for doc, queue in queues:
            if len(sample) >= sample_size:
                break
            if round_index < len(queue):
                motion = doc["motions"][queue[round_index]]
                sample.append(
                    {"file_id": doc["file_id"], "event_date": doc["event_date"][:10],
                     "event_name": doc["event_name"], **motion}
                )
        round_index += 1
    distinct = len({s["file_id"] for s in sample})
    if distinct < min(min_documents, len(docs)):
        raise AssertionError(
            f"sample spans only {distinct} documents; wanted {min_documents}"
        )
    return sample
