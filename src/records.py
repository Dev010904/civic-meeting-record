"""Per-meeting published records — spec §2.4, build step 6a.

Turns Stage A parser output into the JSON artifacts committed under
``data/meetings/``. This is the cross-document layer step 6b (cross-meeting
item tracking) will match over; no matching logic lives here.

What this module guarantees:

- **Spec §2.4 shape.** ``meeting_id``, ``jurisdiction``, ``body``, ``date``,
  ``source``, ``items[]`` — each item carrying ``motions[]``, ``money[]``,
  ``media_timestamp``, ``disposition`` and ``extraction``. Two extensions,
  both for things the parser produces that §2.4 did not anticipate:
  ``minutes_status`` (§2.7 rule 2) and per-motion ``flags``/``notes``.
- **Provenance on every claim** (§2.7 rule 7). Motions, money entries and
  media timestamps each carry their own ``{type, file_id, page}``.
  :func:`validate_record` re-checks the serialised payload — the thing
  actually written — and a record with any violation is not written at all.
  It does not publish with a caveat.
- **Votes only from minutes** (§2.7 rule 1). Every motion's provenance must
  point at the minutes file this record was built from; a motion sourced
  from anywhere else is a validation failure.
- **No name from audio** (§2.7 rule 3). Enforced now, before audio exists:
  any provenance whose type is not ``pdf`` fails validation.
- **No private commenters** (§2.7 rule 4). The record has no field for
  comment text, commenter names or topics — only an aggregate integer count
  that comment occurred (§2.2). Officials named in motions are kept in full
  (NRS 241.0353(1)).

Determinism: records are written with sorted keys and no timestamps, so
rebuilding an unchanged corpus produces byte-identical files. These are
committed and diffed — a noisy diff destroys the audit trail.

Deterministic parsing only; no LLM calls anywhere in this module.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any, Optional

import parse_minutes

JURISDICTION = "ivgid"
SCHEMA_VERSION = 1

# Live-format scope (spec §2.6 product decision: v1 publishes new meetings
# only). The boundaries are the format-era boundaries the benchmark located,
# not calendar convenience: the structured Board format begins with the
# February 2025 minutes (file 1171; January 2025 is still stenographic
# transcript), and the structured Audit Committee format ("MOTION WAS MADE")
# begins December 2024 (file 1051).
LIVE_BOARD_FROM = "2025-02-01"
LIVE_AUDIT_FROM = "2024-12-01"
TRANSCRIPT_ERA_FROM = "2023-01-01"

_SKIP_AUDIT_NARRATIVE = (
    "narrative-prose Audit Committee minutes; the structured "
    f"'MOTION WAS MADE' format begins {LIVE_AUDIT_FROM} — deferred to the "
    "archive phase"
)
_SKIP_TRANSCRIPT = (
    "stenographic transcript era (votes exist only as dialogue in two-column "
    f"court-reporter lines); the structured format begins {LIVE_BOARD_FROM} — "
    "deferred to the archive phase"
)
# January 2025 is a mixed month and the reason recorded for it must say so
# rather than claim a format the document does not have: 2025-01-08 (file
# 1103) and 2025-01-16 (file 1096) are stenographic transcripts and yield no
# motions, but 2025-01-29 (file 1140) is already structured and parses four
# clean motions — all four hand-verified correct in the round-1 check. The
# boundary is a scope decision, not a parser limit.
TRANSITION_FROM = "2025-01-01"
_SKIP_TRANSITION = (
    "January 2025 transitional window, before the live-format boundary "
    f"{LIVE_BOARD_FROM}. The month is mixed: 2025-01-08 and 2025-01-16 are "
    "stenographic transcripts, but 2025-01-29 is already structured and "
    "parses clean. Excluded by scope, not by parser capability — revisit "
    "the boundary before the archive phase"
)
_SKIP_NARRATIVE = (
    "narrative-prose era (2021-2022: 'Trustee X made a motion … the motion "
    "passed unanimously') — deferred to the archive phase"
)

# Body identification, longest-distinguishing match first. The code is the
# meeting_id suffix (spec §2.4 example: "ivgid-2026-07-22-bot").
_BODIES: tuple[tuple[str, str, str], ...] = (
    ("audit", "Audit Committee", "audit"),
    ("capital investment", "Capital Investment Committee", "cic"),
    ("capitol investment", "Capital Investment Committee", "cic"),
    ("golf advisory", "Golf Advisory Committee", "gac"),
    ("board of trustees", "Board of Trustees", "bot"),
    ("trustees", "Board of Trustees", "bot"),
)


# --- Money extraction (spec §2.2) ----------------------------------------
#
# Amounts live inside motion text, in the forms IVGID clerks actually write:
#   "…; in the Amount of $199,000.00; …"
#   "…Contract Value not to Exceed $10,000;…"
#   "…Consultant: Snow Engineering Group; $40,000."
#   "…for an Amount Not to Exceed $553,925 Effluent Export Line Project…"
# Money is read from motion text only — the decision record — never from the
# agenda-item title that repeats the same figures, so nothing double-counts.

# The figure must end on a digit: "…$56,000, Private Donor…" would otherwise
# swallow the list comma and read as a malformed thousands group.
_AMOUNT_RE = re.compile(
    r"\$\s?(\d(?:[\d,]*\d)?(?:\.\d+)?)\s*(million|billion)?(\+?)", re.IGNORECASE
)
_MULTIPLIER = {"million": 1_000_000, "billion": 1_000_000_000}

# A vendor name runs until the clause that follows it. Commas are allowed
# through because corporate suffixes contain them ("Olympus & Associates,
# Inc."); the clause keywords are what actually terminate the name.
_NAME = r"([^;]{2,70}?)(?=\s+(?:for|in|to)\s|;|$)"

# Vendor anchors, each a pattern whose group 1 is the vendor. Ordered only
# for readability — every anchor in the motion text is collected, and each
# amount takes the NEAREST anchor above it, so a consent calendar listing
# several vendors attributes each amount to its own.
_VENDOR_ANCHORS: tuple[re.Pattern[str], ...] = (
    # "…Agreement between Incline Village General Improvement District and X for…"
    re.compile(
        r"\bbetween\s+(?:the\s+)?"
        r"(?:Incline\s+(?:Village\s+)?General\s+Improvement\s+District|District|IVGID)"
        r"\s+and\s+(?:the\s+)?" + _NAME,
        re.IGNORECASE,
    ),
    # "…Agreement/contract with X in the amount of…"
    re.compile(
        r"\b(?:agreement|contract|amendment)\s+with\s+(?:the\s+)?" + _NAME,
        re.IGNORECASE,
    ),
    re.compile(r"\bConsultant:\s*" + _NAME, re.IGNORECASE),
    re.compile(r"\bVendor:\s*" + _NAME, re.IGNORECASE),
    re.compile(r"\bAdditional\s+Funding\s+for\s+(?:the\s+)?" + _NAME, re.IGNORECASE),
    re.compile(r"\bIncreasing\s+the\s+(.{2,60}?)\s+Contract\b", re.IGNORECASE),
)

# A settlement counterparty is not a vendor. "Settlement Agreement with
# Sheila A. Leijon" is shaped exactly like a procurement clause but names a
# private individual in litigation, so the "agreement with" anchor is
# suppressed near the word Settlement and the vendor is left null and
# flagged rather than guessed (spec §2.2: never guess).
_SETTLEMENT_RE = re.compile(r"\bsettlement\b", re.IGNORECASE)

# The purpose clause immediately following a vendor name, bounded by the
# next structural element the clerks write (fund coding, CIP/GL reference,
# amount clause or a semicolon).
_PURPOSE_RE = re.compile(
    r"^\s+for\s+(?:the\s+)?(.{3,140}?)"
    r"(?=;|\s+in\s+(?:the\s+|an\s+|a\s+)?amount\b|\s+FY\s?\d|\s+CIP\s?#"
    r"|\s+GL\s?#|\s+Project\s?#|\s+Fund:|$)",
    re.IGNORECASE,
)

# Consent calendars string several complete items into one motion
# ("… Item F.3. Approve an Agreement … Project #2524SS1010; and, Item F.4.
# Approve a Purchase Agreement …"). These markers bound one item's clause so
# a fund reference belonging to F.3 is never attributed to F.4's amount.
_ITEM_MARKER_RE = re.compile(r"\bItems?\s+[A-Z]\.\d+", re.IGNORECASE)

_CONTRACT_REF_RE = re.compile(
    r"\b(?:CIP|GL|Project|Budget)\s?#\s?[\w-]+"
    r"|\bChange\s+Order\s?#\s?\d+"
    r"|\bResolution\s+(?:No\.\s*)?\d+",
    re.IGNORECASE,
)

_NOT_TO_EXCEED_RE = re.compile(r"not\s+to\s+exceed[^$]{0,25}$", re.IGNORECASE)
_AMOUNT_CLAUSE_RE = re.compile(
    r"\bin\s+(?:the\s+|an\s+|a\s+)?amount\s+of\s+(?:a\s+)?$", re.IGNORECASE
)
_TOTAL_RE = re.compile(r"\btotal\b[^$]{0,70}$", re.IGNORECASE)
_RATE_BEFORE_RE = re.compile(r"\b(?:rate|cost|price|fee|values?)\b[^$]{0,20}$", re.IGNORECASE)
_RATE_AFTER_RE = re.compile(r"^\s*(?:per\s+[\w\s]{1,20}|each)\b", re.IGNORECASE)
_APPROXIMATE_RE = re.compile(r"\b(?:approximate(?:ly)?|up\s+to|about)\b[^$]{0,25}$", re.IGNORECASE)

# The district itself is never its own vendor.
_SELF_RE = re.compile(
    r"^(?:the\s+)?(?:incline\s+(?:village\s+)?general\s+improvement\s+district"
    r"|district|ivgid)\W*$",
    re.IGNORECASE,
)

_LOOKBACK = 80


@dataclass
class Money:
    """One dollar amount decided in a motion (spec §2.2, §2.4).

    ``amount_usd`` is None when the printed figure is malformed — IVGID
    minutes contain real clerical defects ("$359,97", "$307,9250") whose
    intended value is genuinely unknowable. The verbatim ``amount_raw`` is
    always kept, the record is flagged ``malformed_amount``, and no value is
    invented. Same rule for ``vendor`` and ``purpose``: null plus a flag
    beats a guess.
    """

    amount_usd: Optional[float]
    amount_raw: str
    role: str
    vendor: Optional[str]
    purpose: Optional[str]
    contract_ref: Optional[str]
    contingency: bool
    approximate: bool
    provenance: parse_minutes.Provenance
    flags: list[str] = field(default_factory=list)


def _parse_amount(digits: str, multiplier: Optional[str]) -> Optional[float]:
    """Convert a printed figure to a number, or None if it is malformed.

    Comma grouping is the integrity check: every group after the first must
    be exactly three digits. "$359,97" and "$307,9250" fail it, and their
    intended values cannot be recovered without guessing.
    """
    integer_part = digits.split(".")[0]
    if "," in integer_part:
        groups = integer_part.split(",")
        if not 1 <= len(groups[0]) <= 3 or any(len(g) != 3 for g in groups[1:]):
            return None
    value = float(digits.replace(",", ""))
    if multiplier:
        value *= _MULTIPLIER[multiplier.lower()]
    return value


def _classify_role(before: str, after: str) -> str:
    """What kind of figure this is, from the clause that introduces it.

    "not_to_exceed" is tested first because a contingency ceiling can itself
    be phrased as a total ("not to exceed a total of $307,9250").
    """
    if _NOT_TO_EXCEED_RE.search(before):
        return "not_to_exceed"
    if _AMOUNT_CLAUSE_RE.search(before):
        return "amount"
    if _TOTAL_RE.search(before):
        return "total"
    if _RATE_BEFORE_RE.search(before) or _RATE_AFTER_RE.match(after):
        return "rate"
    return "unclassified"


def _vendor_anchors(text: str) -> list[tuple[int, int, str]]:
    """Every vendor-introducing clause in the motion, as
    ``(start, end_of_name, vendor)``, sorted by position."""
    anchors: list[tuple[int, int, str]] = []
    for pattern in _VENDOR_ANCHORS:
        for match in pattern.finditer(text):
            window = text[max(0, match.start() - 60) : match.end()]
            if _SETTLEMENT_RE.search(window):
                continue
            name = re.sub(r"\s+", " ", match.group(1)).strip(" .,;:")
            if len(name) < 2 or _SELF_RE.match(name):
                continue
            anchors.append((match.start(), match.end(), name))
    anchors.sort()
    return anchors


def extract_money(
    text: str, provenance: parse_minutes.Provenance
) -> list[Money]:
    """Extract every dollar amount from one motion's text (spec §2.2).

    Vendor and purpose come from the nearest vendor clause *above* the
    amount, which is what makes consent calendars — several vendors and
    several amounts in one motion — attribute correctly. Where no such
    clause exists the fields stay null and the entry is flagged; nothing is
    inferred from proximity alone.
    """
    anchors = _vendor_anchors(text)
    refs = [(m.start(), m.group(0)) for m in _CONTRACT_REF_RE.finditer(text)]

    entries: list[Money] = []
    for match in _AMOUNT_RE.finditer(text):
        digits, multiplier, plus = match.group(1), match.group(2), match.group(3)
        before = text[max(0, match.start() - _LOOKBACK) : match.start()]
        after = text[match.end() : match.end() + 40]
        flags: list[str] = []

        value = _parse_amount(digits, multiplier)
        if value is None:
            flags.append("malformed_amount")

        vendor: Optional[str] = None
        purpose: Optional[str] = None
        preceding = [a for a in anchors if a[0] < match.start()]
        if preceding:
            _, name_end, vendor = preceding[-1]
            purpose_match = _PURPOSE_RE.match(text[name_end:])
            if purpose_match:
                purpose = re.sub(r"\s+", " ", purpose_match.group(1)).strip(" .,;:")
        if vendor is None:
            flags.append("vendor_not_extracted")
        if purpose is None:
            flags.append("purpose_not_extracted")

        # A fund/contract reference is attributed only within the clause that
        # governs this amount: after the consent-calendar item marker that
        # opens it, and before any vendor clause that opens the next one.
        # Otherwise the nearest reference by distance can belong to a
        # different item entirely — a wrong reference in a published record
        # is worse than a missing one.
        clause_start = max(
            (m.start() for m in _ITEM_MARKER_RE.finditer(text)
             if m.start() <= (preceding[-1][0] if preceding else match.start())),
            default=0,
        )
        clause_end = min(
            (a[0] for a in anchors if a[0] > match.start()), default=len(text)
        )
        in_clause = [r for r in refs if clause_start <= r[0] < clause_end]
        contract_ref = None
        if in_clause:
            nearest = min(in_clause, key=lambda r: abs(r[0] - match.start()))
            contract_ref = re.sub(r"\s+", " ", nearest[1]).strip()

        entries.append(
            Money(
                amount_usd=value,
                amount_raw=match.group(0).strip(),
                role=_classify_role(before, after),
                vendor=vendor,
                purpose=purpose,
                contract_ref=contract_ref,
                contingency=False,
                approximate=bool(plus) or bool(_APPROXIMATE_RE.search(before)),
                provenance=provenance,
                flags=flags,
            )
        )

    # Spec §2.2 asks whether a contingency was attached. A ceiling recorded
    # in the same motion is that contingency, so the principal amounts carry
    # the marker.
    if any(e.role == "not_to_exceed" for e in entries):
        for entry in entries:
            if entry.role == "amount":
                entry.contingency = True
    return entries


# --- Scope (spec §2.6: v1 publishes new meetings only) --------------------


def scope_decision(event_date: str, event_name: str) -> tuple[bool, Optional[str]]:
    """Is this document in the live-format scope, and if not, why not?

    Returns ``(in_scope, reason)``. A skipped document always carries a
    reason — deferred-era documents are recorded, never silently dropped.
    """
    date = event_date[:10]
    if "audit" in event_name.lower():
        if date >= LIVE_AUDIT_FROM:
            return True, None
        return False, _SKIP_AUDIT_NARRATIVE
    if date >= LIVE_BOARD_FROM:
        return True, None
    if date >= TRANSITION_FROM:
        return False, _SKIP_TRANSITION
    if date >= TRANSCRIPT_ERA_FROM:
        return False, _SKIP_TRANSCRIPT
    return False, _SKIP_NARRATIVE


def identify_body(event_name: str) -> tuple[str, str]:
    """``(body, code)`` for an event name. Falls back to the event name
    verbatim with a slugged code rather than guessing a known body."""
    lowered = event_name.lower()
    for needle, body, code in _BODIES:
        if needle in lowered:
            return body, code
    slug = re.sub(r"[^a-z0-9]+", "-", lowered).strip("-") or "unknown"
    return event_name.strip() or "Unknown", slug


def meeting_id(date: str, code: str, file_id: Optional[int] = None) -> str:
    """Spec §2.4 form ``ivgid-2026-07-22-bot``. ``file_id`` is appended only
    to disambiguate several minutes documents for one body on one date
    (IVGID has continued public hearings that produce exactly this)."""
    base = f"{JURISDICTION}-{date}-{code}"
    return f"{base}-{file_id}" if file_id is not None else base


# --- Record assembly ------------------------------------------------------


def _provenance_dict(provenance: parse_minutes.Provenance) -> dict[str, Any]:
    return {
        "type": provenance.type,
        "file_id": provenance.file_id,
        "page": provenance.page,
    }


def _motion_dict(motion: parse_minutes.Motion) -> dict[str, Any]:
    return {
        "text": motion.text,
        "mover": motion.mover,
        "seconder": motion.seconder,
        "yeas": list(motion.yeas),
        "nays": list(motion.nays),
        "abstain": list(motion.abstain),
        "absent": list(motion.absent),
        "tally": dict(motion.tally),
        "outcome": motion.outcome,
        "kind": motion.kind,
        "flags": sorted(motion.flags),
        "notes": sorted(motion.notes),
        "provenance": _provenance_dict(motion.provenance),
    }


def _money_dict(money: Money) -> dict[str, Any]:
    return {
        "amount_usd": money.amount_usd,
        "amount_raw": money.amount_raw,
        "role": money.role,
        "vendor": money.vendor,
        "purpose": money.purpose,
        "contract_ref": money.contract_ref,
        "contingency": money.contingency,
        "approximate": money.approximate,
        "flags": sorted(money.flags),
        "provenance": _provenance_dict(money.provenance),
    }


def _timestamp_dict(ts: parse_minutes.MediaTimestamp) -> dict[str, Any]:
    return {
        "start": ts.start,
        "end": ts.end,
        "provenance": _provenance_dict(ts.provenance),
    }


def _disposition(motions: list[parse_minutes.Motion]) -> Optional[str]:
    """The item's disposition is the outcome of its last decisive motion.

    Motions superseded by a floor amendment carry no outcome of their own,
    so they are skipped; an item whose motions all lack a recorded outcome
    has no disposition rather than an assumed one.
    """
    for motion in reversed(motions):
        if motion.kind != "amended" and motion.outcome is not None:
            return motion.outcome
    return None


def build_record(
    *,
    file_id: int,
    event_id: int,
    event_name: str,
    event_date: str,
    parsed: parse_minutes.ParsedMinutes,
    agenda_file_id: Optional[int] = None,
    media_url: Optional[str] = None,
    disambiguate: bool = False,
) -> dict[str, Any]:
    """Assemble one spec §2.4 meeting record as a plain JSON-ready dict.

    Motions are grouped into ``items[]`` by the agenda item they were parsed
    under, in document order. Money is extracted from each motion's text and
    attached to that motion's item, carrying the motion's provenance.
    """
    date = event_date[:10]
    body, code = identify_body(event_name)

    # Group in first-appearance order; motions already arrive in document
    # order, so this is stable without sorting by anything invented.
    order: list[tuple[Optional[str], Optional[str]]] = []
    grouped: dict[tuple[Optional[str], Optional[str]], list[parse_minutes.Motion]] = {}
    for motion in parsed.motions:
        key = (motion.item_number, motion.item_title)
        if key not in grouped:
            grouped[key] = []
            order.append(key)
        grouped[key].append(motion)

    timestamps: dict[tuple[Optional[str], Optional[str]], list[parse_minutes.MediaTimestamp]] = {}
    for ts in parsed.media_timestamps:
        timestamps.setdefault((ts.item_number, ts.item_title), []).append(ts)

    items: list[dict[str, Any]] = []
    for key in order:
        motions = grouped[key]
        money: list[Money] = []
        for motion in motions:
            money.extend(extract_money(motion.text, motion.provenance))
        item_timestamps = timestamps.get(key, [])
        flags = sorted(
            {f for m in motions for f in m.flags} | {f for e in money for f in e.flags}
        )
        items.append(
            {
                "number": key[0],
                "title": key[1],
                "disposition": _disposition(motions),
                "motions": [_motion_dict(m) for m in motions],
                "money": [_money_dict(e) for e in money],
                # Spec §2.4 carries a single media_timestamp per item; the
                # clerks sometimes write several for one item (an item taken
                # up twice). The spec field holds the first and the full list
                # is kept beside it, because these ranges are Layer 2's
                # alignment key (§3.3) and must not be dropped.
                "media_timestamp": (
                    _timestamp_dict(item_timestamps[0]) if item_timestamps else None
                ),
                "media_timestamps": [_timestamp_dict(t) for t in item_timestamps],
                "extraction": {
                    "stage": "A",
                    "confidence": "flagged" if flags else "exact",
                    "flags": flags,
                },
            }
        )

    return {
        "schema_version": SCHEMA_VERSION,
        "meeting_id": meeting_id(date, code, file_id if disambiguate else None),
        "jurisdiction": JURISDICTION,
        "body": body,
        "date": date,
        # Spec §2.7 rule 2: Nevada allows 45 days for approval, so anything
        # not positively identified as approved is treated as draft
        # downstream. None means undetermined, never "approved".
        "minutes_status": parsed.minutes_status,
        "source": {
            "event_id": event_id,
            "agenda_file_id": agenda_file_id,
            "minutes_file_id": file_id,
            "media_url": media_url,
        },
        # Aggregate only (spec §2.2 records *that* comment occurred; §2.7
        # rule 4 and NRS 241.0353(3) forbid the name or the text). There is
        # deliberately no field here that could carry either.
        "public_comment_count": len(parsed.public_comments),
        "document": {
            "unparseable_pages": sorted(parsed.unparseable_pages),
            "flags": sorted(parsed.flags),
        },
        "items": items,
    }


# --- Validation gate (spec §2.7) -----------------------------------------

# Keys that would carry commenter-derived content. None is ever produced by
# build_record; the gate exists so a future change cannot quietly add one.
_FORBIDDEN_KEYS = frozenset(
    {"commenter", "commenter_name", "comment_text", "public_comments", "speaker"}
)


def _check_provenance(
    payload: Any, path: str, minutes_file_id: int, violations: list[str]
) -> None:
    provenance = payload.get("provenance")
    if not isinstance(provenance, dict):
        violations.append(f"{path}: claim without provenance")
        return
    # §2.7 rule 3 — a name may never come from audio. Enforced before audio
    # exists so the gate is already standing when Layer 2 lands.
    if provenance.get("type") != "pdf":
        violations.append(
            f"{path}: provenance type {provenance.get('type')!r} is not a document"
        )
    file_id = provenance.get("file_id")
    page = provenance.get("page")
    if not isinstance(file_id, int) or isinstance(file_id, bool) or file_id <= 0:
        violations.append(f"{path}: invalid provenance file_id {file_id!r}")
    if not isinstance(page, int) or isinstance(page, bool) or page < 1:
        violations.append(f"{path}: invalid provenance page {page!r}")
    if file_id != minutes_file_id:
        violations.append(
            f"{path}: provenance file {file_id} is not this meeting's "
            f"minutes file {minutes_file_id}"
        )


def validate_record(record: dict[str, Any]) -> list[str]:
    """Check a record against spec §2.7. Returns the list of violations —
    empty means publishable. A record with any violation must not be
    written; it does not publish with a caveat (§2.7 rule 7)."""
    violations: list[str] = []

    for key in ("meeting_id", "jurisdiction", "body", "date", "source", "items"):
        if not record.get(key):
            if key != "items" or "items" not in record:
                violations.append(f"record: missing required field {key!r}")
    # §2.7 rule 2: the field must be present on every record. None is a
    # legitimate value (undetermined, treated as draft downstream) — absence
    # is not.
    if "minutes_status" not in record:
        violations.append("record: missing minutes_status")
    elif record["minutes_status"] not in (None, "draft", "approved"):
        violations.append(
            f"record: invalid minutes_status {record['minutes_status']!r}"
        )

    source = record.get("source") or {}
    minutes_file_id = source.get("minutes_file_id")
    if not isinstance(minutes_file_id, int) or minutes_file_id <= 0:
        violations.append(f"record: invalid minutes_file_id {minutes_file_id!r}")
        return violations

    for i, item in enumerate(record.get("items") or []):
        for j, motion in enumerate(item.get("motions") or []):
            # §2.7 rule 1: votes come only from minutes. _check_provenance
            # pins every motion to this record's minutes file.
            _check_provenance(
                motion, f"items[{i}].motions[{j}]", minutes_file_id, violations
            )
        for j, money in enumerate(item.get("money") or []):
            _check_provenance(
                money, f"items[{i}].money[{j}]", minutes_file_id, violations
            )
        for j, ts in enumerate(item.get("media_timestamps") or []):
            _check_provenance(
                ts, f"items[{i}].media_timestamps[{j}]", minutes_file_id, violations
            )
        if item.get("media_timestamp") is not None:
            _check_provenance(
                item["media_timestamp"],
                f"items[{i}].media_timestamp",
                minutes_file_id,
                violations,
            )

    for key in _find_keys(record):
        if key.lower() in _FORBIDDEN_KEYS:
            violations.append(f"record: forbidden commenter-derived field {key!r}")

    return violations


def _find_keys(payload: Any) -> list[str]:
    """Every mapping key anywhere in the payload."""
    found: list[str] = []
    if isinstance(payload, dict):
        for key, value in payload.items():
            found.append(key)
            found.extend(_find_keys(value))
    elif isinstance(payload, list):
        for value in payload:
            found.extend(_find_keys(value))
    return found


def serialise(record: dict[str, Any]) -> str:
    """Deterministic JSON: sorted keys, fixed indent, trailing newline, no
    timestamps anywhere in the payload. Byte-identical across rebuilds of an
    unchanged corpus, so the git diff is a real audit trail."""
    return json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
