# Hand-verification checklist — item titles shortened by the over-run fix

Seed: **20260727** (`random.Random`, sample drawn from the changed titles that
were not already force-included).

The over-run fix cuts an agenda-item title at the sentence boundary before a
media-reference clause. Three titles were verified by eye before the rule was
written; the rule was then widened mid-build to catch truncated forms of the same
clause (`… can be`, `… is available to be`, `… is available`), which no human has
checked. **Over-trimming is what this checklist is looking for**: a title that lost
real agenda text, not just the sentence pointing at the recording.

- Titles shortened: **99**
- Of those, more than 80 characters removed: **57** — all included below
- Seeded random sample from the remaining 42: **12**
- Total entries to check: **69**

For each: the removed text should be a complete sentence pointing at the meeting
recording, and nothing else. Tick only after comparing against the page.

## A. Every title where more than 80 characters were removed

The largest cuts, where over-trimming would show first.

---

### [ ] 1 of 69 — 2026-04-29 item H.11 (228 characters removed)

File 2778, page 19 · meeting `ivgid-2026-04-29-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=2778,plainText=false)

**Before:**
```
Approve and authorize the Board Chair and Board Secretary to Sign and Execute a Construction Manager At Risk (CMAR) Agreement between Incline Village General Improvement District and Advanced Companies, Inc. for the Championship Course Cart Path Reconstruction GMP1 Project; FY2025/26 Community Services; Championship Golf; CIP #3141LI1202; in the Amount of $2,230,662.28; Discussion and possible Action. (Requesting Staff Member: Director of Public Works Kate Nelson) Item H.10. Formerly Item H.11. Discussion and approval of a CMAR construction agreement between Incline Village General Improvement District and Advanced Companies, Inc for Champion Golf Cart Path Reconstruction GMP 1 Project is available to be viewed/heard
```
**After:**
```
Approve and authorize the Board Chair and Board Secretary to Sign and Execute a Construction Manager At Risk (CMAR) Agreement between Incline Village General Improvement District and Advanced Companies, Inc. for the Championship Course Cart Path Reconstruction GMP1 Project; FY2025/26 Community Services; Championship Golf; CIP #3141LI1202; in the Amount of $2,230,662.28; Discussion and possible Action. (Requesting Staff Member: Director of Public Works Kate Nelson) Item H.10. Formerly Item H.11
```
**The rule removed:**
```
. Discussion and approval of a CMAR construction agreement between Incline Village General Improvement District and Advanced Companies, Inc for Champion Golf Cart Path Reconstruction GMP 1 Project is available to be viewed/heard
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 2 of 69 — 2026-03-11 item H.1 (206 characters removed)

File 2665, page 11 · meeting `ivgid-2026-03-11-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=2665,plainText=false)

**Before:**
```
Discuss and Possibly Approve a Community Services Budget Transfer to Increase Capital Funds Available for Construction of the Incline Bike Park - Phase II to Authorize a Change Order to Pave the Existing and New Pump Tracks in the Amount of $112,000; IVGID Portion of $56,000, Private Donor Portion of $56,000; FY 2025/26 Capital Improvement Project; Fund: Community Services; Division: Parks; Project #4378LI2601. Discussion and Possible Action. (Requesting Staff Member: Director of Public Works Kate Nelson). - pages 217 - 119 Full discussion related to the request for Community Services budget transfer to increase capital funds available for construction of the Incline Bike Park - Phase II, is available to be
```
**After:**
```
Discuss and Possibly Approve a Community Services Budget Transfer to Increase Capital Funds Available for Construction of the Incline Bike Park - Phase II to Authorize a Change Order to Pave the Existing and New Pump Tracks in the Amount of $112,000; IVGID Portion of $56,000, Private Donor Portion of $56,000; FY 2025/26 Capital Improvement Project; Fund: Community Services; Division: Parks; Project #4378LI2601. Discussion and Possible Action. (Requesting Staff Member: Director of Public Works Kate Nelson)
```
**The rule removed:**
```
. - pages 217 - 119 Full discussion related to the request for Community Services budget transfer to increase capital funds available for construction of the Incline Bike Park - Phase II, is available to be
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 3 of 69 — 2026-04-29 item H.7 (188 characters removed)

File 2778, page 15 · meeting `ivgid-2026-04-29-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=2778,plainText=false)

**Before:**
```
Review, Discuss and Accept the Five-Year Capital Plan. (Requesting Staff Members: District Project Manager Bree Waters and Director of Finance Noemi Barter) Following a 5-minute break, the Board reconvened to consider Item H.6, previously Item H.7. The full discussion on Item H.6, a review to accept the 5-year capital plan, is available to be
```
**After:**
```
Review, Discuss and Accept the Five-Year Capital Plan. (Requesting Staff Members: District Project Manager Bree Waters and Director of Finance Noemi Barter)
```
**The rule removed:**
```
Following a 5-minute break, the Board reconvened to consider Item H.6, previously Item H.7. The full discussion on Item H.6, a review to accept the 5-year capital plan, is available to be
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 4 of 69 — 2025-12-10 item H.4 (186 characters removed)

File 1570, page 18 · meeting `ivgid-2025-12-10-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1570,plainText=false)

**Before:**
```
Approve and Authorize the District General Manager to Sign and Execute an Agreement between Incline Village General Improvement District and West Shore Technologies Inc, (dba, Paddles and Peaks) for the renting of the District's Pickleball Courts. (Requesting Staff Member: Director of Community Services Mike Bandelin) Full discussion and approval of the Agreement between IVGID and West Shore Technologies for bulk rental of the Districts Pickleball Courts for the 2026 pickleball season is available to
```
**After:**
```
Approve and Authorize the District General Manager to Sign and Execute an Agreement between Incline Village General Improvement District and West Shore Technologies Inc, (dba, Paddles and Peaks) for the renting of the District's Pickleball Courts. (Requesting Staff Member: Director of Community Services Mike Bandelin)
```
**The rule removed:**
```
Full discussion and approval of the Agreement between IVGID and West Shore Technologies for bulk rental of the Districts Pickleball Courts for the 2026 pickleball season is available to
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 5 of 69 — 2026-04-29 item H.2 (181 characters removed)

File 2778, page 8 · meeting `ivgid-2026-04-29-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=2778,plainText=false)

**Before:**
```
Adopt a Proclamation Recognizing and Thanking Alfonso Gutierrez for his Service to the District. Item H.2. Proclamation Recognizing and Thanking Alfonzo Gutierrez for his service and dedication to Incline Village General Improvement District is available to be viewed/heard at
```
**After:**
```
Adopt a Proclamation Recognizing and Thanking Alfonso Gutierrez for his Service to the District
```
**The rule removed:**
```
. Item H.2. Proclamation Recognizing and Thanking Alfonzo Gutierrez for his service and dedication to Incline Village General Improvement District is available to be viewed/heard at
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 6 of 69 — 2026-04-29 item H.1 (179 characters removed)

File 2778, page 7 · meeting `ivgid-2026-04-29-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=2778,plainText=false)

**Before:**
```
Adopt a Proclamation Recognizing and Thanking Steven Phillips for his Service to the District. Item H.1. Proclamation Recognizing and Thanking Steven Phillips for his service and dedication to Incline Village General Improvement District is available to be viewed/heard at
```
**After:**
```
Adopt a Proclamation Recognizing and Thanking Steven Phillips for his Service to the District
```
**The rule removed:**
```
. Item H.1. Proclamation Recognizing and Thanking Steven Phillips for his service and dedication to Incline Village General Improvement District is available to be viewed/heard at
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 7 of 69 — 2026-05-13 item H.2 (175 characters removed)

File 2779, page 16 · meeting `ivgid-2026-05-13-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=2779,plainText=false)

**Before:**
```
Approve Suggested Revisions to Policy 15.1.0 - Accounting, Auditing, and Financial Reporting, Audit Committee Charter, and Formally Adopt the Revisions, as recommended by the Audit Committee. (Requesting Staff Member: District Legal Counsel David Rigdon) - pages 141 – 150 Item I.4, formerly H.2. – Policy 15.1.0 Revisions (Accounting, Auditing, and Financial Reporting – Audit Committee Charter is available to be viewed / heard
```
**After:**
```
Approve Suggested Revisions to Policy 15.1.0 - Accounting, Auditing, and Financial Reporting, Audit Committee Charter, and Formally Adopt the Revisions, as recommended by the Audit Committee. (Requesting Staff Member: District Legal Counsel David Rigdon)
```
**The rule removed:**
```
- pages 141 – 150 Item I.4, formerly H.2. – Policy 15.1.0 Revisions (Accounting, Auditing, and Financial Reporting – Audit Committee Charter is available to be viewed / heard
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 8 of 69 — 2025-11-12 item H.4 (173 characters removed)

File 1559, page 19 · meeting `ivgid-2025-11-12-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1559,plainText=false)

**Before:**
```
Review, Discuss and Possibly Approve the Agreement between Incline Village General Improvement District and Miles Construction Incorporated for Removal and Replacement of the Existing Recreation Center HVAC System FY 2025/26 Community Services: Rec Center CIP #4899BD2502; in the Amount of $3,154,402; and Authorize Staff to Execute Change Orders for Additional Work if required, of Approximately 10% of the Construction Contract Value; not to Exceed $315,440; FY 2025/26 Community Services: Rec Center CIP #4899BD2502; Discussion and possible Action. (Requesting Staff Member: Director of Public Works Kate Nelson). The Discussion and Approval of the Agreement with Miles Construction for removal and replacement of the Existing Recreation Center HVAC System is available to be viewed or
```
**After:**
```
Review, Discuss and Possibly Approve the Agreement between Incline Village General Improvement District and Miles Construction Incorporated for Removal and Replacement of the Existing Recreation Center HVAC System FY 2025/26 Community Services: Rec Center CIP #4899BD2502; in the Amount of $3,154,402; and Authorize Staff to Execute Change Orders for Additional Work if required, of Approximately 10% of the Construction Contract Value; not to Exceed $315,440; FY 2025/26 Community Services: Rec Center CIP #4899BD2502; Discussion and possible Action. (Requesting Staff Member: Director of Public Works Kate Nelson)
```
**The rule removed:**
```
. The Discussion and Approval of the Agreement with Miles Construction for removal and replacement of the Existing Recreation Center HVAC System is available to be viewed or
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 9 of 69 — 2025-12-10 item H.2 (173 characters removed)

File 1570, page 17 · meeting `ivgid-2025-12-10-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1570,plainText=false)

**Before:**
```
Approve and Authorize the Board Chair and Board Secretary to Sign and Execute an Agreement between Incline Village General Improvement District and American Ramp Company for Construction of the Incline Bike Park - Phase II in the Amount of $297,000; and Authorize Staff to Execute Change Orders for Additional Work if Required, of Approximately 10% of the Construction Contract Value; not to Exceed $29,700; Project funding via combination of private donor funds and IVGID Capital Funds; FY 2025/26 Capital Improvement Project; Fund: Community Services; Division: Parks; Project #4378LI2601. Discussion and Possible Action. (Requesting Staff Member: Director of Public Works Kate Nelson). Full discussion and approval of the Construction Agreement between IVGID and American Ramp Company for the Incline Bike Park Phase II Project FY 2025/26 is available to be
```
**After:**
```
Approve and Authorize the Board Chair and Board Secretary to Sign and Execute an Agreement between Incline Village General Improvement District and American Ramp Company for Construction of the Incline Bike Park - Phase II in the Amount of $297,000; and Authorize Staff to Execute Change Orders for Additional Work if Required, of Approximately 10% of the Construction Contract Value; not to Exceed $29,700; Project funding via combination of private donor funds and IVGID Capital Funds; FY 2025/26 Capital Improvement Project; Fund: Community Services; Division: Parks; Project #4378LI2601. Discussion and Possible Action. (Requesting Staff Member: Director of Public Works Kate Nelson)
```
**The rule removed:**
```
. Full discussion and approval of the Construction Agreement between IVGID and American Ramp Company for the Incline Bike Park Phase II Project FY 2025/26 is available to be
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 10 of 69 — 2026-01-28 item G.1 (170 characters removed)

File 2636, page 4 · meeting `ivgid-2026-01-28-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=2636,plainText=false)

**Before:**
```
Approval of the IVGID Board of Trustees Meeting Minutes for January 14, 2026. (Requesting Staff Member: District Clerk Heidi White) - pages 3 - 18 Discussion on Consent Calendar Item G.1. Approval of the IVGID Board of Trustees Meeting Minutes for January 14, 2026, is available to be viewed/ heard at
```
**After:**
```
Approval of the IVGID Board of Trustees Meeting Minutes for January 14, 2026. (Requesting Staff Member: District Clerk Heidi White)
```
**The rule removed:**
```
- pages 3 - 18 Discussion on Consent Calendar Item G.1. Approval of the IVGID Board of Trustees Meeting Minutes for January 14, 2026, is available to be viewed/ heard at
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 11 of 69 — 2025-12-10 item H.3 (168 characters removed)

File 1570, page 17 · meeting `ivgid-2025-12-10-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1570,plainText=false)

**Before:**
```
Approve and Authorize the District General Manager to Sign and Execute an Agreement with the Incline Tahoe Foundation for Improvements at the Disc Golf Course. (Requesting Board Member: Trustee Dave Noble) Full discussion and approval of the Agreement between IVGID and Incline Tahoe Foundation for Improvements at the Disc Golf Course is available to be viewed or heard at
```
**After:**
```
Approve and Authorize the District General Manager to Sign and Execute an Agreement with the Incline Tahoe Foundation for Improvements at the Disc Golf Course. (Requesting Board Member: Trustee Dave Noble)
```
**The rule removed:**
```
Full discussion and approval of the Agreement between IVGID and Incline Tahoe Foundation for Improvements at the Disc Golf Course is available to be viewed or heard at
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 12 of 69 — 2026-05-13 item I.2 (164 characters removed)

File 2779, page 14 · meeting `ivgid-2026-05-13-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=2779,plainText=false)

**Before:**
```
Review, Discuss and Approve the District General Manager's Annual Performance Review Template. (Requesting Staff Member: Director of Human Resources Eric M ilavsky) - pages 212 – 221 Item I.2. The review and discussion related to the District General Mangers Annual Performance review template is available to be viewed/heard at
```
**After:**
```
Review, Discuss and Approve the District General Manager's Annual Performance Review Template. (Requesting Staff Member: Director of Human Resources Eric M ilavsky)
```
**The rule removed:**
```
- pages 212 – 221 Item I.2. The review and discussion related to the District General Mangers Annual Performance review template is available to be viewed/heard at
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 13 of 69 — 2025-03-19 item E.1 (163 characters removed)

File 1261, page 3 · meeting `ivgid-2025-03-19-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1261,plainText=false)

**Before:**
```
Review, Discuss and Approve the Amended and Restated Cooperative Agreement with North Lake Tahoe Fire Protection District for Fire Reduction (Defensible Space) Services: FY 2025/26 Fund: Community Services; Division: Administration; GL# 30364999-7560 (50% - $100,000): Fund: Utilities; Division; Water; GL#20002299-7560 (25% - $50,000): Fund: Utilities; Division; Sewer; GL#20002599-7560 (25% - $50,000), in an Amount Not to Exceed $200,000. (Requesting Staff Member: Director of Public Works Kate Nelson) Following the introduction to Item E.1. - Chair Tonking recused herself, noting a conflict of interest. The full Board discussion regarding Item E.1. to Approve the Amended Cooperative Agreement with North Lake Tahoe Fire Protection District can be viewed/ heard at
```
**After:**
```
Review, Discuss and Approve the Amended and Restated Cooperative Agreement with North Lake Tahoe Fire Protection District for Fire Reduction (Defensible Space) Services: FY 2025/26 Fund: Community Services; Division: Administration; GL# 30364999-7560 (50% - $100,000): Fund: Utilities; Division; Water; GL#20002299-7560 (25% - $50,000): Fund: Utilities; Division; Sewer; GL#20002599-7560 (25% - $50,000), in an Amount Not to Exceed $200,000. (Requesting Staff Member: Director of Public Works Kate Nelson) Following the introduction to Item E.1. - Chair Tonking recused herself, noting a conflict of interest
```
**The rule removed:**
```
. The full Board discussion regarding Item E.1. to Approve the Amended Cooperative Agreement with North Lake Tahoe Fire Protection District can be viewed/ heard at
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 14 of 69 — 2026-03-11 item H.2 (162 characters removed)

File 2665, page 12 · meeting `ivgid-2026-03-11-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=2665,plainText=false)

**Before:**
```
Review, Discuss and possibly Approve Key Rates and Charges within the District's Community Services Division. (Requesting Staff Member: Director of Community Services Mike Bandelin) - pages 220 - 231 Full discussion and approval of the Key Rates and charges within the District's Community Services Division is available to be viewed/ heard at
```
**After:**
```
Review, Discuss and possibly Approve Key Rates and Charges within the District's Community Services Division. (Requesting Staff Member: Director of Community Services Mike Bandelin)
```
**The rule removed:**
```
- pages 220 - 231 Full discussion and approval of the Key Rates and charges within the District's Community Services Division is available to be viewed/ heard at
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 15 of 69 — 2026-04-08 item H.7 (161 characters removed)

File 2720, page 16 · meeting `ivgid-2026-04-08-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=2720,plainText=false)

**Before:**
```
Set the Date and Time for Public Hearing for the FY2026/2027 Budget and Recreation Roll for Wednesday, May 27, 2026, at 4:00 p.m. or as determined by the Board of Trustees (Requesting Staff Member: Director of Finance Noemi Barter) Item H.7 – Discussion and approval to Set a Date and Time for the Public Hearing for FY 2026–2027 Budget and Recreation Roll is available to be viewed/ heard at
```
**After:**
```
Set the Date and Time for Public Hearing for the FY2026/2027 Budget and Recreation Roll for Wednesday, May 27, 2026, at 4:00 p.m. or as determined by the Board of Trustees (Requesting Staff Member: Director of Finance Noemi Barter)
```
**The rule removed:**
```
Item H.7 – Discussion and approval to Set a Date and Time for the Public Hearing for FY 2026–2027 Budget and Recreation Roll is available to be viewed/ heard at
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 16 of 69 — 2025-11-12 item H.1 (151 characters removed)

File 1559, page 17 · meeting `ivgid-2025-11-12-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1559,plainText=false)

**Before:**
```
Approve and Authorize the District General Manager to Sign and Execute a Grant Agreement between Incline Village General Improvement District and Michael Gross Family Charitable Fund for the Installation of a Memorial Plaza at the Village Green. (Requesting Staff Member: District General Manager Robert Harrison) The Discussion and Approval of the Grant Agreement for the Installation of a Memorial Plaza at the Village Green is available to be viewed or heard at
```
**After:**
```
Approve and Authorize the District General Manager to Sign and Execute a Grant Agreement between Incline Village General Improvement District and Michael Gross Family Charitable Fund for the Installation of a Memorial Plaza at the Village Green. (Requesting Staff Member: District General Manager Robert Harrison)
```
**The rule removed:**
```
The Discussion and Approval of the Grant Agreement for the Installation of a Memorial Plaza at the Village Green is available to be viewed or heard at
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 17 of 69 — 2026-04-29 item H.10 (151 characters removed)

File 2778, page 19 · meeting `ivgid-2026-04-29-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=2778,plainText=false)

**Before:**
```
Review and Approve the Business Impact Statement Related to Proposed Amendments to the Water and Wastewater Rate Schedules in Compliance with Nevada Revised Statutes (NRS) 237.080. (Requesting Staff Member: Director of Public Works Kate Nelson) Item H.9. Formerly H.10. Discussion and approval of the Business Impact Statement related to proposed amendments to the water and wastewater Rate Schedules is available to be
```
**After:**
```
Review and Approve the Business Impact Statement Related to Proposed Amendments to the Water and Wastewater Rate Schedules in Compliance with Nevada Revised Statutes (NRS) 237.080. (Requesting Staff Member: Director of Public Works Kate Nelson) Item H.9. Formerly H.10
```
**The rule removed:**
```
. Discussion and approval of the Business Impact Statement related to proposed amendments to the water and wastewater Rate Schedules is available to be
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 18 of 69 — 2026-04-29 item H.5 (151 characters removed)

File 2778, page 15 · meeting `ivgid-2026-04-29-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=2778,plainText=false)

**Before:**
```
Review, Discuss and Possibly Approve the addition of a District Sports Field Rental Product for Youth Non-Profit at a Rate of $30 per hour for Residents and $38 for Non-Residents. (Requesting Staff Member: Director of Community Services Mike Bandelin) The Full discussion on Item H.5. regarding the additional District Sports Field Rental Product for Youth Non-Profit is available to be viewed/heard at
```
**After:**
```
Review, Discuss and Possibly Approve the addition of a District Sports Field Rental Product for Youth Non-Profit at a Rate of $30 per hour for Residents and $38 for Non-Residents. (Requesting Staff Member: Director of Community Services Mike Bandelin)
```
**The rule removed:**
```
The Full discussion on Item H.5. regarding the additional District Sports Field Rental Product for Youth Non-Profit is available to be viewed/heard at
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 19 of 69 — 2025-08-27 item G.6 (148 characters removed)

File 1511, page 14 · meeting `ivgid-2025-08-27-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1511,plainText=false)

**Before:**
```
Approve and Authorize the Board Chair to Sign and Execute a Letter written by the Incline Village General Improvement District (District) to the Nevada Department of Taxation outlining the Districts' Corrective Action Plan related to the adherence to all applicable Statutes, Regulations, and Policies in the Districts' Administration of Financial Affairs, such as Expenditures, over Appropriations and Budget Augmentation as outlined in the letter dated July 28, 2025. (Requesting Staff Member: Director of Finance Jessica O'Connell) The full discussion related to Item G.6. Letter to NV Department of Taxation regarding the Districts Corrective Action Plan can be viewed/ heard at
```
**After:**
```
Approve and Authorize the Board Chair to Sign and Execute a Letter written by the Incline Village General Improvement District (District) to the Nevada Department of Taxation outlining the Districts' Corrective Action Plan related to the adherence to all applicable Statutes, Regulations, and Policies in the Districts' Administration of Financial Affairs, such as Expenditures, over Appropriations and Budget Augmentation as outlined in the letter dated July 28, 2025. (Requesting Staff Member: Director of Finance Jessica O'Connell)
```
**The rule removed:**
```
The full discussion related to Item G.6. Letter to NV Department of Taxation regarding the Districts Corrective Action Plan can be viewed/ heard at
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 20 of 69 — 2025-08-27 item G.7 (144 characters removed)

File 1511, page 14 · meeting `ivgid-2025-08-27-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1511,plainText=false)

**Before:**
```
Review, Discuss, and possibly Approve the Release of Assigned Net Position associated with Effluent Pipeline Project and Revert Funds to its Source of Origin. (Requesting Staff Member: Director of Finance Jessica O'Connell) The full discussion related to Item G.7. Release of Assigned Net Position associated with the Effluent Pipeline Project can be viewed/ heard at
```
**After:**
```
Review, Discuss, and possibly Approve the Release of Assigned Net Position associated with Effluent Pipeline Project and Revert Funds to its Source of Origin. (Requesting Staff Member: Director of Finance Jessica O'Connell)
```
**The rule removed:**
```
The full discussion related to Item G.7. Release of Assigned Net Position associated with the Effluent Pipeline Project can be viewed/ heard at
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 21 of 69 — 2025-11-12 item H.5 (144 characters removed)

File 1559, page 20 · meeting `ivgid-2025-11-12-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1559,plainText=false)

**Before:**
```
Review, discuss, and possibly approve execution of a contract with Hometown Health Providers Insurance Company, Inc. to provide employee medical insurance coverage from January 1, 2026, to June 30, 2026. (Requesting Staff Member: Director of Human Resources Eric Milavsky) The Discussion and Approval of an agreement with Hometown Health Providers for Employee Medical Insurance is available to be viewed or heard at
```
**After:**
```
Review, discuss, and possibly approve execution of a contract with Hometown Health Providers Insurance Company, Inc. to provide employee medical insurance coverage from January 1, 2026, to June 30, 2026. (Requesting Staff Member: Director of Human Resources Eric Milavsky)
```
**The rule removed:**
```
The Discussion and Approval of an agreement with Hometown Health Providers for Employee Medical Insurance is available to be viewed or heard at
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 22 of 69 — 2025-06-11 item G.6 (142 characters removed)

File 1465, page 15 · meeting `ivgid-2025-06-11-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1465,plainText=false)

**Before:**
```
Adopt Resolution No. 1919 - A Resolution to Codify the Value of a Recreation Punch Card and the Cost of an Additional Recreation Pass and/or Punch Card as determined at the May 30, 2025, Board of Trustees meeting. (Requesting Staff Member: Director of Administrative Services Susan Herron) Item G.6. Resolution No. 1919 - Codifying the Value of a Recreation Punch Card and the Cost of an additional Recreation Pass and/or Punch Card can be viewed/heard at
```
**After:**
```
Adopt Resolution No. 1919 - A Resolution to Codify the Value of a Recreation Punch Card and the Cost of an Additional Recreation Pass and/or Punch Card as determined at the May 30, 2025, Board of Trustees meeting. (Requesting Staff Member: Director of Administrative Services Susan Herron) Item G.6. Resolution No
```
**The rule removed:**
```
. 1919 - Codifying the Value of a Recreation Punch Card and the Cost of an additional Recreation Pass and/or Punch Card can be viewed/heard at
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 23 of 69 — 2026-04-29 item H.3 (141 characters removed)

File 2778, page 13 · meeting `ivgid-2026-04-29-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=2778,plainText=false)

**Before:**
```
First Reading of Ordinance 7 and Set the Time and Date of the Public Hearing for 4:00 p.m. on Wednesday, May 13, 2026. (Requesting Staff Member: Director of Administrative Services Susan Herron) Discussion on Item H.3. First Reading of Ordinance 7, and setting the Time and Date of the Public Hearing is available to be viewed/heard at
```
**After:**
```
First Reading of Ordinance 7 and Set the Time and Date of the Public Hearing for 4:00 p.m. on Wednesday, May 13, 2026. (Requesting Staff Member: Director of Administrative Services Susan Herron)
```
**The rule removed:**
```
Discussion on Item H.3. First Reading of Ordinance 7, and setting the Time and Date of the Public Hearing is available to be viewed/heard at
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 24 of 69 — 2026-04-08 item H.5 (139 characters removed)

File 2720, page 13 · meeting `ivgid-2026-04-08-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=2720,plainText=false)

**Before:**
```
Review, Discuss and Approve the Draft Audited Financial Statements for Fiscal Year Ending June 30, 2025, as presented by Clifton Larson Allen. (Requesting Staff Member: Director of Finance Noemi Barter) Item H.5 – Discussion, and Approval of Draft Audited Financial Statements for FY Ending June 30, 2025, is available to be viewed/ heard at
```
**After:**
```
Review, Discuss and Approve the Draft Audited Financial Statements for Fiscal Year Ending June 30, 2025, as presented by Clifton Larson Allen. (Requesting Staff Member: Director of Finance Noemi Barter)
```
**The rule removed:**
```
Item H.5 – Discussion, and Approval of Draft Audited Financial Statements for FY Ending June 30, 2025, is available to be viewed/ heard at
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 25 of 69 — 2026-05-13 item H.4 (139 characters removed)

File 2779, page 17 · meeting `ivgid-2026-05-13-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=2779,plainText=false)

**Before:**
```
Adopt the Final Legislative Agenda for the 2027 Fiscal Year. (Requesting Staff Member: District General M anager Robert Harrison) - pages 169 – 172 Agenda Item I.5 – formerly Item H.4. Adoption of Final Legislative Agenda for FY 2027 is available to be viewed/heard at
```
**After:**
```
Adopt the Final Legislative Agenda for the 2027 Fiscal Year. (Requesting Staff Member: District General M anager Robert Harrison)
```
**The rule removed:**
```
- pages 169 – 172 Agenda Item I.5 – formerly Item H.4. Adoption of Final Legislative Agenda for FY 2027 is available to be viewed/heard at
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 26 of 69 — 2025-05-30 item G.1 (138 characters removed)

File 1433, page 19 · meeting `ivgid-2025-05-30-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1433,plainText=false)

**Before:**
```
Review, discuss and possibly approve setting a fee for the purchase of an Additional Recreation Pass for 2025/2026 in accordance with Ordinance 7, paragraph 104 (Requesting Staff Member: Diamond Peak Ski Resort Manager Mike Bandelin) Full discussion on Item G.1. Approval to set a fee for the purchase of an Additional Recreation Pass for 2025/2026 can be heard/viewed at
```
**After:**
```
Review, discuss and possibly approve setting a fee for the purchase of an Additional Recreation Pass for 2025/2026 in accordance with Ordinance 7, paragraph 104 (Requesting Staff Member: Diamond Peak Ski Resort Manager Mike Bandelin)
```
**The rule removed:**
```
Full discussion on Item G.1. Approval to set a fee for the purchase of an Additional Recreation Pass for 2025/2026 can be heard/viewed at
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 27 of 69 — 2026-05-13 item I.1 (137 characters removed)

File 2779, page 13 · meeting `ivgid-2026-05-13-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=2779,plainText=false)

**Before:**
```
Review, Discuss, and make a Determination on the Public Bid Protest Submitted by Resource Development Company in Reference to the Bid Submission by Olympus and Associates, Inc. for the IVGID Public Works Steel Reservoir R6C-1 Tank Recoating Project Bid Results. Fund: Utilities: Water; CIP #2221WS2601 (Requesting Staff Member: Director of Public Works Kate Nelson) - pages 173 - 211 Item I.1. Review and discussion related to the public Bid Protest and determination is available to be viewed/heard at
```
**After:**
```
Review, Discuss, and make a Determination on the Public Bid Protest Submitted by Resource Development Company in Reference to the Bid Submission by Olympus and Associates, Inc. for the IVGID Public Works Steel Reservoir R6C-1 Tank Recoating Project Bid Results. Fund: Utilities: Water; CIP #2221WS2601 (Requesting Staff Member: Director of Public Works Kate Nelson)
```
**The rule removed:**
```
- pages 173 - 211 Item I.1. Review and discussion related to the public Bid Protest and determination is available to be viewed/heard at
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 28 of 69 — 2025-05-07 item E.3 (131 characters removed)

File 1432, page 16 · meeting `ivgid-2025-05-07-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1432,plainText=false)

**Before:**
```
Budget Workshop Presentation - Fiscal Year 2025-26 - Review, Discuss and possibly Adopt proposed Changes to Policy 7.1.0 - Budgeting and Fiscal Management, Appropriate Level of Reserves, Effective Fiscal Year Ending June 30, 2022; Policy 18.1.0 - Budgeting and Fiscal Management, Adoption of Central Service Cost Allocation Plan, Effective Fiscal Year Ending June 30, 2022; Policy 21.1.0 - Purchasing Policy for Goods and Services, Effective February 14, 2024; and Policy 21.2.0 - Purchasing Policy for Public Works Contracts - Effective February 14, 2024 (Requesting Staff M ember: Director of Finance Jessica O'Connell) Full presentation and discussion on Item E.3. Budget Workshop Policy Review and Proposed changes to Policy 7.1.0 and 18.1.0 can be
```
**After:**
```
Budget Workshop Presentation - Fiscal Year 2025-26 - Review, Discuss and possibly Adopt proposed Changes to Policy 7.1.0 - Budgeting and Fiscal Management, Appropriate Level of Reserves, Effective Fiscal Year Ending June 30, 2022; Policy 18.1.0 - Budgeting and Fiscal Management, Adoption of Central Service Cost Allocation Plan, Effective Fiscal Year Ending June 30, 2022; Policy 21.1.0 - Purchasing Policy for Goods and Services, Effective February 14, 2024; and Policy 21.2.0 - Purchasing Policy for Public Works Contracts - Effective February 14, 2024 (Requesting Staff M ember: Director of Finance Jessica O'Connell)
```
**The rule removed:**
```
Full presentation and discussion on Item E.3. Budget Workshop Policy Review and Proposed changes to Policy 7.1.0 and 18.1.0 can be
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 29 of 69 — 2026-05-13 item I.3 (130 characters removed)

File 2779, page 15 · meeting `ivgid-2026-05-13-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=2779,plainText=false)

**Before:**
```
Adopt Resolution No. 1925 - A Resolution Delegating Litigation Decision Authority to the Board Chair and District General Manager. (Requesting Staff Member: District Legal C ounsel David Rigdon) - pages 222 – 225 Item I.3. Discussion related to the Adoption of Resolution No. 1925 delegating litigation decision authority to the Board Chair and District General Manager is available to be viewed/heard at
```
**After:**
```
Adopt Resolution No. 1925 - A Resolution Delegating Litigation Decision Authority to the Board Chair and District General Manager. (Requesting Staff Member: District Legal C ounsel David Rigdon) - pages 222 – 225 Item I.3. Discussion related to the Adoption of Resolution No
```
**The rule removed:**
```
. 1925 delegating litigation decision authority to the Board Chair and District General Manager is available to be viewed/heard at
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 30 of 69 — 2026-04-08 item H.3 (127 characters removed)

File 2720, page 10 · meeting `ivgid-2026-04-08-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=2720,plainText=false)

**Before:**
```
Contract Extension of Six Months via Memorandum of Understanding with Waste Management for Solid Waste Services, Fund: Utilities; Division: Solid Waste (Requesting Staff Member: Director of Public Works Kate Nelson) Item H.3 – Contract Extension (Six Months) with Waste Management for Solid Waste Services via Memorandum of Understanding, Discussion is available to be viewed/ heard at
```
**After:**
```
Contract Extension of Six Months via Memorandum of Understanding with Waste Management for Solid Waste Services, Fund: Utilities; Division: Solid Waste (Requesting Staff Member: Director of Public Works Kate Nelson) Item H.3 – Contract Extension (Six Months)
```
**The rule removed:**
```
with Waste Management for Solid Waste Services via Memorandum of Understanding, Discussion is available to be viewed/ heard at
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 31 of 69 — 2026-03-25 item H.3 (125 characters removed)

File 2718, page 13 · meeting `ivgid-2026-03-25-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=2718,plainText=false)

**Before:**
```
Review, Discuss and Possibly Adopt Resolution Number 1922: A Resolution regarding Commercial Watercraft Launching, A Pilot Program for the 2026 Season (Requesting Staff Members: Director of Administrative Services Susan Herron and Recreation Supervisor Adia R.Van Peborgh) Discussion and Adoption of Resolution No. 1922 – A Resolution regarding Commercial Watercraft Launching, a Pilot Program for 2026 is available to be viewed/ heard at
```
**After:**
```
Review, Discuss and Possibly Adopt Resolution Number 1922: A Resolution regarding Commercial Watercraft Launching, A Pilot Program for the 2026 Season (Requesting Staff Members: Director of Administrative Services Susan Herron and Recreation Supervisor Adia R.Van Peborgh) Discussion and Adoption of Resolution No
```
**The rule removed:**
```
. 1922 – A Resolution regarding Commercial Watercraft Launching, a Pilot Program for 2026 is available to be viewed/ heard at
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 32 of 69 — 2025-08-27 item G.8 (123 characters removed)

File 1511, page 15 · meeting `ivgid-2025-08-27-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1511,plainText=false)

**Before:**
```
Review, Discuss and Conduct Incline Village General Improvement District’s General Manager, Robert W. Harrison, Six-Month Performance Evaluation; Direct Staff to work with Board to Establish FY 2026 Goals (Requesting Board Member: Chair Michaela Tonking) The full discussion related to Item G.8. The District General Manager's 6-month Performance review can be viewed/ heard at
```
**After:**
```
Review, Discuss and Conduct Incline Village General Improvement District’s General Manager, Robert W. Harrison, Six-Month Performance Evaluation; Direct Staff to work with Board to Establish FY 2026 Goals (Requesting Board Member: Chair Michaela Tonking)
```
**The rule removed:**
```
The full discussion related to Item G.8. The District General Manager's 6-month Performance review can be viewed/ heard at
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 33 of 69 — 2025-03-19 item E.3 (122 characters removed)

File 1261, page 6 · meeting `ivgid-2025-03-19-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1261,plainText=false)

**Before:**
```
Review, and possibly Approve the Beach (Ski, Incline and Burnt Cedar) Rates for the 2025 Season: Discussion and possible Action. (Requesting Staff Member: Director of Parks and Recreation Karen Crocker) The full Board discussion regarding Item E.3. to Approve District Beach Rates for the 2025 Season can be viewed/ heard at
```
**After:**
```
Review, and possibly Approve the Beach (Ski, Incline and Burnt Cedar) Rates for the 2025 Season: Discussion and possible Action. (Requesting Staff Member: Director of Parks and Recreation Karen Crocker)
```
**The rule removed:**
```
The full Board discussion regarding Item E.3. to Approve District Beach Rates for the 2025 Season can be viewed/ heard at
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 34 of 69 — 2025-08-27 item G.5 (119 characters removed)

File 1511, page 13 · meeting `ivgid-2025-08-27-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1511,plainText=false)

**Before:**
```
Approve and Authorize Additional Funding for Armand Agra – Sierra Meats in the Amount of $30,000, increasing the Blanket Purchase Order related to Additional Costs and bringing the Total Purchase Order to $255,000. (Requesting Staff Member: Director of Finance Jessica O'Connell) The full discussion related to Item G.5. Additional funding for Armand Agra - dba Sierra Meats can be viewed/ heard at
```
**After:**
```
Approve and Authorize Additional Funding for Armand Agra – Sierra Meats in the Amount of $30,000, increasing the Blanket Purchase Order related to Additional Costs and bringing the Total Purchase Order to $255,000. (Requesting Staff Member: Director of Finance Jessica O'Connell)
```
**The rule removed:**
```
The full discussion related to Item G.5. Additional funding for Armand Agra - dba Sierra Meats can be viewed/ heard at
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 35 of 69 — 2025-06-11 item G.1 (110 characters removed)

File 1465, page 9 · meeting `ivgid-2025-06-11-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1465,plainText=false)

**Before:**
```
Review and Acknowledge Receipt of the Incline Village General Improvement District’s Draft Audited Financial Statements, Auditor's report, and report on internal control for the fiscal year ended June 30, 2024, as presented; and, authorize the Director of Finance to proceed with Distribution of the District’s Annual Comprehensive Financial Report (ACFR), once produced, for public record, as required by law. (Requesting Staff Member: Director of Finance Jessica O'Connell, and Jennifer Farr with Davis Farr LLP - Certified Public Accountants) Item G.1. The Districts Draft Audited Financial Statements presentation and discussion can be viewed/heard at
```
**After:**
```
Review and Acknowledge Receipt of the Incline Village General Improvement District’s Draft Audited Financial Statements, Auditor's report, and report on internal control for the fiscal year ended June 30, 2024, as presented; and, authorize the Director of Finance to proceed with Distribution of the District’s Annual Comprehensive Financial Report (ACFR), once produced, for public record, as required by law. (Requesting Staff Member: Director of Finance Jessica O'Connell, and Jennifer Farr with Davis Farr LLP - Certified Public Accountants)
```
**The rule removed:**
```
Item G.1. The Districts Draft Audited Financial Statements presentation and discussion can be viewed/heard at
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 36 of 69 — 2025-05-30 item F.1 (106 characters removed)

File 1433, page 18 · meeting `ivgid-2025-05-30-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1433,plainText=false)

**Before:**
```
Review, Discuss and Possibly Adopt Resolution No. 1917 - A Resolution Approving the Report for Collection of Recreation Standby and Service Charges (Also Known as the Recreation Facility Fee and Beach Facility Fee), for Fiscal Year 2025-2026 (Requesting Staff Member: Director of F inance Jessica O'Connell) Full discussion on Item F.1. Adopt Resolution No. 1917 - Approving the Report for Collection of Recreation Standby and Service Charges can be heard/viewed
```
**After:**
```
Review, Discuss and Possibly Adopt Resolution No. 1917 - A Resolution Approving the Report for Collection of Recreation Standby and Service Charges (Also Known as the Recreation Facility Fee and Beach Facility Fee), for Fiscal Year 2025-2026 (Requesting Staff Member: Director of F inance Jessica O'Connell) Full discussion on Item F.1. Adopt Resolution No
```
**The rule removed:**
```
. 1917 - Approving the Report for Collection of Recreation Standby and Service Charges can be heard/viewed
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 37 of 69 — 2025-03-19 item E.4 (104 characters removed)

File 1261, page 6 · meeting `ivgid-2025-03-19-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1261,plainText=false)

**Before:**
```
Review and Discuss Historical Financial results of District-Owned Golf Courses (Mountain, and Championship) and possibly Approve the Recommended Rates, Rate Structure and Course Operations for the 2025 Golf Season: Discussion, and Possible Action. (Requesting Staff Member: Senior Head Golf Professional Rob Bruce) The full Board discussion regarding Item E.4. to Approve District-owned Golf Courses (Mountain, and Championship) recommended rates, and rate structure and course operations for the 2025 Season can be viewed/ heard at
```
**After:**
```
Review and Discuss Historical Financial results of District-Owned Golf Courses (Mountain, and Championship) and possibly Approve the Recommended Rates, Rate Structure and Course Operations for the 2025 Golf Season: Discussion, and Possible Action. (Requesting Staff Member: Senior Head Golf Professional Rob Bruce) The full Board discussion regarding Item E.4. to Approve District-owned Golf Courses (Mountain, and Championship)
```
**The rule removed:**
```
recommended rates, and rate structure and course operations for the 2025 Season can be viewed/ heard at
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 38 of 69 — 2026-01-28 item H.1 (101 characters removed)

File 2636, page 5 · meeting `ivgid-2026-01-28-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=2636,plainText=false)

**Before:**
```
Review, Discuss and possibly Approve the Employee Separation Incentive Program. (Requesting Staff Member: District General Manager Robert Harrison) - pages 19 - 22 Item H.1. Discussion on the Employee Separation Incentive Program is available to be
```
**After:**
```
Review, Discuss and possibly Approve the Employee Separation Incentive Program. (Requesting Staff Member: District General Manager Robert Harrison)
```
**The rule removed:**
```
- pages 19 - 22 Item H.1. Discussion on the Employee Separation Incentive Program is available to be
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 39 of 69 — 2025-12-10 item H.8 (94 characters removed)

File 1570, page 22 · meeting `ivgid-2025-12-10-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1570,plainText=false)

**Before:**
```
Election of Board of Trustees Officers for the 2026 Term. (Requesting Staff Member: District Clerk Heidi White) The Election of the 2026 Term for the Board of Trustees Officers is available to be viewed or
```
**After:**
```
Election of Board of Trustees Officers for the 2026 Term. (Requesting Staff Member: District Clerk Heidi White)
```
**The rule removed:**
```
The Election of the 2026 Term for the Board of Trustees Officers is available to be viewed or
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 40 of 69 — 2025-04-09 item G.3 (92 characters removed)

File 1344, page 6 · meeting `ivgid-2025-04-09-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1344,plainText=false)

**Before:**
```
Set the Date and Time for the Public Hearing to Implement Amendments to the Sewer and Water rates, as well as Adjustments to the Fee Schedule, for Wednesday, May 14, 2025, at 5:00 p.m. or as Otherwise Determined by the Board of Trustees. (Requesting Staff Member: Director of Public Works Kate Nelson). Full staff report and Board discussion for Item G.2. formerly G.3. can be viewed/ heard at
```
**After:**
```
Set the Date and Time for the Public Hearing to Implement Amendments to the Sewer and Water rates, as well as Adjustments to the Fee Schedule, for Wednesday, May 14, 2025, at 5:00 p.m. or as Otherwise Determined by the Board of Trustees. (Requesting Staff Member: Director of Public Works Kate Nelson)
```
**The rule removed:**
```
. Full staff report and Board discussion for Item G.2. formerly G.3. can be viewed/ heard at
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 41 of 69 — 2025-09-17 item I.4 (92 characters removed)

File 1540, page 15 · meeting `ivgid-2025-09-17-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1540,plainText=false)

**Before:**
```
Approve and Authorize the General Manager to Sign and Execute an Agreement with the Incline Ice Foundation for the Incline Village General Improvement District to Accept a Donation of an Ice Rink Package and a Grant of $50,000+ to Support the Ice Rink Activities. (Requesting Board Member: David Noble) The full discussion related to Item I.4. Incline Ice Foundation Agreement discussion can be
```
**After:**
```
Approve and Authorize the General Manager to Sign and Execute an Agreement with the Incline Ice Foundation for the Incline Village General Improvement District to Accept a Donation of an Ice Rink Package and a Grant of $50,000+ to Support the Ice Rink Activities. (Requesting Board Member: David Noble)
```
**The rule removed:**
```
The full discussion related to Item I.4. Incline Ice Foundation Agreement discussion can be
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 42 of 69 — 2026-04-29 item H.8 (92 characters removed)

File 2778, page 17 · meeting `ivgid-2026-04-29-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=2778,plainText=false)

**Before:**
```
Review, Discuss, and Accept the Facility Fee, and Punch Card Values for Fiscal Year 2027. (Requesting Staff Member: Director of Finance Noemi Barter) Item H.8. discussion and approval of the Facility Fee and Punch Card values is available to
```
**After:**
```
Review, Discuss, and Accept the Facility Fee, and Punch Card Values for Fiscal Year 2027. (Requesting Staff Member: Director of Finance Noemi Barter)
```
**The rule removed:**
```
Item H.8. discussion and approval of the Facility Fee and Punch Card values is available to
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 43 of 69 — 2025-04-09 item G.2 (91 characters removed)

File 1344, page 5 · meeting `ivgid-2025-04-09-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1344,plainText=false)

**Before:**
```
Approve and Authorize the District General Manager to Sign and Execute Amendment 2 of the Retail Concession Agreement between Incline Village General Improvement District and Incline Spirits Inc. to Provide Services at the Restricted Access Beaches Managed by the Incline Village General Improvement District, Discussion and possible Action. (Requesting Staff Member: Director of Parks and Recreation Karen Crocker) Full staff report and Board discussion for Item G.1. formerly G.2. can be viewed/ heard at
```
**After:**
```
Approve and Authorize the District General Manager to Sign and Execute Amendment 2 of the Retail Concession Agreement between Incline Village General Improvement District and Incline Spirits Inc. to Provide Services at the Restricted Access Beaches Managed by the Incline Village General Improvement District, Discussion and possible Action. (Requesting Staff Member: Director of Parks and Recreation Karen Crocker)
```
**The rule removed:**
```
Full staff report and Board discussion for Item G.1. formerly G.2. can be viewed/ heard at
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 44 of 69 — 2025-11-12 item H.2 (91 characters removed)

File 1559, page 17 · meeting `ivgid-2025-11-12-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1559,plainText=false)

**Before:**
```
Review, Discuss and possibly Approve Super Senior Rate(s) at the Recreation Center. (Requesting Staff Member: District General Manager Robert Harrison) The Discussion and Approval of the Super Senior Rate at the Recreation Center is available
```
**After:**
```
Review, Discuss and possibly Approve Super Senior Rate(s) at the Recreation Center. (Requesting Staff Member: District General Manager Robert Harrison)
```
**The rule removed:**
```
The Discussion and Approval of the Super Senior Rate at the Recreation Center is available
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 45 of 69 — 2025-11-12 item H.3 (91 characters removed)

File 1559, page 18 · meeting `ivgid-2025-11-12-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1559,plainText=false)

**Before:**
```
Revision to Policy 18.1.0 Adoption of Central Service Cost Allocation Plan, Budgeting and Fiscal Management. (Requesting Staff Member: Director of Finance Jessica O'Connell) The Discussion and Adoption of Revised Policy 18.1.0 is available to be viewed or heard at
```
**After:**
```
Revision to Policy 18.1.0 Adoption of Central Service Cost Allocation Plan, Budgeting and Fiscal Management. (Requesting Staff Member: Director of Finance Jessica O'Connell)
```
**The rule removed:**
```
The Discussion and Adoption of Revised Policy 18.1.0 is available to be viewed or heard at
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 46 of 69 — 2025-06-11 item G.2 (90 characters removed)

File 1465, page 10 · meeting `ivgid-2025-06-11-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1465,plainText=false)

**Before:**
```
Interview of Firms who submitted Legal Counsel Services responses to the District’s Request for Proposal and authorize Staff to move forward with preparing a contract for legal counsel services for the District effective July 1, 2025. (Requesting Staff Member: Director of Administrative Services Susan Herron) Item G.2. Interviews with law firms for the Districts' Legal Counsel Service needs can be
```
**After:**
```
Interview of Firms who submitted Legal Counsel Services responses to the District’s Request for Proposal and authorize Staff to move forward with preparing a contract for legal counsel services for the District effective July 1, 2025. (Requesting Staff Member: Director of Administrative Services Susan Herron)
```
**The rule removed:**
```
Item G.2. Interviews with law firms for the Districts' Legal Counsel Service needs can be
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 47 of 69 — 2025-09-17 item I.2 (90 characters removed)

File 1540, page 14 · meeting `ivgid-2025-09-17-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1540,plainText=false)

**Before:**
```
Review, Discuss and Possibly Reaffirm and/or Amend the Prior Approval of the Added Alternates #1: Fire Pits and #2: Band Stand, for the Incline Beach House Project, CIP #3973L1302. (Requesting Staff Member: Project Manager Bree Waters) The full discussion related to Item I.2. Beach House Alternates discussion can be viewed/
```
**After:**
```
Review, Discuss and Possibly Reaffirm and/or Amend the Prior Approval of the Added Alternates #1: Fire Pits and #2: Band Stand, for the Incline Beach House Project, CIP #3973L1302. (Requesting Staff Member: Project Manager Bree Waters)
```
**The rule removed:**
```
The full discussion related to Item I.2. Beach House Alternates discussion can be viewed/
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 48 of 69 — 2025-09-17 item J.1 (90 characters removed)

File 1540, page 16 · meeting `ivgid-2025-09-17-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1540,plainText=false)

**Before:**
```
Review, discuss and possibly Add or Remove Long Range Calendar Items to Future Board of Trustee Agendas. The full discussion related to Item J.1. The Long Range Calendar can be viewed/ heard at
```
**After:**
```
Review, discuss and possibly Add or Remove Long Range Calendar Items to Future Board of Trustee Agendas
```
**The rule removed:**
```
. The full discussion related to Item J.1. The Long Range Calendar can be viewed/ heard at
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 49 of 69 — 2025-12-10 item H.7 (90 characters removed)

File 1570, page 21 · meeting `ivgid-2025-12-10-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1570,plainText=false)

**Before:**
```
Review, Discuss and possibly Approve the District General Manager's Proposed Goals. (Requesting Staff and Board Member: Director of Human Resources Eric Milavsky and Trustee Vice Chair Michelle Jezycki) Discussion and Approval of the District General Managers Goals are available to be viewed
```
**After:**
```
Review, Discuss and possibly Approve the District General Manager's Proposed Goals. (Requesting Staff and Board Member: Director of Human Resources Eric Milavsky and Trustee Vice Chair Michelle Jezycki)
```
**The rule removed:**
```
Discussion and Approval of the District General Managers Goals are available to be viewed
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 50 of 69 — 2026-03-25 item G.2 (89 characters removed)

File 2718, page 4 · meeting `ivgid-2026-03-25-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=2718,plainText=false)

**Before:**
```
Approve the Revised Paragraphs in Ordinance 7 as discussed at the January 11, 2026, Board Meeting (Paragraphs 100-103) (Requesting Staff Members: Director of Administrative Services Susan Herron, and Risk Manager Curtis Trujillo) Full discussion on revised Paragraphs in Ordinance 7 is available to be viewed/ heard at
```
**After:**
```
Approve the Revised Paragraphs in Ordinance 7 as discussed at the January 11, 2026, Board Meeting (Paragraphs 100-103) (Requesting Staff Members: Director of Administrative Services Susan Herron, and Risk Manager Curtis Trujillo)
```
**The rule removed:**
```
Full discussion on revised Paragraphs in Ordinance 7 is available to be viewed/ heard at
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 51 of 69 — 2025-03-12 item G.1 (85 characters removed)

File 1262, page 4 · meeting `ivgid-2025-03-12-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1262,plainText=false)

**Before:**
```
Review, Discuss and Appoint a Board Liaison to attend the Interviews of Candidates for the General Manager of Golf Operations Position and Provide Feedback to Staff. (Requesting Staff Member: Director of Human Resources Erin Feore) Item G.1. Board discussion regarding Board-appointed Liaison can be viewed/ heard at
```
**After:**
```
Review, Discuss and Appoint a Board Liaison to attend the Interviews of Candidates for the General Manager of Golf Operations Position and Provide Feedback to Staff. (Requesting Staff Member: Director of Human Resources Erin Feore)
```
**The rule removed:**
```
Item G.1. Board discussion regarding Board-appointed Liaison can be viewed/ heard at
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 52 of 69 — 2025-08-27 item G.1 (85 characters removed)

File 1511, page 10 · meeting `ivgid-2025-08-27-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1511,plainText=false)

**Before:**
```
Approve and Authorize staff to create a Community Services CIP Project for Phase Two (Implementation) of the Point of Sale (POS) System Project; and, Approve and authorize staff to re-budget $400,000 from the FY25/26 Community Services CIP Budget to the FY26/27 CIP Budget and include an additional $433,302 in FY26/27 for a total Community Services CIP Point of Sale System Project Budget of $833,302 in Fiscal Year 2026/2027. (Requesting Staff Members: Director of Administrative Services Susan Herron and Information Technology Manager Mike Gove) The full discussion related to Item G.1. Phase 2 of the Point-of-Sale Project can be
```
**After:**
```
Approve and Authorize staff to create a Community Services CIP Project for Phase Two (Implementation) of the Point of Sale (POS) System Project; and, Approve and authorize staff to re-budget $400,000 from the FY25/26 Community Services CIP Budget to the FY26/27 CIP Budget and include an additional $433,302 in FY26/27 for a total Community Services CIP Point of Sale System Project Budget of $833,302 in Fiscal Year 2026/2027. (Requesting Staff Members: Director of Administrative Services Susan Herron and Information Technology Manager Mike Gove)
```
**The rule removed:**
```
The full discussion related to Item G.1. Phase 2 of the Point-of-Sale Project can be
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 53 of 69 — 2025-04-09 item G.5 (84 characters removed)

File 1344, page 8 · meeting `ivgid-2025-04-09-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1344,plainText=false)

**Before:**
```
Adopt Resolution No. 1912 Codifying the transfer of the Parks Operations from Community Services to the General Fund in Fiscal Year 2023/2024 and Codifying the transfer of the Parks Operations back to Community Services from the General Fund effective July 1, 2025; Discussion and possible Action (Requesting Staff Member: Director of Administrative Services Susan Herron) Full staff and Board discussion for Item G.4. formerly G.5. can be viewed/ heard at
```
**After:**
```
Adopt Resolution No. 1912 Codifying the transfer of the Parks Operations from Community Services to the General Fund in Fiscal Year 2023/2024 and Codifying the transfer of the Parks Operations back to Community Services from the General Fund effective July 1, 2025; Discussion and possible Action (Requesting Staff Member: Director of Administrative Services Susan Herron)
```
**The rule removed:**
```
Full staff and Board discussion for Item G.4. formerly G.5. can be viewed/ heard at
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 54 of 69 — 2025-06-11 item G.4 (83 characters removed)

File 1465, page 14 · meeting `ivgid-2025-06-11-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1465,plainText=false)

**Before:**
```
Review, Discuss and Possibly Approve an Agreement with The Abbi Agency for District Media Buying Services. (Requesting Staff Member: Marketing & Communications Manager Paul Raymore) Item G.4. Abbi Agency District Media Buying Services Agreement can be viewed/heard
```
**After:**
```
Review, Discuss and Possibly Approve an Agreement with The Abbi Agency for District Media Buying Services. (Requesting Staff Member: Marketing & Communications Manager Paul Raymore)
```
**The rule removed:**
```
Item G.4. Abbi Agency District Media Buying Services Agreement can be viewed/heard
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 55 of 69 — 2025-03-12 item G.2 (82 characters removed)

File 1262, page 5 · meeting `ivgid-2025-03-12-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1262,plainText=false)

**Before:**
```
Approve and Authorize the Board Chair and Secretary to Sign an Agreement between the District and CORE West Inc. dba CORE Construction for the 100% Construction Development Contract for Incline Beach House Project - FY 2024/25 Capital Improvement Project; Fund: Community Services; Division: Beaches; Project #3973LI1302; in the amount of $755,000; Discussion and Possible Action. (Requesting Staff Member: Public Works Director Kate Nelson) Item G.2. Presentations and full Board and Staff discussions can be viewed/ heard
```
**After:**
```
Approve and Authorize the Board Chair and Secretary to Sign an Agreement between the District and CORE West Inc. dba CORE Construction for the 100% Construction Development Contract for Incline Beach House Project - FY 2024/25 Capital Improvement Project; Fund: Community Services; Division: Beaches; Project #3973LI1302; in the amount of $755,000; Discussion and Possible Action. (Requesting Staff Member: Public Works Director Kate Nelson)
```
**The rule removed:**
```
Item G.2. Presentations and full Board and Staff discussions can be viewed/ heard
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 56 of 69 — 2025-03-12 item G.3 (82 characters removed)

File 1262, page 5 · meeting `ivgid-2025-03-12-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1262,plainText=false)

**Before:**
```
Review, Discuss and Provide Direction for the Final Design-Build Construction Contract for Skate Park Enhancement Project - FY 2024/25 Capital Improvement Project Fund: General; Division: Parks: Project #4378BD2202; (Requesting Staff Member: Director of Public Works Kate Nelson) Item G.3. Presentations and full Board and Staff discussions can be viewed/ heard
```
**After:**
```
Review, Discuss and Provide Direction for the Final Design-Build Construction Contract for Skate Park Enhancement Project - FY 2024/25 Capital Improvement Project Fund: General; Division: Parks: Project #4378BD2202; (Requesting Staff Member: Director of Public Works Kate Nelson)
```
**The rule removed:**
```
Item G.3. Presentations and full Board and Staff discussions can be viewed/ heard
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 57 of 69 — 2025-08-27 item G.3 (82 characters removed)

File 1511, page 12 · meeting `ivgid-2025-08-27-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1511,plainText=false)

**Before:**
```
Approve and Authorize Additional Funding for Davis Farr in the Amount of $41,000 for additional work, bringing the Total Contract Agreement to $127,040. (Requesting Staff Member: Director of Finance Jessica O'Connell) The full discussion related to Item G.3. Additional funding for Davis Farr can be
```
**After:**
```
Approve and Authorize Additional Funding for Davis Farr in the Amount of $41,000 for additional work, bringing the Total Contract Agreement to $127,040. (Requesting Staff Member: Director of Finance Jessica O'Connell)
```
**The rule removed:**
```
The full discussion related to Item G.3. Additional funding for Davis Farr can be
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

## B. Seeded random sample of the remaining shortened titles

---

### [ ] 58 of 69 — 2025-02-26 item G.2 (61 characters removed)

File 1227, page 4 · meeting `ivgid-2025-02-26-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1227,plainText=false)

**Before:**
```
Nomination and Appointment of Audit Committee seat due to Term Expiration of Trustee Tulloch effective from February 28, 2024, Trustee Tulloch's term is due to expire February 28, 2025. (Requesting Staff Member: District Clerk Heidi White) A brief discussion of the Board of Trustees can be viewed at
```
**After:**
```
Nomination and Appointment of Audit Committee seat due to Term Expiration of Trustee Tulloch effective from February 28, 2024, Trustee Tulloch's term is due to expire February 28, 2025. (Requesting Staff Member: District Clerk Heidi White)
```
**The rule removed:**
```
A brief discussion of the Board of Trustees can be viewed at
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 59 of 69 — 2025-02-26 item G.3 (54 characters removed)

File 1227, page 5 · meeting `ivgid-2025-02-26-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1227,plainText=false)

**Before:**
```
Review, Discuss and Approve Board Recommended Goals for District General Manager through June 30, 2025. (Requesting Board Member: Trustee Michelle Jezycki, and Requesting Staff Member: Human Resource Director Erin Feore) Human Resources Director Erin Feore and Trustee Jezycki provided an overview of the recommended targeted goals and key performance indicators (KPIs) for the District General Manager for the first 6 months. She clarified that the target dates are not carved in stone; the dates are to assist GM Harrison to schedule the many ongoing goals constructively. The full Board and Staff discussion can be viewed at
```
**After:**
```
Review, Discuss and Approve Board Recommended Goals for District General Manager through June 30, 2025. (Requesting Board Member: Trustee Michelle Jezycki, and Requesting Staff Member: Human Resource Director Erin Feore) Human Resources Director Erin Feore and Trustee Jezycki provided an overview of the recommended targeted goals and key performance indicators (KPIs) for the District General Manager for the first 6 months. She clarified that the target dates are not carved in stone; the dates are to assist GM Harrison to schedule the many ongoing goals constructively
```
**The rule removed:**
```
. The full Board and Staff discussion can be viewed at
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 60 of 69 — 2025-03-05 item E.3 (70 characters removed)

File 1229, page 3 · meeting `ivgid-2025-03-05-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1229,plainText=false)

**Before:**
```
Review, Discuss and Possibly Approve the Fields Fee Rate Schedule. (Requesting Staff Member: Director Parks and Recreation Karen Crocker) Item E.3. Board and Staff discussion can be viewed in its entirety at
```
**After:**
```
Review, Discuss and Possibly Approve the Fields Fee Rate Schedule. (Requesting Staff Member: Director Parks and Recreation Karen Crocker)
```
**The rule removed:**
```
Item E.3. Board and Staff discussion can be viewed in its entirety at
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 61 of 69 — 2025-03-26 item F.1 (77 characters removed)

File 1343, page 3 · meeting `ivgid-2025-03-26-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1343,plainText=false)

**Before:**
```
Review, Discuss and Approve the Update to the Water Management Plan and the Purchase of 8.81 ac-ft of IVGID Water Rights for $140,960 by Incline Hotel LLC; for possible Action. (Requesting Staff Member: Director of Public Works Kate Nelson) The full staff report and Board discussion for Item F.1. can be viewed/heard
```
**After:**
```
Review, Discuss and Approve the Update to the Water Management Plan and the Purchase of 8.81 ac-ft of IVGID Water Rights for $140,960 by Incline Hotel LLC; for possible Action. (Requesting Staff Member: Director of Public Works Kate Nelson)
```
**The rule removed:**
```
The full staff report and Board discussion for Item F.1. can be viewed/heard
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 62 of 69 — 2025-04-30 item F.4 (23 characters removed)

File 1341, page 9 · meeting `ivgid-2025-04-30-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1341,plainText=false)

**Before:**
```
Approve and Authorize the Board Chair and Board Secretary to Sign and Execute a Professional Services Agreement between Incline Village General Improvement District and Carollo Engineers for Development of a SCADA Master Plan; FY 2024/25 Utilities: Water: GL #20002297-7510; in the Amount of $359,972; Discussion and possible Action. (Requesting Staff Member: Director of Public Works Kate Nelson) Full staff report and Board discussion for Item G.7. (Formerly Consent Calendar Item F.4.) can be viewed/heard at
```
**After:**
```
Approve and Authorize the Board Chair and Board Secretary to Sign and Execute a Professional Services Agreement between Incline Village General Improvement District and Carollo Engineers for Development of a SCADA Master Plan; FY 2024/25 Utilities: Water: GL #20002297-7510; in the Amount of $359,972; Discussion and possible Action. (Requesting Staff Member: Director of Public Works Kate Nelson) Full staff report and Board discussion for Item G.7. (Formerly Consent Calendar Item F.4.)
```
**The rule removed:**
```
can be viewed/heard at
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 63 of 69 — 2025-04-30 item G.7 (7 characters removed)

File 1341, page 10 · meeting `ivgid-2025-04-30-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1341,plainText=false)

**Before:**
```
Review, Discuss, and Possibly Approve Utility Fund Re-Allocation of $375,000 from Utility CIP Sewer Fund to the Water Resource Recovery Facility (WRRF) Roof Replacement CIP # 2599BD1105; FY2024/25; Fund Utilities; Division: Sewer, (Requesting Staff Member: Director of Public Works Kate Nelson) Full staff report and Board discussion for Item G.8. (Formerly Item G.7.) can be
```
**After:**
```
Review, Discuss, and Possibly Approve Utility Fund Re-Allocation of $375,000 from Utility CIP Sewer Fund to the Water Resource Recovery Facility (WRRF) Roof Replacement CIP # 2599BD1105; FY2024/25; Fund Utilities; Division: Sewer, (Requesting Staff Member: Director of Public Works Kate Nelson) Full staff report and Board discussion for Item G.8. (Formerly Item G.7.)
```
**The rule removed:**
```
can be
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 64 of 69 — 2025-05-14 item H.4 (29 characters removed)

File 1428, page 22 · meeting `ivgid-2025-05-14-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1428,plainText=false)

**Before:**
```
Review, Discuss and Possibly Adopt Resolution No. 1916 - a Resolution Preliminarily Approving the Report for Collection of Recreation Standby and Service Charges for Fiscal Year 2025/2026 and Confirming the Public Hearing Date for Friday, May 30, 2025, at 12: 00 p.m. (Requesting Staff Members: District General Manager Robert Harrison and Director of Administrative Services Susan Herron) Full discussion on Item H.4. To Adopt Resolution No. 1916 can be heard/viewed at
```
**After:**
```
Review, Discuss and Possibly Adopt Resolution No. 1916 - a Resolution Preliminarily Approving the Report for Collection of Recreation Standby and Service Charges for Fiscal Year 2025/2026 and Confirming the Public Hearing Date for Friday, May 30, 2025, at 12: 00 p.m. (Requesting Staff Members: District General Manager Robert Harrison and Director of Administrative Services Susan Herron) Full discussion on Item H.4. To Adopt Resolution No
```
**The rule removed:**
```
. 1916 can be heard/viewed at
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 65 of 69 — 2025-05-30 item E.1 (79 characters removed)

File 1433, page 13 · meeting `ivgid-2025-05-30-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1433,plainText=false)

**Before:**
```
Adopt the Fiscal Year 2025/2026 Incline Village General Improvement District Budgets of which there are six (6) components: (1) Operating Budget; (2) Capital Improvement Projects Budget; (3) Facility Fees (consisting of a Recreation Facility Fee and Beach Facility Fee); (4) Authorized Positions List; (5) Final Form 4404LGF; and (6) Central Services Cost Allrocation Plan (Requesting Staff Member: Director of Finance Jessica O'Connell) Full discussion on Item E.1. FY 2025-2026 District Budgets can be heard/viewed
```
**After:**
```
Adopt the Fiscal Year 2025/2026 Incline Village General Improvement District Budgets of which there are six (6) components: (1) Operating Budget; (2) Capital Improvement Projects Budget; (3) Facility Fees (consisting of a Recreation Facility Fee and Beach Facility Fee); (4) Authorized Positions List; (5) Final Form 4404LGF; and (6) Central Services Cost Allrocation Plan (Requesting Staff Member: Director of Finance Jessica O'Connell)
```
**The rule removed:**
```
Full discussion on Item E.1. FY 2025-2026 District Budgets can be heard/viewed
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 66 of 69 — 2025-06-11 item G.5 (26 characters removed)

File 1465, page 14 · meeting `ivgid-2025-06-11-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1465,plainText=false)

**Before:**
```
Review, Discuss and Approve a change to Policy Resolution 137 - Public Records (Requesting Staff Member: District General Counsel Sergio Rudin) Item G.5. Changes to Policy Procedure 137 - Resolution No. 1918 can be viewed/heard
```
**After:**
```
Review, Discuss and Approve a change to Policy Resolution 137 - Public Records (Requesting Staff Member: District General Counsel Sergio Rudin) Item G.5. Changes to Policy Procedure 137 - Resolution No
```
**The rule removed:**
```
. 1918 can be viewed/heard
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 67 of 69 — 2025-06-26 item H.1 (77 characters removed)

File 1489, page 12 · meeting `ivgid-2025-06-26-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1489,plainText=false)

**Before:**
```
Approve the Designation of an Auditing Firm, and Accept a Letter of Engagement from Clifton Larson Allen LLP, for Fiscal Year 2024/2025. (Requesting Staff Member: District General Manager Robert Harrison) Item H.3. Approve the Designation of an Auditing Firm can be viewed/heard at
```
**After:**
```
Approve the Designation of an Auditing Firm, and Accept a Letter of Engagement from Clifton Larson Allen LLP, for Fiscal Year 2024/2025. (Requesting Staff Member: District General Manager Robert Harrison)
```
**The rule removed:**
```
Item H.3. Approve the Designation of an Auditing Firm can be viewed/heard at
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 68 of 69 — 2025-07-30 item H.4 (61 characters removed)

File 1491, page 11 · meeting `ivgid-2025-07-30-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1491,plainText=false)

**Before:**
```
Review, Discuss, and Possibly Approve a Proposed Amendment to Ordinance #2 - Sewer to Revise a Single Section to Allow Use of Hydromechanical Grease Interceptors within the District. (Requesting Staff Member: Director of Public Works Kate Nelson) Item H.4. Board and staff discussions can be viewed/heard at
```
**After:**
```
Review, Discuss, and Possibly Approve a Proposed Amendment to Ordinance #2 - Sewer to Revise a Single Section to Allow Use of Hydromechanical Grease Interceptors within the District. (Requesting Staff Member: Director of Public Works Kate Nelson)
```
**The rule removed:**
```
Item H.4. Board and staff discussions can be viewed/heard at
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

---

### [ ] 69 of 69 — 2025-07-30 item H.5 (61 characters removed)

File 1491, page 11 · meeting `ivgid-2025-07-30-bot`
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1491,plainText=false)

**Before:**
```
Review, Discuss and Possibly Approve the Added Alternates for the Incline Beach House Project, CIP #3973LI1302. (Requesting Staff Members: Director of Public Works Kate Nelson, and District Project Manager Bree Waters) Item H.5. Board and staff discussions can be viewed/heard at
```
**After:**
```
Review, Discuss and Possibly Approve the Added Alternates for the Incline Beach House Project, CIP #3973LI1302. (Requesting Staff Members: Director of Public Works Kate Nelson, and District Project Manager Bree Waters)
```
**The rule removed:**
```
Item H.5. Board and staff discussions can be viewed/heard at
```
Removed text is a media-reference sentence and nothing else?   [ ] yes   [ ] no — what was lost: ______________________

## C. Not truncations — recorded for completeness, not for ticking

These changed for a different reason and are listed so the count reconciles.
Most are the `" ."` → `"."` whitespace cleanup that came with the same edit;
the negative counts are items whose title grew because the lettered sub-item
form (`E.1.A`) is now its own item rather than being folded into `E.1`.

- 2025-01-29 item F.1 (file 1140 p3), 1 chars: `Approval of the IVGID Board of Trustees Meeting Minutes for …` → `Approval of the IVGID Board of Trustees Meeting Minutes for …`
- 2025-01-29 item G.1 (file 1140 p3), 1 chars: `Review, Discuss and Possibly Approve the Employment Contract…` → `Review, Discuss and Possibly Approve the Employment Contract…`
- 2025-01-29 item G.2 (file 1140 p5), 1 chars: `Review, Discuss and Possibly Approve the Request for Qualifi…` → `Review, Discuss and Possibly Approve the Request for Qualifi…`
- 2025-01-29 item G.3 (file 1140 p6), 1 chars: `Open Discussion and Possible Direction on Proceeding with (a…` → `Open Discussion and Possible Direction on Proceeding with (a…`
- 2025-03-05 item E.2 (file 1229 p2), 71 chars: `Review, Discuss and possibly Approve the 2025/2026 Group Pic…` → `Review, Discuss and possibly Approve the 2025/2026 Group Pic…`
- 2025-05-14 item E.1 (file 1428 p8), -100 chars: `A Review Discuss and possibly Adopt Resolution No. 1914 - a …` → `PUBLIC HEARING - Time: Not earlier than 5:00 PM and as soon …`
- 2025-06-26 item H.2 (file 1489 p14), -184 chars: `formerly G.4. Review, discuss and possibly approve a propose…` → `Approve the Cooperative Agreement with the North Lake Tahoe …`
- 2025-06-26 item H.4 (file 1489 p17), -88 chars: `formerly H.2. Approve the Cooperative Agreement with the Nor…` → `Appoint a Trustee to Serve on the Interview Panel for the Di…`
- 2025-06-26 item H.5 (file 1489 p17), -202 chars: `Formerly H.3. Draft Communication to Parcel Owners regarding…` → `Review, Discuss and Conduct Incline Village General Improvem…`
- 2026-05-13 item E.1 (file 2779 p3), -231 chars: `A. Review, Discuss and Possibly Adopt Resolution No. 1924 - …` → `PUBLIC HEARING - Time: Not earlier than 4:00 PM and as soon …`
- 2026-05-13 item E.2 (file 2779 p6), -103 chars: `A Review, Discuss, and Possibly Adopt Resolution No. 1923 – …` → `PUBLIC HEARING - Time: Not earlier than 4:00 PM and as soon …`

