"""Tests for src/civicclerk.py against real recorded API responses.

Fixtures in tests/fixtures/ were captured live from the CivicClerk API by
scripts/record_fixtures.py on 26 July 2026. Each of the six verified quirks
in docs/civicclerk-api.md has a test proving it is handled.
"""

from __future__ import annotations

import time

import httpx
import pytest

import civicclerk
from conftest import FIXTURES, load_fixture


# --- Quirk 2 + 3: transparent pagination of past events, newest first -----


def test_pagination_transparently_yields_more_than_15_events(
    fixture_client, requested_urls
):
    with fixture_client() as client:
        events = civicclerk.list_events(
            "ivgid", "2026-07-26", limit=20, client=client
        )
    assert len(events) == 20  # server page cap is 15; this crossed a page
    assert len(requested_urls) == 2  # page 1 + followed @odata.nextLink
    assert "skiptoken" in requested_urls[1]
    # The caller sees one flat list; page order is preserved.
    page1_ids = [e["id"] for e in load_fixture("ivgid_events_page1.json")["value"]]
    page2_ids = [e["id"] for e in load_fixture("ivgid_events_page2.json")["value"]]
    assert [e["id"] for e in events] == (page1_ids + page2_ids)[:20]


def test_past_filter_always_present(fixture_client, requested_urls):
    with fixture_client() as client:
        civicclerk.list_events("ivgid", "2026-07-26", limit=1, client=client)
    # Quirk 3: default sort returns future events first, so every listing
    # must pair with startDateTime lt {date}.
    assert "startDateTime%20lt%202026-07-26" in requested_urls[0]


# --- Quirk 1: $select must never be emitted ------------------------------


def test_no_constructed_url_contains_select(fixture_client, requested_urls):
    with fixture_client() as client:
        civicclerk.list_events("ivgid", "2026-07-26", limit=20, client=client)
        civicclerk.list_events(
            "ivgid", "2026-07-26", category_id=26, limit=1, client=client
        )
        civicclerk.get_event("ivgid", 743, client=client)
        civicclerk.list_categories("ivgid", client=client)
        civicclerk.fetch_file("ivgid", 2800, client=client)
    assert requested_urls  # the calls above really went through the client
    for url in requested_urls:
        assert "$select" not in url.lower()
        assert "%24select" not in url.lower()


def test_select_guard_raises():
    base = "https://ivgid.api.civicclerk.com/v1/Events"
    with pytest.raises(civicclerk.SelectNotAllowedError):
        civicclerk._check_url(base + "?$select=id")
    with pytest.raises(civicclerk.SelectNotAllowedError):
        civicclerk._check_url(base + "?%24select=id")
    with pytest.raises(civicclerk.SelectNotAllowedError):
        civicclerk._check_url(base + "?%24SELECT=id")
    civicclerk._check_url(base + "?$filter=id%20eq%20743")  # clean URL passes


def test_request_rejects_select_before_sending():
    def handler(request: httpx.Request) -> httpx.Response:
        raise AssertionError("a $select URL must never reach the wire")

    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(civicclerk.SelectNotAllowedError):
            civicclerk._request(
                "https://ivgid.api.civicclerk.com/v1/Events?$select=id",
                client=client,
            )


# --- Quirk 4: two-key orderby whenever categoryId is filtered ------------


def test_two_key_orderby_present_with_category_id(fixture_client, requested_urls):
    with fixture_client() as client:
        civicclerk.list_events(
            "ivgid", "2026-07-26", category_id=26, limit=1, client=client
        )
    url = requested_urls[0]
    assert "categoryId%20eq%2026" in url
    # Single-key orderby returns empty when categoryId is filtered; both
    # keys must be present.
    assert "%24orderby=" in url or "$orderby=" in url
    assert "startDateTime%20desc" in url
    assert "eventName%20desc" in url


# --- Quirk 5: files come only from publishedFiles[] ----------------------


def test_published_files_reads_only_published_files():
    event = load_fixture("ivgid_event_743.json")["value"][0]
    files = civicclerk.published_files(event)
    assert [f["type"] for f in files] == ["Agenda", "Agenda Packet"]
    assert all("fileId" in f for f in files)

    agendas = civicclerk.published_files(event, file_type="Agenda")
    assert len(agendas) == 1
    assert agendas[0]["type"] == "Agenda"

    # agendaFile / minutesFile are empty stubs and must never be read:
    # removing them entirely must change nothing.
    stripped = dict(event)
    del stripped["agendaFile"]
    del stripped["minutesFile"]
    assert civicclerk.published_files(stripped) == files


# --- Quirk 6: liveStartTime/liveEndTime exposed raw ----------------------


def test_live_times_exposed_raw(fixture_client):
    with fixture_client() as client:
        event = civicclerk.get_event("ivgid", 743, client=client)
    recorded = load_fixture("ivgid_event_743.json")["value"][0]
    # Unreliable fields pass through untouched — no derived duration exists
    # anywhere on the returned object.
    assert event["liveStartTime"] == recorded["liveStartTime"]
    assert event["liveEndTime"] == recorded["liveEndTime"]


# --- Media: expose as-is, flag relative paths ----------------------------


def test_absolute_media_path_not_flagged():
    event = load_fixture("ivgid_event_743.json")["value"][0]
    media = civicclerk.media_stream(event)
    assert media is not None
    assert media.path == "https://cpmedia.azureedge.net/ivgid/104a898503.mp4"
    assert media.is_relative is False


def test_relative_media_path_flagged_not_resolved():
    # Real bristolct event recorded live: mediaStreamPath uses the
    # relative "stream/{SLUG}/{guid}.mp4" form whose base is not established.
    event = load_fixture("relative_media_event.json")["value"][0]
    raw = event["mediaStreamPath"]
    assert not raw.lower().startswith("http")  # the fixture really is relative
    media = civicclerk.media_stream(event)
    assert media is not None
    assert media.is_relative is True
    assert media.path == raw  # unresolved: exactly the raw value, no base glued on


# --- Cancelled event: no media, agenda only, parses without error --------


def test_cancelled_event_parses(fixture_client):
    with fixture_client() as client:
        event = civicclerk.get_event("ivgid", 738, client=client)
    assert event["eventName"] == "Board of Trustees Meeting - Canceled"
    assert civicclerk.media_stream(event) is None
    files = civicclerk.published_files(event)
    assert [f["type"] for f in files] == ["Agenda"]
    assert civicclerk.published_files(event, "Minutes") == []


# --- get_event -----------------------------------------------------------


def test_get_event_returns_full_object(fixture_client, requested_urls):
    with fixture_client() as client:
        event = civicclerk.get_event("ivgid", 743, client=client)
    assert event["id"] == 743
    assert event["hasMedia"] is True
    # Full object, no $select: the ~110-field payload comes back intact.
    assert len(event) > 50
    # Single-entity addressing Events({id}) 404s; the id filter is used.
    assert "Events(" not in requested_urls[0]
    assert "id%20eq%20743" in requested_urls[0]


def test_get_event_missing_raises(fixture_client):
    with fixture_client() as client:
        with pytest.raises(LookupError):
            civicclerk.get_event("ivgid", 999999, client=client)


# --- list_categories -----------------------------------------------------


def test_list_categories(fixture_client):
    with fixture_client() as client:
        categories = civicclerk.list_categories("ivgid", client=client)
    assert categories  # ivgid has at least one body
    assert all("id" in c for c in categories)


# --- fetch_file ----------------------------------------------------------


def test_fetch_file_returns_pdf_bytes(fixture_client, requested_urls):
    with fixture_client() as client:
        pdf = civicclerk.fetch_file("ivgid", 2800, client=client)
    assert pdf.startswith(b"%PDF")
    assert pdf == (FIXTURES / "ivgid_file_2800.pdf").read_bytes()
    assert "Meetings/GetMeetingFileStream(fileId=2800,plainText=false)" in (
        requested_urls[0]
    )


# --- Behaviour: retries, backoff, User-Agent, rate limit, timeout --------


def test_retry_with_backoff_on_5xx_and_429(monkeypatch):
    sleeps: list[float] = []
    monkeypatch.setattr(civicclerk.time, "sleep", sleeps.append)
    statuses = iter([500, 429])

    def handler(request: httpx.Request) -> httpx.Response:
        status = next(statuses, 200)
        if status != 200:
            return httpx.Response(status)
        return httpx.Response(200, json={"value": []})

    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        response = civicclerk._request(
            "https://ivgid.api.civicclerk.com/v1/EventCategories", client=client
        )
    assert response.status_code == 200
    assert sleeps == [1.0, 2.0]  # exponential backoff between attempts


def test_retry_on_transport_errors(monkeypatch):
    """Timeouts, DNS failures and connection resets retry with the same
    backoff as 429/5xx (all were observed transiently in the benchmark)."""
    sleeps: list[float] = []
    monkeypatch.setattr(civicclerk.time, "sleep", sleeps.append)
    errors = iter([httpx.ConnectError("dns fail"), httpx.ReadTimeout("slow")])

    def handler(request: httpx.Request) -> httpx.Response:
        error = next(errors, None)
        if error is not None:
            raise error
        return httpx.Response(200, json={"value": []})

    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        response = civicclerk._request(
            "https://ivgid.api.civicclerk.com/v1/EventCategories", client=client
        )
    assert response.status_code == 200
    assert sleeps == [1.0, 2.0]


def test_transport_error_raises_after_max_retries(monkeypatch):
    monkeypatch.setattr(civicclerk.time, "sleep", lambda _: None)
    calls = {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        raise httpx.ReadError("connection reset")

    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(httpx.ReadError):
            civicclerk._request(
                "https://ivgid.api.civicclerk.com/v1/EventCategories",
                client=client,
            )
    assert calls["n"] == civicclerk.MAX_RETRIES + 1


def test_retry_gives_up_after_max_retries(monkeypatch):
    monkeypatch.setattr(civicclerk.time, "sleep", lambda _: None)
    calls = {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        return httpx.Response(503)

    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(httpx.HTTPStatusError):
            civicclerk._request(
                "https://ivgid.api.civicclerk.com/v1/EventCategories",
                client=client,
            )
    assert calls["n"] == civicclerk.MAX_RETRIES + 1


def test_non_retryable_error_raises_immediately():
    calls = {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        return httpx.Response(404)

    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(httpx.HTTPStatusError):
            civicclerk._request(
                "https://ivgid.api.civicclerk.com/v1/Nope", client=client
            )
    assert calls["n"] == 1


def test_user_agent_identifies_project():
    seen: dict[str, str] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["ua"] = request.headers["user-agent"]
        return httpx.Response(200, json={"value": []})

    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        civicclerk.list_categories("ivgid", client=client)
    assert seen["ua"] == civicclerk.USER_AGENT
    assert "civic-meeting-record" in seen["ua"]
    assert "contact" in seen["ua"].lower()


def test_timeout_set_on_every_request():
    seen: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["timeout"] = request.extensions.get("timeout")
        return httpx.Response(200, json={"value": []})

    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        civicclerk.list_categories("ivgid", client=client)
    assert seen["timeout"] == {
        "connect": civicclerk.TIMEOUT_SECONDS,
        "read": civicclerk.TIMEOUT_SECONDS,
        "write": civicclerk.TIMEOUT_SECONDS,
        "pool": civicclerk.TIMEOUT_SECONDS,
    }


def test_rate_limit_enforces_minimum_interval(monkeypatch):
    sleeps: list[float] = []
    monkeypatch.setattr(civicclerk.time, "sleep", sleeps.append)
    monkeypatch.setattr(civicclerk, "MIN_REQUEST_INTERVAL", 1.0)
    monkeypatch.setattr(civicclerk, "_last_request_time", time.monotonic())
    civicclerk._throttle()
    assert len(sleeps) == 1
    assert 0.9 <= sleeps[0] <= 1.0  # back-to-back requests wait ~1 second
