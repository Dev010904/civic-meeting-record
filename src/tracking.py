"""Cross-meeting item tracking — spec §2.5, build step 6b.

Reads the committed per-meeting records in ``data/meetings/`` and reports
what they show about items that recur across meetings. This is the layer
spec §2.5 calls "the differentiating feature": the findings no summariser
produces and no resident can assemble by hand.

Deterministic matching only. No LLM anywhere in this module.

**Conservatism is the design constraint.** A wrong link between two
unrelated items is far worse than a missed link, because it produces a
false claim about a public body. Three consequences run through everything
below:

1. Every finding carries a ``confidence``. ``asserted`` is used only where
   the records share a unique identifier — a CIP/Project code, or an
   identical normalised title. Everything weaker is a ``candidate``,
   recorded as a possible link rather than presented as a fact.
2. Title matching strips procurement boilerplate before comparing. Two
   unrelated contracts both open "Approve and Authorize the Board Chair and
   Board Secretary to Sign and Execute an Agreement between Incline Village
   General Improvement District and …"; comparing raw titles would score
   that near-identical. Only the distinctive remainder is compared, and a
   match needs enough distinctive tokens on both sides to mean anything.
3. Findings are phrased as reports of what the records show, never as
   assertions by the project (spec §2.7, §5). "Item H.1 does not appear in
   the minutes of any later meeting in the published set" — never "the
   board quietly dropped it". Absence claims are always scoped to the
   published set, which is 39 meetings, not the whole archive.

Provenance (spec §2.7 rule 7) is required on both ends of every link: file
id and page for each meeting involved. A finding missing either end fails
:func:`validate_finding` and is not written.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any, Optional

JURISDICTION = "ivgid"
SCHEMA_VERSION = 1

CONFIDENCE_ASSERTED = "asserted"
CONFIDENCE_CANDIDATE = "candidate"

PATTERNS = {
    "project_referenced_at_multiple_meetings": (
        "The same CIP/Project code recorded at more than one meeting, with "
        "the amounts each meeting's minutes record against it. This is the "
        "matching layer of spec §2.5 made visible: the project code is the "
        "one unique identifier in the corpus, so these links are the only "
        "ones that can be asserted rather than offered as candidates. It "
        "reports that the same project was before the board more than once "
        "and what figures appear each time — not that one figure replaced "
        "another, which the minutes alone do not establish."
    ),
    "amount_increase_after_prior_approval": (
        "A motion raising, extending or adding to an amount the records show "
        "was committed at an earlier meeting (spec §2.5: a change order "
        "raising a previously approved amount). Distinguished from the "
        "pattern above by explicit increase language in the later motion — "
        "a change order, additional funding, or a contract amendment."
    ),
    "continued_then_acted": (
        "An item the records show was continued, tabled or deferred at one "
        "meeting and taken up at a later one (spec §2.5)."
    ),
    "agenda_removal_vote": (
        "A recorded vote on removing an item from the agenda, and what the "
        "published records show about that item afterwards."
    ),
    "item_vanished_from_agenda": (
        "An item the minutes show was explicitly removed — named in a "
        "recorded removal vote, or carrying a note that staff removed it — "
        "which produced no motion of its own, with what the published set "
        "shows about it afterwards (spec §2.5). Restricted to explicit "
        "removals: an item simply appearing once and not returning is the "
        "ordinary shape of a discussion or report item, not a finding."
    ),
}

# Patterns that link two or more meetings. Findings of these types must
# carry provenance at every end, and must span more than one meeting.
LINKING_PATTERNS = frozenset({
    "project_referenced_at_multiple_meetings",
    "amount_increase_after_prior_approval",
    "continued_then_acted",
})

# --- Normalisation --------------------------------------------------------

# Boilerplate that appears in most IVGID item titles and carries no
# distinguishing information. Removed before any similarity comparison —
# without this, two unrelated procurement items score as near-identical.
_BOILERPLATE = frozenset("""
a an and the of for to at in on or with as be by is are this that these those
review reviewed discuss discussed discussion possibly possible action actions
approve approved approval authorize authorized authorization execute execution
sign signed board chair secretary trustees trustee district general improvement
incline village agreement contract consider consideration considering provide
provides providing direction regarding update updates report reports item items
requesting request staff member members director finance recreation parks
public works manager fiscal year years following further such shall may will
new proposed amended restated between from into per its it their our
""".split())

_STAFF_PAREN_RE = re.compile(
    r"\((?:requesting|for\s+possible|not\s+for\s+possible)[^)]*\)", re.IGNORECASE
)
_MEDIA_TAIL_RE = re.compile(
    r"\bbe\s+(?:viewed|heard|watched|listened)[\s\S]*$", re.IGNORECASE
)
# Minimum distinctive tokens on each side before a similarity score means
# anything, and the score a candidate link must reach.
MIN_DISTINCTIVE_TOKENS = 3
CANDIDATE_SIMILARITY = 0.6


def normalise_title(title: Optional[str]) -> str:
    """Lowercase, strip the staff parenthetical and any media-reference tail,
    drop punctuation and collapse whitespace. Verbatim words are preserved —
    this is only for comparison, never for output."""
    if not title:
        return ""
    text = _STAFF_PAREN_RE.sub(" ", title)
    text = _MEDIA_TAIL_RE.sub(" ", text)
    text = re.sub(r"[^a-z0-9]+", " ", text.lower())
    return re.sub(r"\s+", " ", text).strip()


def distinctive_tokens(title: Optional[str]) -> frozenset[str]:
    """The tokens of a title that actually distinguish it, boilerplate and
    bare numbers removed."""
    return frozenset(
        t for t in normalise_title(title).split()
        if t not in _BOILERPLATE and len(t) > 2 and not t.isdigit()
    )


def similarity(left: Optional[str], right: Optional[str]) -> float:
    """Jaccard overlap of distinctive tokens. Returns 0.0 when either side
    is too thin to compare — a near-empty title must never match anything."""
    a, b = distinctive_tokens(left), distinctive_tokens(right)
    if len(a) < MIN_DISTINCTIVE_TOKENS or len(b) < MIN_DISTINCTIVE_TOKENS:
        return 0.0
    return len(a & b) / len(a | b)


def contract_key(ref: Optional[str]) -> Optional[str]:
    """A CIP/Project/GL code reduced to comparable form. These are the only
    unique identifiers in the corpus — "CIP #2221WS22601" and
    "CIP#2221WS22601" are the same project — so they are the one basis
    strong enough to assert a link on."""
    if not ref:
        return None
    key = re.sub(r"[^A-Z0-9]", "", ref.upper())
    return key or None


def vendor_key(vendor: Optional[str]) -> Optional[str]:
    if not vendor:
        return None
    key = re.sub(r"[^a-z0-9]", "", vendor.lower())
    return key or None


# --- Records --------------------------------------------------------------


@dataclass(frozen=True)
class Endpoint:
    """One end of a cross-meeting link, carrying its own provenance."""

    meeting_id: str
    date: str
    body: str
    file_id: int
    page: int
    item_number: Optional[str]
    item_title: Optional[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "meeting_id": self.meeting_id,
            "date": self.date,
            "body": self.body,
            "item_number": self.item_number,
            "item_title": self.item_title,
            "provenance": {
                "type": "pdf",
                "file_id": self.file_id,
                "page": self.page,
            },
        }


@dataclass
class Finding:
    pattern: str
    confidence: str
    match_basis: str
    summary: str
    endpoints: list[Endpoint]
    detail: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "pattern": self.pattern,
            "confidence": self.confidence,
            "match_basis": self.match_basis,
            "summary": self.summary,
            "endpoints": [e.to_dict() for e in self.endpoints],
            "detail": self.detail,
        }


def _endpoint(record: dict[str, Any], item: dict[str, Any], page: int) -> Endpoint:
    return Endpoint(
        meeting_id=record["meeting_id"],
        date=record["date"],
        body=record["body"],
        file_id=record["source"]["minutes_file_id"],
        page=page,
        item_number=item.get("number"),
        item_title=item.get("title"),
    )


def _uk_date(iso: str) -> str:
    """'2025-05-14' -> '14 May 2025', for readable summary prose."""
    months = ("January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December")
    year, month, day = iso.split("-")
    return f"{int(day)} {months[int(month) - 1]} {year}"


def _item_page(item: dict[str, Any], fallback: int = 1) -> int:
    """The page this item is traceable to: where its heading appears, or
    failing that the earliest page any claim on it was drawn from. A
    motion-free item has only the heading, which is why records carry it."""
    if isinstance(item.get("page"), int) and item["page"] >= 1:
        return item["page"]
    pages = [m["provenance"]["page"] for m in item["motions"]]
    pages += [m["provenance"]["page"] for m in item["money"]]
    return min(pages) if pages else fallback


def _amounts(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """The amount fields carried into a finding's detail, deduplicated and
    ordered so the payload is stable across builds."""
    seen = {
        (m["amount_raw"], m["role"], str(m["vendor"]), str(m["purpose"])): {
            "amount_raw": m["amount_raw"],
            "amount_usd": m["amount_usd"],
            "role": m["role"],
            "vendor": m["vendor"],
            "purpose": m["purpose"],
            "flags": m["flags"],
        }
        for m in entries
    }
    return [seen[key] for key in sorted(seen)]


def _occurrences(records: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Every (record, item, money entries) grouped by project code.

    The CIP/Project code is the only unique identifier in the corpus, so it
    is the one key strong enough to assert identity on.
    """
    index: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        for item in record["items"]:
            by_key: dict[str, list[dict[str, Any]]] = {}
            for money in item["money"]:
                key = contract_key(money["contract_ref"])
                if key:
                    by_key.setdefault(key, []).append(money)
            for key, entries in by_key.items():
                index.setdefault(key, []).append(
                    {"record": record, "item": item, "money": entries}
                )
    return index


# --- Pattern: the same project before the board more than once ------------


def detect_project_links(records: list[dict[str, Any]]) -> list[Finding]:
    """Report each project code that appears at more than one meeting.

    One finding per project, with an endpoint per meeting — not one per
    pair of amounts. Pairing every earlier figure with every later one
    would imply comparisons the minutes do not make: a contingency ceiling
    is not comparable to a principal, and a donor's share is not comparable
    to a project total. The finding reports what each meeting recorded and
    leaves the comparison to the reader.
    """
    findings: list[Finding] = []
    for key, occurrences in _occurrences(records).items():
        if len({o["record"]["meeting_id"] for o in occurrences}) < 2:
            continue
        ordered = sorted(
            occurrences,
            key=lambda o: (o["record"]["date"], o["record"]["meeting_id"],
                           o["item"].get("number") or ""),
        )
        ref = next(
            (m["contract_ref"] for o in ordered for m in o["money"] if m["contract_ref"]),
            key,
        )
        # Distinct meeting dates, oldest first, without repeating a date that
        # carries the reference on more than one item.
        dates = " and ".join(
            dict.fromkeys(_uk_date(o["record"]["date"]) for o in ordered)
        )
        findings.append(
            Finding(
                pattern="project_referenced_at_multiple_meetings",
                confidence=CONFIDENCE_ASSERTED,
                match_basis=f"shared project reference {ref}",
                summary=(
                    f"The minutes of {dates} each record amounts against {ref}. "
                    "The figures recorded at each meeting are listed below, with "
                    "the page each was drawn from."
                ),
                endpoints=[
                    _endpoint(o["record"], o["item"], _item_page(o["item"]))
                    for o in ordered
                ],
                detail={
                    "contract_ref": ref,
                    "meetings": [
                        {
                            "meeting_id": o["record"]["meeting_id"],
                            "date": o["record"]["date"],
                            "item_number": o["item"].get("number"),
                            "amounts": _amounts(o["money"]),
                        }
                        for o in ordered
                    ],
                },
            )
        )
    return _dedupe(findings)


# --- Pattern: amount raised after a prior approval ------------------------

# Motions that add to, raise or extend money already committed. Each of
# these is an explicit clerk formulation, not an inference from the numbers.
_INCREASE_RE = re.compile(
    r"\bchange\s+order\b"
    r"|\badditional\s+funding\b"
    r"|\bincreasing\s+the\b[\s\S]{0,60}?\bcontract\b"
    r"|\bcontract\s+amendment\b"
    r"|\badditional\s+\$"
    r"|\bbudget\s+transfer\b",
    re.IGNORECASE,
)


def _increase_motion(item: dict[str, Any]) -> Optional[dict[str, Any]]:
    """The item's motion carrying explicit increase language, if any."""
    for motion in item["motions"]:
        if _INCREASE_RE.search(motion["text"]):
            return motion
    return None


def _increase_finding(
    earlier: dict[str, Any],
    later: dict[str, Any],
    motion: dict[str, Any],
    confidence: str,
    basis: str,
) -> Finding:
    outcome = motion["outcome"] or "carrying no recorded outcome"
    return Finding(
        pattern="amount_increase_after_prior_approval",
        confidence=confidence,
        match_basis=basis,
        summary=(
            f"The minutes of {_uk_date(earlier['record']['date'])} record amounts "
            f"under item {earlier['item'].get('number')}. The minutes of "
            f"{_uk_date(later['record']['date'])} record a motion under item "
            f"{later['item'].get('number')} referring to a change order, additional "
            f"funding or a contract amendment; that motion is recorded as {outcome}. "
            "The figures on each side are listed below."
        ),
        endpoints=[
            _endpoint(earlier["record"], earlier["item"], _item_page(earlier["item"])),
            _endpoint(later["record"], later["item"], motion["provenance"]["page"]),
        ],
        detail={
            "earlier_amounts": _amounts(earlier["money"]),
            "later_amounts": _amounts(later["money"]),
            "later_motion_text": motion["text"],
            "later_motion_outcome": motion["outcome"],
        },
    )


def detect_amount_increases(records: list[dict[str, Any]]) -> list[Finding]:
    """Link a motion that raises an amount to the earlier meeting whose
    records show money already committed to the same project or vendor.

    Asserted only on a shared CIP/Project code. A shared vendor is recorded
    as a candidate instead: the same firm can hold several unrelated
    contracts with the district, so a vendor name is not identity. Either
    way the later motion must carry explicit increase language, so the
    pattern rests on what the clerk wrote rather than on comparing numbers.
    """
    findings: list[Finding] = []
    for key, occurrences in _occurrences(records).items():
        ordered = sorted(
            occurrences,
            key=lambda o: (o["record"]["date"], o["record"]["meeting_id"]),
        )
        for position, later in enumerate(ordered):
            motion = _increase_motion(later["item"])
            if motion is None:
                continue
            for earlier in ordered[:position]:
                if earlier["record"]["meeting_id"] == later["record"]["meeting_id"]:
                    continue
                ref = next(
                    (m["contract_ref"] for m in later["money"] if m["contract_ref"]),
                    key,
                )
                findings.append(
                    _increase_finding(
                        earlier, later, motion, CONFIDENCE_ASSERTED,
                        f"shared project reference {ref}",
                    )
                )

    # Vendor-based candidates, only where no project code already links the
    # two meetings and the item titles overlap on distinctive words.
    linked = {(f.endpoints[0].meeting_id, f.endpoints[-1].meeting_id) for f in findings}
    for position, record in enumerate(records):
        for item in record["items"]:
            motion = _increase_motion(item)
            if motion is None:
                continue
            vendors = {vendor_key(m["vendor"]) for m in item["money"]} - {None}
            if not vendors:
                continue
            for prior in records[:position]:
                if (prior["meeting_id"], record["meeting_id"]) in linked:
                    continue
                for prior_item in prior["items"]:
                    shared = vendors & (
                        {vendor_key(m["vendor"]) for m in prior_item["money"]} - {None}
                    )
                    if not shared:
                        continue
                    if similarity(item["title"], prior_item["title"]) < CANDIDATE_SIMILARITY:
                        continue
                    name = next(
                        (m["vendor"] for m in item["money"]
                         if vendor_key(m["vendor"]) in shared),
                        None,
                    )
                    findings.append(
                        _increase_finding(
                            {"record": prior, "item": prior_item,
                             "money": prior_item["money"]},
                            {"record": record, "item": item, "money": item["money"]},
                            motion, CONFIDENCE_CANDIDATE,
                            f"shared vendor {name!r} and overlapping item title",
                        )
                    )
    return _dedupe(findings)


# --- Pattern: continued or tabled, then acted on --------------------------

# A deliberate continuation, not the word "table" in "(Table 1)". Each form
# requires the verb to govern an item or a future meeting.
_CONTINUED_RE = re.compile(
    r"\b(?:continue|continued|postpone|postponed|defer|deferred|tabled)\b"
    r"[\s\S]{0,50}?\b(?:item|matter|until|to\s+the\s+(?:next|meeting|board))"
    r"|\bto\s+table\s+(?:this|the)\b",
    re.IGNORECASE,
)


def _title_link_basis(
    left: dict[str, Any], right: dict[str, Any]
) -> Optional[tuple[str, str]]:
    """How strongly two items are linked by title, or None for no link."""
    left_refs = {contract_key(m["contract_ref"]) for m in left["money"]} - {None}
    right_refs = {contract_key(m["contract_ref"]) for m in right["money"]} - {None}
    shared = left_refs & right_refs
    if shared:
        return CONFIDENCE_ASSERTED, f"shared project reference {sorted(shared)[0]}"
    left_norm = normalise_title(left["title"])
    right_norm = normalise_title(right["title"])
    if left_norm and left_norm == right_norm:
        return CONFIDENCE_ASSERTED, "identical normalised item title"
    if similarity(left["title"], right["title"]) >= CANDIDATE_SIMILARITY:
        return CONFIDENCE_CANDIDATE, "overlapping distinctive title tokens"
    return None


def detect_continuations(records: list[dict[str, Any]]) -> list[Finding]:
    """Link an item the records show was continued to the later meeting that
    took it up. Asserted only on an identical normalised title or a shared
    project reference; anything weaker is a candidate."""
    findings: list[Finding] = []
    for index, record in enumerate(records):
        for item in record["items"]:
            for motion in item["motions"]:
                if not _CONTINUED_RE.search(motion["text"]):
                    continue
                page = motion["provenance"]["page"]
                for later in records[index + 1:]:
                    for later_item in later["items"]:
                        basis = _title_link_basis(item, later_item)
                        if basis is None:
                            continue
                        confidence, why = basis
                        findings.append(
                            Finding(
                                pattern="continued_then_acted",
                                confidence=confidence,
                                match_basis=why,
                                summary=(
                                    f"The minutes of {_uk_date(record['date'])} record a "
                                    f"motion on item {item['number']} referring to "
                                    "continuing, tabling or deferring the matter. The "
                                    f"minutes of {_uk_date(later['date'])} record item "
                                    f"{later_item['number']} on a matching title."
                                ),
                                endpoints=[
                                    _endpoint(record, item, page),
                                    _endpoint(later, later_item, _item_page(later_item)),
                                ],
                                detail={
                                    "continuing_motion_text": motion["text"],
                                    "continuing_motion_outcome": motion["outcome"],
                                    "later_disposition": later_item["disposition"],
                                },
                            )
                        )
    return _dedupe(findings)


# --- Pattern: votes to remove an item from the agenda ---------------------

_REMOVAL_RE = re.compile(
    r"\bremov\w+\b[\s\S]{0,250}?\bfrom\s+the\s+agenda\b"
    r"|\bfrom\s+the\s+agenda\b[\s\S]{0,80}?\bremov\w+",
    re.IGNORECASE,
)
# The item the removal motion names ("Removing Item H.1. …", "remove Item
# H.5. from the Agenda").
_TARGET_ITEM_RE = re.compile(r"\bitem\s+([A-Z]\.\d+)", re.IGNORECASE)


def _tally_phrase(motion: dict[str, Any]) -> str:
    aye, nay = motion["tally"].get("aye"), motion["tally"].get("nay")
    if aye is None or nay is None:
        return "vote counts not fully recorded"
    return f"{aye} in favour, {nay} against"


def detect_agenda_removals(records: list[dict[str, Any]]) -> list[Finding]:
    """Report each recorded vote on removing an item from an agenda, and
    what the published records show about the named item afterwards.

    Found during the new-blocks verification: two of the five newly
    surfaced decision blocks were this manoeuvre, neither recorded as a
    formal motion. Where the named item does not reappear, that is reported
    as an absence from the published set — which is not the same as an
    absence from the district's record, and is worded so.
    """
    findings: list[Finding] = []
    for index, record in enumerate(records):
        for item in record["items"]:
            for motion in item["motions"]:
                if not _REMOVAL_RE.search(motion["text"]):
                    continue
                page = motion["provenance"]["page"]
                targets = sorted(
                    {m.group(1).upper() for m in _TARGET_ITEM_RE.finditer(motion["text"])}
                )
                endpoints = [_endpoint(record, item, page)]
                later_hits: list[dict[str, Any]] = []
                # The item the vote was about sits in this same meeting's
                # agenda. Before the record layer carried motion-free items
                # it was invisible, so the vote could not be linked to what
                # it was aimed at.
                same_meeting: list[dict[str, Any]] = []
                for target in targets:
                    for target_item in record["items"]:
                        if (target_item.get("number") or "").upper() != target:
                            continue
                        same_meeting.append({
                            "target": target,
                            "item_title": target_item.get("title"),
                            "motions_recorded": len(target_item["motions"]),
                            "disposition": target_item["disposition"],
                        })
                        endpoints.append(
                            _endpoint(record, target_item, _item_page(target_item))
                        )
                for target in targets:
                    for later in records[index + 1:]:
                        for later_item in later["items"]:
                            if (later_item.get("number") or "").upper() != target:
                                continue
                            if similarity(item["title"], later_item["title"]) \
                                    < CANDIDATE_SIMILARITY:
                                continue
                            later_hits.append({
                                "target": target,
                                "meeting_id": later["meeting_id"],
                                "date": later["date"],
                            })
                            endpoints.append(
                                _endpoint(later, later_item, _item_page(later_item))
                            )
                outcome_phrase = {
                    "failed": "The motion is recorded as failed",
                    "passed": "The motion is recorded as passed",
                }.get(motion["outcome"], "No outcome is recorded for the motion")
                plural = "s" if len(targets) > 1 else ""
                named = f", naming item{plural} {', '.join(targets)}" if targets else ""
                summary = (
                    f"The minutes of {_uk_date(record['date'])} record a vote on "
                    f"removing an item from the agenda{named}. {outcome_phrase} "
                    f"({_tally_phrase(motion)})."
                )
                for hit in same_meeting:
                    if hit["motions_recorded"]:
                        summary += (
                            f" Item {hit['target']} of the same meeting records "
                            f"{hit['motions_recorded']} motion(s)."
                        )
                    else:
                        summary += (
                            f" Item {hit['target']} appears on the agenda of the same "
                            "meeting with no motion recorded against it."
                        )
                if targets and not later_hits:
                    summary += (
                        f" The published set contains no later meeting whose minutes "
                        f"record item{plural} {', '.join(targets)} on a matching title."
                    )
                findings.append(
                    Finding(
                        pattern="agenda_removal_vote",
                        confidence=CONFIDENCE_ASSERTED,
                        match_basis="removal language in a recorded vote",
                        summary=summary,
                        endpoints=endpoints,
                        detail={
                            "motion_text": motion["text"],
                            "outcome": motion["outcome"],
                            "flags": motion["flags"],
                            "notes": motion["notes"],
                            "tally": motion["tally"],
                            "yeas": motion["yeas"],
                            "nays": motion["nays"],
                            "named_items": targets,
                            "same_meeting_targets": same_meeting,
                            "later_appearances": later_hits,
                        },
                    )
                )
    return _dedupe(findings)


# --- Pattern: an item explicitly removed from an agenda -------------------

# The minutes recording that an item was taken off, in the clerk's own words
# rather than inferred from the item not recurring.
_REMOVED_NOTE_RE = re.compile(
    r"\b(?:was|were)\s+removed\b|\bremoved\s+by\s+staff\b"
    r"|\bpulled\s+from\s+the\s+agenda\b",
    re.IGNORECASE,
)


def detect_vanished_items(records: list[dict[str, Any]]) -> list[Finding]:
    """Report items the minutes show were explicitly removed and produced no
    motion, with what the published set shows about them afterwards.

    Deliberately restricted to explicit removals. Any motion-free item that
    does not recur would be a far larger set — 199 of them in this corpus —
    but it is dominated by verbal updates, workshop presentations and
    consent-calendar entries disposed of by a motion on their parent item.
    Reporting those as items that vanished would assert a pattern where the
    records show only that something was discussed once, which is the
    ordinary shape of a report item.
    """
    findings: list[Finding] = []
    for index, record in enumerate(records):
        # Items named in a removal vote at this meeting.
        named: dict[str, dict[str, Any]] = {}
        for item in record["items"]:
            for motion in item["motions"]:
                if not _REMOVAL_RE.search(motion["text"]):
                    continue
                for match in _TARGET_ITEM_RE.finditer(motion["text"]):
                    named[match.group(1).upper()] = {
                        "motion": motion, "vote_item": item,
                    }

        for item in record["items"]:
            number = (item.get("number") or "").upper()
            note = _REMOVED_NOTE_RE.search(item.get("title") or "")
            vote = named.get(number)
            if not note and not vote:
                continue
            if item["motions"]:
                # Removed but still acted on: not a vanishing item.
                continue

            reason = (
                "the minutes note that the item was removed"
                if note else
                "the item is named in a recorded vote on removing an item "
                "from the agenda"
            )
            endpoints = [_endpoint(record, item, _item_page(item))]
            later_hits = []
            for later in records[index + 1:]:
                for later_item in later["items"]:
                    if similarity(item["title"], later_item["title"]) < CANDIDATE_SIMILARITY:
                        continue
                    later_hits.append({
                        "meeting_id": later["meeting_id"],
                        "date": later["date"],
                        "item_number": later_item.get("number"),
                        "motions_recorded": len(later_item["motions"]),
                    })
                    endpoints.append(
                        _endpoint(later, later_item, _item_page(later_item))
                    )
            summary = (
                f"The minutes of {_uk_date(record['date'])} record item {number} on "
                f"the agenda with no motion against it, and {reason}."
            )
            if later_hits:
                first = later_hits[0]
                summary += (
                    f" The minutes of {_uk_date(first['date'])} record item "
                    f"{first['item_number']} on a matching title."
                )
            else:
                summary += (
                    " No later meeting in the published set records an item on a "
                    "matching title."
                )
            findings.append(
                Finding(
                    pattern="item_vanished_from_agenda",
                    confidence=CONFIDENCE_ASSERTED if note else CONFIDENCE_CANDIDATE,
                    match_basis=(
                        "removal recorded in the item heading" if note
                        else "item named in a recorded agenda-removal vote"
                    ),
                    summary=summary,
                    endpoints=endpoints,
                    detail={
                        "item_number": item.get("number"),
                        "item_title": item.get("title"),
                        "removal_note": bool(note),
                        "removal_vote_outcome": (
                            vote["motion"]["outcome"] if vote else None
                        ),
                        "removal_vote_text": (
                            vote["motion"]["text"] if vote else None
                        ),
                        "later_appearances": later_hits,
                    },
                )
            )
    return _dedupe(findings)


# --- Assembly, validation, output ----------------------------------------


def _dedupe(findings: list[Finding]) -> list[Finding]:
    """Collapse identical findings and order them deterministically."""
    seen: dict[str, Finding] = {}
    for finding in findings:
        key = json.dumps(finding.to_dict(), sort_keys=True, ensure_ascii=False)
        seen.setdefault(key, finding)
    return [seen[key] for key in sorted(seen)]


def detect_all(records: list[dict[str, Any]]) -> list[Finding]:
    """Every pattern, over records sorted oldest first."""
    ordered = sorted(records, key=lambda r: (r["date"], r["meeting_id"]))
    return (
        detect_project_links(ordered)
        + detect_amount_increases(ordered)
        + detect_continuations(ordered)
        + detect_agenda_removals(ordered)
        + detect_vanished_items(ordered)
    )


def validate_finding(finding: dict[str, Any]) -> list[str]:
    """Check a finding against spec §2.7. Returns violations; empty means
    publishable. Provenance is required on *every* end of a link — a
    finding that can only be traced at one end is not a verifiable claim
    and is not written."""
    violations: list[str] = []
    if finding.get("pattern") not in PATTERNS:
        violations.append(f"unknown pattern {finding.get('pattern')!r}")
    if finding.get("confidence") not in (CONFIDENCE_ASSERTED, CONFIDENCE_CANDIDATE):
        violations.append(f"invalid confidence {finding.get('confidence')!r}")
    if not (finding.get("summary") or "").strip():
        violations.append("empty summary")
    if not (finding.get("match_basis") or "").strip():
        violations.append("empty match_basis")

    endpoints = finding.get("endpoints") or []
    if not endpoints:
        violations.append("finding has no endpoints")
    linking = finding.get("pattern") in LINKING_PATTERNS
    if linking and len(endpoints) < 2:
        violations.append(
            f"{finding.get('pattern')} links meetings but carries "
            f"{len(endpoints)} endpoint(s) — every end needs provenance"
        )
    for i, endpoint in enumerate(endpoints):
        for key in ("meeting_id", "date", "body"):
            if not endpoint.get(key):
                violations.append(f"endpoints[{i}]: missing {key}")
        provenance = endpoint.get("provenance")
        if not isinstance(provenance, dict):
            violations.append(f"endpoints[{i}]: claim without provenance")
            continue
        if provenance.get("type") != "pdf":
            violations.append(
                f"endpoints[{i}]: provenance type {provenance.get('type')!r} "
                "is not a document"
            )
        file_id, page = provenance.get("file_id"), provenance.get("page")
        if not isinstance(file_id, int) or isinstance(file_id, bool) or file_id <= 0:
            violations.append(f"endpoints[{i}]: invalid file_id {file_id!r}")
        if not isinstance(page, int) or isinstance(page, bool) or page < 1:
            violations.append(f"endpoints[{i}]: invalid page {page!r}")
    if linking and len({e.get("meeting_id") for e in endpoints}) < 2:
        violations.append("link endpoints are all the same meeting")
    return violations


def serialise(payload: Any) -> str:
    """Deterministic JSON: sorted keys, fixed indent, trailing newline, no
    timestamps. These files are committed and diffed."""
    return json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
