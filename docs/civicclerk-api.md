# CivicClerk API — full map

**Verified:** 26 July 2026, by live unauthenticated requests. Every field name and value below was read off a real response.

**Correction to `source-recon.md` §A3:** I previously marked this API "⬜U — returned empty." **That was my error.** The API is fully open. My earlier calls failed because of `$` encoding in my fetcher, not because the endpoint was dead. Retracted.

---

## 1. Base and auth

```
https://{slug}.api.civicclerk.com/v1/
```

**Auth: none.** No key, no token, no Origin/Referer check. Plain GET.
**Protocol:** OData v4 (`@odata.context`, `@odata.nextLink`, `$filter`, `$orderby`, `$top`).

---

## 2. Endpoints verified live

| Endpoint | Status | Notes |
|---|---|---|
| `Events?$filter=…&$orderby=…` | ✅ 200 | Main entity. Everything you need is here. |
| `EventCategories` | ✅ 200 | Small payload. Body list + `id` for `categoryId` filtering. |
| `Meetings/GetMeetingFileStream(fileId={id},plainText=false)` | ✅ 200 | **Returns the actual PDF.** This is the file download endpoint. |
| `GetDaysInMonthWithEvents(date='…',categories=[])` | ✅ 200 (reported by you; not re-tested) | Calendar widget backing call. |

### Quirks that will bite you

1. **`$select` silently returns an empty result set.** Not an error — a `200` with `"value":[]`. Verified twice on `greenwoodvillageco`. **Do not use `$select`.** Fetch full objects and discard fields client-side.
2. **Server-side page cap is 15.** `$top=30` still returns 15. Follow `@odata.nextLink`, which carries a `$skiptoken` of the form `startDateTime-2026-11-16T18%3A00%3A00Z,id-4061`.
3. **`$filter` on `categoryId` works; combining `categoryId` with a date range worked only with the two-key orderby** `$orderby=startDateTime desc, eventName desc`. With a single-key orderby plus `$select` it returned empty. Use the two-key form.
4. **Default sort returns future events first.** Always pair with `startDateTime lt {today}` for past meetings.
5. `eventCategoryName eq 'City Council'` works as a string filter — useful when you don't know the numeric id.

### Working call templates

```
# past meetings, all bodies, newest first
GET /v1/Events?$filter=startDateTime+lt+2026-07-26&$orderby=startDateTime+desc,+eventName+desc

# past meetings for one body by numeric id
GET /v1/Events?$filter=categoryId+eq+26+and+startDateTime+lt+2026-07-26&$orderby=startDateTime+desc,+eventName+desc

# by body name
GET /v1/Events?$filter=eventCategoryName+eq+%27City+Council%27&$orderby=startDateTime+desc

# body list
GET /v1/EventCategories

# fetch a published file
GET /v1/Meetings/GetMeetingFileStream(fileId=2800,plainText=false)
```

---

## 3. `Events` schema — real values

~110 fields per event. The ones that matter, with **actual observed values**:

### Identity & scheduling
```
id                     4136
eventName              "Board of Adjustments and Appeals Regular Meeting"
eventDate              "2026-07-23T18:00:00Z"
startDateTime          "2026-07-23T18:00:00Z"
categoryId             28
eventCategoryName      "Board of Adjustments and Appeals"
eventTemplateName      "One Time Event" | "City Council Meeting"
eventDescription       "Third Monday of the Month at 6:00 PM"   ← cadence, in plain text
isPublished            "Published"
eventLocation.address1 "6060 S Quebec St"
eventLocation.city/state/zipCode
```

### Media — **the decisive block**
```
hasMedia               true
mediaStreamPath        "https://cpmedia.azureedge.net/greenwoodvillageco/8f1a01b698.mp4"
mediaSourcePathMp4     "https://cpmedia.azureedge.net/greenwoodvillageco/8f1a01b698.mp4"
mediaOrigFileName      "Board of Adjustments and Appeals Regular Meeting.mp4"
mediaAwsKeyName        "8f1a01b698.mp4"
liveStartTime          "2026-07-23T17:54:37.93Z"
liveEndTime            "2026-07-23T19:40:55.217Z"
mediaUploadedOn        "2026-07-23T19:41:25.8Z"
mediaTotalPlay         3
youtubeVideoId         ""      ← field exists; empty on all clients I sampled
externalMediaUrl       ""
closedCaptionSourcePath  null
closedCaptionFileName    null
closedCaptionStatus      null
```

**This is a direct MP4 on a CDN. Not a player embed. Not DRM. Not HLS.** A plain HTTP GET gets you the file.

**⚠️ Two URL forms — you must handle both:**
- Absolute: `https://cpmedia.azureedge.net/{slug}/{hash}.mp4`
- **Relative:** `stream/GREENWOODVILLAGECO/{guid}.mp4` — observed on `greenwoodvillageco` 2026-05-18, and dominant on `bristolct` and `portlandme`. **The base for this form is not established.** ⬜U — resolve it from the portal's network tab before building.

**⚠️ `liveStartTime`/`liveEndTime` are unreliable for duration.** Mostly correct (IVGID 2026-07-22: 16:04→18:28 = 2h24m ✓) but sometimes span days (IVGID 2026-06-10: 16:04 Jun 10 → 13:13 Jun 11 = 21h; Greenwood Village Municipal Court showed 1,541 min). The stream almost certainly wasn't stopped. **Derive duration from the MP4, not from these fields.**

**`closedCaption*` fields were null on every event I sampled across 10 clients.** The plumbing exists; nobody in my sample uses it.

### Files
```
hasAgenda              true
publishedAgendaTimeStamp "Agenda Posted on July 16, 2026 10:17 AM"
publishedFiles: [
  { fileId: 10889, type: "Agenda",        name: "Final Agenda July.23.2026",
    url: "stream/GREENWOODVILLAGECO/87967595-411c-44d6-986c-05d4e002d846.pdf",
    publishOn: "2026-07-16T10:17:34.987Z", sort: 1, fileType: 1 },
  { fileId: 10890, type: "Agenda Packet", name: "Agenda Packet July.23.2026", ... }
]
agendaFile   { agendaId, fileName, dateUploaded, createdBy }   ← null in practice
minutesFile  { minutesId, eventId, fileName, createdOn, ... }  ← null in practice
```

**`publishedFiles[].type` observed values: `Agenda`, `Agenda Packet`, `Minutes`, `Notice`, `Other`.**

**Ignore `agendaFile` and `minutesFile`** — they were empty stubs on every event across every client. All real files live in `publishedFiles[]`.

**Fetch a file by `fileId`, not by `url`:**
`GET /v1/Meetings/GetMeetingFileStream(fileId=10889,plainText=false)` → `Content-Type: application/pdf`, **text-extractable**. Verified on Greenwood Village and IVGID.

---

## 4. What CivicClerk does NOT give you

Important, because it changes the build versus Legistar:

- ❌ **No agenda-item entity.** No per-item rows, no item IDs, no `EventItems` equivalent. Agenda structure exists only as text inside the PDF.
- ❌ **No mover / seconder / tally / passed fields.** Votes exist only as prose in the minutes PDF.
- ❌ **No per-item video index.** *(But see the IVGID exception in `final-recommendation.md` — that district writes media timestamps into its minutes by hand, which is better than a database field because it is human-verified.)*
- ❌ **No captions in practice.**

So: **CivicClerk gives superb media and file access, and zero structured legislative data.** Legistar is the reverse — rich structure, video behind a Granicus handle. Neither is strictly better.

---

## 5. Video posture and terms of service

### Where the media actually lives
`cpmedia.azureedge.net` — CivicPlus's Azure CDN. The content is the **municipality's public meeting recording**; CivicPlus is the host. No login, no signed URL, no token in the paths I observed.

### CivicPlus Terms of Use — quoted ✅V
Fetched from `https://www.civicplus.com/terms-of-use/` (page last modified 2023-10-18):

> **"3. Permitted Use of the Products and Site** — You may use the CivicPlus proprietary websites (individually and collectively, the "Site"), and the information, writings, images and/or other works that you see, hear or otherwise experience on the Site (singly or collectively, the "Site Content") **solely for your non-commercial, personal purposes** and/or to learn about CivicPlus Solutions, products and services, and solely in compliance with these TOS."

And notably:

> **"16. Downloading Files** — CivicPlus cannot and does not guarantee or warrant that files available for downloading through the Site or any Solution will be free of infection by software viruses or other harmful computer code, files or programs."

### Reading, stated carefully

**Much better than YouTube, with one real limit.**

1. **There is no prohibition on downloading.** §16 contemplates downloading and merely disclaims a virus warranty. Contrast YouTube's ToS, which prohibits "access, reproduce, download…" outright. **This removes the single sharpest legal obstacle identified in `legal-footing.md` §3.**
2. **"Non-commercial, personal purposes" is a genuine constraint.** A free public-interest accountability site is a comfortable fit. A paid product is not. **If this ever monetises, revisit — and by then you should be asking the district for the files directly anyway.**
3. ⬜U **Scope is unresolved.** These TOS sit on `civicplus.com`, CivicPlus's own marketing site, with `meta-robots: noindex`. Whether they govern `{slug}.api.civicclerk.com` and `cpmedia.azureedge.net` — which serve a *municipality's* public records — is **not established**. There is a strong argument they do not: the recordings are public records of a public body under state open-meetings law, and a vendor's marketing-site TOS cannot convert a public record into private property.
4. **The clean move remains the same:** ask the district. IVGID's own agenda footer states recordings are posted to five public locations including the state noticing site. A clerk who publishes that widely is not going to object to a transcript project.

**No robots.txt or crawl-delay check was performed on `cpmedia.azureedge.net`.** ⬜U — do that, and rate-limit politely regardless.

---

## 6. Slug enumeration

Confirmed live slugs (each returned 200 from the API):

| Slug | Jurisdiction | Video? |
|---|---|---|
| `ivgid` | Incline Village General Improvement District, NV | **14/15** ✅ |
| `middletownnj` | Middletown Township, NJ | **14/15** ✅ |
| `greenwoodvillageco` | Greenwood Village, CO | **11 council videos / 5 mo** ✅ |
| `portlandme` | Portland, ME | many ✅ |
| `bristolct` | Bristol, CT | 5/15, partial ⚠️ |
| `glenellynil` | Glen Ellyn, IL | 3/15, Village Board only ⚠️ |
| `stanlyconc` | Stanly County, NC | **0** ❌ |
| `mcfarlandwi` | Village of McFarland, WI | **0** ❌ |
| `essexvt` | Town of Essex, VT | **0** ❌ |
| `abingtonpa` | Abington Township, PA | **0** ❌ |
| `wbtownshipmi` | West Bloomfield Township, MI | **0** ❌ |
| `mobileal`, `vancouverwa`, `vallejoca`, `saltlakecounty`, `greenbaywi`, `rankincoms`, `santarosacosdfl`, `lenaweecomi`, `usbe` | various, mostly out of population band | not tested |

**Naming convention:** `{cityname}{state}` (`bristolct`), `{county}co{state}` (`stanlyconc`, `lenaweecomi`), or an acronym (`ivgid`, `usbe`). Predictable enough to brute-force.

**Enumeration method that worked:** site-restricted search for `portal.civicclerk.com`. Better method for scale ⬜U: CivicPlus publishes customer lists, and `EventCategories` is a cheap 200/404 probe (~1 KB) for testing guessed slugs.

---

## 7. The structural finding that matters most

**Video is a paid add-on module, and its presence tracks municipal wealth.**

Of the eleven clients I tested for video: the five with zero video are a rural NC county, a Wisconsin village, a Vermont town, a Pennsylvania township and a Michigan township — **exactly the small, thin-budget places that are most likely to be news deserts.** The ones with video are a wealthy Denver suburb, a Nevada resort district, a New Jersey commuter township, and three cities over 60,000.

**This is the central tension in P16 and it is now measured, not guessed:**

> The jurisdictions that most need automated meeting coverage are the least likely to have the video that makes it possible.

Consequences, carried forward into `final-recommendation.md`:
- The video filter is not a formality. It eliminated 5 of 11 CivicClerk candidates outright.
- It also **anti-selects for news deserts**, so expect the chosen jurisdiction to have *some* press.
- The genuinely uncovered small places (Stanly County NC, McFarland WI, Essex VT) all publish **agendas, packets and minutes** — they are viable for a **document-only** product, just not an audio one. That is a real fallback and it is cheap, because the same `GetMeetingFileStream` endpoint serves them all.

**⚠️ Caveat added 26 July 2026:** "zero video in CivicClerk" ≠ "no recording exists." Vermont's Open Meeting Law, effective 1 July 2024, **requires** non-advisory public bodies to record meetings and post them electronically for at least 30 days after minutes are approved 🟡P. So `essexvt`'s 0/15 means the recording is not *in CivicClerk* — not that it is not made. See `legal-footing-v2.md` Part II. **Check the town's own site before classifying any jurisdiction as document-only.**

---

## 8. Media variants — is there anything lighter than the 2 GB MP4?

**Confirmed by you:** `https://cpmedia.azureedge.net/ivgid/104a898503.mp4` downloads as a plain public file, **2.0 GB for a 2h24m meeting** (≈1.9 Mbps). No `robots.txt` on that host (404).

**Short answer: no lighter variant exists. Strip audio during download.**

### 8.1 Every media field in the `Events` schema, checked on IVGID event 743

I dumped all ~110 fields and filtered for anything media-related. **Every alternate-representation field is empty:**

| Field | Value on IVGID 743 | Reading |
|---|---|---|
| `mediaStreamPath` | `https://cpmedia.azureedge.net/ivgid/104a898503.mp4` | the only populated path |
| `mediaSourcePathMp4` | *identical string* | **not a second rendition — the same URL** |
| `mediaSourcePath` | `''` | empty |
| `mobileMediaStreamPath` | `''` | **empty — no mobile rendition** |
| `mobileMediaSourcePath` | `''` | empty |
| `mobileMediaOrigFileName` | `''` | empty |
| `externalMediaUrl` | `''` | empty |
| `youtubeVideoId` | `''` | empty; `youtubeVideoUploaded` = 0 |
| `jwPlayerCode` | `null` | no JW Player manifest |
| `zoomMeetingId` | `null` | — |
| `closedCaptionSourcePath` | `null` | **no captions** |
| `closedCaptionBlobPath` | `null` | — |
| `closedCaptionStatus` / `FileName` / `FileType` | `null` | `closedCaptionSeconds` = 0, `closedCaptionCost` = 0 |
| `mediaAwsKeyName` | `104a898503.mp4` | just the filename |
| `mediaFileSize` | `0` | **unpopulated — you cannot size-check via the API** |
| `mediaTypeId` | `1` (IVGID) vs `2` (Greenwood Village) | ⬜U meaning unknown; possibly upload-vs-live origin |
| `streamId` | `1` | ⬜U |
| `streamingStatus` | `0` | not live |
| `cpMediaOnly` | `false` | ⬜U |

**The `mobileMedia*` triplet is the significant negative.** CivicClerk clearly *supports* a separate mobile rendition — three dedicated fields exist for it — but IVGID has not generated one. ⬜U whether any client populates it; worth one probe against `portlandme` or `vancouverwa`, since a mobile rendition would be exactly the lighter file you want.

### 8.2 CDN path probes

| URL tried | Result |
|---|---|
| `…/ivgid/104a898503.m3u8` | empty response — no HLS manifest at the sibling path |
| `…/ivgid/104a898503.mp3` | empty response — no audio-only sibling |

Both ⬜U as to exact status code — my fetcher returns empty for both 404s and binary payloads, so I **cannot distinguish "absent" from "present but unrenderable."** Confirm with `curl -I` before concluding absolutely. The absence of `jwPlayerCode` and of any manifest field in the schema is the stronger evidence: the portal has nothing to point a streaming player at.

### 8.3 What the portal player actually requests — ⬜U

**Not verified.** The portal is a JS SPA and I could not observe its network activity. Given `mediaStreamPath` is a direct `.mp4` and no manifest or player-code field is populated, **the overwhelmingly likely behaviour is a plain HTML5 `<video src>` against that MP4, relying on HTTP Range requests for seeking.** That is a prediction, not an observation. Check the Network tab — it takes a minute and would also settle 8.2.

### 8.4 Consequence for the pipeline

**Progressive MP4 interleaves audio and video.** There is no way to fetch only the audio track from a single-file MP4 without transferring essentially the whole file. So:

- **Bytes over the wire: ~2 GB per meeting — unavoidable from this source.**
- **Bytes stored: ~20–35 MB**, if you transcode on the fly.

Practical form — never write the MP4 to disk:

```bash
ffmpeg -i "https://cpmedia.azureedge.net/ivgid/104a898503.mp4" \
       -vn -ac 1 -ar 16000 -c:a libopus -b:a 16k \
       meeting.opus
```

`-vn` drops video; mono 16 kHz is what Whisper wants anyway; Opus at 16 kbps gives roughly **17 MB for 2h24m** — a ~120× reduction. ffmpeg streams over HTTP and discards video frames as they arrive.

**Volume check.** IVGID ran ~14 recorded meetings in six months ≈ 28/year × 2 GB ≈ **56 GB/year of ingress**. On GitHub Actions (public repo, unmetered minutes) that is comfortable — but it is exactly the usage that should be **rate-limited and scheduled off-peak**, out of courtesy to a CDN whose bandwidth a 9,200-person district is paying for. One meeting per run, nightly, with a conditional check on `mediaUploadedOn` so you never re-download.

**The better long-term answer is Part I of `legal-footing-v2.md`.** NRS 241.035(2) entitles you to a **copy of the audio recording, free, on request**, and NRS 241.035(4) requires the district to make an audio recording of every meeting. The *audio* recording is likely far smaller than the video file. **Asking the clerk for audio is not just politeness — it is the cheapest technical fix available, and Nevada law says they must provide it.** Add it to the clerk email.

### 8.5 Open probes

| # | Probe | Cost |
|---|---|---|
| 1 | `curl -I` on the `.m3u8` and `.mp3` paths for real status codes | 2 min |
| 2 | Does `cpmedia.azureedge.net` honour `Range:`? (`curl -r 0-1023 -I`) | 2 min |
| 3 | Portal Network tab — what does the player request? | 5 min |
| 4 | Is `mobileMediaStreamPath` populated on *any* client? | 10 min |
| 5 | Ask IVGID for the audio-only recording under NRS 241.035(2) | one email |

**Probe 5 is the one that eliminates the problem rather than mitigating it.**
