"""RSS and Atom adapter."""

from __future__ import annotations

import feedparser

from agentfeeds_runtime.adapters.common import envelope, stable_hash


def fetch_rss(stream: dict, adapter: dict, stream_uri: str) -> list[dict]:
    parsed = feedparser.parse(adapter["url"])
    if parsed.bozo:
        raise ValueError(f"{stream['id']}: failed to parse RSS feed: {parsed.bozo_exception}")
    events = []
    for entry in parsed.entries:
        data = {
            "title": entry.get("title", ""),
            "link": entry.get("link"),
            "summary": entry.get("summary"),
            "published": entry.get("published"),
            "id": entry.get("id") or entry.get("guid") or entry.get("link"),
        }
        event_id = data["id"] or stable_hash(data)
        events.append(envelope(stream, stream_uri, event_id, data))
    return events
