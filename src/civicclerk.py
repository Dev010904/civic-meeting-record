"""CivicClerk OData v4 API client.

Talks to ``https://{slug}.api.civicclerk.com/v1/`` — unauthenticated, plain GET.
Multi-jurisdiction capable via ``slug``; only ``ivgid`` is exercised in v1.

Verified API quirks handled here (see docs/civicclerk-api.md §2):

1. ``$select`` returns HTTP 200 with an empty ``value`` array. This module
   never emits ``$select`` and ``_check_url`` raises if one ever appears in a
   constructed URL.
2. The server caps pages at 15 items regardless of ``$top``. ``list_events``
   follows ``@odata.nextLink`` (which carries a ``$skiptoken``) so callers
   never see pagination.
3. The default sort returns future events first. Every event listing pairs
   with ``startDateTime lt {date}``.
4. Filtering on ``categoryId`` requires the two-key
   ``$orderby=startDateTime desc, eventName desc``; a single-key orderby
   returns empty. The two-key form is used unconditionally.
5. ``agendaFile`` and ``minutesFile`` are empty stubs on every client. They
   are never read; all real files come from ``publishedFiles[]`` via
   :func:`published_files`.
6. ``liveStartTime``/``liveEndTime`` are unreliable — they sometimes span
   days. They are exposed raw on the event object and never used to derive
   duration. See :func:`get_event`.

Additional verified behaviour (26 July 2026, this build): OData single-entity
addressing ``Events({id})`` returns 404 on ``ivgid``; :func:`get_event`
therefore uses ``$filter=id eq {id}``.

Media: ``mediaStreamPath`` is exposed as-is via :func:`media_stream`. Two URL
forms exist — absolute (``https://cpmedia.azureedge.net/{slug}/{hash}.mp4``)
and relative (``stream/{SLUG}/{guid}.mp4``). The base URL for the relative
form is not established, so relative paths are returned unresolved and
flagged with ``is_relative=True``. This module never downloads media.
"""

from __future__ import annotations

import time
from datetime import date, datetime
from typing import Any, NamedTuple, Optional, Union
from urllib.parse import quote

import httpx

BASE_URL_TEMPLATE = "https://{slug}.api.civicclerk.com/v1/"

# Descriptive User-Agent identifying the project, with a contact placeholder.
USER_AGENT = (
    "civic-meeting-record/0.1 "
    "(public-meeting record project; contact: CONTACT-EMAIL-PLACEHOLDER)"
)

TIMEOUT_SECONDS = 30.0

# Politeness: at most one request per second — this is a public government
# service. Tests may lower this; production code must not.
MIN_REQUEST_INTERVAL = 1.0

# Retry with exponential backoff on 429 and 5xx.
MAX_RETRIES = 3
BACKOFF_BASE_SECONDS = 1.0

# Quirk 4: two-key orderby, required whenever categoryId is filtered and
# harmless otherwise, so it is used on every event listing.
TWO_KEY_ORDERBY = "startDateTime desc, eventName desc"

# Quirk 2: the server returns at most this many items per page.
SERVER_PAGE_CAP = 15

_DateLike = Union[str, date, datetime]


class SelectNotAllowedError(ValueError):
    """Raised when a constructed URL contains ``$select`` (quirk 1)."""


class MediaPath(NamedTuple):
    """A ``mediaStreamPath`` value, exposed as-is.

    ``is_relative`` is True for the ``stream/{SLUG}/{guid}.mp4`` form, whose
    base URL is not established — do not attempt to resolve it.
    """

    path: str
    is_relative: bool


def _check_url(url: str) -> None:
    """Guard against quirk 1: raise if ``$select`` appears in a URL.

    ``$select`` silently returns HTTP 200 with ``"value": []``, so it must
    never be emitted. Checks both the literal and percent-encoded forms.
    """
    lowered = url.lower()
    if "$select" in lowered or "%24select" in lowered:
        raise SelectNotAllowedError(
            f"URL contains $select, which the CivicClerk API silently "
            f"ignores by returning an empty result set: {url}"
        )


_last_request_time = 0.0


def _throttle() -> None:
    """Enforce the one-request-per-second courtesy rate limit."""
    global _last_request_time
    elapsed = time.monotonic() - _last_request_time
    wait = MIN_REQUEST_INTERVAL - elapsed
    if wait > 0:
        time.sleep(wait)
    _last_request_time = time.monotonic()


def _request(url: str, client: Optional[httpx.Client] = None) -> httpx.Response:
    """GET ``url`` with the $select guard, rate limit, timeout and retries.

    Retries with exponential backoff (1s, 2s, 4s) on 429, 5xx, and
    transport-level failures (timeouts, DNS errors, connection resets —
    ``httpx.TransportError``); the first full-archive benchmark showed all
    of those occurring transiently against this API. Any other error status
    raises ``httpx.HTTPStatusError`` immediately.
    """
    _check_url(url)
    headers = {"User-Agent": USER_AGENT}
    owns_client = client is None
    if owns_client:
        client = httpx.Client(timeout=TIMEOUT_SECONDS)
    try:
        for attempt in range(MAX_RETRIES + 1):
            _throttle()
            try:
                response = client.get(url, headers=headers, timeout=TIMEOUT_SECONDS)
            except httpx.TransportError:
                if attempt < MAX_RETRIES:
                    time.sleep(BACKOFF_BASE_SECONDS * (2**attempt))
                    continue
                raise
            if response.status_code == 429 or response.status_code >= 500:
                if attempt < MAX_RETRIES:
                    time.sleep(BACKOFF_BASE_SECONDS * (2**attempt))
                    continue
            response.raise_for_status()
            return response
        raise AssertionError("unreachable")
    finally:
        if owns_client:
            client.close()


def _base_url(slug: str) -> str:
    return BASE_URL_TEMPLATE.format(slug=slug)


def _format_date(value: _DateLike) -> str:
    """Format a date bound for a ``startDateTime lt {date}`` filter.

    Strings pass through verbatim. Naive datetimes are treated as UTC.
    """
    if isinstance(value, str):
        return value
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%dT%H:%M:%SZ")
    return value.isoformat()


def list_events(
    slug: str,
    before_date: _DateLike,
    category_id: Optional[int] = None,
    limit: Optional[int] = None,
    client: Optional[httpx.Client] = None,
) -> list[dict[str, Any]]:
    """List completed past events, newest first, across all pages.

    Pagination is transparent to the caller (quirk 2): the server caps pages
    at 15 items regardless of ``$top``, so this follows ``@odata.nextLink``
    until exhausted or ``limit`` events have been collected.

    ``before_date`` is required because the API's default sort returns future
    events first (quirk 3); every request filters ``startDateTime lt {date}``.

    The two-key ``$orderby=startDateTime desc, eventName desc`` is always
    sent (quirk 4): it is mandatory when ``category_id`` is passed — a
    single-key orderby returns an empty result — and harmless otherwise.

    Full event objects are returned; nothing is ``$select``-ed (quirk 1).
    Callers should discard unwanted fields client-side.
    """
    filter_expr = f"startDateTime lt {_format_date(before_date)}"
    if category_id is not None:
        filter_expr = f"categoryId eq {category_id} and {filter_expr}"
    url = (
        _base_url(slug)
        + "Events?$filter="
        + quote(filter_expr)
        + "&$orderby="
        + quote(TWO_KEY_ORDERBY)
    )

    events: list[dict[str, Any]] = []
    next_url: Optional[str] = url
    while next_url:
        payload = _request(next_url, client=client).json()
        events.extend(payload.get("value", []))
        if limit is not None and len(events) >= limit:
            return events[:limit]
        next_url = payload.get("@odata.nextLink")
    return events


def get_event(
    slug: str,
    event_id: int,
    client: Optional[httpx.Client] = None,
) -> dict[str, Any]:
    """Fetch one event as its full (~110-field) object.

    Uses ``$filter=id eq {event_id}`` because single-entity addressing
    ``Events({id})`` returns 404 on this API (verified on ``ivgid``,
    26 July 2026). Raises ``LookupError`` if no event matches.

    Caveat (quirk 6): the returned object's ``liveStartTime`` and
    ``liveEndTime`` are unreliable — the stream is sometimes left running and
    they can span days. They are exposed raw; never derive meeting duration
    from them. Derive duration from the media file itself if needed.
    """
    url = _base_url(slug) + "Events?$filter=" + quote(f"id eq {event_id}")
    payload = _request(url, client=client).json()
    value = payload.get("value", [])
    if not value:
        raise LookupError(f"event {event_id} not found for slug {slug!r}")
    return value[0]


def list_categories(
    slug: str,
    client: Optional[httpx.Client] = None,
) -> list[dict[str, Any]]:
    """List the jurisdiction's bodies (``EventCategories``).

    Each entry carries the ``id`` used for ``category_id`` filtering in
    :func:`list_events`. The human-readable body name is in ``categoryDesc``
    (observed live on ``ivgid``, 26 July 2026 — there is no ``name`` or
    ``categoryName`` field).
    """
    url = _base_url(slug) + "EventCategories"
    payload = _request(url, client=client).json()
    return payload.get("value", [])


def fetch_file(
    slug: str,
    file_id: int,
    client: Optional[httpx.Client] = None,
) -> bytes:
    """Fetch a published file (PDF) by ``fileId`` and return its bytes.

    Uses ``Meetings/GetMeetingFileStream(fileId={id},plainText=false)`` —
    files are fetched by ``fileId``, never by the ``url`` field on
    ``publishedFiles[]`` entries (whose relative form has no established
    base URL).
    """
    url = (
        _base_url(slug)
        + f"Meetings/GetMeetingFileStream(fileId={file_id},plainText=false)"
    )
    return _request(url, client=client).content


def published_files(
    event: dict[str, Any],
    file_type: Optional[str] = None,
) -> list[dict[str, Any]]:
    """Extract an event's files from ``publishedFiles[]``.

    ``agendaFile`` and ``minutesFile`` are empty stubs on every client
    (quirk 5) and are deliberately never read — all real files live in
    ``publishedFiles[]``.

    ``file_type`` filters on the ``type`` field; observed values are
    ``Agenda``, ``Agenda Packet``, ``Minutes``, ``Notice``, ``Other``.
    """
    files = event.get("publishedFiles") or []
    if file_type is not None:
        files = [f for f in files if f.get("type") == file_type]
    return list(files)


def media_stream(event: dict[str, Any]) -> Optional[MediaPath]:
    """Return the event's ``mediaStreamPath`` as-is, or None if absent.

    Two URL forms exist: absolute
    (``https://cpmedia.azureedge.net/{slug}/{hash}.mp4``) and relative
    (``stream/{SLUG}/{guid}.mp4``). The base for the relative form is not
    established, so relative paths are returned unresolved with
    ``is_relative=True`` — do not guess a base, and do not download media
    here.
    """
    path = event.get("mediaStreamPath") or ""
    if not path:
        return None
    is_relative = not path.lower().startswith(("http://", "https://"))
    return MediaPath(path=path, is_relative=is_relative)
