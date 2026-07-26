"""Print the first N lines of an IVGID minutes PDF with page:line numbers.

Ground-truth viewer for designing the step-3 parser: shows the actual
structure of motions, vote blocks and Media Timestamp lines as extracted,
with the same page/line coordinates the parser will see.

Usage:
    python scripts/inspect_minutes.py [pdf_path] [num_lines]

Defaults: tests/fixtures/ivgid_minutes_2778.pdf, 200 lines.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

import pdftext  # noqa: E402

DEFAULT_PDF = REPO_ROOT / "tests" / "fixtures" / "ivgid_minutes_2778.pdf"


def main() -> None:
    pdf_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PDF
    num_lines = int(sys.argv[2]) if len(sys.argv) > 2 else 200

    lines = pdftext.extract_lines(pdf_path.read_bytes())
    print(f"# {pdf_path.name} — first {num_lines} of {len(lines)} lines (page:line)")
    for line in lines[:num_lines]:
        print(f"p{line.page_number:>2}:{line.line_number:>3}  {line.text}")


if __name__ == "__main__":
    main()
