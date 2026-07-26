"""Stage A coverage report over the real minutes fixtures.

Prints, per fixture and in total: how many motions parsed cleanly, every
flag raised, unparseable pages, and — most importantly — candidate decision
lines that Stage A did NOT capture as motions. Those misses define what
Stage B (the LLM fallback, step 5) must handle.

Usage: python scripts/report_coverage.py
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

import parse_minutes as pm  # noqa: E402
import pdftext  # noqa: E402

FIXTURES = REPO_ROOT / "tests" / "fixtures"

# Lines that look like decisions but are not MOTION blocks.
_DECISION_HINT = re.compile(
    r"\b(was approved|was adopted|was closed|was tabled|was continued|"
    r"no objections|by consensus|moved to a future meeting|"
    r"will return at a later date)\b",
    re.IGNORECASE,
)


def report(name: str, file_id: int) -> tuple[int, int, Counter]:
    data = (FIXTURES / name).read_bytes()
    parsed = pm.parse_minutes(data, file_id=file_id)

    clean = [m for m in parsed.motions if not m.flags]
    flag_counts: Counter = Counter(f for m in parsed.motions for f in m.flags)

    print(f"=== {name} (file_id={file_id}) ===")
    print(f"motions found:        {len(parsed.motions)}")
    print(f"motions clean:        {len(clean)}"
          f"  ({100 * len(clean) / len(parsed.motions):.0f}%)" if parsed.motions
          else "motions clean:        0")
    for flag, count in sorted(flag_counts.items()):
        print(f"  flagged {flag}: {count}")
    print(f"media timestamps:     {len(parsed.media_timestamps)}"
          f" ({sum(1 for m in parsed.media_timestamps if m.end is None)}"
          f" without end time)")
    print(f"public comments:      {len(parsed.public_comments)} (metadata only)")
    print(f"unparseable pages:    {parsed.unparseable_pages or 'none'}")
    print(f"document flags:       {parsed.flags or 'none'}")

    # Candidate misses: decision-like lines outside motion blocks and
    # outside public-comment regions.
    lines = pdftext.extract_lines(data)
    in_motion_pages: set[tuple[int, str]] = set()
    for motion in parsed.motions:
        for raw_line in motion.raw.split("\n"):
            in_motion_pages.add(raw_line.strip())
    print("candidate decisions NOT captured as motions (Stage B input):")
    misses = 0
    comment_pages = {c.provenance.page for c in parsed.public_comments}
    for line in lines:
        if not _DECISION_HINT.search(line.text):
            continue
        if line.text.strip() in in_motion_pages:
            continue
        if line.page_number in comment_pages and "MOTION" not in line.text:
            # Could still be comment prose; report but mark it.
            pass
        misses += 1
        print(f"  p{line.page_number:>2}:{line.line_number:>3}  {line.text}")
    if not misses:
        print("  (none)")
    print()
    return len(parsed.motions), len(clean), flag_counts


def main() -> None:
    totals = [0, 0]
    all_flags: Counter = Counter()
    for name, file_id in (
        ("ivgid_minutes_2778.pdf", 2778),
        ("ivgid_minutes_draft_2783.pdf", 2783),
    ):
        found, clean, flags = report(name, file_id)
        totals[0] += found
        totals[1] += clean
        all_flags.update(flags)
    print("=== Stage A totals ===")
    print(f"motions: {totals[1]}/{totals[0]} clean "
          f"({100 * totals[1] / totals[0]:.0f}%)")
    print(f"flags:   {dict(all_flags) or 'none'}")


if __name__ == "__main__":
    main()
