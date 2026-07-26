# Project: Civic Meeting Record

Automated coverage of IVGID (Incline Village General Improvement District, Nevada)
public meetings. Publishes what was decided, with a verifiable source for every claim.

## Read first
- `docs/spec-v1.md` — the build spec. Authoritative.
- `docs/civicclerk-api.md` — verified API behaviour and quirks.
- `docs/legal-footing-v2.md` — legal and ethical constraints.

## Language and stack
Python 3.11+. Standard library plus: httpx, pdfplumber, pytest.
No database. Data is JSON committed to this repo.
No paid services. Everything must run on free tiers.

## Hard rules — violating any of these is a build failure
1. Votes come only from official minutes, never from transcription.
   If minutes are unavailable, report no vote at all.
2. Every published claim carries provenance (file ID + page, or video timestamp).
   A claim without provenance fails validation. It does not publish with a caveat.
3. Never publish a name derived from audio.
4. Officials are named. Private commenters are "a resident".
5. Deterministic parsing first; LLM only as fallback for what the parser misses.
6. Never use `$select` in CivicClerk API calls — it returns empty results.

## Working style
- Build one working end-to-end path before adding breadth.
- Tests against real recorded API responses, not mocks invented from the schema.
- Small commits, one concern each.
- If the spec and an instruction conflict, stop and say so. Do not guess.