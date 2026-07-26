"""Record real CivicClerk API responses to tests/fixtures/ as JSON.

Captures, from the live ``ivgid`` API:

- ``ivgid_events_page1.json`` — first page of past events, with a real
  ``@odata.nextLink``
- ``ivgid_events_page2.json`` — the page that nextLink points at (proves
  pagination against real skiptokens)
- ``ivgid_event_743.json`` — a single event with media and published files
- ``ivgid_categories.json`` — the body list
- ``ivgid_event_cancelled.json`` — a cancelled event (no media, agenda only)
- ``ivgid_file_{id}.pdf`` — a real published Agenda PDF
- ``relative_media_event.json`` — an event (from another live slug) whose
  ``mediaStreamPath`` uses the relative ``stream/{SLUG}/…`` form, if one is
  found

Run from the repo root: ``python scripts/record_fixtures.py``
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

import civicclerk  # noqa: E402

FIXTURES = REPO_ROOT / "tests" / "fixtures"
BEFORE_DATE = "2026-07-26"


def save_json(name: str, payload: dict[str, Any]) -> None:
    path = FIXTURES / name
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"wrote {path.relative_to(REPO_ROOT)}")


def record_pages() -> dict[str, Any]:
    """Record the first two pages of past ivgid events; return page 1."""
    url = (
        civicclerk._base_url("ivgid")
        + "Events?$filter="
        + civicclerk.quote(f"startDateTime lt {BEFORE_DATE}")
        + "&$orderby="
        + civicclerk.quote(civicclerk.TWO_KEY_ORDERBY)
    )
    page1 = civicclerk._request(url).json()
    save_json("ivgid_events_page1.json", page1)
    next_link = page1.get("@odata.nextLink")
    if not next_link:
        raise SystemExit("page 1 had no @odata.nextLink — cannot record pagination")
    page2 = civicclerk._request(next_link).json()
    save_json("ivgid_events_page2.json", page2)
    return page1


def record_single_event() -> dict[str, Any]:
    event = civicclerk.get_event("ivgid", 743)
    assert event.get("hasMedia"), "event 743 was expected to have media"
    assert event.get("publishedFiles"), "event 743 was expected to have files"
    save_json("ivgid_event_743.json", {"value": [event]})
    return event


def record_categories() -> None:
    url = civicclerk._base_url("ivgid") + "EventCategories"
    save_json("ivgid_categories.json", civicclerk._request(url).json())


def record_cancelled_event(max_pages: int = 12) -> None:
    """Find a cancelled ivgid event (no media, agenda only) and record it."""
    url = (
        civicclerk._base_url("ivgid")
        + "Events?$filter="
        + civicclerk.quote(f"startDateTime lt {BEFORE_DATE}")
        + "&$orderby="
        + civicclerk.quote(civicclerk.TWO_KEY_ORDERBY)
    )
    next_url: Optional[str] = url
    for _ in range(max_pages):
        if not next_url:
            break
        payload = civicclerk._request(next_url).json()
        for event in payload.get("value", []):
            name = (event.get("eventName") or "").lower()
            if "cancel" in name and not event.get("hasMedia"):
                save_json("ivgid_event_cancelled.json", {"value": [event]})
                print(
                    f"cancelled event: id={event['id']} "
                    f"{event['eventName']!r} files="
                    f"{[f.get('type') for f in event.get('publishedFiles') or []]}"
                )
                return
        next_url = payload.get("@odata.nextLink")
    raise SystemExit("no cancelled event found — widen the search")


def record_agenda_pdf(event: dict[str, Any]) -> None:
    agendas = civicclerk.published_files(event, "Agenda")
    file_id = agendas[0]["fileId"]
    pdf = civicclerk.fetch_file("ivgid", file_id)
    assert pdf.startswith(b"%PDF"), f"expected PDF magic, got {pdf[:16]!r}"
    path = FIXTURES / f"ivgid_file_{file_id}.pdf"
    path.write_bytes(pdf)
    print(f"wrote {path.relative_to(REPO_ROOT)} ({len(pdf)} bytes)")


def record_relative_media_event(max_pages: int = 4) -> None:
    """Find a real event with a relative mediaStreamPath on another slug."""
    for slug in ("bristolct", "portlandme", "greenwoodvillageco"):
        url = (
            civicclerk._base_url(slug)
            + "Events?$filter="
            + civicclerk.quote(f"startDateTime lt {BEFORE_DATE}")
            + "&$orderby="
            + civicclerk.quote(civicclerk.TWO_KEY_ORDERBY)
        )
        next_url: Optional[str] = url
        for _ in range(max_pages):
            if not next_url:
                break
            payload = civicclerk._request(next_url).json()
            for event in payload.get("value", []):
                path = event.get("mediaStreamPath") or ""
                if path and not path.lower().startswith(("http://", "https://")):
                    save_json("relative_media_event.json", {"value": [event]})
                    print(f"relative media on {slug}: id={event['id']} {path!r}")
                    return
            next_url = payload.get("@odata.nextLink")
    print("WARNING: no relative-form mediaStreamPath found on any probed slug")


def main() -> None:
    FIXTURES.mkdir(parents=True, exist_ok=True)
    record_pages()
    event = record_single_event()
    record_categories()
    record_cancelled_event()
    record_agenda_pdf(event)
    record_relative_media_event()
    print("done")


if __name__ == "__main__":
    main()
