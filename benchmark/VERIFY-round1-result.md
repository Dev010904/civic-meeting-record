# VERIFICATION RESULT — round 1 (archived)

This is the human verification of the round-1 checklist (25 motions, seed
20260726), preserved verbatim after the checklist file was regenerated.
The defects listed here drove the step-6 fixes; see benchmark/REPORT.md.

**Verified:** 26 July 2026, by reading each cited page of the source PDF and comparing every field.

## Headline

**Vote records: 25 of 25 correct.** Every mover, seconder, YEAS name, NAYS name, count and
outcome matched the source exactly — including wrapped name lists, Audit Committee
title-heavy names, legitimate no-seconder cases, and both `truncated_outcome` calls
(confirmed on the page: the clerk genuinely omitted the outcome word).

**No false vote was published in the sample.**

## Fully correct entries: 14 of 25
1, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 23, 24, 25

## Entries with defects: 11 of 25
- **9 entries (2-10)** — media timestamp missed (parser knew only the parenthesised
  form; all failures dated February-May 2025)
- **2 entries (20, 22)** — trivial motion-text / name artifacts

## MAJOR FINDING — recall failure (file 1428, page 8)
A complete roll-call vote labelled `QUESTION:` instead of `MOTION:` was invisible
to the parser: a 1-4 FAILED vote to strip Item H.1. from the agenda.

## SUSPECTED recall gap (file 1229, page 2)
Narrative form "Trustee Noble made a Motion to approve ..." — confirmed invisible.

## OPEN QUESTION — draft minutes labelling
Files 1342 and 1433 watermarked DRAFT; parser did not record minutes status.

## Accuracy figures from this round
- Vote accuracy (movers, seconders, names, counts, outcomes): 25/25 = 100%.
- Full-field accuracy including media timestamps: 14/25 = 56%, concentrated
  entirely in the February-May 2025 window.
- Full-field accuracy for June 2025 onward: 14/16 (both exceptions trivial
  text artifacts).
