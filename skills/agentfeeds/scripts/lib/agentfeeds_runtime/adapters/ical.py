"""iCalendar adapter."""

from __future__ import annotations

import icalendar
import requests

from agentfeeds_runtime.adapters.common import envelope, stable_hash
from agentfeeds_runtime.constants import REQUEST_TIMEOUT_SECONDS


def serialize_ical_value(value: object) -> str | None:
    if value is None:
        return None
    decoded = getattr(value, "dt", value)
    if hasattr(decoded, "isoformat"):
        return decoded.isoformat()
    return str(decoded)


def fetch_ical(stream: dict, adapter: dict, stream_uri: str) -> list[dict]:
    response = requests.get(adapter["url"], timeout=REQUEST_TIMEOUT_SECONDS)
    response.raise_for_status()
    calendar = icalendar.Calendar.from_ical(response.content)
    events = []
    for component in calendar.walk("VEVENT"):
        data = {
            "uid": str(component.get("uid", "")),
            "summary": str(component.get("summary", "")),
            "starts_at": serialize_ical_value(component.get("dtstart")),
            "ends_at": serialize_ical_value(component.get("dtend")),
            "location": str(component.get("location")) if component.get("location") else None,
        }
        events.append(envelope(stream, stream_uri, data["uid"] or stable_hash(data), data))
    return events
