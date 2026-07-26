# Stage A benchmark report — IVGID minutes archive

Generated 2026-07-26 by scripts/run_benchmark.py.

## Spec correction

Spec §2.6 names Augusta Charter Township (146 PDFs) as the benchmark corpus; that is stale — it predates the switch to IVGID. The benchmark is the full IVGID minutes archive. Augusta is deferred to phase two as a generalisation test.

## Corpus

- Minutes PDFs: **153**
- Date range: **2021-05-12 to 2026-05-20**
- Slug: `ivgid`, events before 2026-07-26

## Automated metrics (not accuracy)

- Motions found: **183**
- Motions parsed clean (coverage): **149 (81.4%)**
- Documents crashed: **0**

### Flag breakdown

- `missing_mover`: 24 — e.g. file 2670 p1, file 1570 p9, file 1489 p16, file 1489 p17, file 1433 p10
- `missing_outcome`: 15 — e.g. file 2670 p1, file 1570 p21, file 1570 p21, file 1540 p16, file 1490 p3
- `tally_mismatch`: 9 — e.g. file 2670 p1, file 1570 p21, file 1570 p21, file 1540 p16, file 1465 p12
- `missing_vote_sections`: 6 — e.g. file 1489 p16, file 750 p5, file 750 p12, file 750 p26, file 750 p27

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
- file 1432 (2025-05-07 Special Meeting of the Board of Trustees): unparseable pages [19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54]; zero motions found
- file 1341 (2025-04-30 Regular Meeting of the Board of Trustees): unparseable pages [14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53]
- file 1342 (2025-04-14 Special Meeting of the IVGID Board of Trustees): unparseable pages [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
- file 1344 (2025-04-09 Regular Meeting of the Board of Trustees): unparseable pages [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36]; zero motions found
- file 1343 (2025-03-26 Regular Meeting of the Board of Trustees): unparseable pages [9, 10, 11, 12, 13, 14]; zero motions found
- file 1261 (2025-03-19 Special Meeting of the Board of Trustees): unparseable pages [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42]
- file 1262 (2025-03-12 Regular Meeting of the Board of Trustees): unparseable pages [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]
- file 1229 (2025-03-05 Special Meeting of the Board of Trustees): unparseable pages [6, 7, 8, 9, 10, 11, 12]; zero motions found
- file 1227 (2025-02-26 Regular Meeting of the Board of Trustees): unparseable pages [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34]
- file 1171 (2025-02-12 Regular Meeting of the Board of Trustees): unparseable pages [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
- file 1096 (2025-01-16 Special Meeting of the IVGID  Board of Trustees): unparseable pages [42, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60]; doc flags ['raw_fallback_page:1', 'raw_fallback_page:26']; zero motions found
- file 1103 (2025-01-08 Regular Meeting of the Board of Trustees): unparseable pages [42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118]; doc flags ['raw_fallback_page:1']; zero motions found
- file 1051 (2024-12-19 Regular Meeting of the Audit Committee): unparseable pages [6, 7, 8]; zero motions found
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

### [ ] 1. file 2665, page 12 (2026-03-11 Board of Trustees Meeting)

- text: to Approve the proposed Golf Key Rates as presented with a 3% increase in all Daily Green Fees and Numbered Play Pass products (10 play, 20 play passes) while the Seasonal Play Passes (Season Pass, Season Couples Passes) remain the same as the 2025 season as presented in Supplementary Item H.2. that
- mover: Trustee Noble | seconder: Trustee Homan
- yeas (4): Trustee Chair Tonking, Trustee Jezycki, Trustee Noble, Trustee Homan
- nays (1): Trustee Tulloch
- outcome: passed | flags: none

### [ ] 2. file 750, page 5 (2022-02-09 Regular Meeting of the Board of Trustees)

- text: Trustee Schmitz moved to remove General Business Item 1.2. from the agenda. Trustee Dent seconded the motion. Trustee Tonking asked if we approve those specific numbers in that agenda item, do they have to be those exact numbers or can they go lower because I remember there was something with the re
- mover: None | seconder: None
- yeas (None): —
- nays (None): —
- outcome: None | flags: ['missing_outcome', 'missing_mover', 'missing_vote_sections']

### [ ] 3. file 2636, page 4 (2026-01-28 Board of Trustees Meeting)

- text: to Approve the IVGID Board of Trustees Meeting Minutes for January 14, 2026.
- mover: Trustee Noble | seconder: Trustee Homan
- yeas (3): Trustee Chair Tonking, Trustee Jezycki, Trustee Homan
- nays (0): —
- outcome: passed | flags: none

### [ ] 4. file 2670, page 1 (2026-01-28 Audit Committee Meeting)

- text: to Approve and Follow the Agenda as Submitted/Posted. Moved By Audit Committee Chair Brandle
- mover: None | seconder: None
- yeas (3): Audit Committee Chair Brandle, Trustee Homan, At-Large Audit Committee  Member Lighthart
- nays (None): None  MOTION D. REPORTS TO THE COMMITTEE - (Not for possible Action) IVGID Audit Committee -- Meeting Minutes January, (Not for possible Action) - Progress on Material Weaknesses (MWs) & the Changes Associated with the Rubin Brown Report. (Requesting Staff Member: Director of Finance Noemi Barter) - pages  -  Full discussion on Item D.. Progress on Material Weaknesses (MW's) & the changes associated with the Rubin Brown Report can be viewed/ heard at: https://ivgid.portal.civicclerk.com/event//media Media Timestamp(:: - ::) Director of Finance Noemi Barter provided an update on the progress on material weaknesses associated with the Rubin Brown Report. She reportedthatthe auditprocesshasbegun;previousauditfindingsremain listed untilofficially resolved. Bankreconciliations are current and have been submitted to the state. The Tyler bank reconciliation module isunderway, currentlyin aside-by-side comparison phase.Internalservice fund billings are based on budget; a review ofthe prior six months and fiscal  is in progress to address shortfalls. Audit-related cash augmentations for the Board/fiscal  are to be submitted by June, ; preparations are ongoing. Inventory counts are complete and awaiting auditor review. The initial indication is that the inventory balance is not material. Staff haveprovided auditors with capital asset schedules, including potential write-offs; auditor action will depend on materiality. Revenues and point-of-sale system entries are now uploaded daily and tracked monthly. The P-card transaction process is transitioning back to Wells Fargo for streamlining; it remainsmanual untilthe module is implemented. Committee member Mich Homan requested that future reports include specific dates on when material weaknesses are remedied to demonstrate progress. He emphasized that adding timelines for future actions such as budget reviews, inventory counts, and planned system
- outcome: None | flags: ['missing_outcome', 'missing_mover', 'tally_mismatch']

### [ ] 5. file 1428, page 21 (2025-05-14 Regular Meeting of the Board of Trustees)

- text: to Adopt Resolution No.1915 – a Resolution prohibiting Commercial Watercraft Launching where prohibited by the Tahoe Regional Planning Agency (TRPA) Code of Ordinances and directing changes to Ordinance 7 – effective immediately. Moved by Trustee Noble; Seconded by Trustee Homan
- mover: None | seconder: None
- yeas (5): Trustee Noble, Trustee Tulloch, Trustee Homan, Trustee Jezycki, Trustee Tonking
- nays (0): —
- outcome: passed | flags: ['missing_mover']

### [ ] 6. file 1490, page 3 (2025-07-22 Meeting of the Board of Trustees)

- text: Appoint Trustee Jezycki to Serve on the Interview Panel for the Director of Human Resource Position.
- mover: Trustee Homan | seconder: Trustee Noble
- yeas (4): Trustee Noble, Trustee Tulloch, Trustee Homan, Trustee  Tonking
- nays (0): —
- abstain: ['Trustee Jezycki  MOTION PASSES F. FINAL PUBLIC COMMENTS - Limited to a maximum of three minutes Media Timestamp (:: - ::) Media Timestamp (:: - ::) G. ADJOURNMENT (for possible action) The meeting of the Board of Trustees was adjourned at : PM. Written Public Comment submitted for the Record July'] | absent: []
- outcome: None | flags: ['missing_outcome']

### [ ] 7. file 1489, page 16 (2025-06-26 Regular Meeting of the Board of Trustees)

- text: to Approve the draft letter with the following revisions: Pages 271 of 295 of the Board packet - Line 5: employee beach access program pending strike “receipt of” and insert “the outcome of this correspondence”; strike “a sufficient number” Line 9: as a property owner would you, strike “like” insert
- mover: None | seconder: None
- yeas (None): —
- nays (None): —
- outcome: None | flags: ['missing_outcome', 'missing_mover', 'missing_vote_sections']

### [ ] 8. file 747, page 7 (2022-02-03 Regular Meeting of the Board of Trustees)

- text: Trustee Schmitz moved that the Board of Trustees approved policy 15.1.0 with the changes identified here this evening and in addition to make additions and corrections to the memorandum to have the accurate up-to-date information in the memorandum. Trustee Tonking seconded the motion which carried u
- mover: None | seconder: None
- yeas (None): —
- nays (None): —
- outcome: None | flags: ['missing_outcome', 'missing_mover', 'missing_vote_sections']

### [ ] 9. file 1491, page 12 (2025-07-30 Meeting of the Board of Trustees)

- text: to approve Alternate #5: RFID Pedestrian Gate - Underground work Only.
- mover: Trustee Noble | seconder: Trustee Homan
- yeas (4): Trustee Noble, Trustee Tulloch, Trustee Homan, Trustee Tonking
- nays (1): Trustee Jezycki
- outcome: passed | flags: none

### [ ] 10. file 2806, page 5 (2026-04-28 Audit Committee Meeting)

- text: to Approve the Annual Audit Committee Assessment Report as required by Board Policy 15.1.0, section 2.9. to the Board of Trustees with the edits discussed.
- mover: Trustee Chair Tonking | seconder: At-Large Audit Committee Member Kelly
- yeas (4): Trustee Chair Tonking, Trustee Homan, At-Large Audit Committee Member  Kelly, At-Large Audit Committee Member Lighthart
- nays (0): —
- outcome: passed | flags: none

### [ ] 11. file 1261, page 7 (2025-03-19 Special Meeting of the Board of Trustees)

- text: to Approve the proposed Golf Rates as presented with the exception of Play Cards; direction to staff to return to the Board with Additional Options to the Play Passes to include a PM pass and Couples pass options Moved By Trustee H oman, Seconded by Trustee Noble
- mover: None | seconder: None
- yeas (5): Trustee Noble, Trustee Tulloch, Trustee Homan, Trustee Jezycki, Trustee Tonking
- nays (0): —
- outcome: passed | flags: ['missing_mover']

### [ ] 12. file 1559, page 21 (2025-11-12 Meeting of the IVGID Board of Trustees)

- text: to Approve the execution of a contract with Hometown Health Providers Insurance Company, Inc. to provide employee medical insurance coverage from January 1, 2026, to June 30, 2026.
- mover: Trustee Noble | seconder: Trustee Vice Chair Jezycki
- yeas (5): Trustee Noble, Trustee Tulloch, Trustee Homan, Trustee Vice Chair  Jezycki, Trustee Chair Tonking
- nays (0): —
- outcome: passed | flags: none

### [ ] 13. file 2783, page 2 (2026-05-20 Board of Trustees Meeting)

- text: to Approve and Authorize the Board Chair and Board Secretary to Sign and Execute an Agreement between Incline Village General Improvement District and Olympus & Associates, Inc. for Exterior Re-coating of Water Reservoir R6C-1; FY2025/26 Utilities: Water: CIP #2221WS22601; in the Amount of $199,000.
- mover: Trustee Homan | seconder: Trustee Jezycki
- yeas (4): Trustee Chair Tonking, Trustee Jezycki, Trustee Homan, Trustee Tulloch
- nays (0): —
- outcome: passed | flags: none

### [ ] 14. file 1171, page 3 (2025-02-12 Regular Meeting of the Board of Trustees)

- text: Approve the following consent matters, as submitted: Item F.1. Approval of the IVGID Board of Trustees Special Meeting Minutes for January 16, 2025; and Item F.2. Approval of the IVGID Board of Trustees Meeting Minutes for January 29, 2025. Media Timestamp 02:00:34
- mover: Trustee Noble | seconder: Trustee Homan.
- yeas (5): Trustee Noble, Trustee Tulloch, Trustee Homan, Trustee Jezycki, Trustee Tonking
- nays (0): —
- outcome: passed | flags: none

### [ ] 15. file 1140, page 3 (2025-01-29 Regular Meeting of the IVGID Board of Trustees)

- text: To approve the IVGID Board of Trustees Meeting Minutes for January 8, 2025.
- mover: Trustee Noble | seconder: Trustee Jezycki
- yeas (4): Trustee Noble, Trustee Tulloch, Trustee Jezycki, Trustee Tonking
- nays (0): —
- outcome: passed | flags: none

### [ ] 16. file 1341, page 8 (2025-04-30 Regular Meeting of the Board of Trustees)

- text: Approve and Authorize the Board Chair and Board Secretary to Sign and Execute an Agreement between Incline Village General Improvement District and KP Construction, Inc. for Capital Improvement Fire Hydrant Replacement – 2025; FY 2023/24 Utilities: Water: CIP #1F24200300; in the Amount of $209,980.0
- mover: Trustee Noble | seconder: Trustee Homan
- yeas (4): Trustee Noble, Trustee Tulloch, Trustee Homan, Trustee  Jezycki
- nays (0): —
- outcome: passed | flags: none

### [ ] 17. file 1227, page 6 (2025-02-26 Regular Meeting of the Board of Trustees)

- text: to Approve Diamond Peak Ski Resort’s Season Pass Rates for the 2025-26 Ski Season.
- mover: Trustee Noble | seconder: Trustee Jezycki
- yeas (5): Trustee Noble, Trustee Tulloch, Trustee Homan, Trustee  Jezycki, Trustee Tonking
- nays (0): —
- outcome: passed | flags: none

### [ ] 18. file 2779, page 8 (2026-05-13 Board of Trustees Meeting)

- text: to Close the Public Hearing for Recommended Amendments to the Incline Village General Improvement District Water and Wastewater Rates and Adjustments to the Fee Schedule.
- mover: Trustee Homan | seconder: Trustee Noble
- yeas (5): Trustee Chair Tonking, Trustee Jezycki, Trustee Noble, Trustee Homan, Trustee Tulloch
- nays (0): —
- outcome: passed | flags: none

### [ ] 19. file 1570, page 21 (2025-12-10 Meeting of the IVGID Board of Trustees)

- text: to Approve Resolution 1920 - Guest Employee Beach Access Program.
- mover: Trustee Jezycki | seconder: Trustee Homan
- yeas (4): Trustee Noble, Trustee Homan, Trustee Jezycki, Trustee Chair Tonking
- nays (None): Trustee Tulloch  MOTION PASSES H. (For possible Action) Review, Discuss and possibly Approve the District General Manager's Proposed Goals. (Requesting Staff and Board Member: Director of Human Resources Eric Milavsky and Trustee Vice Chair Michelle Jezycki) Discussion and Approval of the District General Managers Goals are available to be viewed or heard at: https://ivgid.portal.civicclerk.com/event//media Media Timestamp (:: - ::) The Director of Human Resources, Eric Milavsky, presented the review and compilation of the District General Managers Goals. He explained that he reached out to each Trustee individually to gather feedback on goals and objectives for the General Manager (GM) for the remainder of the fiscal year. He and Trustee Jezycki then consolidated the feedback into a single working document, aiming to capture the spirit of all trustees' input. The compilation process included combining overlapping suggestions and rewording for clarity
- outcome: None | flags: ['missing_outcome', 'tally_mismatch']

### [ ] 20. file 2720, page 10 (2026-04-08 Board of Trustees Meeting)

- text: to Approve the Date and Time for the Public Hearing to Implement Amendments to the Water and Wastewater rates, as well as Adjustments to the Fee Schedule, for Wednesday, May 13, 2026, at 5:00 p.m.
- mover: Trustee Jezycki | seconder: Trustee Noble
- yeas (5): Trustee Chair Tonking, Trustee Jezycki, Trustee Noble, Trustee Homan, Trustee Tulloch
- nays (0): —
- outcome: passed | flags: none

### [ ] 21. file 1511, page 16 (2025-08-27 Meeting of the Board of Trustees)

- text: to Appoint Vice Chair Michelle Jezycki as Board Liaison to work with the Human Resource Director to update an evaluation process for the District General Manager's 2026 annual review cycle.
- mover: Trustee Noble | seconder: Trustee Homan
- yeas (3): Trustee Noble, Trustee Homan, Trustee Jezycki
- nays (0): —
- outcome: passed | flags: none

### [ ] 22. file 1433, page 13 (2025-05-30 Special Meeting of the IVGID Board of Trustees)

- text: to close the Public Hearing on the Fiscal Year 2025-2026 Operating and Capital Improvement Projects Budgets. M oved By Trustee Jezycki; Seconded by Trustee Homan
- mover: None | seconder: None
- yeas (4): Trustee Noble, Trustee Homan, Trustee Jezycki, Trustee Tonking
- nays (0): —
- outcome: passed | flags: ['missing_mover']

### [ ] 23. file 1602, page 8 (2026-01-14 Board of Trustees Meeting)

- text: to Ratify and Adopt Resolution No. 1921 authorizing Incline Village General Improvement District to create and maintain Fiduciary Fund 700 - Tahoe Water Supply Association. This Fund is established for the specific purpose of accounting for assets held by the Incline Village General Improvement Dist
- mover: Trustee Noble | seconder: Trustee Jezycki
- yeas (5): Trustee Chair Tonking, Trustee Jezycki, Trustee Noble, Trustee Homan, Trustee Tulloch
- nays (0): —
- outcome: passed | flags: none

### [ ] 24. file 1540, page 8 (2025-09-17 Meeting of the IVGID Board of Trustees)

- text: to Close the Public Hearing
- mover: Trustee Jezycki | seconder: Trustee Homan
- yeas (5): Trustee Noble, Trustee Tulloch, Trustee Homan, Trustee Jezycki, Trustee  Tonking
- nays (0): —
- outcome: passed | flags: none

### [ ] 25. file 2778, page 17 (2026-04-29 Board of Trustees Meeting)

- text: to Approve the Facility Fee for Fiscal Year 2027, with the Ice-Skating project removed.
- mover: Trustee Homan | seconder: Trustee Noble
- yeas (3): Trustee Jezycki, Trustee Noble, Trustee Homan
- nays (2): Trustee Chair Tonking, Trustee Tulloch
- outcome: passed | flags: none

## Failure catalogue (specification for Stage B)

### `missing_mover` — 17 occurrence(s)

**file 1570, page 9 (2025-12-10)**

```
MOTION: To remove Item H.5. from the Agenda
Moved by Trustee Tulloch, Trustee Chair Tonking called for a Vote to remove Item H.5.
from the agenda as requested.
YEAS: Trustee Tulloch 1
NAYS: Trustee Secretary Noble, Trustee Treasurer Homan, Trustee Vice Chair 4
Jezycki, Trustee Chair Tonking
MOTION FAILED
```

**file 1489, page 17 (2025-06-26)**

```
Motion: To modify the motion on the floor by adding the following revision to page 272 of
295 of the Board packet - Line 31: where "the Answer" was stricken, insert the word "No"
before the proposed new answer - insert “no”.
Moved by: Trustee Homan
Trustee Noble accepted the Motion as modified; Seconded by Trustee Homan.
YEAS: Trustee Homan, Trustee Jezycki, Trustee Noble, and Chair Tonking 4
NAYS: Trustee Tulloch 1
MOTION PASSED
```

**file 1433, page 10 (2025-05-30)**

```
MOTION: Moved By Trustee Homan; made a motion to open the Public Hearing on
the Fiscal Year 2025-2026 Operating and Capital Improvement Projects
Budgets; Seconded by Trustee Jezycki
YEAS: Trustee Noble, Trustee Homan, Trustee Jezycki, Trustee Tonking 4
NAYS: None 0
MOTION PASSED
```

**file 1433, page 13 (2025-05-30)**

```
MOTION: to close the Public Hearing on the Fiscal Year 2025-2026 Operating and
Capital Improvement Projects Budgets.
M oved By Trustee Jezycki; Seconded by Trustee Homan
YEAS: Trustee Noble, Trustee Homan, Trustee Jezycki, Trustee Tonking 4
NAYS: None 0
MOTION PASSED
```

**file 1433, page 14 (2025-05-30)**

```
MOTION: to Approve the Recreation Facility Fee totaling $1,375; Moved By Trustee
Homan, Seconded by Trustee Jezycki
YEAS: Trustee Noble, Trustee Homan, Trustee Jezycki, Trustee Tonking 4
NAYS: None 0
MOTION PASSED
```

**file 1428, page 8 (2025-05-14)**

```
MOTION: To open the Public Hearing – on the Recommended Amendments to the
Sewer and Water Rate Fee Schedule.
Moved by Trustee Jezycki; Seconded by Trustee Homan
YEAS: Trustee Noble, Trustee Tulloch, Trustee Homan, Trustee Jezycki, 5
Trustee Tonking 0
NAYS: None
MOTION PASSED
```

**file 1428, page 12 (2025-05-14)**

```
Motion: to Close the Public Hearing - On the Recommended Amendments to the
Sewer and Water Rate Fee Schedule.
Moved by Trustee Noble; Seconded by Trustee Homan
YEAS: Trustee Noble, Trustee Tulloch, Trustee Homan, Trustee Jezycki, 5
Trustee Tonking 0
NAYS: None
MOTION PASSED
```

**file 1428, page 12 (2025-05-14)**

```
MOTION: to Adopt Resolution No. 1914 - a Resolution approving the
Amendments to the Sewer and Water Rates, as well as Adjustments to the Fee
Schedule, and the revised final proposed Alternate 4.
Moved by Trustee Noble Seconded by Trustee Homan
YEAS: Trustee Noble, Trustee Homan, Trustee Jezycki, Trustee 4
Tonking 1
NAYS: Trustee Tulloch
MOTION PASSED
```

**file 1428, page 21 (2025-05-14)**

```
MOTION: to Adopt Resolution No.1915 – a Resolution prohibiting Commercial
Watercraft Launching where prohibited by the Tahoe Regional Planning Agency
(TRPA) Code of Ordinances and directing changes to Ordinance 7 – effective
immediately. Moved by Trustee Noble; Seconded by Trustee Homan
YEAS: Trustee Noble, Trustee Tulloch, Trustee Homan, Trustee Jezycki, 5
Trustee Tonking 0
NAYS: None
MOTION PASSED
```

**file 1428, page 22 (2025-05-14)**

```
MOTION: Adopt Resolution No. 1916 - a Resolution Preliminarily Approving the
Report for Collection of Recreation Standby and Service Charges for Fiscal Year
2025/2026 and Confirming the Public Hearing Date for Friday, May 30, 2025, at 12:
00 p.m. Moved by Trustee Noble; Seconded by Trustee Homan
YEAS: Trustee Noble, Trustee Homan, Trustee Jezycki, Trustee Tonking 4
NAYS: Trustee Tulloch 1
MOTION PASSED
```

**file 1342, page 3 (2025-04-14)**

```
MOTION: Approve; Moved By Trustee Homan: to Approve Additional Play Pass
Options along with season Pass Sales Incentives and Rate Adjustment to the Pricing
of the PM Season Pass; Seconded by Trustee Jezycki
YEAS: Trustee Noble, Trustee Homan, Trustee Jezycki, Trustee Tonking 4
NAYS: Trustee Tulloch 1
MOTION PASSED
```

**file 1261, page 7 (2025-03-19)**

```
MOTION: to Approve the proposed Golf Rates as presented with the exception of
Play Cards; direction to staff to return to the Board with Additional Options to the Play
Passes to include a PM pass and Couples pass options Moved By Trustee
H oman, Seconded by Trustee Noble
YEAS: Trustee Noble, Trustee Tulloch, Trustee Homan, Trustee Jezycki, 5
Trustee Tonking 0
NAYS: None
MOTION PASSED
```

**file 1262, page 4 (2025-03-12)**

```
MOTION: to Appoint Trustee Michelle Jezycki, Board Liaison, to attend the
Interviews for Candidates for the General Manager of Golf Operations Position
and Provide Feedback to Staff. Moved by Trustee Homan, Seconded by
Trustee Noble
YEAS: Trustee Noble, Trustee Tulloch, Trustee Homan, Trustee Jezycki, 5
Trustee Tonking 0
NAYS: None
MOTION PASSED
```

**file 1262, page 5 (2025-03-12)**

```
MOTION: to Approve and Authorize the Board Chair and Secretary to Sign an
Agreement between the District and CORE West Inc. dba CORE Construction for
the 100% Construction Development Contract for Incline Beach House Project -
FY 2024/25 Capital Improvement Project; Fund: Community Services; Division:
Beaches; Project #3973LI1302; in the amount of $755,000. Moved by Trustee
Jezycki, Seconded by Trustee Homan
YEAS: Trustee Noble, Trustee Homan, Trustee Jezycki, Trustee Tonking 4
NAYS: None 0
ABSTAIN: Trustee Tulloch
MOTION PASSED
```

**file 1262, page 5 (2025-03-12)**

```
MOTION: to Approve a project budget of $500,000 to include the final design for
Option 2 titlements permitting, and direct staff to move forward with Spohn Ranch,
to provide a final construction proposal. Moved By Trustee Noble, Seconded by
Trustee Tulloch
YEAS: Trustee Noble, Trustee Tulloch, Trustee Homan, Trustee Jezycki, 5
Trustee Tonking 0
NAYS: None
MOTION PASSED
```

**file 1262, page 7 (2025-03-12)**

```
MOTION: to Approve the engagement with Thorndal Armstrong, PC for defense of
litigation filed as provided in the recommendation; amended by Trustee Tulloch to
request a push for cost recovery. Moved By Trustee Homan, Seconded by
Trustee Tulloch
YEAS: Trustee Noble, Trustee Tulloch, Trustee Homan, Trustee Jezycki, 5
Trustee Tonking 0
NAYS: None
MOTION PASSED
```

**file 1227, page 5 (2025-02-26)**

```
MOTION: To nominate Trustee Michaela Tonking as the newest Board
Member of the Audit Committee. Moved By Trustee Jezycki, Seconded by
T rustee Noble
YEAS: Trustee Noble, Trustee Tulloch, Trustee Homan, Trustee 5
Jezycki, Trustee Tonking 0
NAYS: None
MOTION PASSED
```

### `missing_outcome,tally_mismatch` — 6 occurrence(s)

**file 1570, page 21 (2025-12-10)**

```
MOTION: to Approve Resolution 1920 - Guest Employee Beach Access Program.
Moved By Trustee Jezycki, Seconded by Trustee Homan
YEAS: Trustee Noble, Trustee Homan, Trustee Jezycki, Trustee Chair Tonking 4
NAYS: Trustee Tulloch 1
MOTION PASSES
H.7 (For possible Action) Review, Discuss and possibly Approve the District
General Manager's Proposed Goals. (Requesting Staff and Board Member:
Director of Human Resources Eric Milavsky and Trustee Vice Chair Michelle
Jezycki)
Discussion and Approval of the District General Managers Goals are available to be viewed
or heard at: https://ivgid.portal.civicclerk.com/event/588/media
Media Timestamp (02:45:33 - 03:01:15)
The Director of Human Resources, Eric Milavsky, presented the review and compilation of
the District General Managers Goals. He explained that he reached out to each Trustee
individually to gather feedback on goals and objectives for the General Manager (GM) for the
remainder of the fiscal year. He and Trustee Jezycki then consolidated the feedback into a
single working document, aiming to capture the spirit of all trustees' input. The compilation
process included combining overlapping suggestions and rewording for clarity.
```

**file 1570, page 21 (2025-12-10)**

```
MOTION: to Approve the District General Manager's Proposed Goals, with the changes
discussed.
Moved By Trustee Homan, Seconded by Trustee Noble
YEAS: Trustee Noble, Trustee Tulloch, Trustee Homan, Trustee Jezycki, Trustee 5
Chair Tonking
NAYS: None 0
MOTION PASSES
The Boards suggested edits below:
• Remove the legal advice objective (V.12.) from the GM Goals document.
• Revise language on venue profitability and relative KPIs to focus on optimizing
financial performance rather than mandating cost recovery or profitability.
• Number 12 (pages 337 and 344) add the Bike Park Phase II.
• Adjust overly prescriptive objectives to broader, more flexible language, particularly
for the timing and execution of senior team reviews.
• Incorporate cost-benefit analysis as a KPI in section 2.B.6. and clarify language in that
section.
• Add consideration of year-round/seasonal staff review and feedback to the
organizational structure objectives.
• The new Chart Style Tracking tool is in the development stage (per Trustee Jezycki).
• HR Director Milavsky to update and distribute the revised document to Board
members for final review before the January Board Meeting.
*Note taken for the District Clerk to explore solutions to add pages to the digital agenda
document for ease of navigation on Trustee iPads.
H.8 (For possible Action) Election of Board of Trustees Officers for the 2026 Term.
(Requesting Staff Member: District Clerk Heidi White)
The Election of the 2026 Term for the Board of Trustees Officers is available to be viewed or
heard at: https://ivgid.portal.civicclerk.com/event/588/media
Media Timestamp (03:01:17 - 03:03:10)
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
J. LONG RANGE CALENDAR - (for possible action)
J.1 (For possible Action) - Review, discuss and possibly Add or Remove Long
Range Calendar Items to Future Board of Trustee Agendas.
The full discussion related to Item J.1. The Long Range Calendar can be viewed/ heard at:
https://ivgid.portal.civicclerk.com/event/703/media
Media Timestamp (02:22:11 - 02:28:04)
Director of Administrative Services Susan Herron began the conversation by letting the Board
know that the next calendar will include 2026 dates, continuing with once-a-month meetings
by default, due to positive staff feedback. She then asked for a formal motion to cancel the
November 26 and December 31, 2025, meetings, due to their proximity to holidays, clarifying
that additional meetings can be scheduled as needed, designated as special meetings. She
also noted that regular meeting starting times will be changed to 5:00 PM starting in the fall.
Chair Tonking anticipates a need for extra workshops or meetings, especially related to
strategic planning and the budget.
```

**file 1465, page 12 (2025-06-11)**

```
MOTION: to Authorize Staff to move forward with preparing a contract for legal counsel
services to engage Taggart & Taggart as District Legal Counsel effective July 1, 2025;
Moved By Trustee Noble, Seconded by Trustee Homan
YEAS: Trustee Noble, Trustee Homan, Trustee Jezycki, Trustee Tonking 4
NAYS: None 0
ABSTAIN: Trustee Tulloch 1
MOTION PASSES
G.3 Review, Discuss, and Approve the Employee Pass Program for Beach
Access; Review, Discuss, and Approve Any Applicable Fees; Direct Staff to
Send Correspondence to Property Owners to Determine Whether Any
Property Owners Elect to Designate Staff (and Their Dependents) As Their
Guests for Beach Access; Direct Staff to Monitor Daily Beach Visits and
P rovide Weekly Reports. (Requesting Board Member: Trustee Dave Noble)
Item G.3. Employee Pass Program for Beach Access can be viewed/heard
at: https://ivgid.portal.civicclerk.com/event/578/media
Media Timestamp (02:12:59 - 02:59:45)
Trustee Noble returned the proposed reinstatement of the employee pass program for
beach access and provided outlined steps including review and approval of applicable
fees, sending correspondence to property owners asking if they'd sponsor staff and
dependence as beach guests, and setting up daily monitoring of beach visits with
weekly reports.
During Board deliberations, questions were raised about potential overcrowding and the
authority provided by the beach deed regarding access for property owners and their
guests.
It was clarified by Legal Counsel Rudin that the deed grants the Board authority to set
access rules and designating employees as guests does not require property owners to
use their punch cards for employee access.
Debate centered around whether revising assignment and guest provisions in
Ordinance 7 was necessary, with clarity that this program operates under the 'guest'
provision, not 'assignment'.
```

**file 1433, page 18 (2025-05-30)**

```
MOTION: to Close the Public Heaaring for the Incline Village General Improvement
District Fiscal Year 2025/2026 Facility Fees Public Hearing for the Incline Village
General Improvement District Fiscal Year 2025/2026 Facility Fees.
M oved By Trustee Jezycki, Seconded by Trustee Homan
r
YEAS: Trustee Noble, Trustee Homan, Trustee Jezycki, Trustee Tonking 4
NAYS: None 0
D MOTION PASSED
F.1 Review, Discuss and Possibly Adopt Resolution No. 1917 - A Resolution
Approving the Report for Collection of Recreation Standby and Service
Charges (Also Known as the Recreation Facility Fee and Beach Facility
Fee), for Fiscal Year 2025-2026 (Requesting Staff Member: Director of
F inance Jessica O'Connell)
Full discussion on Item F.1. Adopt Resolution No. 1917 - Approving the Report for
Collection of Recreation Standby and Service Charges can be heard/viewed
at: https://ivgid.portal.civicclerk.com/event/646/media Media Timestamp (02:41:38)
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
G.4 Review, Discuss, and Approve the 2025/2026 Budget Workshop
Schedule: Discussion, Direction, and possible Action.
(Requesting Staff Member: District General Manager Robert
Harrison)
The full Board and Staff discussion can be viewed at:
https://ivgid.portal.civicclerk.com/event/561/media,
MEDIA TIMESTAMP 00:53:43
```

### `missing_outcome,missing_mover,missing_vote_sections` — 6 occurrence(s)

**file 1489, page 16 (2025-06-26)**

```
MOTION: to Approve the draft letter with the following revisions:
Pages 271 of 295 of the Board packet - Line 5: employee beach access program pending
strike “receipt of” and insert “the outcome of this correspondence”; strike “a sufficient
number”
Line 9: as a property owner would you, strike “like” insert “be willing.” Continue on - to sponsor
staff and their dependents as your guests for access to the beaches - and insert “knowing any
applicable beach entry fees will be paid by staff and their dependents”;
Lines 12 through 14: “If yes”(words) would be bolded, the rest would be underlined
Line 16: “If no” (words) would be bolded.
Page 272 of 295 of the Board packet: Line 31: Will specific staff and their dependents be
assigned to me; strike “(that answer)” and insert “staff and their dependents will be pooled
with property owners period”; then
Line 41: starting after the period, the Board of Trustees - insert “has already” strike “also” so
it would read: “The Board of Trustees has already directed staff to provide weekly reports on
beach visits to monitor numbers” and then insert comma and insert the words “if the program
moves forward it will include”; and then strike “in case limits on”, and then it will continue on
the number of staff so that phrase would read “If the program moves forward, it will include
the number of staff and their dependents”; and then strike “should it be implemented.”
Page 273 of 295 - Line 52: starting with the word no: “no other people will be allowed beach
access through the employee beach access program”. This wasn't discussed, but I would
recommend just underlining that for emphasis:
Lines 55 through 56: That Q&A would go to that would be #1 in the Q&As.
Page 274 of 295 - Line 70: Will the employee beach access program expose it to legal
challenges strike “it is possible there will be a legal challenge” insert “a legal challenge it's
always a possibility” and then continue on “as IVGID cannot prevent anyone from filing” strike
“unwarranted”.
Line 74: Starts with deed strike the word “and” put a comma in, so that it would read
“including” strike “this” insert “taking” and then the word “additional” insert the word “proactive”
continues on “step of asking property owners if they would like to sponsor staff and their
dependents as their guests” strike “for” insert the word “enabling access to the beaches” and
```

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
```

### `missing_outcome` — 2 occurrence(s)

**file 1490, page 3 (2025-07-22)**

```
MOTION: Appoint Trustee Jezycki to Serve on the Interview Panel for the
Director of Human Resource Position.
Moved By Trustee Homan, Seconded by Trustee Noble
YEAS: Trustee Noble, Trustee Tulloch, Trustee Homan, Trustee 4
Tonking
NAYS: None 0
ABSTAIN: Trustee Jezycki 1
MOTION PASSES
F. FINAL PUBLIC COMMENTS - Limited to a maximum of three minutes
Media Timestamp (00:07:29 - 00:10:04)
Media Timestamp (00:08:13 - 00:10:04)
G. ADJOURNMENT (for possible action)
The meeting of the Board of Trustees was adjourned at 4:08 PM.
Written Public Comment
submitted for the
Record
July 22, 2025
```

**file 1227, page 6 (2025-02-26)**

```
MOTION: To approve the Budget Schedule with the understanding that if
there needs to be some flexibility, the Board of Trustees will be notified, and
the meeting schedule will be modified accordingly.
Moved By Trustee Noble, Seconded by Trustee Tulloch
YEAS: Trustee Noble, Trustee Tulloch, Trustee Homan, Trustee 5
Jezycki, Trustee Tonking 0
NAYS: None
M OTION PASSES
G.5 Review, Discuss and possibly Approve Diamond Peak Ski
Resort’s Season Pass Rates for 2025-2026 Ski Season. (For
possible Action) (Requesting Staff Member: Diamond Peak
General Manager Mike Bandelin)
Diamond Peak Ski General Manager Mike Bandelin provided a brief overview
of the Diamond Peak Ski Resort Season Pass Rates for 2025-2026.
The full Board and Staff discussion can be viewed at:
https://ivgid.portal.civicclerk.com/event/561/media,
MEDIA TIMESTAMP 01:03:27
```

### `tally_mismatch` — 2 occurrence(s)

**file 1433, page 14 (2025-05-30)**

```
MOTION: to Adopt a fee value of 60% for individual punch cards for the equitable
usage of Capital Improvement;
Moved By Trustee Jezycki, Seconded by Trustee Homan
YEAS: Trustee Noble, Trustee Homan, Trustee Jezycki, Trustee Tonking 4
NAYS: None t 0
MOTION PASSED
```

**file 1433, page 14 (2025-05-30)**

```
MOTION: to Approve the Central Services Cost Allocation Plan, allocating
a
Approximately $4.05 Million in the General Fund costs to the utility, Community
Services and Beach Funds;
Moved By Trustee Homan, Seconded by Trustee Jezycki
r
YEAS: Trustee Noble, Trustee Homan, Trustee Jezycki, Trustee Tonking 4
NAYS: None 0
D
MOTION PASSED
```

### `missing_outcome,missing_mover,tally_mismatch` — 1 occurrence(s)

**file 2670, page 1 (2026-01-28)**

```
MOTION: to Approve and Follow the Agenda as Submitted/Posted.
Moved By Audit Committee Chair Brandle
YEAS: Audit Committee Chair Brandle, Trustee Homan, At-Large Audit Committee 3
Member Lighthart
NAYS: None 0
MOTION
D. REPORTS TO THE COMMITTEE - (Not for possible Action)
IVGID Audit Committee -2- Meeting Minutes January 28, 2026
1. (Not for possible Action) - Progress on Material Weaknesses (MWs) & the Changes
Associated with the Rubin Brown Report. (Requesting Staff Member: Director of
Finance Noemi Barter) - pages 3 - 8
Full discussion on Item D.1. Progress on Material Weaknesses (MW's) & the changes associated
with the Rubin Brown Report can be viewed/ heard at:
https://ivgid.portal.civicclerk.com/event/726/media Media Timestamp(00:11:40 - 00:18:08)
Director of Finance Noemi Barter provided an update on the progress on material weaknesses
associated with the Rubin Brown Report.
She reportedthatthe auditprocesshasbegun;previousauditfindingsremain listed untilofficially
resolved. Bankreconciliations are current and have been submitted to the state. The Tyler bank
reconciliation module isunderway,currentlyin aside-by-side comparison phase.Internalservice
fund billings are based on budget; a review ofthe prior six months and fiscal 2025 is in progress
to address shortfalls. Audit-related cash augmentations for the Board/fiscal 2026 are to be
submitted by June 30, 2026; preparations are ongoing. Inventory counts are complete and
awaiting auditor review. The initial indication is that the inventory balance is not material. Staff
haveprovided auditors with capital asset schedules, including potential write-offs; auditor action
will depend on materiality. Revenues and point-of-sale system entries are now uploaded daily
and tracked monthly. The P-card transaction process is transitioning back to Wells Fargo for
streamlining; it remainsmanual untilthe module is implemented.
Committee member Mich Homan requested that future reports include specific dates on when
material weaknesses are remedied to demonstrate progress. He emphasized that adding
timelines for future actions such as budget reviews, inventory counts, and planned system
```
