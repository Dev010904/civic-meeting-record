# Build Spec v1 — Civic Meeting Record

**Jurisdiction:** IVGID — Incline Village General Improvement District, Nevada (`ivgid`)
**Platform:** CivicClerk
**Status:** ready to build
**Version:** 1.2 — hardened against `legal-footing-v2.md` and City Bureau's published standards
**Date:** 26 July 2026

---

## 0. What this is

An automated system that reads every public meeting of a local government body and
publishes what happened, with a verifiable source for every claim.

**Non-goals for v1.** No summarising of debate. No opinion. No prediction. No
"what this means for you." The product is a *record*, not an analysis. Anything
that cannot be traced to a page number or a video timestamp does not get published.

---

## 1. Architecture in one line

```
GitHub Actions (cron)
  → CivicClerk API (events + PDFs)
  → document extraction        [Layer 1 — build first]
  → audio transcription        [Layer 2 — build second]
  → JSON artifacts committed to the repo
  → static site built and deployed to Cloudflare Pages
```

**Everything lives in one public GitHub repo.** Data is committed as JSON.
This is not a shortcut — it is the provenance mechanism. Every change to every
published claim is a git diff with a timestamp and a commit. Corrections are
auditable by anyone. No database is needed at v1 scale and none should be added.

---

## 2. Layer 1 — Documents (build this first, entirely)

Layer 1 must be complete, benchmarked, and published before any audio code is written.
It has no ASR, no rate-limit pressure, and it works on jurisdictions with no video —
which is the entire phase-two market.

### 2.1 Ingest

```
GET https://ivgid.api.civicclerk.com/v1/Events
    ?$filter=startDateTime+lt+{today}
    &$orderby=startDateTime+desc,+eventName+desc
```

**API quirks that are already verified and must be handled:**

| Quirk | Handling |
|---|---|
| `$select` returns `200` with empty `value` | **Never use `$select`.** Fetch full objects, discard client-side. |
| Server page cap is 15 regardless of `$top` | Follow `@odata.nextLink` (carries a `$skiptoken`). |
| Default sort returns future events first | Always pair with `startDateTime lt {today}`. |
| Two-key orderby required with `categoryId` filter | Use `$orderby=startDateTime desc, eventName desc`. |
| `agendaFile` / `minutesFile` are empty stubs | **Ignore both.** All real files are in `publishedFiles[]`. |
| `liveStartTime`/`liveEndTime` sometimes span days | Never derive duration from these. |

**File fetch — by `fileId`, never by the `url` field:**

```
GET /v1/Meetings/GetMeetingFileStream(fileId={id},plainText=false)
```

Returns `application/pdf`, text-extractable. `publishedFiles[].type` observed
values: `Agenda`, `Agenda Packet`, `Minutes`, `Notice`, `Other`.

### 2.2 Extraction targets

From **Minutes** PDFs, extract structured records:

- **Motions** — item reference, mover, seconder, vote tally, outcome (passed / failed / tabled / continued)
  - ⚠️ NRS 241.035(1)(c) requires per-member vote records only *at a member's request*. IVGID records them every time **by practice, not obligation**. The parser must treat their absence as normal, not as a failure.
- **Dollar amounts** — value, vendor, purpose, contract/PO reference, whether a contingency was attached
- **Agenda items** — number, title, disposition
- **Media timestamps** — IVGID clerks hand-write `Media Timestamp (HH:MM:SS - HH:MM:SS)` per item. Capture these. They are the alignment key for Layer 2 and they are human-verified, which is better than any model output.
- **Public comment** — see §5. Extract *that* comment occurred and on what topic. Private commenters are **not named** in output. Do **not** copy verbatim text into published output.

From **Agenda** and **Agenda Packet** PDFs:

- Item numbering and titles (the pre-meeting skeleton)
- Attached staff reports and contract values

### 2.3 Extraction method — two-stage, deterministic first

**Stage A — deterministic parser.** IVGID minutes use a rigid format. Regex and
structural parsing must run first and handle the well-formed majority. This costs
zero LLM calls and is exactly reproducible.

**Stage B — LLM fallback.** Only lines Stage A fails on go to a model. This keeps
daily request count far inside free limits and keeps most output non-stochastic.

**Never let Stage B silently overwrite Stage A.** If they disagree, record both and
flag the item for review. Disagreement is signal.

### 2.4 Data model

```jsonc
{
  "meeting_id": "ivgid-2026-07-22-bot",
  "jurisdiction": "ivgid",
  "body": "Board of Trustees",
  "date": "2026-07-22",
  "source": {
    "event_id": 4136,
    "agenda_file_id": 2800,
    "minutes_file_id": null,
    "media_url": "https://cpmedia.azureedge.net/ivgid/104a898503.mp4"
  },
  "items": [{
    "number": "F.1",
    "title": "Snowmaking Pump Replacement",
    "disposition": "passed",
    "motions": [{
      "mover": "…", "seconder": "…",
      "tally": { "aye": 4, "nay": 1, "abstain": 0, "absent": 0 },
      "outcome": "passed",
      "provenance": { "type": "pdf", "file_id": 2800, "page": 7 }
    }],
    "money": [{
      "amount_usd": 350236,
      "vendor": "Trillium Pumps USA",
      "purpose": "snowmaking pump replacement",
      "provenance": { "type": "pdf", "file_id": 2800, "page": 7 }
    }],
    "media_timestamp": { "start": "00:12:15", "end": "00:31:03" },
    "extraction": { "stage": "A", "confidence": "exact", "flags": [] }
  }]
}
```

**Provenance is a required field on every extracted claim.** A claim without
provenance is a bug and must fail validation, not publish with a caveat.

### 2.5 Cross-meeting tracking

The differentiating feature. Match items across meetings by normalised title +
vendor + amount, and detect:

- An item tabled/continued at one meeting and acted on later
- A contract value that changed between agenda and minutes
- A change order raising a previously approved amount
- An item that appeared on an agenda and then silently vanished

These are the findings no summariser produces and no resident can assemble by hand.
This is the actual product.

### 2.6 Accuracy gate — must pass before publishing anything

**Benchmark corpora:**

- **Augusta Charter Township, MI** — 146 minutes PDFs, text-extractable draft
  minutes with roll-call votes. Includes a known clerical contradiction
  (Trustee Prain recorded as both aye and absent on item 15, 24 Mar 2026).
- **IVGID** — minutes with per-item media timestamps and structured vote blocks.

**Targets:**

| Metric | Target |
|---|---|
| Vote tally exact match, well-formed motions | ≥ 99% |
| Dollar amount + vendor exact match | ≥ 99% |
| Mover / seconder exact match | ≥ 97% |
| Source contradictions detected | scored separately — see below |
| Claims published without provenance | **0** |

**The Prain case is scored separately and must not count as a parser failure.**
The correct behaviour is to detect and flag the contradiction, not to resolve it.
Flagging clerical contradictions is a feature; silently picking one is a defect.

**Publish the accuracy number on the site.** That number is the credential the
project does not otherwise have.

---

## 3. Layer 2 — Audio (only after Layer 1 ships)

### 3.1 The 2 GB problem

Confirmed: `https://cpmedia.azureedge.net/ivgid/104a898503.mp4` is a plain public
file, no auth, no DRM, **2.0 GB for 2h24m**. No `robots.txt` on that host (404).
No lighter rendition exists — `mobileMediaStreamPath`, `externalMediaUrl`,
`jwPlayerCode`, `youtubeVideoId` and all `closedCaption*` fields are empty across
every sampled client.

**Handling:** stream through ffmpeg, never store the video.

```bash
ffmpeg -i "$URL" -vn -ac 1 -ar 16000 -c:a libopus -b:a 16k out.opus
```

~2 GB over the wire, ~17 MB stored. Rate-limit to one file at a time, with a
descriptive User-Agent identifying the project and a contact address.

**Better path, available under statute:** NRS 241.035(2) requires that a copy of
the minutes *or audio recording* be provided to any member of the public on
request at no charge. Ask IVGID for audio directly. That is both cheaper and the
start of the institutional relationship the project needs. Draft exists at
`02-shortlist/clerk-email.md`.

### 3.2 Transcription

Groq `whisper-large-v3-turbo`, free tier: **28,800 audio-seconds/day = 8 hours.**
IVGID runs roughly 10 hours/month. The budget is not close to binding.

Chunk with overlap, stitch on overlap, preserve absolute timestamps throughout.
Every transcript segment carries a timestamp into the source MP4.

### 3.3 Alignment

Use the clerk's hand-written `Media Timestamp` ranges from the minutes as the
alignment key. This is human-authored ground truth and should be trusted over any
model inference. Where a meeting lacks them, fall back to matching agenda item
titles against transcript text — and mark those alignments as inferred.

### 3.4 What audio adds

Only: what was actually said, quoted, with a timestamp link. Never a claim about
an outcome — outcomes come from minutes. Audio is evidence, not authority.

---

### 2.7 Hard publication rules (from `legal-footing-v2.md`)

These are validation gates, not guidelines. Violating any of them is a build failure.

1. **Votes come only from minutes.** Never from transcription. If minutes are
   unavailable for a meeting, **report no vote at all** — a visible gap, never an
   inference. This converts the highest-risk failure mode into an absence.
2. **Label minutes status.** Nevada allows 45 days for approval. Pages built from
   unapproved minutes must be labelled *draft minutes*.
3. **Never publish a name derived from audio.** Unconditional. Names are what ASR
   gets wrong, and misattribution is defamation-shaped. If the name came from the
   recording rather than a document, it is dropped.
4. **Officials named, private commenters not.** Trustees, staff, counsel, vendor
   representatives — named in full, absolutely privileged under NRS 241.0353(1).
   Residents in public comment — rendered as "a resident," aggregated where
   possible ("nine of eleven commenters opposed the increase").
   **Peer-confirmed.** City Bureau's Documenters note-taking guidance offers exactly
   two options: name the commenter *after approaching them in person to confirm the
   spelling*, "or you can describe them generally (for example, 'a resident')."
   An automated system cannot take the first branch. The second is not the cautious
   choice — it is the only available one.
5. **Frame every page as a report of an official proceeding.** This is what keeps
   the fair report privilege available. The site reports what a meeting recorded;
   it does not assert facts of its own.
6. **`noindex` public-comment sections** or exclude them from search while keeping
   them linkable.
7. **A claim without provenance fails validation.** It does not publish with a caveat.


---

## 3.5 Peer standard — City Bureau / Documenters

City Bureau has run the Documenters program since 2018, trains paid human witnesses
to cover local government meetings, and publishes AI usage guidelines. It is the
closest thing to a professional standard in this field. Their guidelines are
stricter than this project in one respect, and that gap is addressed deliberately
rather than ignored.

**Their position, quoted:**
- "Just submitting an AI generated transcription or summary as your assignment is not acceptable."
- "What happens in a meeting can't be represented by transcription alone, and transcripts often contain mistakes."
- "Your notes are always reviewed and edited by a Documenters staff member prior to publication."
- "Any AI usage must be disclosed."
- "Always cross check what AI tells you with a reliable primary source." / "Only cite primary sources."

**How this project relates to it.**

Their rules protect what they pay Documenters for: a community member's presence,
perspective and synthesis. **This project does not produce that and must never
claim to.** §8 already forbids LLM narrative summaries; that non-goal is now a
principle, not a scoping decision.

What this project does is index a primary source — votes, amounts and vendors taken
from the district's own approved minutes, each linked to a page. That is closer to
a finding aid than to reporting, and it operates where no witness exists at all.

**The gap, stated honestly: this project has no human editor. Documenters has one.**

**The rule adopted in response:**

| Layer | Human review |
|---|---|
| **Layer 1 — documents** | **Not required.** Every claim carries page-level provenance from an official public record and is verifiable by a reader in seconds. |
| **Layer 2 — audio** | **Required. No quote derived from transcription publishes without human review.** This is precisely the case City Bureau describes, and they are right about it. |

**Consequent disclosure requirements:**
- State on every page that output is machine-generated.
- State plainly that this is **not a substitute for attending or watching a meeting**, and that transcripts contain errors.
- Cite only primary sources. Never cite the system's own prior output as a source.
- Present the site as a finding aid pointing at the district's records — never as an
  account of what a meeting *meant*.

---

## 4. Publishing

- Static site, built by GitHub Actions, deployed to Cloudflare Pages (free).
- One page per meeting; one page per tracked item across meetings.
- Every fact links to either a PDF page or a video timestamp.
- Full-text search over transcripts and minutes.
- Email alerts on keyword match — deferred past v1.
- A visible **corrections page** and a mechanism to report an error. The full policy is drafted in `legal-footing-v2.md` §6 and **must be live before the first meeting page publishes**, not after the first complaint.
- A disclosure that output is machine-generated and unreviewed, stated up front.
- The published accuracy number, updated on every benchmark run.

---

## 5. Legal and ethical constraints — non-negotiable

**Statutory footing (Nevada):**
- NRS 241.035(4) — a public body **shall** record every meeting; the recording **is a public record**, retained ≥3 years.
- NRS 241.035(2) — a copy of the minutes or audio recording must be provided to any member of the public on request **at no charge**.
- NRS 318.075(1) + NRS 241.015(5)(a)(2) — IVGID is a general improvement district and therefore a public body subject to Chapter 241. Verified via two independent routes.

**The defamation constraint — this shapes the product:**

NRS 241.0353 grants trustees absolute privilege for statements made in meetings.
Subsection (3) expressly withholds that privilege from **members of the public
giving public comment**. Republication doctrine means republishing a defamatory
public comment exposes the republisher. The defence is fair report, which requires
accuracy and report-framing.

**Therefore:**
- **Do not mirror IVGID's verbatim public-comment transcripts.** Report *that*
  comment was made, by whom, on what subject.
- Officials' statements in meetings may be quoted with a timestamp.
- Never publish an unverified allegation made by a member of the public as fact.
- Frame everything as a report of a meeting, not as an assertion by the project.

**Naming private citizens:** no settled civic-tech standard was found — the
Documenters Field Guide could not be read (JavaScript-gated). SPJ guidance applies:
legal access to information is not the same as ethical justification to publish.
**Default for v1: name officials, do not name private commenters.** Revisit only
with a documented standard.

**Corrections policy** must be published before the first meeting goes live. Error
reported → verified against source → corrected with a visible, dated correction
note → the git commit is the audit trail.

---

## 6. Free-tier budget

| Resource | Free allocation | Projected use | Headroom |
|---|---|---|---|
| Groq Whisper | 28,800 audio-sec/day | ~10 h/month | very large |
| Groq `llama-3.3-70b` | 1,000 req/day, 100k tok/day | Stage-B fallback only | large if Stage A works |
| Groq `llama-3.1-8b` | 14,400 req/day, 500k tok/day | classification legs | very large |
| GitHub Actions | unlimited on public repos | cron + build | fine (6h job cap) |
| Cloudflare Pages | unlimited static requests | hosting | fine |

**The binding constraint is `llama-3.3-70b` at 100k tokens/day.** That is roughly
25 long documents. It is the reason Stage A must be deterministic and Stage B must
be a genuine fallback rather than the default path.

Put the static extraction rulebook in a cached prefix — Groq does not count cached
tokens toward rate limits.

---

## 7. Build order

1. CivicClerk client with all six quirks handled, plus tests against real responses
2. PDF fetch and text extraction
3. Stage A deterministic parser for IVGID minutes
4. Benchmark harness + Augusta corpus → **first published accuracy number**
5. Stage B LLM fallback for parser misses
6. Cross-meeting item tracking
7. Static site with provenance links + corrections page + /accuracy page
8. **Ship. Publish.**

**Layer 2 gate — do not start audio work until all four are done:**
- A human review step exists for every published quote (see §3.5)
- Nevada fair report privilege — controlling authority located, not secondary summaries
- Corrections policy live
- Layer 1 accuracy number published

9. **Then:** audio download, transcription, alignment

**Do not build steps 1–8 in parallel.** Step 4 is a gate: if the accuracy number
is not publishable, nothing downstream matters.

---

## 8. Explicit non-goals for v1

- No email alerts
- No multi-jurisdiction support (the client should be written so it is possible, not shipped)
- No user accounts
- No LLM-written narrative summaries of meetings
- No mobile app
- No monetisation — CivicPlus ToS permits non-commercial use; revisit only after
  requesting files directly from the district
