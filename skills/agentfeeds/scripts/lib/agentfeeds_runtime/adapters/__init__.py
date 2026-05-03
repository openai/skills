"""Adapter registry for Agent Feeds streams."""

from __future__ import annotations

from agentfeeds_runtime.adapters.http import fetch_json
from agentfeeds_runtime.adapters.ical import fetch_ical
from agentfeeds_runtime.adapters.local_sources import fetch_filesystem_scan, fetch_git_status, fetch_markdown_scan
from agentfeeds_runtime.adapters.local_command import fetch_local_command
from agentfeeds_runtime.adapters.local_file import fetch_local_file
from agentfeeds_runtime.adapters.mac_native import fetch_apple_automation, fetch_plist_reading_list, fetch_sqlite_query
from agentfeeds_runtime.adapters.rss import fetch_rss


def run_adapter(stream: dict, parameters: dict, *, validate_parameters, source_uri_for, substitute) -> tuple[str, list[dict]]:
    validate_parameters(stream, parameters)
    stream_uri = source_uri_for(stream, parameters)
    adapter = substitute(stream["adapter"], parameters)
    kind = adapter["kind"]
    if kind in {"json_http", "paginated_json_http"}:
        return stream_uri, fetch_json(stream, adapter, stream_uri)
    if kind == "rss":
        return stream_uri, fetch_rss(stream, adapter, stream_uri)
    if kind == "ical":
        return stream_uri, fetch_ical(stream, adapter, stream_uri)
    if kind == "local_file":
        return stream_uri, fetch_local_file(stream, adapter, stream_uri)
    if kind == "filesystem_scan":
        return stream_uri, fetch_filesystem_scan(stream, adapter, stream_uri)
    if kind == "markdown_scan":
        return stream_uri, fetch_markdown_scan(stream, adapter, stream_uri)
    if kind == "git_status":
        return stream_uri, fetch_git_status(stream, adapter, stream_uri)
    if kind == "local_command":
        return stream_uri, fetch_local_command(stream, adapter, stream_uri)
    if kind == "apple_automation":
        return stream_uri, fetch_apple_automation(stream, adapter, stream_uri)
    if kind == "sqlite_query":
        return stream_uri, fetch_sqlite_query(stream, adapter, stream_uri)
    if kind == "plist_reading_list":
        return stream_uri, fetch_plist_reading_list(stream, adapter, stream_uri)
    raise ValueError(f"unsupported adapter kind: {kind}")
