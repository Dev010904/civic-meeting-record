# Hand-verification checklist — Stage A parser

Seed: **20260726** (random.Random, scripts/make_verify.py — rerun it to reproduce this exact sample).

Selection criteria: documents dated 2025-02-01 or later, plus Audit Committee documents dated 2024-12-01 or later (the format-era boundaries: the structured Board era begins February 2025; the structured Audit era begins December 2024). All truncated_outcome motions are force-included; the rest are drawn round-robin across shuffled documents so the sample spans as many distinct PDFs as possible.

Sample: **25 motions across 24 documents**, sorted by document then page. Every field below is parser output; compare each against the PDF at the fetch URL. Coverage is not accuracy — this checklist is what separates the two.

### 1 of 25
Document: 2024-12-19 Regular Meeting of the Audit Committee (file 1051, page 5)
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1051,plainText=false)

Parser says:
  Motion:    Approve the Audit Committee Meeting Minutes for November 18, 2024.
  Mover:     — (not recorded in minutes)
  Seconder:  — (not recorded in minutes)
  YEAS (3):  Committee Members Brandle, Schmitz, Tulloch
  NAYS (0):  —
  Outcome:   PASSED
  Timestamp: — (none on this page)

Correct? [x] yes  [ ] no — what's wrong: ________________

### 2 of 25
Document: 2025-02-12 Regular Meeting of the Board of Trustees (file 1171, page 3)
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1171,plainText=false)

Parser says:
  Motion:    Approve the following consent matters, as submitted: Item F.1. Approval of the IVGID Board of Trustees Special...
  Mover:     Trustee Noble
  Seconder:  Trustee Homan
  YEAS (5):  Trustee Noble, Trustee Tulloch, Trustee Homan, Trustee Jezycki, Trustee Tonking
  NAYS (0):  —
  Outcome:   PASSED
  Timestamp: — (none on this page)

Correct? [ ] yes  [x] no — what's wrong: Timestamp missed — page 3 has "Media Timestamp 02:00:34" inside the motion block (plus 01:20:45, 00:34:29, 00:36:48 on the page). All vote fields correct.

### 3 of 25
Document: 2025-02-26 Regular Meeting of the Board of Trustees (file 1227, page 5)
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1227,plainText=false)

Parser says:
  Motion:    to Approve Board Recommended Goals for District General Manager through June 30, 2025.
  Mover:     Trustee Noble
  Seconder:  Trustee Homan
  YEAS (5):  Trustee Noble, Trustee Tulloch, Trustee Homan, Trustee Jezycki, Trustee Tonking
  NAYS (0):  —
  Outcome:   UNKNOWN — bare 'MOTION' terminator, outcome word missing in minutes (flagged truncated_outcome)
  Timestamp: — (none on this page)
  Flags:     truncated_outcome

Correct? [ ] yes  [x] no — what's wrong: Timestamp missed — page 5 has "MEDIA TIMESTAMP 00:43:15" directly above the motion. Bare MOTION terminator confirmed on page — clerk did omit the outcome word. All vote fields correct.

### 4 of 25
Document: 2025-02-26 Regular Meeting of the Board of Trustees (file 1227, page 6)
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1227,plainText=false)

Parser says:
  Motion:    to Approve Diamond Peak Ski Resort’s Season Pass Rates for the 2025-26 Ski Season.
  Mover:     Trustee Noble
  Seconder:  Trustee Jezycki
  YEAS (5):  Trustee Noble, Trustee Tulloch, Trustee Homan, Trustee Jezycki, Trustee Tonking
  NAYS (0):  —
  Outcome:   PASSED
  Timestamp: — (none on this page)

Correct? [ ] yes  [x] no — what's wrong: Timestamp missed — page 6 has "MEDIA TIMESTAMP 01:03:27" above the motion. All vote fields correct.

### 5 of 25
Document: 2025-03-05 Special Meeting of the Board of Trustees (file 1229, page 2)
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1229,plainText=false)

Parser says:
  Motion:    to approve staff's recommendation as contained in the memo of the Board packet; approving the 2025/2026 Group ...
  Mover:     Trustee Noble
  Seconder:  Trustee Jezycki
  YEAS (3):  Trustee Noble, Trustee Jezycki, Trustee Tonking
  NAYS (1):  Trustee Tulloch
  Outcome:   PASSED
  Timestamp: — (none on this page)

Correct? [ ] yes  [x] no — what's wrong: Timestamp missed — page 2 has "Time Stamp 00:13:59" above the motion. All vote fields correct (3-1 with 4 voters is what the minutes record).

### 6 of 25
Document: 2025-03-19 Special Meeting of the Board of Trustees (file 1261, page 7)
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1261,plainText=false)

Parser says:
  Motion:    to Approve the proposed Golf Rates as presented with the exception of Play Cards; direction to staff to return...
  Mover:     Trustee Homan
  Seconder:  Trustee Noble
  YEAS (5):  Trustee Noble, Trustee Tulloch, Trustee Homan, Trustee Jezycki, Trustee Tonking
  NAYS (0):  —
  Outcome:   PASSED
  Timestamp: — (none on this page)

Correct? [ ] yes  [x] no — what's wrong: Timestamp missed — page 7 has "Media Timestamp - 02:45:36" above the motion. All vote fields correct.

### 7 of 25
Document: 2025-04-09 Regular Meeting of the Board of Trustees (file 1344, page 4)
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1344,plainText=false)

Parser says:
  Motion:    Moved by Trustee Homan: to approve the Consent Calendar as documented; Motion Seconded by Trustee Jezycki. Ite...
  Mover:     Trustee Homan
  Seconder:  Trustee Jezycki
  YEAS (4):  Trustee Tulloch, Trustee Homan, Trustee Jezycki, Trustee Tonking
  NAYS (0):  —
  Outcome:   PASSED
  Timestamp: — (none on this page)

Correct? [ ] yes  [x] no — what's wrong: (1) Timestamp missed — page has "Media Timestamp 00:45:35". (2) Motion text retains the attribution clause: starts "Moved by Trustee Homan:" and contains "Motion Seconded by Trustee Jezycki". Vote fields correct.

### 8 of 25
Document: 2025-04-14 Special Meeting of the IVGID Board of Trustees (file 1342, page 3)
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1342,plainText=false)

Parser says:
  Motion:    Approve; : to Approve Additional Play Pass Options along with season Pass Sales Incentives and Rate Adjustment...
  Mover:     Trustee Homan
  Seconder:  Trustee Jezycki
  YEAS (4):  Trustee Noble, Trustee Homan, Trustee Jezycki, Trustee Tonking
  NAYS (1):  Trustee Tulloch
  Outcome:   PASSED
  Timestamp: — (none on this page)

Correct? [ ] yes  [x] no — what's wrong: (1) Motion text mangled: "Approve; : to Approve Additional Play Pass Options..." — leftover "Approve;" prefix and orphaned colon. (2) Timestamp missed — page has "Media Timestamp 00:28:25" and "00:28:40". Vote fields correct. NOTE: document watermarked DRAFT.

### 9 of 25
Document: 2025-05-07 Special Meeting of the Board of Trustees (file 1432, page 17)
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1432,plainText=false)

Parser says:
  Motion:    : to Approve to reset the date and time for the Public Hearing(s) for the FY 2025/2026 Budget and Recreation R...
  Mover:     Trustee Noble
  Seconder:  Trustee Homan
  YEAS (4):  Trustee Noble, Trustee Homan, Trustee Jezycki, Trustee Tonking
  NAYS (1):  Trustee Tulloch
  Outcome:   PASSED
  Timestamp: — (none on this page)

Correct? [ ] yes  [x] no — what's wrong: (1) Motion text starts with a stranded colon: ": to Approve to reset the date and time...". (2) Timestamp missed — page has "Media Timestamp 02:01:05". Vote fields correct.

### 10 of 25
Document: 2025-05-14 Regular Meeting of the Board of Trustees (file 1428, page 8)
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1428,plainText=false)

Parser says:
  Motion:    To open the Public Hearing – on the Recommended Amendments to the Sewer and Water Rate Fee Schedule.
  Mover:     Trustee Jezycki
  Seconder:  Trustee Homan
  YEAS (5):  Trustee Noble, Trustee Tulloch, Trustee Homan, Trustee Jezycki, Trustee Tonking
  NAYS (0):  —
  Outcome:   PASSED
  Timestamp: — (none on this page)

Correct? [ ] yes  [x] no — what's wrong: Timestamp missed — page has "Media Timestamp 00:39:47". Vote fields correct. SEE MAJOR FINDING BELOW re: the QUESTION: block on this page.

### 11 of 25
Document: 2025-05-30 Special Meeting of the IVGID Board of Trustees (file 1433, page 15)
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1433,plainText=false)

Parser says:
  Motion:    to open the Public Hearing for the Incline Village General Improvement District Fiscal Year 2025/2026 Facility...
  Mover:     Trustee Homan
  Seconder:  Trustee Noble
  YEAS (4):  Trustee Noble, Trustee Homan, Trustee Jezycki, Trustee Tonking
  NAYS (0):  —
  Outcome:   PASSED
  Timestamp: 02:31:58; 01:56:09

Correct? [x] yes  [ ] no — what's wrong: Timestamps correctly found (parenthesised format). NOTE: document watermarked Draft.

### 12 of 25
Document: 2025-06-09 Regular Meeting of the IVGID Audit Committee (file 1527, page 5)
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1527,plainText=false)

Parser says:
  Motion:    to Appoint Trustee Mick Homan as Vice-Chair of the Audit Committee for the 2025 term.
  Mover:     Trustee Tonking
  Seconder:  At-Large Member Kelly
  YEAS (5):  Trustee Homan, Trustee Tonking, At-Large Member Kelly, At-Large Member Lighthart, Audit Committee Chair Brandle
  NAYS (0):  —
  Outcome:   PASSED
  Timestamp: 00:20:00; 00:22:19 - 01:05:25

Correct? [x] yes  [ ] no — what's wrong: ________________

### 13 of 25
Document: 2025-06-11 Regular Meeting of the Board of Trustees (file 1465, page 13)
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1465,plainText=false)

Parser says:
  Motion:    to Approve the employee program for beach access pending a final vote. Following correspondence, and receiving...
  Mover:     Trustee Noble
  Seconder:  Trustee Homan
  YEAS (4):  Trustee Noble, Trustee Homan, Trustee Jezycki, Trustee Tonking
  NAYS (1):  Trustee Tulloch
  Outcome:   PASSED
  Timestamp: — (none on this page)

Correct? [x] yes  [ ] no — what's wrong: No media timestamp on this page — "none" is correct.

### 14 of 25
Document: 2025-06-26 Regular Meeting of the Board of Trustees (file 1489, page 11)
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1489,plainText=false)

Parser says:
  Motion:    Approve the following consent matters, Item G.1. SUBJECT: Approval of the IVGID Board of Trustees Meeting Minu...
  Mover:     Trustee Noble
  Seconder:  Trustee Homan
  YEAS (5):  Trustee Noble, Trustee Tulloch, Trustee Homan, Trustee Jezycki, Trustee Tonking
  NAYS (0):  —
  Outcome:   PASSED
  Timestamp: 02:28:04 - 02:30:00; 02:30:12

Correct? [x] yes  [ ] no — what's wrong: ________________

### 15 of 25
Document: 2025-06-26 Audit Committee Meeting (file 1528, page 6)
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1528,plainText=false)

Parser says:
  Motion:    That the Audit Committee Provide a Recommendation to the Board of Trustees to Accept a Letter of Engagement fr...
  Mover:     Trustee Tonking
  Seconder:  Committee Member Kelly
  YEAS (4):  Trustee Homan, Trustee Tonking, Committee Member Kelly, Committee Member Lighthart
  NAYS (0):  —
  Outcome:   PASSED
  Timestamp: — (none on this page)

Correct? [x] yes  [ ] no — what's wrong: No media timestamp on this page — "none" is correct.

### 16 of 25
Document: 2025-09-17 Meeting of the IVGID Board of Trustees (file 1540, page 16)
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1540,plainText=false)

Parser says:
  Motion:    to Approve and Authorize the General Manager to Sign and Execute an Agreement with the Incline Ice Foundation ...
  Mover:     Trustee Homan
  Seconder:  Trustee Jezycki
  YEAS (4):  Trustee Noble, Trustee Homan, Trustee Jezycki, Trustee Tonking
  NAYS (1):  Trustee Tulloch
  Outcome:   UNKNOWN — bare 'MOTION' terminator, outcome word missing in minutes (flagged truncated_outcome)
  Timestamp: 02:22:11 - 02:28:04
  Flags:     truncated_outcome

Correct? [x] yes  [ ] no — what's wrong: Bare MOTION terminator confirmed on page — truncated_outcome flag is correct.

### 17 of 25
Document: 2025-11-12 Meeting of the IVGID Board of Trustees (file 1559, page 18)
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1559,plainText=false)

Parser says:
  Motion:    to Approve Super Senior Rate(s) at the Recreation Center.
  Mover:     Trustee Homan
  Seconder:  Trustee Noble
  YEAS (5):  Trustee Noble, Trustee Tulloch, Trustee Homan, Trustee Vice Chair Jezycki, Trustee Chair Tonking
  NAYS (0):  —
  Outcome:   PASSED
  Timestamp: 02:04:50 - 02:12:57; 02:12:58 - 02:20:55

Correct? [x] yes  [ ] no — what's wrong: ________________

### 18 of 25
Document: 2026-01-28 Board of Trustees Meeting (file 2636, page 4)
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=2636,plainText=false)

Parser says:
  Motion:    to Approve the IVGID Board of Trustees Meeting Minutes for January 14, 2026.
  Mover:     Trustee Noble
  Seconder:  Trustee Homan
  YEAS (3):  Trustee Chair Tonking, Trustee Jezycki, Trustee Homan
  NAYS (0):  —
  Outcome:   PASSED
  Timestamp: 00:23:51 - 00:38:20; 00:38:23 - 00:38:55

Correct? [x] yes  [ ] no — what's wrong: Source oddity, not a parser error: Trustee Noble moved but is not listed in YEAS. Parser transcribed the minutes faithfully.

### 19 of 25
Document: 2026-01-28 Audit Committee Meeting (file 2670, page 1)
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=2670,plainText=false)

Parser says:
  Motion:    to Approve and Follow the Agenda as Submitted/Posted.
  Mover:     Audit Committee Chair Brandle
  Seconder:  — (no second recorded)
  YEAS (3):  Audit Committee Chair Brandle, Trustee Homan, At-Large Audit Committee Member Lighthart
  NAYS (0):  —
  Outcome:   UNKNOWN — bare 'MOTION' terminator, outcome word missing in minutes (flagged truncated_outcome)
  Timestamp: — (none on this page)
  Flags:     truncated_outcome

Correct? [x] yes  [ ] no — what's wrong: No-seconder correct; wrapped name "At-Large Audit Committee Member Lighthart" reassembled correctly; bare MOTION confirmed.

### 20 of 25
Document: 2026-02-25 Board of Trustees Meeting (file 2649, page 7)
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=2649,plainText=false)

Parser says:
  Motion:    Approve Consent Calendar Items G.1., G.2., and G.3., as submitted. .
  Mover:     Trustee Noble
  Seconder:  Trustee Jezycki
  YEAS (5):  Trustee Chair Tonking, Trustee Jezycki, Trustee Noble, Trustee Homan, Trustee Tulloch
  NAYS (0):  —
  Outcome:   PASSED
  Timestamp: 01:20:18 - 01:21:06

Correct? [ ] yes  [x] no (minor text artifact) — what's wrong: Motion text ends " ." — stray space and duplicated period. All other fields correct.

### 21 of 25
Document: 2026-03-11 Board of Trustees Meeting (file 2665, page 14)
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=2665,plainText=false)

Parser says:
  Motion:    to Approve the proposed increase to Beach Kayak and Paddleboard Storage Rack Rental as presented through Decem...
  Mover:     Trustee Noble
  Seconder:  Trustee Homan
  YEAS (4):  Trustee Chair Tonking, Trustee Jezycki, Trustee Noble, Trustee Homan
  NAYS (1):  Trustee Tulloch
  Outcome:   PASSED
  Timestamp: — (none on this page)

Correct? [x] yes  [ ] no — what's wrong: No media timestamp on this page — "none" is correct.

### 22 of 25
Document: 2026-03-31 Audit Committee Meeting (file 2721, page 12)
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=2721,plainText=false)

Parser says:
  Motion:    to Approve the Audit Committee Meeting Minutes January 28, 2026.
  Mover:     Trustee Homan
  Seconder:  At-Large Audit Committee Member Lighthart
  YEAS (5):  Audit Committee Chair Brandle, Trustee Chair Tonking, Trustee Homan, At- Large Audit Committee Member Kelly, At-Large Audit Committee Member Lighthart
  NAYS (0):  —
  Outcome:   PASSED
  Timestamp: 01:23:28 - 01:23:52

Correct? [ ] yes  [x] no (minor text artifact) — what's wrong: YEAS name reads "At- Large Audit Committee Member Kelly" — hyphenation artifact from a line break; source reads "At-Large". All other fields correct.

### 23 of 25
Document: 2026-04-28 Audit Committee Meeting (file 2806, page 5)
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=2806,plainText=false)

Parser says:
  Motion:    to Approve the Annual Audit Committee Assessment Report as required by Board Policy 15.1.0, section 2.9. to th...
  Mover:     Trustee Chair Tonking
  Seconder:  At-Large Audit Committee Member Kelly
  YEAS (4):  Trustee Chair Tonking, Trustee Homan, At-Large Audit Committee Member Kelly, At-Large Audit Committee Member Lighthart
  NAYS (0):  —
  Outcome:   PASSED
  Timestamp: 00:25:22 - 00:29:28

Correct? [x] yes  [ ] no — what's wrong: ________________

### 24 of 25
Document: 2026-05-13 Board of Trustees Meeting (file 2779, page 17)
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=2779,plainText=false)

Parser says:
  Motion:    to Approve the suggested revisions to Policy 15.1.0, including the removal of the word “review.”
  Mover:     Trustee Jezycki
  Seconder:  Trustee Homan
  YEAS (5):  Trustee Chair Tonking, Trustee Jezycki, Trustee Noble, Trustee Homan, Trustee Tulloch
  NAYS (0):  —
  Outcome:   PASSED
  Timestamp: 01:46:42 - 01:47:05

Correct? [x] yes  [ ] no — what's wrong: ________________

### 25 of 25
Document: 2026-05-20 Board of Trustees Meeting (file 2783, page 2)
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=2783,plainText=false)

Parser says:
  Motion:    to Approve and Authorize the Board Chair and Board Secretary to Sign and Execute an Agreement between Incline ...
  Mover:     Trustee Homan
  Seconder:  Trustee Jezycki
  YEAS (4):  Trustee Chair Tonking, Trustee Jezycki, Trustee Homan, Trustee Tulloch
  NAYS (0):  —
  Outcome:   PASSED
  Timestamp: 00:16:46 - 00:18:18; 00:18:20 - 01:13:00

Correct? [x] yes  [ ] no — what's wrong: ________________


---

# VERIFICATION RESULT

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
- **9 entries (2-10)** — media timestamp missed
- **2 entries (20, 22)** — trivial motion-text / name artifacts

## Defect 1 — media timestamps missed (9 entries)

The parser only recognises the **parenthesised** form. Seven variants exist:

| Variant | Recognised |
|---|---|
| `Media Timestamp (00:12:15 - 00:31:03)` | yes |
| `Media Timestamp (00:16:31)` | yes |
| `Media Timestamp 02:00:34` | **no** |
| `Timestamp Media 00:18:58` | **no** |
| `MEDIA TIMESTAMP 00:43:15` | **no** |
| `Time Stamp 00:13:59` | **no** |
| `Media Timestamp - 02:45:36` | **no** |

**Critical scoping finding: every failure is dated February-May 2025.** IVGID standardised on
the parenthesised form around June 2025. All 15 sampled entries from June 2025 onward
have correct timestamps. The live pipeline is unaffected; only the early-2025 backfill window is.

Media timestamps are the alignment key for Layer 2 (audio). This defect would have broken
the audio layer silently — every affected motion parsed clean with zero flags and counted
toward the 98.4% coverage figure.

## Defect 2 — motion text debris (entries 7, 8, 9, 20)

Where the clerk fuses the label and attribution on one line
(`MOTION: Approve; Moved By Trustee Homan: to ...`), stripping the attribution leaves debris:
- Entry 7: attribution left in the text entirely
- Entry 8: `Approve; : to Approve ...` — orphaned prefix and colon
- Entry 9: `: to Approve to reset ...` — stranded leading colon
- Entry 20: trailing `" ."`

Vote data unaffected; this is published-text quality.

## Defect 3 — hyphenation artifact (entry 22)

`At- Large Audit Committee Member Kelly` — a line-break hyphenation not rejoined.
Affects a name field, so worth fixing properly.

## MAJOR FINDING — recall failure (file 1428, page 8)

A complete roll-call vote is almost certainly invisible to the parser because the clerk
labelled it `QUESTION:` rather than `MOTION:`:

```
QUESTION: All in favor of Removing Item H.1. ... please vote by saying "Yea",
all those opposed say "Nay."
YEAS: Trustee Tulloch                                              1
NAYS: Trustee Noble, Trustee Homan, Trustee Jezycki, Chair Tonking 4
MOTION FAILED ITEM H.1. WILL REMAIN ON THE AGENDA
```

A 1-4 **failed** vote to strip an item from the agenda — a contested procedural fight — would
not appear in the record at all. This is a recall failure, not a formatting error, and no
coverage metric can detect it because the parser never sees the block.

Two further details in that block: the outcome line carries trailing text
(`MOTION FAILED ITEM H.1. WILL REMAIN ON THE AGENDA`), and the NAYS list uses
`Chair Tonking` rather than `Trustee Tonking`.

## SUSPECTED recall gap (file 1229, page 2)

`Trustee Noble made a Motion to approve the Field Rental Fee Rate Schedule` — a narrative
motion form appearing inside a 2025 structured-era document, alongside `MOTION:` and
`MOTION By Trustee X` in the same file. Needs checking for whether the parser sees it.

## OPEN QUESTION — draft minutes labelling

Files 1342 and 1433 are watermarked **DRAFT**. Spec §2.7 rule 2 requires pages built from
unapproved minutes to be labelled *draft minutes*. The checklist does not surface minutes
status, so this needs confirming.

## What this means for the published accuracy figure

- **Vote accuracy (movers, seconders, names, counts, outcomes): 25/25 = 100%** in this sample.
- **Full-field accuracy including media timestamps: 14/25 = 56%**, concentrated entirely in
  the February-May 2025 window.
- **Full-field accuracy for June 2025 onward: 14/16**, with the two exceptions being trivial
  text artifacts, not data errors.

These must be reported separately. Reporting only the first would overstate; reporting only
the second would understate the live-format performance the site actually depends on.
