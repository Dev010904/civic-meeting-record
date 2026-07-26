# Stage A benchmark report — IVGID minutes archive

Generated 2026-07-26 by scripts/run_benchmark.py.

## Spec correction

Spec §2.6 names Augusta Charter Township (146 PDFs) as the benchmark corpus; that is stale — it predates the switch to IVGID. The benchmark is the full IVGID minutes archive. Augusta is deferred to phase two as a generalisation test.

## Corpus

- Minutes PDFs: **153**
- Date range: **2021-05-12 to 2026-05-20**
- Slug: `ivgid`, events before 2026-07-26

## Automated metrics (not accuracy)

- Motions found: **202**
- Motions parsed clean (coverage): **193 (95.5%)**
- Documents crashed: **0**

### Before/after (baseline: 2026-07-26 (step 5, pre-verification-round))

Recall fixes change the denominator — the motion counts differ, so the two coverage percentages are rates over different populations and must not be read as a like-for-like delta.

| | baseline | current |
|---|---|---|
| motions found | 197 | 202 |
| motions clean | 189 | 193 |
| coverage | 95.9% | 95.5% |
| flags | {'missing_outcome': 5, 'missing_mover': 5, 'missing_vote_sections': 5, 'truncated_outcome': 3} | {'truncated_outcome': 3, 'missing_outcome': 6, 'missing_mover': 5, 'missing_vote_sections': 5} |

## Live-format subset (docs ≥ 2025-01-01 + all Audit Committee)

This is the subset the live pipeline will meet, and the number for the published /accuracy page. Reported separately from the full archive; the archive includes deferred format eras.

- Documents: **57**
- Motions: **197**, clean **193** (**98.0%**)
- Flags: {'truncated_outcome': 3, 'missing_outcome': 1}
- Zero-motion documents (recall): **19**
  - file 1427 (2025-05-21 Special Meeting of the IVGID Board of Trustees): Genuinely motion-free: presentation-only special meeting; no motion language anywhere in its 55 pages. Legitimate zero — not a parser gap.
  - file 1096 (2025-01-16 Special Meeting of the IVGID  Board of Trustees): Stenographic transcript format (interleaved two-column court-reporter lines) — the transcript era extends through January 2025. Deferred to the archive phase; not a live-format gap.
  - file 1103 (2025-01-08 Regular Meeting of the Board of Trustees): Stenographic transcript format, as file 1096. The structured era begins February 2025 (file 1171 parses cleanly). Deferred to the archive phase.
  - file 1041 (2024-11-18 Regular Meeting of the Audit Committee): Narrative-prose minutes ('X made a motion… Y seconded the motion… the motion carried') — the deferred narrative era. The structured Audit Committee format (MOTION WAS MADE) begins December 2024 (file 1051). In the live subset only because the subset includes all Audit docs.
  - file 1048 (2024-10-15 Regular Meeting of the Audit Committee): Narrative-prose minutes ('X made a motion… Y seconded the motion… the motion carried') — the deferred narrative era. The structured Audit Committee format (MOTION WAS MADE) begins December 2024 (file 1051). In the live subset only because the subset includes all Audit docs.
  - file 977 (2024-08-20 Regular Meeting of Audit Committee): Narrative-prose minutes ('X made a motion… Y seconded the motion… the motion carried') — the deferred narrative era. The structured Audit Committee format (MOTION WAS MADE) begins December 2024 (file 1051). In the live subset only because the subset includes all Audit docs.
  - file 975 (2024-06-17 Regular Meeting of the Audit Committee): Narrative-prose minutes ('X made a motion… Y seconded the motion… the motion carried') — the deferred narrative era. The structured Audit Committee format (MOTION WAS MADE) begins December 2024 (file 1051). In the live subset only because the subset includes all Audit docs.
  - file 950 (2024-03-25 Special Meeting of the Audit Committee): Narrative-prose minutes ('X made a motion… Y seconded the motion… the motion carried') — the deferred narrative era. The structured Audit Committee format (MOTION WAS MADE) begins December 2024 (file 1051). In the live subset only because the subset includes all Audit docs.
  - file 931 (2023-03-30 Regular Meeting of the Audit Committee): Narrative-prose minutes ('X made a motion… Y seconded the motion… the motion carried') — the deferred narrative era. The structured Audit Committee format (MOTION WAS MADE) begins December 2024 (file 1051). In the live subset only because the subset includes all Audit docs.
  - file 826 (2022-12-05 Regular Meeting of the IVGID Audit Committee ): Narrative-prose minutes ('X made a motion… Y seconded the motion… the motion carried') — the deferred narrative era. The structured Audit Committee format (MOTION WAS MADE) begins December 2024 (file 1051). In the live subset only because the subset includes all Audit docs.
  - file 810 (2022-09-28 Regular Meeting of the IVGID Audit Committee): Narrative-prose minutes ('X made a motion… Y seconded the motion… the motion carried') — the deferred narrative era. The structured Audit Committee format (MOTION WAS MADE) begins December 2024 (file 1051). In the live subset only because the subset includes all Audit docs.
  - file 794 (2022-06-16 Regular Meeting of the IVGID Audit Committee): Narrative-prose minutes ('X made a motion… Y seconded the motion… the motion carried') — the deferred narrative era. The structured Audit Committee format (MOTION WAS MADE) begins December 2024 (file 1051). In the live subset only because the subset includes all Audit docs.
  - file 788 (2022-06-01 Regular Meeting of the IVGID Audit Committee): Narrative-prose minutes ('X made a motion… Y seconded the motion… the motion carried') — the deferred narrative era. The structured Audit Committee format (MOTION WAS MADE) begins December 2024 (file 1051). In the live subset only because the subset includes all Audit docs.
  - file 777 (2022-05-10 Regular Meeting of the IVGID Audit Committee): Narrative-prose minutes ('X made a motion… Y seconded the motion… the motion carried') — the deferred narrative era. The structured Audit Committee format (MOTION WAS MADE) begins December 2024 (file 1051). In the live subset only because the subset includes all Audit docs.
  - file 771 (2022-04-21 Regular Meeting of the Audit Committee): Narrative-prose minutes ('X made a motion… Y seconded the motion… the motion carried') — the deferred narrative era. The structured Audit Committee format (MOTION WAS MADE) begins December 2024 (file 1051). In the live subset only because the subset includes all Audit docs.
  - file 764 (2022-04-13 Regular Meeting of the IVGID Audit Committee): Narrative-prose minutes ('X made a motion… Y seconded the motion… the motion carried') — the deferred narrative era. The structured Audit Committee format (MOTION WAS MADE) begins December 2024 (file 1051). In the live subset only because the subset includes all Audit docs.
  - file 782 (2022-02-22 Regular Meeting of the IVGID Audit Committee): Narrative-prose minutes ('X made a motion… Y seconded the motion… the motion carried') — the deferred narrative era. The structured Audit Committee format (MOTION WAS MADE) begins December 2024 (file 1051). In the live subset only because the subset includes all Audit docs.
  - file 736 (2021-12-16 Regular Meeting of the IVGID Audit Committee): Narrative-prose minutes ('X made a motion… Y seconded the motion… the motion carried') — the deferred narrative era. The structured Audit Committee format (MOTION WAS MADE) begins December 2024 (file 1051). In the live subset only because the subset includes all Audit docs.
  - file 725 (2021-12-08 Regular Meeting of the IVGID Audit Committee): Narrative-prose minutes ('X made a motion… Y seconded the motion… the motion carried') — the deferred narrative era. The structured Audit Committee format (MOTION WAS MADE) begins December 2024 (file 1051). In the live subset only because the subset includes all Audit docs.

### Flag breakdown

- `missing_outcome`: 6 — e.g. file 1342 p2, file 750 p5, file 750 p12, file 750 p26, file 750 p27
- `missing_mover`: 5 — e.g. file 750 p5, file 750 p12, file 750 p26, file 750 p27, file 747 p7
- `missing_vote_sections`: 5 — e.g. file 750 p5, file 750 p12, file 750 p26, file 750 p27, file 747 p7
- `truncated_outcome`: 3 — e.g. file 2670 p1, file 1540 p16, file 1227 p5

### Per-document anomalies

- file 2779 (2026-05-13 Board of Trustees Meeting): unparseable pages [21, 22, 25]
- file 2778 (2026-04-29 Board of Trustees Meeting): unparseable pages [25, 26, 27, 28, 29]
- file 2720 (2026-04-08 Board of Trustees Meeting): unparseable pages [27, 29, 32, 43, 52, 54]
- file 2718 (2026-03-25 Board of Trustees Meeting): unparseable pages [20, 37, 39]; doc flags ['raw_fallback_page:34']
- file 2665 (2026-03-11 Board of Trustees Meeting): unparseable pages [18, 28, 30, 33, 36, 38, 39, 40, 41, 42, 43]; doc flags ['raw_fallback_page:34']
- file 2649 (2026-02-25 Board of Trustees Meeting): unparseable pages [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106]
- file 2636 (2026-01-28 Board of Trustees Meeting): unparseable pages [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33]
- file 1602 (2026-01-14 Board of Trustees Meeting): unparseable pages [15, 16]
- file 1570 (2025-12-10 Meeting of the IVGID Board of Trustees): unparseable pages [28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58]
- file 1559 (2025-11-12 Meeting of the IVGID Board of Trustees): unparseable pages [32, 33, 34, 35, 36, 37, 38]
- file 1601 (2025-10-28 Meeting of the IVGID Audit Committee): unparseable pages [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
- file 1540 (2025-09-17 Meeting of the IVGID Board of Trustees): unparseable pages [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45]
- file 1511 (2025-08-27 Meeting of the Board of Trustees): unparseable pages [18, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98]
- file 1491 (2025-07-30 Meeting of the Board of Trustees): unparseable pages [15, 16, 17, 21, 25, 26, 27, 28, 29, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65]; doc flags ['raw_fallback_page:18']
- file 1490 (2025-07-22 Meeting of the Board of Trustees): unparseable pages [6, 7, 8, 9, 10, 11, 12, 13, 14]
- file 1489 (2025-06-26 Regular Meeting of the Board of Trustees): unparseable pages [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87]
- file 1528 (2025-06-26 Audit Committee Meeting): unparseable pages [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75]
- file 1465 (2025-06-11 Regular Meeting of the Board of Trustees): unparseable pages [19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57]
- file 1527 (2025-06-09 Regular Meeting of the IVGID Audit Committee): unparseable pages [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60]
- file 2748 (2025-06-06 Special Meeting of the  Board of Trustees): unparseable pages [5, 6, 7, 8, 9, 10]
- file 1433 (2025-05-30 Special Meeting of the IVGID Board of Trustees): unparseable pages [23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95]
- file 1427 (2025-05-21 Special Meeting of the IVGID Board of Trustees): unparseable pages [14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]; zero motions found
- file 1428 (2025-05-14 Regular Meeting of the Board of Trustees): unparseable pages [26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47]
- file 1432 (2025-05-07 Special Meeting of the Board of Trustees): unparseable pages [19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54]
- file 1341 (2025-04-30 Regular Meeting of the Board of Trustees): unparseable pages [14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53]
- file 1342 (2025-04-14 Special Meeting of the IVGID Board of Trustees): unparseable pages [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
- file 1344 (2025-04-09 Regular Meeting of the Board of Trustees): unparseable pages [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36]
- file 1343 (2025-03-26 Regular Meeting of the Board of Trustees): unparseable pages [9, 10, 11, 12, 13, 14]
- file 1261 (2025-03-19 Special Meeting of the Board of Trustees): unparseable pages [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42]
- file 1262 (2025-03-12 Regular Meeting of the Board of Trustees): unparseable pages [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]
- file 1229 (2025-03-05 Special Meeting of the Board of Trustees): unparseable pages [6, 7, 8, 9, 10, 11, 12]
- file 1227 (2025-02-26 Regular Meeting of the Board of Trustees): unparseable pages [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34]
- file 1171 (2025-02-12 Regular Meeting of the Board of Trustees): unparseable pages [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
- file 1096 (2025-01-16 Special Meeting of the IVGID  Board of Trustees): unparseable pages [42, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60]; doc flags ['raw_fallback_page:1', 'raw_fallback_page:26']; zero motions found
- file 1103 (2025-01-08 Regular Meeting of the Board of Trustees): unparseable pages [42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118]; doc flags ['raw_fallback_page:1']; zero motions found
- file 1051 (2024-12-19 Regular Meeting of the Audit Committee): unparseable pages [6, 7, 8]
- file 1064 (2024-12-11 Regular Meeting of the Board of Trustees): unparseable pages [28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58]; doc flags ['raw_fallback_page:1']; zero motions found
- file 1034 (2024-11-27 Special Meeting of the Board of Trustees): unparseable pages [23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48]; doc flags ['raw_fallback_page:1']; zero motions found
- file 1041 (2024-11-18 Regular Meeting of the Audit Committee): zero motions found
- file 1066 (2024-11-13 Regular Meeting of the Board of Trustees): unparseable pages [58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117]; doc flags ['raw_fallback_page:1', 'raw_fallback_page:3']; zero motions found
- file 1065 (2024-10-30 Regular Meeting of the Board of Trustees): unparseable pages [76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111]; doc flags ['raw_fallback_page:1']; zero motions found
- file 1048 (2024-10-15 Regular Meeting of the Audit Committee): zero motions found
- file 1021 (2024-10-09 Regular Meeting of the Board of Trustees): unparseable pages [35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65]; doc flags ['raw_fallback_page:1']; zero motions found
- file 1020 (2024-09-24 Regular Meeting of the Board of Trustees): unparseable pages [32, 33, 34, 35, 36, 37, 38]; doc flags ['raw_fallback_page:1', 'raw_fallback_page:30']; zero motions found
- file 971 (2024-09-11 Regular Meeting of the Board of Trustees): unparseable pages [57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89]; doc flags ['raw_fallback_page:1', 'raw_fallback_page:35', 'raw_fallback_page:44']; zero motions found
- file 972 (2024-08-28 Regular Meeting of the Board of Trustees): unparseable pages [68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]; doc flags ['raw_fallback_page:1', 'raw_fallback_page:8', 'raw_fallback_page:37']; zero motions found
- file 969 (2024-08-20 Special Meeting of the Board of Trustees): unparseable pages [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44]; doc flags ['raw_fallback_page:1', 'raw_fallback_page:19']; zero motions found
- file 1324 (2024-08-20 Capital Investment Committee Meeting): zero motions found
- file 977 (2024-08-20 Regular Meeting of Audit Committee): unparseable pages [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]; zero motions found
- file 970 (2024-08-06 Regular Meeting of the Board of Trustees): unparseable pages [57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 103]; doc flags ['raw_fallback_page:1']; zero motions found
- file 953 (2024-07-31 Regular Meeting of the Board of Trustees): unparseable pages [30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102]; doc flags ['raw_fallback_page:1', 'raw_fallback_page:28']; zero motions found
- file 941 (2024-07-10 Regular Meeting of the Board of Trustees): unparseable pages [43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56]; zero motions found
- file 940 (2024-06-26 Regular Meeting of the Board of Trustees): unparseable pages [48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64]; zero motions found
- file 975 (2024-06-17 Regular Meeting of the Audit Committee): zero motions found
- file 959 (2024-06-12 Regular Meeting of the Board of Trustees): unparseable pages [34, 35, 36, 37, 38, 39, 40, 41, 42, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59]; doc flags ['raw_fallback_page:1']; zero motions found
- file 938 (2024-05-31 Regular Meeting of the Board of Trustees of 05/29/2024 (Public Hearing Continued)): unparseable pages [40, 41, 42, 43, 44, 45]; doc flags ['raw_fallback_page:1']; zero motions found
- file 937 (2024-05-30 Regular Meeting of the Board of Trustees of 05/29/2024 (Public Hearing Continued)): doc flags ['raw_fallback_page:1']; zero motions found
- file 936 (2024-05-29 Regular Meeting of the IVGID Board of Trustees): unparseable pages [28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80]; doc flags ['raw_fallback_page:1']; zero motions found
- file 935 (2024-05-28 Special Meeting of the IVGID Board of Trustees): unparseable pages [47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65]; doc flags ['raw_fallback_page:1', 'raw_fallback_page:45']; zero motions found
- file 934 (2024-05-23 Special Meeting of the IVGID Board of Trustees): unparseable pages [42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52]; doc flags ['raw_fallback_page:1']; zero motions found
- file 613 (2024-05-20 Special Meeting of the Board of Trustees): unparseable pages [24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45]; doc flags ['raw_fallback_page:1']; zero motions found
- file 610 (2024-05-08 Regular Meeting of the Board of Trustees): unparseable pages [61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99]; zero motions found
- file 605 (2024-04-24 Regular Meeting of the Board of Trustees): unparseable pages [50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84]; doc flags ['raw_fallback_page:1', 'raw_fallback_page:49']; zero motions found
- file 595 (2024-04-10 Regular Meeting of the Board of Trustees): unparseable pages [23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34]; doc flags ['raw_fallback_page:1']; zero motions found
- file 645 (2024-04-05 Special Meeting of the Golf Advisory Committee): doc flags ['raw_fallback_page:1']; zero motions found
- file 649 (2024-04-04 Regular Meeting of the Capitol Investment Committee): doc flags ['raw_fallback_page:1']; zero motions found
- file 602 (2024-03-28 Special Meeting of the Board of Trustees): doc flags ['raw_fallback_page:1']; zero motions found
- file 652 (2024-03-28 Regular Meeting of the Golf Advisory Committee): doc flags ['raw_fallback_page:1']; zero motions found
- file 950 (2024-03-25 Special Meeting of the Audit Committee): zero motions found
- file 586 (2024-03-13 Regular Meeting of the Board of Trustees): unparseable pages [21, 22, 23, 24, 25]; doc flags ['raw_fallback_page:1', 'raw_fallback_page:19']; zero motions found
- file 582 (2024-03-06 Special Meeting of the Board of Trustees): unparseable pages [29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52]; doc flags ['raw_fallback_page:1', 'raw_fallback_page:27']; zero motions found
- file 1322 (2024-03-04 Regular Meeting of the Capital Investment Committee): zero motions found
- file 577 (2024-02-28 Regular Meeting of the Board of Trustees): unparseable pages [26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59]; doc flags ['raw_fallback_page:1']; zero motions found
- file 572 (2024-02-14 Regular Meeting of the Board of Trustees): unparseable pages [26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84]; doc flags ['raw_fallback_page:1', 'raw_fallback_page:24']; zero motions found
- file 553 (2024-01-31 Regular Meeting of the Board of Trustees): doc flags ['raw_fallback_page:1']; zero motions found
- file 547 (2024-01-25 Special Meeting of the Board of Trustees): doc flags ['raw_fallback_page:1']; zero motions found
- file 544 (2024-01-10 Regular Meeting of the Board of Trustees): doc flags ['raw_fallback_page:1']; zero motions found
- file 540 (2023-12-13 Regular Meeting of the Board of Trustees): zero motions found
- file 1318 (2023-11-21 Regular Meeting of the Capital Investment Committee): doc flags ['raw_fallback_page:3']; zero motions found
- file 539 (2023-11-08 Regular Meeting of the Board of Trustees): doc flags ['raw_fallback_page:1', 'raw_fallback_page:36']; zero motions found
- file 537 (2023-10-25 Regular Meeting of the Board of Trustees): doc flags ['raw_fallback_page:1']; zero motions found
- file 535 (2023-10-11 Board of Trustees Townhall/ Forum): doc flags ['raw_fallback_page:1', 'raw_fallback_page:30']; zero motions found
- file 523 (2023-09-27 Regular Meeting of the Board of Trustees): unparseable pages [43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67]; doc flags ['raw_fallback_page:1', 'raw_fallback_page:4']; zero motions found
- file 1313 (2023-09-26 Regular Meeting of the Capital Investment Committee): doc flags ['raw_fallback_page:1', 'raw_fallback_page:22']; zero motions found
- file 520 (2023-09-19 Regular Meeting of the Board of Trustees): unparseable pages [29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95]; doc flags ['raw_fallback_page:1', 'raw_fallback_page:22']; zero motions found
- file 517 (2023-08-30 Regular Meeting of the Board of Trustees): unparseable pages [49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162]; doc flags ['raw_fallback_page:1']; zero motions found
- file 509 (2023-08-09 Regular Meeting of the Board of Trustees): unparseable pages [57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111]; doc flags ['raw_fallback_page:1']; zero motions found
- file 513 (2023-07-26 Regular Meeting of the Board of Trustees): unparseable pages [51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 125, 126, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198]; zero motions found
- file 511 (2023-07-12 Regular Meeting of the Board of Trustees): unparseable pages [50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155]; doc flags ['raw_fallback_page:1', 'raw_fallback_page:31', 'raw_fallback_page:32']; zero motions found
- file 503 (2023-07-06 Special Meeting of the Board of Trustees): unparseable pages [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 28, 29, 30, 31]; zero motions found
- file 501 (2023-06-28 Regular Meeting of the Board of Trustees): unparseable pages [40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133]; zero motions found
- file 499 (2023-06-23 Special Meeting of the Board of Trustees): unparseable pages [1, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186]; zero motions found
- file 496 (2023-06-14 Regular Meeting of the Board of Trustees): unparseable pages [1, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423]; zero motions found
- file 495 (2023-05-25 Regular Meeting of the Board of Trustees): unparseable pages [1, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380]; zero motions found
- file 494 (2023-05-10 Regular Meeting of the Board of Trustees): unparseable pages [1, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250]; zero motions found
- file 493 (2023-05-08 Regular Meeting of the Board of Trustees): unparseable pages [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246]; zero motions found
- file 491 (2023-04-12 Regular Meeting of the Board of Trustees): unparseable pages [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88]; zero motions found
- file 490 (2023-04-05 Special Meeting of the Board of Trustees): unparseable pages [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73]; zero motions found
- file 931 (2023-03-30 Regular Meeting of the Audit Committee): zero motions found
- file 488 (2023-03-22 Regular Meeting of the Board of Trustees): unparseable pages [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127]; zero motions found
- file 486 (2023-03-08 Regular Meeting of the Board of Trustees): unparseable pages [34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109]; zero motions found
- file 484 (2023-02-22 Regular Meeting of the Board of Trustees): unparseable pages [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141]; zero motions found
- file 481 (2023-02-08 Regular Meeting of the Board of Trustees): unparseable pages [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85]; zero motions found
- file 505 (2023-01-25 Regular Meeting of the Board of Trustees): unparseable pages [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56]; zero motions found
- file 529 (2023-01-11 Regular Meeting of the Board of Trustees): zero motions found
- file 829 (2022-12-14 Regular Meeting of the Board of Trustees): unparseable pages [33, 39, 49, 54, 61, 63, 66, 82, 85, 89, 94, 98, 102, 107, 116, 119, 121, 123, 126]; doc flags ['raw_fallback_page:104', 'raw_fallback_page:105']; zero motions found
- file 826 (2022-12-05 Regular Meeting of the IVGID Audit Committee ): unparseable pages [19]; zero motions found
- file 823 (2022-11-09 Regular Meeting of the Board of Trustees ): unparseable pages [25, 32, 34, 37, 39, 50, 53, 62]; zero motions found
- file 820 (2022-10-24 Special Meeting of the Board of Trustees): unparseable pages [37, 43, 45, 47, 49, 51, 53, 56, 59, 62, 65, 67, 70]; zero motions found
- file 816 (2022-10-12 Regular Meeting of the Board of Trustees ): unparseable pages [34, 40, 43, 46, 48, 51, 53, 57, 61, 70, 73, 76, 81, 85, 88, 92, 97, 104]; zero motions found
- file 813 (2022-09-28 Regular Meeting of the Board of Trustees): unparseable pages [38]; zero motions found
- file 810 (2022-09-28 Regular Meeting of the IVGID Audit Committee): zero motions found
- file 806 (2022-09-14 Regular Meeting of the Board of Trustees): unparseable pages [32]; zero motions found
- file 803 (2022-08-31 Regular Meeting of the Board of Trustees): unparseable pages [19, 22, 26, 31, 39, 44, 54, 58, 74]; zero motions found
- file 800 (2022-07-27 Regular Meeting of the Board of Trustees): unparseable pages [23, 31, 37, 39, 41, 48, 53, 56, 58]; zero motions found
- file 797 (2022-06-29 Regular Meeting of the Board of Trustees): zero motions found
- file 794 (2022-06-16 Regular Meeting of the IVGID Audit Committee): zero motions found
- file 791 (2022-06-08 Regular Meeting of the Board of Trustees): unparseable pages [24, 27, 29, 35, 43, 46, 48]; zero motions found
- file 788 (2022-06-01 Regular Meeting of the IVGID Audit Committee): zero motions found
- file 785 (2022-05-26 Regular Meeting of the Board of Trustees): unparseable pages [51, 56, 62, 64, 68]; zero motions found
- file 781 (2022-05-11 Regular Meeting of the Board of Trustees): zero motions found
- file 777 (2022-05-10 Regular Meeting of the IVGID Audit Committee): zero motions found
- file 774 (2022-04-27 Regular Meeting of the Board of Trustees): zero motions found
- file 771 (2022-04-21 Regular Meeting of the Audit Committee): zero motions found
- file 767 (2022-04-13 Regular Meeting of the Board of Trustees): zero motions found
- file 764 (2022-04-13 Regular Meeting of the IVGID Audit Committee): zero motions found
- file 761 (2022-03-30 Regular Meeting of the Board of Trustees): zero motions found
- file 758 (2022-03-09 Regular Meeting of the Board of Trustees): zero motions found
- file 755 (2022-03-01 Regular Meeting of the Board of Trustees): zero motions found
- file 782 (2022-02-22 Regular Meeting of the IVGID Audit Committee): zero motions found
- file 747 (2022-02-03 Regular Meeting of the Board of Trustees): unparseable pages [31, 34, 40, 43, 46]
- file 742 (2022-01-12 Regular Meeting of the Board of Trustees): unparseable pages [40, 44, 46, 49]; zero motions found
- file 736 (2021-12-16 Regular Meeting of the IVGID Audit Committee): zero motions found
- file 732 (2021-12-14 Special Meeting  of the Board of Trustees (Workshop)): zero motions found
- file 728 (2021-12-08 Regular Meeting of the Board of Trustees): zero motions found
- file 725 (2021-12-08 Regular Meeting of the IVGID Audit Committee): zero motions found
- file 722 (2021-11-22 Special Meeting of the Board of Trustees): unparseable pages [8, 10, 13, 16]; zero motions found
- file 719 (2021-11-10 Regular Meeting of the Board of Trustees): unparseable pages [40, 41]; doc flags ['raw_fallback_page:71']; zero motions found
- file 716 (2021-11-03 Regular Meeting of the Board of Trustees): unparseable pages [32, 34, 39, 54, 57, 69, 73, 79, 85, 89, 92, 94, 106, 115, 117]; doc flags ['raw_fallback_page:40', 'raw_fallback_page:75', 'raw_fallback_page:77', 'raw_fallback_page:78']; zero motions found
- file 713 (2021-10-13 Regular Meeting of the Board of Trustees): unparseable pages [29, 36, 38, 44, 55, 63, 65, 67]; zero motions found
- file 709 (2021-09-30 Regular Meeting of the Board of Trustees): zero motions found
- file 705 (2021-09-02 Regular Meeting of the Board of Trustees): zero motions found
- file 702 (2021-08-10 Regular Meeting of the Board of Trustees): unparseable pages [20, 21, 22, 27, 30, 33, 36, 39, 42, 43]; zero motions found
- file 699 (2021-07-13 Regular Meeting of the Board of Trustees): zero motions found
- file 1277 (2021-06-09 Board of Trustees Meeting): unparseable pages [33, 39, 44, 47, 58, 61, 63, 65, 70, 95, 99, 104, 107, 110, 115, 118, 120, 123, 127, 131]; zero motions found
- file 1289 (2021-05-26 Board of Trustees Meeting): unparseable pages [62, 66, 69, 71, 73, 76, 78, 80, 82, 84, 86]; zero motions found
- file 1293 (2021-05-12 Board of Trustees Meeting): zero motions found

## Hand-verified accuracy — **PENDING HUMAN VERIFICATION**

Coverage is not accuracy. The following seeded random sample of 25 motions across 25 documents must be checked by eye against the PDFs (cache/<file_id>.pdf, page as listed). Tick each box only after comparing every field.

### [ ] 1. file 1432, page 16 (2025-05-07 Special Meeting of the Board of Trustees)

- text: Adopt proposed Changes to Policy 7.1.0 - Budgeting and Fiscal Management, Appropriate Level of Reserves, Effective Fiscal Year Ending June 30, 2022; Policy 18.1.0 - Budgeting and Fiscal Management, Adoption of Central Service Cost Allocation Plan
- mover: Trustee Homan | seconder: Trustee Tonking
- yeas (5): Trustee Noble, Trustee Tulloch, Trustee Homan, Trustee Jezycki, Trustee Tonking
- nays (0): —
- outcome: passed | flags: none

### [ ] 2. file 2649, page 12 (2026-02-25 Board of Trustees Meeting)

- text: In accordance with NRS 241.0395(1), Receive a Report Acknowledging the Attorney General's February 5, 2026, Findings of Fact and Conclusions of Law regarding Open Meeting Law Complaint Filed by Mr. Aaron Katz (OAG File No. 13897-530). Note: Pursuant to NRS 241.0395(2), an acknowledgment of an Attorn
- mover: Trustee Noble | seconder: Trustee Jezycki
- yeas (5): Trustee Chair Tonking, Trustee Jezycki, Trustee Noble, Trustee Homan, Trustee Tulloch
- nays (0): —
- outcome: passed | flags: none

### [ ] 3. file 1559, page 18 (2025-11-12 Meeting of the IVGID Board of Trustees)

- text: to Approve Super Senior Rate(s) at the Recreation Center.
- mover: Trustee Homan | seconder: Trustee Noble
- yeas (5): Trustee Noble, Trustee Tulloch, Trustee Homan, Trustee Vice Chair Jezycki, Trustee Chair Tonking
- nays (0): —
- outcome: passed | flags: none

### [ ] 4. file 1140, page 3 (2025-01-29 Regular Meeting of the IVGID Board of Trustees)

- text: To approve the IVGID Board of Trustees Meeting Minutes for January 8, 2025.
- mover: Trustee Noble | seconder: Trustee Jezycki
- yeas (4): Trustee Noble, Trustee Tulloch, Trustee Jezycki, Trustee Tonking
- nays (0): —
- outcome: passed | flags: none

### [ ] 5. file 1171, page 3 (2025-02-12 Regular Meeting of the Board of Trustees)

- text: Approve the following consent matters, as submitted: Item F.1. Approval of the IVGID Board of Trustees Special Meeting Minutes for January 16, 2025; and Item F.2. Approval of the IVGID Board of Trustees Meeting Minutes for January 29, 2025. Media Timestamp 02:00:34 Action: Approve.
- mover: Trustee Noble | seconder: Trustee Homan
- yeas (5): Trustee Noble, Trustee Tulloch, Trustee Homan, Trustee Jezycki, Trustee Tonking
- nays (0): —
- outcome: passed | flags: none

### [ ] 6. file 2665, page 14 (2026-03-11 Board of Trustees Meeting)

- text: to Approve the proposed increase to Beach Kayak and Paddleboard Storage Rack Rental as presented through December 31, 2026, as provided in the Board packet.
- mover: Trustee Noble | seconder: Trustee Homan
- yeas (4): Trustee Chair Tonking, Trustee Jezycki, Trustee Noble, Trustee Homan
- nays (1): Trustee Tulloch
- outcome: passed | flags: none

### [ ] 7. file 2783, page 2 (2026-05-20 Board of Trustees Meeting)

- text: to Approve and Authorize the Board Chair and Board Secretary to Sign and Execute an Agreement between Incline Village General Improvement District and Olympus & Associates, Inc. for Exterior Re-coating of Water Reservoir R6C-1; FY2025/26 Utilities: Water: CIP #2221WS22601; in the Amount of $199,000.
- mover: Trustee Homan | seconder: Trustee Jezycki
- yeas (4): Trustee Chair Tonking, Trustee Jezycki, Trustee Homan, Trustee Tulloch
- nays (0): —
- outcome: passed | flags: none

### [ ] 8. file 1227, page 6 (2025-02-26 Regular Meeting of the Board of Trustees)

- text: To approve the Budget Schedule with the understanding that if there needs to be some flexibility, the Board of Trustees will be notified, and the meeting schedule will be modified accordingly.
- mover: Trustee Noble | seconder: Trustee Tulloch
- yeas (5): Trustee Noble, Trustee Tulloch, Trustee Homan, Trustee Jezycki, Trustee Tonking
- nays (0): —
- outcome: passed | flags: none

### [ ] 9. file 1433, page 15 (2025-05-30 Special Meeting of the IVGID Board of Trustees)

- text: to Adopt the FY 2025 Fiscal Year 2025/2026 Incline Village General Improvement District Budget Final Form 4f404LGF;
- mover: Trustee Homan | seconder: Trustee Jezycki
- yeas (4): Trustee Noble, Trustee Homan, Trustee Jezycki, Trustee Tonking
- nays (0): —
- outcome: passed | flags: none

### [ ] 10. file 1540, page 15 (2025-09-17 Meeting of the IVGID Board of Trustees)

- text: to reinsert the Fire Pits as one of the alternates in the bid package for the Beach House Project.
- mover: Trustee Homan | seconder: Trustee Noble
- yeas (4): Trustee Noble, Trustee Homan, Trustee Jezycki, Trustee Tonking
- nays (1): Trustee Tulloch
- outcome: passed | flags: none

### [ ] 11. file 2670, page 8 (2026-01-28 Audit Committee Meeting)

- text: to Approve the Audit Committee Meeting Minutes for October 28, 2025.
- mover: Trustee Homan | seconder: Audit Committee Member Kelly
- yeas (4): Audit Committee Chair Brandle, Trustee Homan, At-Large Audit Committee Member Kelly, At-Large Audit Committee Member Lighthart
- nays (0): —
- outcome: passed | flags: none

### [ ] 12. file 1261, page 3 (2025-03-19 Special Meeting of the Board of Trustees)

- text: to Approve the Amended and Restated Cooperative Agreement with North Lake Tahoe Fire Protection District for Fire Reduction (Defensible Space) Services: FY 2025/26 Fund: Community Services; Division: Administration; GL# 30364999-7560 (50% - $100,000): Fund: Utilities; Division; Water; GL#20002299-75
- mover: Trustee Homan | seconder: Trustee Noble
- yeas (3): Trustee Noble, Trustee Homan, Trustee Jezycki
- nays (0): —
- abstain: ['Chair Tonking', 'Trustee Tulloch'] | absent: []
- outcome: passed | flags: none

### [ ] 13. file 1051, page 5 (2024-12-19 Regular Meeting of the Audit Committee)

- text: Approve the Audit Committee Meeting Minutes for November 18, 2024.
- mover: None | seconder: None
- yeas (3): Committee Members Brandle, Schmitz, Tulloch
- nays (0): —
- outcome: passed | flags: none

### [ ] 14. file 1528, page 6 (2025-06-26 Audit Committee Meeting)

- text: That the Audit Committee Provide a Recommendation to the Board of Trustees to Accept a Letter of Engagement from Clifton Larson Allen LLP, and Approve a Contract Agreement with the Auditing Firm for FY 2024/2025.
- mover: Trustee Tonking | seconder: Committee Member Kelly
- yeas (4): Trustee Homan, Trustee Tonking, Committee Member Kelly, Committee Member Lighthart
- nays (0): —
- outcome: passed | flags: none

### [ ] 15. file 2636, page 5 (2026-01-28 Board of Trustees Meeting)

- text: to Approve the Employee Separation Incentive Program; MOTION AMENDED: to Approve the Employee Separation Incentive Program with the approval of any application that the general manager consults with legal and or HR; Amended By Trustee Noble Trustee Homan Accepted the Amendment suggested by Trustee N
- mover: Trustee Homan | seconder: Trustee Noble
- yeas (4): Trustee Chair Tonking, Trustee Jezycki, Trustee Noble, Trustee Homan
- nays (1): Trustee Tulloch
- outcome: passed | flags: none

### [ ] 16. file 750, page 26 (2022-02-09 Regular Meeting of the Board of Trustees)

- text: Trustee Wong moved to add parcel number 130-33-103, address 1709 Lakeshore, to the District Rec Roll. Trustee 381 Minutes Meeting of February 9, 2022 Page 27 Tonking seconded the motion, Board Chairman Callicrate called the question and the motion was passed unanimously. 5. SUBJECT: REVIEW, DISCUSS 
- mover: None | seconder: None
- yeas (None): —
- nays (None): —
- outcome: None | flags: ['missing_outcome', 'missing_mover', 'missing_vote_sections']

### [ ] 17. file 2806, page 7 (2026-04-28 Audit Committee Meeting)

- text: to Approve the Audit Committee Meeting Minutes March 31, 2026.
- mover: Trustee Chair Tonking | seconder: At-Large Audit Committee Member Kelly
- yeas (4): Trustee Chair Tonking, Trustee Homan, At-Large Audit Committee Member Kelly, At-Large Audit Committee Member Lighthart
- nays (0): —
- outcome: passed | flags: none

### [ ] 18. file 747, page 7 (2022-02-03 Regular Meeting of the Board of Trustees)

- text: Trustee Schmitz moved that the Board of Trustees approved policy 15.1.0 with the changes identified here this evening and in addition to make additions and corrections to the memorandum to have the accurate up-to-date information in the memorandum. Trustee Tonking seconded the motion which carried u
- mover: None | seconder: None
- yeas (None): —
- nays (None): —
- outcome: None | flags: ['missing_outcome', 'missing_mover', 'missing_vote_sections']

### [ ] 19. file 1489, page 16 (2025-06-26 Regular Meeting of the Board of Trustees)

- text: to Approve the draft letter with the following revisions: Pages 271 of 295 of the Board packet - Line 5: employee beach access program pending strike “receipt of” and insert “the outcome of this correspondence”; strike “a sufficient number” Line 9: as a property owner would you, strike “like” insert
- mover: Trustee Noble | seconder: None
- yeas (None): —
- nays (None): —
- outcome: None | flags: none

### [ ] 20. file 1465, page 14 (2025-06-11 Regular Meeting of the Board of Trustees)

- text: to Authorize staff to enter into an agreement with the Abbey Agency for the 2025-26 fiscal year, Media Buying Services for Diamond Peak Ski Resort, Championship and Mountain Golf Courses and the Facilities Department for not to exceed a total of $307,9250 cash and $53,000 trade.
- mover: Trustee Homan | seconder: Trustee Noble
- yeas (5): Trustee Noble, Trustee Tulloch, Trustee Homan, Trustee Jezycki, Trustee Tonking
- nays (0): —
- outcome: passed | flags: none

### [ ] 21. file 1428, page 14 (2025-05-14 Regular Meeting of the Board of Trustees)

- text: Approve the following consent matters, Item G.1. and Item G.2. as submitted in the Agenda Packet.
- mover: Trustee Noble | seconder: Trustee Jezycki
- yeas (5): Trustee Noble, Trustee Tulloch, Trustee Homan, Trustee Jezycki, Trustee Tonking
- nays (0): —
- outcome: passed | flags: none

### [ ] 22. file 2721, page 9 (2026-03-31 Audit Committee Meeting)

- text: to Approve and provide a Recommendation to the Board of Trustees to Approve the Draft Financial Statements and Single Audit for June 30, 2025.
- mover: Audit Committee Chair Brandle | seconder: Trustee Homan
- yeas (5): Audit Committee Chair Brandle, Trustee Tonking, Trustee Homan, At-Large Audit Committee Member Kelly, At-Large Audit Committee Member Lighthart
- nays (0): —
- outcome: passed | flags: none

### [ ] 23. file 1342, page 3 (2025-04-14 Special Meeting of the IVGID Board of Trustees)

- text: to Approve Additional Play Pass Options along with season Pass Sales Incentives and Rate Adjustment to the Pricing of the PM Season Pass;
- mover: Trustee Homan | seconder: Trustee Jezycki
- yeas (4): Trustee Noble, Trustee Homan, Trustee Jezycki, Trustee Tonking
- nays (1): Trustee Tulloch
- outcome: passed | flags: none

### [ ] 24. file 1262, page 4 (2025-03-12 Regular Meeting of the Board of Trustees)

- text: Approve the following consent matters: Item F.1. Approve and Authorize the District General Manager to execute a Payment between the Incline General Improvement District and the Nevada Department of Transportation for the Adjustment of Manholes, Valve Covers and Meter Boxes; FY 2024/25 Utilities Fun
- mover: Trustee Homan | seconder: Trustee Noble
- yeas (5): Trustee Noble, Trustee Tulloch, Trustee Homan, Trustee Jezycki, Trustee Tonking
- nays (0): —
- outcome: passed | flags: none

### [ ] 25. file 1344, page 4 (2025-04-09 Regular Meeting of the Board of Trustees)

- text: to approve the Consent Calendar as documented. Item F.1. Meeting Minutes for March 12, 2025; Item F.2. Meeting Minutes for March 19, 2025; Item F.3. Approve an Agreement between Incline Village General Improvement District and Construction Material Engineers, Inc. to provide Professional Services fo
- mover: Trustee Homan | seconder: Trustee Jezycki
- yeas (4): Trustee Tulloch, Trustee Homan, Trustee Jezycki, Trustee Tonking
- nays (0): —
- outcome: passed | flags: none

## Failure catalogue (specification for Stage B)

### `missing_outcome,missing_mover,missing_vote_sections` — 5 occurrence(s)

**file 750, page 5 (2022-02-09)**

```
MOTION: Trustee Schmitz moved to remove General Business Item 1.2. from the
agenda. Trustee Dent seconded the motion. Trustee Tonking asked if we approve
those specific numbers in that agenda item, do they have to be those exact
numbers or can they go lower because I remember there was something with the
rec fee that could be lower, but it couldn't go higher; I'm just curious about how that
works. District General Counsel Nelson said yes, we could go lower than what's
posted on the agenda, and we wouldn't want to go higher. The motion carried 3-2.
Trustees Wong and Tonking opposed. General Business Item 1.2., as well as
Consent Item H.2. receiving the Audit Committee report was removed.
E. DISTRICT GENERAL MANAGER REPORT*
District General Manager Winquest said I have two updates for my report and then
happy answer any questions. First, as everyone knows, we have hired special
counsel to review. I won't go through all these issues on page 6 of the board
packet. I'm working with a couple of members of the Ordinance 7 committee; we
put together draft recommendations that have been given to special counsel. The
special counsel is currently reviewing them. I had another meeting with a member
of the Ordinance 7 committee and special counsel. The special counsel is
comfortable with 90% of what has been given to him. There are a couple of other
issues that we're continuing to work through as we gather more information.
360
Minutes
Meeting of February 9, 2022
Page 6
However, I have enough information now where I am finalizing the draft
recommendations while layering in the survey materials, adding in some historical
information, and painting the picture on all the different recommendations that
we're going to be making. I expect down with that middle of next week. Then, I will
have to call a final meeting with the Ordinance 7 committee to go over the draft
recommendations with the entire committee. If we need to make any final edits,
we will. I'll be emailing the full board about your availability for a special meeting to
deliver these recommendations. A lot of things will have to come together for a
meeting like that. We need all the trustees, special counsel, legal counsel and
hoping to have all members of the Ordinance 7 committee present. We want to
acknowledge them for all their hard work and help make presentations and answer
questions by this board. I know this has taken a lot longer than we all would have
liked, including myself, but these are huge decisions that impact the community
and our parcel owners in the district. We are taking the right path by having special
counsel review this. The special counsel is also reviewing all the other issues that
were included in the scope of work. And so he continues to work through all of that,
ask questions, gather information, and look at relevant case law that may be out
there. We're taking this very seriously because these are very serious decisions
that we will be making. I want to give you an update on that. I've been receiving
correspondence regarding the United States Forest Service special use permit for
a potential dog park. And I finally was able to touch base with the planner we've
been working with. And for those of you who don't know, there's a new US Forest
Service Manager. They needed to get all the information to him so that he can get
familiar with this special use permit to decide whether or not they were going to
continue to push forward and work with us. I've also been it's also been signaled
to me by the United States Forest Service that they're extremely short-staffed. And
they've had some issues. And so for all these reasons, this process is now being
slowed down, unfortunately. As I've stated, I'll be putting together an Advisory
Committee for a dog park over the next couple of weeks. Not just for this particular
location, it could mean identifying other locations that we can continue to pursue
as we try to build a dedicated dog park. Thank you, Trustee Schmitz, for
volunteering to represent the board on that committee. She and I work together on
selecting reasonable and fair folks that we think would be productive on a
committee like that. Unfortunately, I have found out that a few community members
have continued to reach out to the Forest Service in protest of us getting this
parcel. I have two things to say about that one, based on what I've heard, a lot of
the things being said to the Forest Service are false as far as what we're trying to
```

**file 750, page 12 (2022-02-09)**

```
Motion: Trustee Wong moved to approve the consent calendar.
Trustee Tonking seconded the motion. Board Chairman
Callicratec called the question and the motion passed with
Trustee Schmitz voting opposed and added that the suggestion
should have been incorporated.
District General Manager Winquest asked for clarification; are you
suggesting we put the actual GL account where it's being charged to into
the contract? Trustee Schmitz said in the conversation that I had with
Director of Finance Navazio, he indicated that there are additional numeric
codes that would help identify. If you recall, we've had issues with whether
it is expensed or capitalized. So by identifying it here, the decision is being
made, and therefore, there isn't a judgment call when individual invoices
come in, and there's less probability of error so that was the suggestion.
Trustee Wong said what Trustee Schmitz is suggesting is an accounting
matter and doesn't really have any bearing as to whether or not we approve
this contract. If this is something that she wants to work with our finance
team and District General Manager to bring a proposal back offline, I'm
totally fine with that. But that's an accounting matter, not a contract matter.
Trustee Tonking asked if we do that in any of our other contracts? So it
would just be on this one which would be odd. Director of Finance Navazio
said I think that's a correct assumption, we don't. I just might clarify that. I
think we understand Trustee Schmitz's intent in that is that we're all clear
upfront about how we're going to account for it. I think it would be unusual
to put in the contract, or what I would clarify if it's helpful is it when a contract
like this work to is approved, the next thing we do is set up a purchase order.
The purchase order has to tie to a specific account code based on where it's
budgeted and the nature of the expense. So as long as the vendor is
referencing the project, as noted here, and we set up the purchase order
with the proper accounting, that happens automatically. We would be
providing the vendor with the account codes because they don't make that
367
Minutes
Meeting of February 9, 2022
Page 13
determination. Our process already is set up to ensure that the invoices are
paid for the proper account based on the project, the fund, and the nature of
the expenditure.
Board Chairman Callicrate said the motion did pass as it was presented. But
I think that moving forward with what Director of Finance Navazio had just
mentioned, through the purchase order situation, the clarification that
Trustee Schmitz brought up, I think that there is an opportunity, if that would
be the appropriate place. But if that's an opportunity to incorporate the
concerns of Trustee Schmitz, which are valid, to whether it's expensed or
capitalized, if we were able to do that through the PO situation, to give more
clarity, so that there aren't any mistakes or misunderstandings, I think that
would be an appropriate opportunity.
Director of Finance Navazio said there is an opportunity for us to say some
things because there's no guarantee on a particular contract that every dollar
charge in the contract is going to one account code. So in the purchase
order, there are different line items. Still, it's incumbent on the contractors to
accurately report information on the invoice sufficient to allow Staff to be
appropriately allocate by line item. So I don't want to give it the impression
that it's just a one-size-fits-all fix. Trustee Schmitz's comment arises from
past situations where we've had some confusion. We've addressed them as
best we can we're going to continue to work on them. I'm not sure about
putting in the contract the account codes because it'll depend on the nature
of the expenditure.
District General Manager Winquest said I completely understand Trustee
Schmitz's points of concern on this. The best thing to do is to work with
Trustee Schmitz and show her the process we go through. And if she's still
```

**file 750, page 26 (2022-02-09)**

```
MOTION: Trustee Wong moved to add parcel number 130-33-103,
address 1709 Lakeshore, to the District Rec Roll. Trustee
381
Minutes
Meeting of February 9, 2022
Page 27
Tonking seconded the motion, Board Chairman Callicrate called
the question and the motion was passed unanimously.
5. SUBJECT: REVIEW, DISCUSS AND POSSIBLY APPROVE A
MEMORANDUM OF UNDERSTANDING BETWEEN THE INCLINE
VILLAGE GENERAL IMPROVEMENT DISTRICT AND THE CHERYL AND
DAVID DUFFIELD FOUNDATION FOR THE CONCEPTUAL PHASE OF
THE EXPANSION OF THE RECREATION CENTER
District General Manager Win quest introduced the item.
```

**file 750, page 27 (2022-02-09)**

```
MOTION: Trustee Wong moved to approve the memorandum of
understanding between the Incline Village General Improvement
District and the David and Cheryl Duffield Foundation for the
conceptual phase of the expansion of the Recreation Center.
Trustee Tonking seconded the motion.
Trustee Schmitz said I just have a question for the District General Manager -when
it talks about administrative space in Exhibit A, could you just clarify the
administrative space? I'm assuming you're not talking about administrative space,
i.e., the admin staff's movement over to that building? District General Manager
Winquest said that's correct. We envision, upon entry, a small front desk area to
check people in. And then probably a couple of offices administration offices for
Staff, such as an office for Staff and maybe one for the Boys & Girls Club. Trustee
Schmitz said under the project cost estimation, I see that this will be an outsourced
project. But there still will be some element of IVGID staff time; it probably won't
be significant. But when we get the project cost estimation, can we please also
estimate IVGID staff time? District General Manager Winquest said I want to
clarify. I felt it is important. There will be a minimal amount of staff time during the
conceptual phase. I have talked to the Duffield Foundation; they are aware that as
we move into the actual project, internal engineering time and staff time will all be
included in the grant amount we will be getting from the Duffields. So it would
include similar to what you see with our other projects, and estimation of
engineering staff or engineering time as part of the project. Trustee Schmitz
thanked the District General Manager for answering the questions. Trustee Wong
said I just want to make sure we express our gratitude to the Duffields for their
continued support of our community, and I'm very excited to see this project move
forward. The motion carried unanimously. Chair Callicrate thanked Dave & Cheryl
Duffield.
382
Minutes
Meeting of February 9, 2022
Page 28
J. MEETING MINUTES (for possible action)
1. Meeting Minutes of January 12, 2022 - The meeting minutes are
approved pending the necessary changes that the District Clerk had
identified.
K. FINAL PUBLIC COMMENTS*
L. ADJOURNMENT (for possible action)
The meeting was adjourned at 9:31 p.m.
Respectfully submitted,
Misty A. Moga
Acting District Clerk
Attachments*:
*In accordance with NRS 241.035.1 (d), the following attachments are included but
have neither been fact checked or verified by the District and are solely the
thoughts, opinions, statements, etc. of the author as identified below.
Submitted by Cliff Dobler
Submitted by Ellie Dobler
Contacted Mr. Katz about his written statements and he has none to provide at this
time.
383
Public Comment - IVGID Board of Trustee Meeting 2-9-2022 by Cliff Dobler
This written statement is to be made part of the minutes of this meeting.
Regarding the Budget Workshop held on February 3, 6 days ago, I provided a memo to Trustees Schmitz and Dent
regarding several gross errors contained in the presentation. Trustee Schmitz asked that I refrain from public
comments as the items were embarrassing to the Board and she would disclose them at the meeting. She did not.
Do not expect me to refrain from speaking any more.
On tonight's packet page 58, Underwood makes the following statement: "There are Public Service Recreation
irrigation accounts that do not pay excess water charges. Revising this long standing Board policy decision would
SIGNIFICANTLY impact operating costs at these venues." If proper charges were instituted it would save the 4,000
residential customers $.30 per month $14,000 per year. I find it laughable that $14,000 per year is SIGNIFICANT
```

**file 747, page 7 (2022-02-03)**

```
MOTION: Trustee Schmitz moved that the Board of Trustees
approved policy 15.1.0 with the changes identified here this
evening and in addition to make additions and corrections to the
memorandum to have the accurate up-to-date information in the
memorandum. Trustee Tonking seconded the motion which
carried unanimously 4-0. Trustee Wong was not in attendance.
Trustee Callicrate thanked Trustees Tonking, Schmitz and Dent.
H.1. SUBJECT: BOARD PRACTICE FOR APPROVAL - BUDGETING
AND FISCAL MANAGEMENT, DISTRICT-WIDE PRICING FOR
PRODUCTS AND SERVICES, PRACTICE 6.2.0
Recommendation for Action: Review, discuss and possibly take action to
approve the new Board Practice.
Director of Finance Paul Navazio said last year, it was identified as either a need
or an improvement to try to craft a pricing policy to guide the setting of prices and
fees for district services across all venues. As noted in the background section,
there is language currently in Policy 6.1 that basically references that the district
will adopt the process in a manner in which fees and charges are set through the
315
Minutes
Meeting of February 3, 2022
Page 8
budget process. And with the adoption of a formal practice to support policy 16.1,
that's the objective here. We discussed kind of a framework for pricing policy last
November; we brought the first draft of the pricing policy for discussion at the
December 10 meeting and based on feedback that we received, we have revised
the draft, which begins on page 18 of your board packet. I would note that right
behind it, beginning on page 25 is kind of the redline version to show the changes
that were incorporated into this draft from the version shared with the Board back
in December. I would just note that in the board memo under the discussion section
on page 17, I'll highlight these. We modified the memo for this item after the
rescheduling of this meeting based on feedback that we were receiving on some
specific aspects. We wanted to highlight that the two areas where staff continues
to receive some feedback and at times some conflicting feedback which has to do
with the definition section. It was also noted during a public comment on whether
the pricing policy should define guests or residents or picture passholders because
we use that terminology throughout. And whether that's defined in this policy or
Ordinance 7 or some other policy document, our goal is just to ensure that there's
clarity in the policy, so there's no ambiguity. Any feedback from the Board on that
would be helpful. Also, there was comments about incorporating definitions or
making sure the Board is comfortable with the definitions of full costs and operating
costs that are in here. And finally, some comments regarding the administration of
the policy. Ifs to clarify what fees the Board intends or wishes to formally approve
on an annual basis. And there are some fees that staff believes were absolutely
appropriate for the Board to review and approve but not necessarily all the fees.
We want to make sure that the Board is comfortable with kind of how the
administration is drafted so that it's clear what authority the District General
Manager and venue managers have to set fees consistent with the policy versus
what policy or what fees, particularly the picture passholder fees that would
continue to come to the Board for approval. We just call that out in the memo.
Based on feedback, we'll either modify again and bring it back, or see what the
pleasure is of the Board.
District General Manager Winquest said there wasn't an expectation necessarily
for the Board to approve this evening. What we are trying to do is gather feedback.
We believe this is based on feedback from the Board. We are prepared to take
feedback, do a quick turnaround, get the policy updated, and then have in front of
you on February 9. Our staff is currently working on developing preliminary
budgets and this policy helps dictate and guide what we are going to be doing with
a lot of the pricing and our revenue projects. The pricing policy is important, and
we1re excited to be coming to some closure on this issue. We had several public
comments about tennis and golf. I believe what we brought is what the Board has
```

### `truncated_outcome` — 3 occurrence(s)

**file 2670, page 1 (2026-01-28)**

```
MOTION: to Approve and Follow the Agenda as Submitted/Posted.
Moved By Audit Committee Chair Brandle
YEAS: Audit Committee Chair Brandle, Trustee Homan, At-Large Audit Committee 3
Member Lighthart
NAYS: None 0
MOTION
```

**file 1540, page 16 (2025-09-17)**

```
MOTION: to Approve and Authorize the General Manager to Sign and Execute an
Agreement with the Incline Ice Foundation for the Incline Village General Improvement
District to Accept a Donation of an Ice Rink Package and a Grant of $50,000+ to Support the
Ice Rink Activities.
M oved By Trustee Homan, Seconded by Trustee Jezycki
YEAS: Trustee Noble, Trustee Homan, Trustee Jezycki, Trustee Tonking 4
NAYS: Trustee Tulloch 1
MOTION
```

**file 1227, page 5 (2025-02-26)**

```
MOTION: to Approve Board Recommended Goals for District General
Manager through June 30, 2025.
Moved By Trustee Noble, Seconded by Trustee Homan
YEAS: Trustee Noble, Trustee Tulloch, Trustee Homan, Trustee 5
Jezycki, Trustee Tonking 0
NAYS: None
MOTION
```

### `missing_outcome` — 1 occurrence(s)

**file 1342, page 2 (2025-04-14)**

```
called for a vote on the request to remove this item from the agenda.
YEAS: Trustee Tulloch 1
NAYS: Trustee Noble, Trustee Homan, Trustee Jezycki, Trustee Tonking 4
The vote was 1/4 (Trustee Tulloch voted in favor of removing Item E.2., and the
remaining 4 Trustees voted in opposition to removing the Item). Item E.2. to review,
discuss and possibly approve the Districts' Tentative Budget as filed on Nevada State
Form 4404, will remain on the agenda.
E. GENERAL BUSINESS (for possible action)
E.1 Review, Discuss and Approve Additional Play Pass Options along with
season Pass Sales Incentives and Rate Adjustment to the Pricing of the
PM Season Pass. (Requesting Staff Member: Senior Head Golf
Professional Rob Bruce)
Full staff report and Board discussion for Item E.1. can be viewed/heard at:
https://ivgid.portal.civicclerk.com/event/659/media
Media Timestamp 00:16:07
```
