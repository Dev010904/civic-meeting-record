# Hand-verification checklist — decision blocks new since round 1

These are the **5 decision blocks the round-2 recall fixes surfaced**. Every one was
invisible to the parser when the round-1 sample was drawn, so no human has checked any
of them. They are not a random sample: this is the complete set of the difference
between the pre-round-2 benchmark (`d896168`, 197 motions) and the current one
(202 motions).

Each entry states **what introduced the block** — the rule that caused it to be seen —
so the rule can be judged, not just the values. A block whose fields are all correct
but whose rule is unsound is still a defect: it will fire somewhere else.

`Item` and `Money` are printed for every block. Both are **new since round 1** and
wholly unverified: agenda-item association did not exist when round 1 was checked, and
money extraction did not exist at all.

Compare each field against the PDF at the URL given. Tick only after comparing every one.

---

### [ ] 1 of 5

Document: 2025-03-05 Special Meeting of the Board of Trustees (file 1229, page 3)
Minutes status: approved
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1229,plainText=false)

**What introduced this block**

**Pass 2 — the narrative-motion rule.** The walk-back matches `<Name> made a Motion` (`_NARRATIVE_RE`) and opens the block at that sentence, taking the capitalised run before `made a motion` as the mover. It only ever fires when a real vote block follows, so an agenda heading or a passing mention of a motion cannot be mistaken for one. This is the gap round 1 flagged as SUSPECTED at file 1229 and could not confirm.

**Parser says:**
```
  Motion:    to approve the Field Rental Fee Rate Schedule to include: Item 1 - an increase of 3.5% to Field Rental Rates as shown in (Table 1); Item 2 - IVGID Recreation Pass Holder Discount of 20% of Public Rates for Field Rental Rates (Table 1); Item 3 - the new daily tournament fee of $200 per field per day; and Item 5 - the Local Youth Sports League Fee ($3000 season); to exclude Item 4 - the local Non-Profit Rate. Additionally, he provided direction for the Staff to review the percentage of resident tournament participation and return to the Board for consideration to implement resident and non-resident rates; Staff directed to monitor the tournament play this summer; and track additional Staff time and district expenses born by fixing and maintaining fields following tournaments and determine if there is need for a protocol to be developed; Staff to return to the Board to review the implementation of additional fees to cover costs incurred, for consideration next year.
  Mover:     Trustee Noble
  Seconder:  Trustee Jezycki
  YEAS (3):   Trustee Noble, Trustee Jezycki, Trustee Tonking
  NAYS (0):   —
  ABSTAIN:   Trustee Tulloch
  ABSENT:    —
  Outcome:   PASSED
  Kind:      motion
  Flags:     none
  Notes:     ['narrative_motion']
  Item:      E.3 | Review, Discuss and Possibly Approve the Fields Fee Rate Schedule. (Requesting Staff Member: Director Parks and Recreation Karen Crocker) Item E.3. Board and Staff discussion can be viewed in its entirety at
  Timestamp: 00:31:06 (item-level)
  Money:
    $200  usd=200.0  role=rate
      vendor=None purpose=None
      contract_ref=None contingency=False approximate=False
      flags=['vendor_not_extracted', 'purpose_not_extracted']
    $3000  usd=3000.0  role=rate
      vendor=None purpose=None
      contract_ref=None contingency=False approximate=False
      flags=['vendor_not_extracted', 'purpose_not_extracted']
```

**Raw block as parsed** (what the rule actually captured):

```
Trustee Noble made a Motion to approve the Field Rental Fee Rate Schedule
to include: Item 1 - an increase of 3.5% to Field Rental Rates as shown in
(Table 1) ; Item 2 - IVGID Recreation Pass Holder Discount of 20% of Public
Rates for Field Rental Rates (Table 1); Item 3 - the new daily tournament fee
of $200 per field per day; and Item 5 - the Local Youth Sports League Fee
($3000 season); to exclude Item 4 - the local Non-Profit Rate. Additionally, he
provided direction for the Staff to review the percentage of resident tournament
participation and return to the Board for consideration to implement resident
and non-resident rates; Staff directed to monitor the tournament play this
summer; and track additional Staff time and district expenses born by fixing
and maintaining fields following tournaments and determine if there is need for
a protocol to be developed; Staff to return to the Board to review the
implementation of additional fees to cover costs incurred, for consideration
next year. The motion was seconded by Trustee Jezycki.
YEAS: Trustee Noble, Trustee Jezycki, Trustee Tonking 3
NAYS: None 0
ABSTAIN: Trustee Tulloch
MOTION PASSED
```

Values correct?      [x] yes   [ ] no — mover, seconder, YEAS(3), NAYS(0), ABSTAIN Tulloch and PASSED all match the page exactly.

Rule sound?          [x] yes   [ ] no — "Trustee Noble made a Motion" is unambiguous, the mover is taken from the capitalised run before it, and a real vote block follows. No over-firing risk visible.

Item association?    [ ] correct   [x] WRONG: title over-runs. It should end at "...Director Parks and Recreation Karen Crocker)" but continues with a separate sentence: "Item E.3. Board and Staff discussion can be viewed in its entirety at". Title assembly stops at a URL but not at the clause introducing one.

Money correct?       [x] yes   [ ] no — $200 (daily tournament fee per field per day) and $3000 (Local Youth Sports League Fee, season) both correct, both correctly typed as rates with no vendor. The 3.5% and 20% figures are percentages, correctly not captured as amounts.

---

### [ ] 2 of 5

Document: 2025-03-05 Special Meeting of the Board of Trustees (file 1229, page 4)
Minutes status: approved
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1229,plainText=false)

**What introduced this block**

**Pass 2 — the narrative-motion rule.** The walk-back matches `<Name> made a Motion` (`_NARRATIVE_RE`) and opens the block at that sentence, taking the capitalised run before `made a motion` as the mover. It only ever fires when a real vote block follows, so an agenda heading or a passing mention of a motion cannot be mistaken for one. This is the gap round 1 flagged as SUSPECTED at file 1229 and could not confirm.

**Parser says:**
```
  Motion:    to approve staff recommendations and direct staff to prepare the budget with the Parks Division in the Community Services Fund instead of the General Fund for Fiscal Year 2025-26.
  Mover:     Trustee Noble
  Seconder:  Trustee Jezycki
  YEAS (3):   Trustee Noble, Trustee Jezycki, Trustee Tonking
  NAYS (1):   Trustee Tulloch
  ABSTAIN:   —
  ABSENT:    —
  Outcome:   PASSED
  Kind:      motion
  Flags:     none
  Notes:     ['narrative_motion']
  Item:      E.4 | Review, Discuss and Provide Direction Regarding Funding of the Parks Division; Currently part of the General Fund and the recommendation to move the Parks Division to the Community Services Fund for Fiscal Year 2025-26 and Subsequent Years. (Requesting Staff Members Director of Finance Jessica O'Connell and Director of Parks and Recreation Karen Crocker) Item E.4. Board and Staff discussion can be viewed in its entirety at
  Timestamp: 00:45:07 (item-level)
  Money:     — (no dollar amounts in this motion)
```

**Raw block as parsed** (what the rule actually captured):

```
Trustee Noble made a motion to approve staff recommendations and direct
staff to prepare the budget with the Parks Division in the Community Services
Fund instead of the General Fund for Fiscal Year 2025-26. The motion was
seconded by Trustee Jezycki.
YEAS: Trustee Noble, Trustee Jezycki, Trustee Tonking 3
NAYS: Trustee Tulloch 1
MOTION PASSED
```

Values correct?      [x] yes   [ ] no — mover Noble, seconder Jezycki, YEAS(3), NAYS(1) Tulloch, PASSED — all match the page.

Rule sound?          [x] yes   [ ] no — same narrative rule as block 1, same reasoning. Second confirmation on a different motion in the same document.

Item association?    [ ] correct   [x] WRONG: same title over-run defect. Should end at "...Director of Parks and Recreation Karen Crocker)" but continues "Item E.4. Board and Staff discussion can be viewed in its entirety at".

---

### [ ] 3 of 5

Document: 2025-04-30 Regular Meeting of the Board of Trustees (file 1341, page 6)
Minutes status: approved
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1341,plainText=false)

**What introduced this block**

**Pass 2 — arbitrary labelled introducer**, same rule as `QUESTION:`. Worth noting *why* pass 1 missed this one: `_label_kind` recognises `MOTION:`, `MOTION WAS MADE` and `MOTION By`/`MOTION Moved by`, but this clerk wrote `MOTION Moved:` — the colon falls after `Moved` rather than after `MOTION`, so it matches none of them. The vote structure caught it instead. Mover and seconder then came from the ordinary `Moved By X, Seconded by Y` clause inside the block.

**Parser says:**
```
  Motion:    Direction to staff to move forward with the three firms that have submitted proposals and request an extension from BBK as well as a possible reconsideration to provide a proposal to the District RFP if they have an interest in remaining as District Legal Counsel.
  Mover:     Trustee Tulloch
  Seconder:  Trustee Noble
  YEAS (4):   Trustee Noble, Trustee Tulloch, Trustee Homan, Trustee Jezycki
  NAYS (0):   —
  ABSTAIN:   —
  ABSENT:    —
  Outcome:   PASSED
  Kind:      motion
  Flags:     none
  Notes:     ['label_variant:MOTION Moved']
  Item:      G.3 | Review and discuss submitted responses to Legal Counsel Services RFP and possibly set a date for interviews of firms and discussion of applications received for In House District Counsel (Requesting Staff Members: Director of Administrative Services Susan Herron and Director of Human Resources Erin Feore) Full staff report and Board discussion for Item G.3. can be viewed/heard at
  Timestamp: 01:25:18 (item-level)
  Money:     — (no dollar amounts in this motion)
```

**Raw block as parsed** (what the rule actually captured):

```
MOTION Moved: Direction to staff to move forward with the three firms that
have submitted proposals and request an extension from BBK as well as a
possible reconsideration to provide a proposal to the District RFP if they have
an interest in remaining as District Legal Counsel. Moved By Trustee
Tulloch, Seconded by Trustee Noble
YEAS: Trustee Noble, Trustee Tulloch, Trustee Homan, Trustee 4
Jezycki 0
NAYS: None
MOTION PASSED
```

Values correct?      [x] yes   [ ] no — mover Tulloch, seconder Noble, YEAS(4) Noble/Tulloch/Homan/Jezycki, NAYS(0), PASSED. Note the source wraps the YEAS list with the counts interleaved mid-name ("Trustee   4 / Jezycki   0"); parsed correctly.

Rule sound?          [x] yes   [ ] no — the block has a full recorded vote and the mover/seconder come from an ordinary "Moved By X, Seconded by Y" clause. Catching it on vote structure rather than label punctuation is right; "MOTION Moved:" is a clerk typo, not a distinct format.

Item association?    [ ] correct   [x] WRONG: same title over-run. Should end at "...Director of Human Resources Erin Feore)" but continues "Full staff report and Board discussion for Item G.3. can be viewed/heard at".

NOTE: this document carries a visible DRAFT watermark, but the checklist reports minutes_status = approved. See the minutes-status note at the end of this file.

---

### [ ] 4 of 5

Document: 2025-04-14 Special Meeting of the IVGID Board of Trustees (file 1342, page 2)
Minutes status: approved
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1342,plainText=false)

**What introduced this block**

**Pass 2 — the chair-called-vote rule.** A recurring clerk phrasing for a vote taken with no formal motion on the floor: the walk-back matches `called for a vote` and opens the block there. This block carries no `MOTION PASSED`/`FAILED` terminator at all — the outcome is narrated in the prose that follows — so it is flagged `missing_outcome` and the outcome is left null rather than being read out of the sentence. **The flag is the thing to check here as much as the values.**

**Parser says:**
```
  Motion:    called for a vote on the request to remove this item from the agenda.
  Mover:     — (not recorded in minutes)
  Seconder:  — (not recorded in minutes)
  YEAS (1):   Trustee Tulloch
  NAYS (4):   Trustee Noble, Trustee Homan, Trustee Jezycki, Trustee Tonking
  ABSTAIN:   —
  ABSENT:    —
  Outcome:   NONE RECORDED
  Kind:      motion
  Flags:     ['missing_outcome']
  Notes:     ['label_variant:CALLED FOR A VOTE', 'mover_not_recorded']
  Item:      D | APPROVAL OF AGENDA
  Timestamp: 00:14:18 (item-level)
  Money:     — (no dollar amounts in this motion)
```

**Raw block as parsed** (what the rule actually captured):

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

Values correct?      [x] yes   [ ] no — YEAS(1) Tulloch and NAYS(4) Noble/Homan/Jezycki/Tonking match the page exactly. Outcome is genuinely absent from the source: there is no MOTION PASSED/FAILED line, only the following prose "The vote was 1/4 ... will remain on the agenda". Leaving the outcome null and flagging missing_outcome is correct behaviour.
                     MINOR: the motion text begins "called for a vote on the request to remove this item from the agenda." — the walk-back opened mid-sentence and dropped the subject "Chair Tonking". Reads oddly; not a false claim.

Rule sound?          [x] yes   [ ] no — a recorded roll-call vote on a real question (removing an agenda item) belongs in the record whether or not a formal motion was made. Refusing to read the outcome out of the narrative sentence is the right call; interpreting prose is exactly what the parser should not do.

Item association?    [x] correct   [ ] wrong — D | APPROVAL OF AGENDA is right.

NOTE: this document also carries a visible DRAFT watermark while reporting approved.

---

### [ ] 5 of 5

Document: 2025-05-14 Regular Meeting of the Board of Trustees (file 1428, page 8)
Minutes status: approved
Open: https://ivgid.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=1428,plainText=false)

**What introduced this block**

**Pass 2 — decision blocks defined by their vote structure alone.** Pass 1 only opens a block at a recognised `MOTION` label, so a vote the clerk introduced with `QUESTION:` was invisible. Pass 2 now takes any orphan `YEAS:` line that no pass-1 block consumed, walks back to the line that introduced it, and accepts an arbitrary labelled introducer matching `^[A-Z][A-Za-z ]{1,24}:` — any word but the vote-section words and a bare `MOTION`. The governing idea: a decision block is defined by having a recorded vote, not by the word that opens it.

**Parser says:**
```
  Motion:    All in favor of Removing Item H.1. Review, discuss, and possibly approve the Employee Pass Program for Beach access; From the Agenda, please vote by saying "Yea", all those opposed say "Nay."
  Mover:     — (not recorded in minutes)
  Seconder:  — (not recorded in minutes)
  YEAS (1):   Trustee Tulloch
  NAYS (4):   Trustee Noble, Trustee Homan, Trustee Jezycki, Chair Tonking
  ABSTAIN:   —
  ABSENT:    —
  Outcome:   FAILED
  Kind:      motion
  Flags:     none
  Notes:     ['label_variant:QUESTION', 'mover_not_recorded']
  Item:      D | APPROVAL OF AGENDA
  Timestamp: 00:38:54 (item-level)
  Money:     — (no dollar amounts in this motion)
```

**Raw block as parsed** (what the rule actually captured):

```
QUESTION: All in favor of Removing Item H.1. Review, discuss, and possibly approve
the Employee Pass Program for Beach access; From the Agenda, please vote by saying
"Yea", all those opposed say "Nay."
YEAS: Trustee Tulloch 1
NAYS: Trustee Noble, Trustee Homan, Trustee Jezycki, Chair Tonking 4
MOTION FAILED ITEM H.1. WILL REMAIN ON THE AGENDA
```

Values correct?      [x] yes   [ ] no — YEAS(1) Tulloch, NAYS(4) Noble/Homan/Jezycki/Chair Tonking, outcome FAILED. The outcome was correctly extracted from a line carrying trailing text ("MOTION FAILED ITEM H.1. WILL REMAIN ON THE AGENDA"), and the name form "Chair Tonking" was preserved verbatim rather than normalised.

Rule sound?          [x] yes   [ ] no — a decision block defined by its vote structure rather than its opening label is the correct general principle. This 1-4 FAILED vote to strip an item from the agenda was entirely invisible before, and nothing in the sample suggests the rule over-fires.

Item association?    [x] correct   [ ] wrong — D | APPROVAL OF AGENDA is right; section D continues from the previous page.



---

# VERIFICATION RESULT — new blocks

**Verified:** 26 July 2026, by reading each cited page of the source PDF and comparing every field.

## Headline

**5 of 5 values correct. 5 of 5 rules sound.**

Every mover, seconder, YEAS name, NAYS name, count and outcome matched the source —
including block 1's ABSTAIN line, block 3's wrapped YEAS list with counts interleaved
mid-name, and block 5's outcome extracted from a line carrying trailing text.

**The recall rules are not over-firing.** That was the risk in this round: a rule loose
enough to see new shapes is loose enough to invent motions. It did not happen in the
complete set of blocks the fixes surfaced.

Block 4 is the strongest evidence the parser behaves honestly under pressure: it found a
genuine roll-call vote with no formal motion and no written outcome, recorded the vote,
and left the outcome null with `missing_outcome` rather than reading "The vote was 1/4"
out of the narrative sentence that followed.

## Defect — item title over-run (3 of 5)

Blocks 1, 2 and 3. The agenda-item title absorbs the sentence that introduces a media URL:

```
...(Requesting Staff Member: Director Parks and Recreation Karen Crocker)
   Item E.3. Board and Staff discussion can be viewed in its entirety at
```

Everything from "Item E.3." onward is a separate sentence. Title assembly terminates at a
URL but not at the clause introducing one. Affects published item titles in `data/meetings/`.

Observed lead-in forms: `Item <N>. Board and Staff discussion can be viewed in its entirety at`,
`Full staff report and Board discussion for Item <N>. can be viewed/heard at`.

## Discrepancy — DRAFT watermark vs reported status

Files **1341 and 1342** both carry a **visible DRAFT watermark** on the page, but both are
recorded as `minutes_status: approved`. This is the known image-only-watermark ambiguity
(no extractable text; the file name carries an approval signal), but it affects two files
rather than one, and both are in the published record.

Practical consequence: a reader following the source link from a published page sees DRAFT
stamped across the document while the page asserts approved minutes. Worth surfacing on the
page rather than resolving silently either way.

## Minor — motion text opens mid-sentence (block 4)

`called for a vote on the request to remove this item from the agenda.` — the walk-back
opened at the matched phrase and dropped the subject (`Chair Tonking`). Not a false claim;
reads badly.

## Bearing on the published /accuracy figure

Combined with round 1 (25/25 vote records correct), **30 of 30 hand-checked vote records
have been correct**. Every defect found across both rounds has been in supporting fields —
media timestamps, motion text formatting, item titles — never in a vote.
