# Legal and ethical footing v2

**Supersedes `legal-footing.md`.** That file was written when Augusta Charter Township, MI was the build jurisdiction. Michigan now matters only as a document-benchmark source. Nevada governs the build.

**Verified 26 July 2026.** Statutes quoted, not paraphrased. **I am not a lawyer; this is sourced reconnaissance, not legal advice.**

**Key:** `✅V` primary source fetched and quoted · `🟡P` secondary source only · `⬜U` unverified

---

# PART I — NEVADA (IVGID, build jurisdiction)

## 1. Is IVGID a "public body" under the Open Meeting Law? — ✅V, chain complete

Three links, each quoted.

**Link 1 — a general improvement district is a governmental subdivision.**
NRS 318.075(1):

> "the adoption of the ordinance creating the district shall finally and conclusively establish the regular organization of the district against all persons, **which district shall thenceforth be a governmental subdivision of the State of Nevada, a body corporate and politic and a quasi-municipal corporation.**"

Reinforced by NRS 318.015(1):

> "…**each district organized pursuant to the provisions of this chapter shall be a body corporate and politic and a quasi-municipal corporation.** For the accomplishment of these purposes the provisions of this chapter shall be broadly construed."

**Link 2 — districts are created by statute, via county ordinance.**
NRS 318.055(1)–(2): formation is initiated by resolution of the board of county commissioners or by petition, and "the organization of the district must be initiated by the adoption of an ordinance by the board of county commissioners."

**Link 3 — the OML definition catches it.**
NRS 241.015(5)(a):

> "'public body' means: (a) **Any administrative, advisory, executive or legislative body of the State or a local government consisting of at least two persons which expends or disburses or is supported in whole or in part by tax revenue** … including, but not limited to, any board, commission, committee, subcommittee or other subsidiary thereof … if the administrative, advisory, executive or legislative body is created by: … **(2) Any statute of this State;** … or **(7) A resolution or an action by the governing body of a political subdivision of this State.**"

**Conclusion.** The IVGID Board of Trustees is a five-member legislative/executive body of a governmental subdivision, created under NRS Chapter 318 by Washoe County ordinance, supported by tax revenue and assessments. It satisfies (a)(2) and (a)(7) independently. **IVGID is a public body subject to NRS Chapter 241.** ✅

**Corroboration from IVGID's own documents:** the 22 July 2026 agenda cites NRS 288.220(4) for its closed session and certifies posting under Assembly Bill 213 to five locations including Nevada's public notice website. The district plainly treats itself as OML-bound.

---

## 2. NRS 241.035 — what the district must keep and give you — ✅V

**This is materially stronger than Michigan. Nevada does not merely permit recording; it compels it and makes the recording a public record.**

### 241.035(1) — what minutes must contain

> "Each public body shall keep written minutes of each of its meetings, including:
> (a) The date, time and place of the meeting.
> (b) Those members of the public body who were present … and those who were absent.
> **(c) The substance of all matters proposed, discussed or decided and, at the request of any member, a record of each member's vote on any matter decided by vote.**
> **(d) The substance of remarks made by any member of the general public who addresses the public body if the member of the general public requests that the minutes reflect those remarks** or, if the member of the general public has prepared written remarks, a copy of the prepared remarks if the member of the general public submits a copy for inclusion.
> (e) Any other information which any member of the public body requests to be included…"
>
> "Unless good cause is shown, a public body shall approve the minutes of a meeting **within 45 days** after the meeting or at the next meeting of the public body, whichever occurs later."

**Two build-relevant consequences.**
- Roll-call detail is recorded **at a member's request**, not automatically. IVGID happens to record it for every motion — that is district practice exceeding the statutory floor, and **it could stop without any legal change.** Do not architect on the assumption it is guaranteed.
- **§(d) is decisive for the naming question.** A public commenter's remarks go into the minutes *at the commenter's own request*. IVGID transcribes verbatim regardless — again exceeding the floor. See §4.
- The 45-day approval rule explains the draft/approved gap in `ground-truth-v2.md` A3.

### 241.035(2) — minutes and audio are public records, free on request

> "**Minutes of public meetings are public records.** Minutes or an audio recording of a meeting made in accordance with subsection 4 **must be made available for inspection by the public within 30 working days** after adjournment of the meeting. **A copy of the minutes or audio recording must be made available to a member of the public upon request at no charge.** The minutes shall be deemed to have permanent value and **must be retained by the public body for at least 5 years.**"

### 241.035(3) — the public's own right to record

> "**All or part of any meeting of a public body may be recorded on audiotape or any other means of sound or video reproduction by a member of the general public if it is a public meeting so long as this in no way interferes with the conduct of the meeting.**"

### 241.035(4) — the district *must* record, and that recording is a public record

> "**a public body shall, for each of its meetings, whether public or closed, record the meeting on audiotape or another means of sound reproduction** or cause the meeting to be transcribed by a court reporter… If a public body makes an audio recording of a meeting…the audio recording or transcript:
> (a) **Must be retained by the public body for at least 3 years** after the adjournment of the meeting…;
> (b) Except as otherwise provided in this section, **is a public record and must be made available for inspection by the public** during the time the recording or transcript is retained; and
> (c) Must be made available to the Attorney General upon request."

### What this settles

| Question | Answer |
|---|---|
| Are meeting recordings public records? | **Yes, explicitly** — §241.035(4)(b) |
| Must IVGID retain them? | **Yes — audio ≥3 years; minutes ≥5 years and "permanent value"** |
| Must IVGID give you a copy? | **Yes — "upon request at no charge"** (§2) |
| Within what time? | Available for inspection **within 30 working days** of adjournment |
| May you record yourself? | **Yes**, without approval, absent interference (§3) |
| Any republication restriction in Chapter 241? | **None found.** The chapter is silent on downstream use. `⬜U` on Nevada case law. |

**Practical effect on the build.** The CivicPlus TOS scope question in `civicclerk-api.md` §5 is now largely moot for Nevada. Even on the most restrictive reading of a vendor's marketing-site terms, **you have an independent statutory right to a free copy of the same audio directly from the district.** The clerk email in `clerk-email.md` should cite NRS 241.035(2) — it converts a request into a statutory entitlement politely exercised.

---

## 3. Defamation — Nevada draws a line that matters — ✅V

**NRS 241.0353** — quoted in full:

> "**1.** Any statement which is made by **a member of a public body** during the course of a public meeting is **absolutely privileged** and does not impose liability for defamation or constitute a ground for recovery in any civil action.
>
> **2.** A witness who testifies under oath, subject to the penalties set forth in NRS 199.120, before a public body may publish defamatory matter as part of a public meeting. It is unlawful to misrepresent any fact knowingly when testifying before a public body.
>
> **3.** Except as otherwise provided by law, **nothing in this chapter shall be construed to affect any civil cause of action for defamation, libel, slander or any similar cause of action arising from defamatory statements made by a member of the public while he or she provides public comment to a public body.**"

*(Added 2005; amended 2021 and 2025.)*

### The asymmetry, stated plainly

- **Trustees** — absolutely privileged. You can republish anything Tonking, Jezycki, Homan, Noble or Tulloch says in a meeting without the underlying statement being actionable.
- **Sworn witnesses** — qualified privilege.
- **Members of the public giving public comment** — **no privilege at all.** Subsection 3 preserves the cause of action expressly.

### Why this is a republication problem, not just a speaker problem

Under ordinary republication doctrine, one who repeats a defamatory statement can be liable as if they had made it. Nevada has just told you, in statute, that public comment is the one category with no privilege. **A verbatim transcript of a resident accusing a named contractor of fraud is the exact fact pattern.**

**The defence is the fair report privilege.** Nevada recognises it 🟡P: a fair and accurate report of an official proceeding open to the public is privileged, provided the average reader would understand it as a report or summary of that proceeding. `⬜U` — I have not read the controlling Nevada authority, only secondary summaries.

**Design rules that follow — these are not optional:**
1. **Frame everything as a report of the meeting.** Headers, labels and framing must make clear the reader is looking at a record of an official proceeding — not the site's own assertions. This is what keeps fair report available.
2. **Accuracy is the whole defence.** Fair report protects *accurate* reports. A garbled ASR transcript that changes who said what forfeits the privilege precisely when you need it.
3. **Never publish an ASR-derived name.** Already the rule for accuracy reasons; §241.0353(3) makes it a liability rule too.
4. **Prefer summary over verbatim for public comment**, and attribute allegations to the speaker as allegations.

---

## 4. Naming private citizens — what is actually documented

The previous file marked this `⬜U` and said no documented standard was found. **I found more this time, and it changes part of the answer.**

### 4a. What is genuinely documented ✅V

**SPJ Code of Ethics** (revised 6 Sept 2014) — fetched and quoted. Four provisions bear directly:

> "**Recognize that legal access to information differs from an ethical justification to publish or broadcast.**"

> "**Realize that private people have a greater right to control information about themselves than public figures and others who seek power, influence or attention. Weigh the consequences of publishing or broadcasting personal information.**"

> "**Consider the long-term implications of the extended reach and permanence of publication.** Provide updated and more complete information as appropriate."

> "Balance the public's need for information against potential harm or discomfort. Pursuit of the news is not a license for arrogance or undue intrusiveness."

**This is the standard, and it is directly on point.** The first line answers the whole question: *the fact that a public meeting is legally open does not by itself justify publishing a resident's name.* The third addresses the specific harm — a permanent, searchable, machine-readable record is a different thing from a meeting that was public in the moment.

**Nevada statute, in tension with the ethical rule** — NRS 241.035(1)(d), quoted above: a commenter's remarks enter the minutes **at the commenter's request**. So the statutory design assumes the *speaker* elects to be recorded. IVGID's practice of transcribing everyone verbatim goes beyond that.

**Pennsylvania goes further still** — 65 Pa.C.S. § 706 ✅V requires minutes to include:

> "**(4) The names of all citizens who appeared officially and the subject of their testimony.**"

Worth knowing for `abingtonpa` in phase two: **there, naming is statutorily mandated in the source document.**

### 4b. What I still could not verify ⬜U

- **Documenters Field Guide.** It exists at `fieldguide.documenters.org` with a `legal-reference/quick-reference` section — but it is hosted on Notion and served me only "JavaScript must be enabled." **I could not read it.** Secondary sources indicate it covers not recording private conversations and displaying recording devices prominently 🟡P. **Read it in a browser; it is the closest thing to a peer standard and I am flagging that I failed to get it.**
- **citymeetings.nyc.** Public writing describes transcription into "moments and useful summaries that faithfully represent things people say on the record," with human oversight at every step 🟡P. **No published policy on commenter names found.** Given NYC council testimony is overwhelmingly from organisational representatives and repeat advocates rather than anonymous residents, it may simply not have faced the question in the same form.
- **Any Nevada-specific privacy constraint on republishing meeting participants' names.** None found in Chapter 241. `⬜U`.

### 4c. So: is there a settled practice?

**No.** I looked in the three places you named and found a general journalism ethics standard that applies cleanly, one statute that assumes speaker election, one statute that mandates naming — and **no published, specific, civic-tech convention for automated systems.** I am not going to dress reasoning up as consensus.

### 4d. Reasoned policy — marked as reasoning `[I]`

Grounded in the SPJ provisions above and NRS 241.0353(3).

1. **Officials, staff and paid representatives: always named in full.** Trustees, GM, directors, District Clerk, contractors' representatives, counsel. They act in public roles, they are absolutely privileged under §241.0353(1), and IVGID's own minutes name them.
2. **Private residents in public comment: not named by default.** Render as "a resident," optionally with self-declared context ("a resident of Lakeshore Boulevard"). **The substance of the argument is the news; the surname almost never is.**
3. **Report public comment in aggregate where possible.** "Nine of eleven commenters opposed the fee increase, citing X" beats eleven names.
4. **Name a private individual only where they have assumed a public role** — campaign organiser, petition filer, litigant, candidate, or someone appearing on behalf of an organisation.
5. **Never publish a name derived from audio.** Hard technical rule. Names are what ASR gets wrong, misattribution is defamation-shaped, and §241.0353(3) removes the speaker's privilege. **If the name came from the recording rather than a document, drop it.**
6. **`noindex` public-comment sections**, or exclude them from the search index while keeping them linkable. Directly serves SPJ's "long-term implications of the extended reach and permanence of publication."
7. **Removal path.** Visible contact address; act on requests from private individuals.
8. **Do not mirror IVGID's verbatim transcripts wholesale.** The district publishing them does not oblige you to amplify them. Link to the district's minutes instead — the reader gets the full record, and the searchable copy stays where the public body chose to put it.

Rule 5 makes rules 2 and 8 nearly free: reliable attribution comes from documents (which name officials), unreliable attribution comes from audio (where residents appear). **The technically safe policy and the ethically safe policy are the same policy.**

---

# PART II — PHASE-TWO DOCUMENT-ONLY JURISDICTIONS

Five zero-video CivicClerk clients. All publish agendas, packets and minutes via `GetMeetingFileStream`. Short entries as requested. Statutes 🟡P via secondary sources except where marked.

## Stanly County, North Carolina — `stanlyconc`
- **Open meetings:** N.C.G.S. Chapter 143, Article 33C (§ 143-318.9 *et seq.*).
- **Recording:** **§ 143-318.14(a)** — any person may photograph, film or record any part of an open official meeting; a body may regulate equipment placement to prevent undue interference but **cannot ban recording**.
- **Minutes:** § 143-318.10(e) — full and accurate minutes required; **may take the form of sound or video-and-sound recordings**.
- **Peculiarity:** none blocking republication found. NC is a one-party-consent state, irrelevant to open meetings.
- **Verdict:** ✅ clear for document republication.

## Village of McFarland, Wisconsin — `mcfarlandwi`
- **Open meetings:** Wis. Stat. §§ 19.81–19.98.
- **Recording:** **§ 19.90** — "the body **shall make a reasonable effort to accommodate any person desiring to record, film or photograph the meeting**," provided it does not interfere.
- **Minutes/votes:** **§ 19.88(3)** — the **motions and roll-call votes** of each meeting "shall be recorded, preserved and open to public inspection." Roll-call votes are statutorily guaranteed, which is better than Nevada's on-request rule.
- **Peculiarity:** Wisconsin's public records law (§§ 19.31–19.39) has a strong presumption of openness.
- **Verdict:** ✅ clear. **Best statutory vote guarantee of the five.**

## Town of Essex, Vermont — `essexvt`
- **Open meetings:** 1 V.S.A. §§ 310–314.
- **Minutes:** **§ 312** — minutes "shall cover all topics and motions that arise at the meeting and give a true indication of the business of the meeting"; **"Minutes of all public meetings shall be matters of public record"**, available for inspection and purchase at cost **after five days**.
- **🔴 Important correction to `candidates-v2.md`.** Vermont's Open Meeting Law, **effective 1 July 2024**, requires all **non-advisory** public bodies to **record meetings in audio or video and post the recording** in a designated electronic location for **at least 30 days** after the minutes are approved and posted 🟡P. **So Essex's zero-video result in CivicClerk does not mean no recording exists — it means the recording is not in CivicClerk.** Look elsewhere (town website, Front Porch Forum, a local access channel) before writing Essex off as document-only. This may be the strongest phase-two candidate, not the weakest.
- **Verdict:** ✅ clear, and **re-check for video**.

## Abington Township, Pennsylvania — `abingtonpa`
- **Open meetings:** Sunshine Act, 65 Pa.C.S. §§ 701–716.
- **Minutes:** **§ 706** ✅V, quoted in full:
  > "Written minutes shall be kept of all open meetings of agencies. The minutes shall include: (1) The date, time and place of the meeting. (2) The names of members present. **(3) The substance of all official actions and a record by individual member of the roll call votes taken.** **(4) The names of all citizens who appeared officially and the subject of their testimony.**"
- **Peculiarity — two, both notable.** §706(3) **guarantees per-member roll-call votes in the minutes by statute.** §706(4) **requires naming citizens who appear.** So Pennsylvania mandates in the source document exactly what §4d rule 2 says you should not amplify. **The ethical rule still governs your output** — the statute binds the agency, not you.
- **Verdict:** ✅ clear for documents; apply the naming policy with particular care.

## West Bloomfield Township, Michigan — `wbtownshipmi`
- **Open meetings:** Michigan OMA, MCL 15.261–15.275.
- **Recording:** **MCL 15.263(1)** ✅V (quoted in the superseded file): "The right of a person to attend a meeting of a public body includes the right to tape-record, to videotape, to broadcast live on radio, and to telecast live on television the proceedings of a public body at a public meeting. **The exercise of this right does not depend on the prior approval of the public body.**"
- **Minutes:** MCL 15.269 — minutes are public records, must show members present/absent, decisions, and the purpose of closed sessions; proposed minutes within 8 business days, approved within 5 days of the next meeting 🟡P.
- **Peculiarity:** none blocking republication.
- **Verdict:** ✅ clear. Same statutory footing already validated for Augusta.

**Across all five: no state restriction on republishing agendas, minutes or transcripts was found.** ⬜U on state case law in each.

---

# PART III — CORRECTIONS AND TAKEDOWN

This becomes a published page. Concrete, with real models.

## 5. Real examples ✅V

**The Texas Tribune** — the cleanest short model, quoted from its Code of Ethics:

> "When we make a mistake — and from time to time, we will — we will **work quickly to fully address the error, correcting it within the story, detailing the error on the story page and adding it to a running list of Tribune corrections.** If you find an error, email corrections@texastribune.org."

Four mechanisms in one sentence: **fix in place · disclose on the page · log centrally · one published contact address.** The Tribune maintains that running list at `texastribune.org/corrections/`, and states its code "borrows generously from" ProPublica, NPR and the Center for Investigative Reporting.

**The Tribune's AI policy** is the closer model for you, since your publisher *is* an automated system. Directly transferable commitments:

> "We will not publish text generated by AI tools unless it has gone through a rigorous verification and editing process."

> "They will treat **AI-generated output as unverified information** and work to independently verify it."

> "**If we build journalism products that rely on AI tools to generate published information for readers**, such as a chatbot or interactive module, **we will disclose the usage of these tools and add context to clarify the role of AI in the product.**"

**SPJ Code of Ethics**, "Be Accountable and Transparent" ✅V:

> "**Acknowledge mistakes and correct them promptly and prominently. Explain corrections and clarifications carefully and clearly.**"
> "**Respond quickly to questions about accuracy, clarity and fairness.**"
> "Explain ethical choices and processes to audiences."

And from "Seek Truth and Report It":

> "**Provide access to source material when it is relevant and appropriate.**"
> "Gather, update and correct information throughout the life of a news story."

## 6. Draft published policy

To go up **before the first meeting summary is published**, not after the first complaint.

---

> ### Corrections and accuracy
>
> **What this site is.** Automated summaries and transcripts of IVGID Board of Trustees and Audit Committee meetings, generated by software from the district's own published recordings, agendas and minutes. **Machine-generated and not reviewed by a human before publication unless a page says otherwise.** Treat it as a finding aid pointing at primary sources, not as a substitute for them.
>
> **Where every claim comes from.** Every factual statement links to either a page of a district PDF or a timestamp in the district's own recording. **If a claim has no source link, it is a bug — please report it.**
>
> **Votes.** Vote records are taken **only from the district's minutes**, never from automated transcription. Where minutes are not yet approved, the page is labelled *draft minutes*. Where minutes are unavailable, **no vote is reported at all.**
>
> **What we get wrong.** Known error rates against a benchmark of past meetings are published at /accuracy, including every case we currently get wrong. That page is updated whenever the system changes.
>
> **Reporting an error.** Email **[address]**. Include the page and, if you can, the timestamp or document page. Errors from anyone are welcome — residents, trustees, staff.
>
> **What we do when told.**
> - **Factual error** (wrong vote, wrong figure, wrong name, wrong attribution): corrected within **2 business days**; a dated correction notice stays on the page permanently; the entry is added to the corrections log.
> - **Systemic error** (a whole class of items parsed wrongly): every affected page corrected, one log entry describing the class and the fix.
> - **Unclear or misleading but not false:** clarification note added, logged.
> - **Disputed:** we publish the dispute alongside the claim and link to the primary source so readers can judge.
>
> **We do not silently edit.** A page whose substance changes carries a visible dated note. The corrections log at /corrections is permanent and in reverse chronological order.
>
> **Takedown requests.**
> - **A private individual asking not to be named in public comment:** honoured, no reason required, normally within 2 business days. The substance of the comment stays; the identifier goes.
> - **A public official asking to remove an accurate record of official conduct:** declined, and the request is logged publicly.
> - **Claimed defamation:** the passage is reviewed against the district's recording and minutes immediately. If we misreported, corrected at once. If we accurately reported what a person said at a public meeting, that is noted along with a link to the source, and the complaint is directed to the speaker.
> - **Every takedown request and its outcome is logged** — requester category (private individual / official / organisation), date, action taken. Never the requester's name.
>
> **Suspension.** If a systemic fault means output can't be trusted, publication is suspended and a notice posted until it's fixed. Silence is a worse failure than a gap.

---

## 7. Why these specific choices `[I]`

- **Disclosing that it is machine-generated up front** is the Tribune's AI-policy commitment applied honestly, and it sets the reader's standard of care correctly.
- **"No vote reported when minutes are unavailable"** is the single most important line. It converts the highest-risk failure into a gap rather than an error.
- **Publishing the error rate before anyone asks** is the `walls.md` move — ship verifiability instead of authority.
- **Logging declined takedowns** deters pressure from officials, which in a district with contested fee and beach decisions is a live prospect.
- **Honouring private-individual name removal with no reason required** costs almost nothing, since §4d rule 2 means you should not have named them anyway.
- **Permanent correction notices** rather than silent edits — SPJ's "promptly and prominently."

---

# PART IV — SUMMARY

| Question | Answer | Confidence |
|---|---|---|
| Is IVGID subject to Nevada's OML? | **Yes** — NRS 318.075(1) + 318.015(1) + 241.015(5)(a)(2),(7) | ✅ High, chain quoted |
| Are meeting recordings public records? | **Yes** — NRS 241.035(4)(b) | ✅ High |
| Must the district give you a copy? | **Yes, free, on request** — NRS 241.035(2) | ✅ High |
| Retention | Audio **≥3 years**; minutes **≥5 years**, "permanent value" | ✅ High |
| May you record yourself? | **Yes, no prior approval** — NRS 241.035(3) | ✅ High |
| Restriction on republishing recordings/transcripts? | **None found in NRS 241** | ✅ statute / ⬜U case law |
| Defamation risk from trustees' words? | **None** — absolutely privileged, NRS 241.0353(1) | ✅ High |
| Defamation risk from public comment? | **Real** — NRS 241.0353(3) preserves the cause of action | ✅ High |
| Defence available? | **Fair report privilege**, if the report is accurate and framed as a report | 🟡 Moderate |
| Documented civic-tech standard on naming? | **No.** SPJ's general standard applies; Documenters' guide unread | ⬜U on practice, ✅V on SPJ |
| Phase-two states clear for document republication? | **All five, yes** | 🟡 Moderate |
| Biggest real risk | **Still accuracy, not law** | ✅ High |

**The one-line version:** Nevada is the best legal footing encountered in this project — the district is *required* to record, the recording *is* a public record, and you are entitled to a free copy. The only sharp edge is that public commenters have no defamation privilege, which is an argument for summarising rather than mirroring their words — the same conclusion the ethics reached independently.

## Open items ⬜U

1. **Read the Documenters Field Guide** at `fieldguide.documenters.org/legal-reference/quick-reference/` in a browser. I could not.
2. **Nevada fair report privilege** — find the controlling authority rather than relying on secondary summaries.
3. **Vermont recording mandate** — confirm the 1 July 2024 requirement and locate where Essex actually posts recordings.
4. **Case law** in all six states on republishing meeting recordings. None found; none searched exhaustively.
