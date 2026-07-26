"""Shared test setup: path wiring, fixture loading, mock transport.

Tests run against real recorded API responses in tests/fixtures/ (captured by
scripts/record_fixtures.py), served through an httpx.MockTransport so the
client's full request path — URL construction, $select guard, pagination,
retries — executes for real.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Callable

import httpx
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

import civicclerk  # noqa: E402

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def load_fixture(name: str) -> dict[str, Any]:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


@pytest.fixture(autouse=True)
def no_rate_limit(monkeypatch: pytest.MonkeyPatch) -> None:
    """Disable the 1 req/s courtesy delay so the suite runs fast."""
    monkeypatch.setattr(civicclerk, "MIN_REQUEST_INTERVAL", 0.0)


@pytest.fixture
def requested_urls() -> list[str]:
    return []


@pytest.fixture
def fixture_client(
    requested_urls: list[str],
) -> Callable[[], httpx.Client]:
    """An httpx.Client whose transport serves the recorded fixtures.

    Every requested URL is appended to ``requested_urls`` for assertions.
    """
    page1 = load_fixture("ivgid_events_page1.json")
    page2 = load_fixture("ivgid_events_page2.json")
    event_743 = load_fixture("ivgid_event_743.json")
    event_cancelled = load_fixture("ivgid_event_cancelled.json")
    categories = load_fixture("ivgid_categories.json")
    pdf_bytes = (FIXTURES / "ivgid_file_2800.pdf").read_bytes()

    def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        requested_urls.append(url)
        if "GetMeetingFileStream" in url:
            return httpx.Response(
                200, content=pdf_bytes, headers={"Content-Type": "application/pdf"}
            )
        if "EventCategories" in url:
            return httpx.Response(200, json=categories)
        if "id%20eq%20743" in url or "id eq 743" in url:
            return httpx.Response(200, json=event_743)
        if "id%20eq%20738" in url or "id eq 738" in url:
            return httpx.Response(200, json=event_cancelled)
        if "id%20eq%20" in url or "id eq " in url:
            return httpx.Response(200, json={"value": []})
        if "skiptoken" in url:
            # Only the skiptoken recorded on page 1's real nextLink is known.
            assert "id-749" in url, f"unexpected skiptoken URL: {url}"
            return httpx.Response(200, json=page2)
        if "/Events" in url:
            return httpx.Response(200, json=page1)
        raise AssertionError(f"unexpected URL: {url}")

    return lambda: httpx.Client(transport=httpx.MockTransport(handler))
