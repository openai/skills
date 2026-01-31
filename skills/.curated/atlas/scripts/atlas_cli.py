from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterable, Sequence

from atlas_common import (
    AtlasError,
    copy_sqlite_db,
    detect_atlas_app_name,
    detect_tab_capable_app_name,
    get_bookmarks_path,
    get_history_path,
    tell_atlas,
)

ROW_SEP = "|||"
CHROME_EPOCH_OFFSET_SECONDS = 11_644_473_600
DEFAULT_HISTORY_LIMIT = 200
DEFAULT_BOOKMARK_LIMIT = 200


@dataclass(slots=True)
class Tab:
    title: str
    url: str
    window_id: int
    tab_index: int
    is_active: bool


@dataclass(slots=True)
class HistoryRow:
    id: int
    url: str
    title: str
    last_visited_at: str


@dataclass(slots=True)
class Bookmark:
    id: str
    name: str
    url: str
    date_added: str
    folder: str | None = None


def _escape_applescript_string(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def _chrome_microseconds_to_iso_date(value: str | None) -> str:
    if not value:
        return "unknown"

    try:
        timestamp = int(value)
    except ValueError:
        return "unknown"

    unix_seconds = timestamp / 1_000_000 - CHROME_EPOCH_OFFSET_SECONDS
    try:
        dt = datetime.fromtimestamp(unix_seconds)
    except (OverflowError, OSError, ValueError):
        return "unknown"
    return dt.date().isoformat()


def _chrome_time_from_unix_seconds(unix_seconds: float) -> int:
    return int((unix_seconds + CHROME_EPOCH_OFFSET_SECONDS) * 1_000_000)


def _chrome_time_bounds_today() -> tuple[int, int]:
    now = datetime.now().astimezone()
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)
    return (
        _chrome_time_from_unix_seconds(start.timestamp()),
        _chrome_time_from_unix_seconds(end.timestamp()),
    )


def get_tabs() -> list[Tab]:
    tab_app = detect_tab_capable_app_name()
    script_body = f"""
set tabList to {{}}

repeat with w in every window
  set windowId to id of w
  set tabIndex to 0
  set activeIndex to active tab index of w
  try
    set winTabs to every tab of w
    repeat with t in winTabs
      set tabIndex to tabIndex + 1
      set tabTitle to title of t
      set tabURL to URL of t
      set isActive to (tabIndex = activeIndex)
      set end of tabList to {{tabTitle, tabURL, windowId, tabIndex, isActive}}
    end repeat
  end try
end repeat

set output to ""
repeat with tabInfo in tabList
  set output to output & item 1 of tabInfo & "{ROW_SEP}" & item 2 of tabInfo & "{ROW_SEP}" & item 3 of tabInfo & "{ROW_SEP}" & item 4 of tabInfo & "{ROW_SEP}" & item 5 of tabInfo & "\\n"
end repeat

return output
""".strip()

    raw = tell_atlas(script_body, app_name=tab_app)
    if not raw:
        return []

    tabs: list[Tab] = []
    for line in raw.splitlines():
        parts = line.split(ROW_SEP)
        if len(parts) != 5:
            continue
        title, url, window_id, tab_index, is_active = parts
        try:
            tabs.append(
                Tab(
                    title=title,
                    url=url,
                    window_id=int(window_id),
                    tab_index=int(tab_index),
                    is_active=is_active == "true",
                )
            )
        except ValueError:
            continue

    return tabs


def open_new_tab(url: str) -> None:
    escaped_url = _escape_applescript_string(url)
    script_body = f"""
activate
delay 0.1
open location "{escaped_url}"

activate
""".strip()
    tell_atlas(script_body)


def focus_tab(window_id: int, tab_index: int) -> None:
    tab_app = detect_tab_capable_app_name()
    script_body = f"""
activate
set _wnd to first window whose id is {window_id}
set index of _wnd to 1
set active tab index of _wnd to {tab_index}
return true
""".strip()
    tell_atlas(script_body, app_name=tab_app)


def close_tab(window_id: int, tab_index: int) -> None:
    tab_app = detect_tab_capable_app_name()
    script_body = f"""
set _wnd to first window whose id is {window_id}
tell _wnd
  close tab {tab_index}
end tell
""".strip()
    tell_atlas(script_body, app_name=tab_app)


def reload_tab(window_id: int, tab_index: int) -> None:
    tab_app = detect_tab_capable_app_name()
    script_body = f"""
set _wnd to first window whose id is {window_id}
tell _wnd
  reload tab {tab_index}
end tell
""".strip()
    tell_atlas(script_body, app_name=tab_app)


def _history_query(
    terms: Sequence[str],
    limit: int,
    *,
    chrome_start: int | None = None,
    chrome_end: int | None = None,
) -> tuple[str, list[str | int]]:
    params: list[str | int] = []
    conditions: list[str] = []

    if terms:
        for term in terms:
            conditions.append("(url LIKE ? OR title LIKE ?)")
            like = f"%{term}%"
            params.extend([like, like])

    if chrome_start is not None:
        conditions.append("last_visit_time >= ?")
        params.append(chrome_start)

    if chrome_end is not None:
        conditions.append("last_visit_time < ?")
        params.append(chrome_end)

    where_clause = ""
    if conditions:
        where_clause = "\nWHERE " + " AND ".join(conditions)

    base = f"""
WITH filtered AS (
  SELECT id, url, title, last_visit_time
  FROM urls{where_clause}
),
ranked AS (
  SELECT
    id,
    url,
    title,
    last_visit_time,
    ROW_NUMBER() OVER (
      PARTITION BY url
      ORDER BY last_visit_time DESC, id DESC
    ) AS rn
  FROM filtered
)
SELECT
  id,
  url,
  title,
  datetime(last_visit_time / 1000000 + (strftime('%s', '1601-01-01')), 'unixepoch', 'localtime') AS lastVisitedAt
FROM ranked
WHERE rn = 1
ORDER BY last_visit_time DESC
LIMIT ?
""".strip()

    params.append(limit)
    return base, params


def search_history(search_text: str | None, limit: int, *, today: bool = False) -> list[HistoryRow]:
    history_path = get_history_path()
    db_copy = copy_sqlite_db(history_path)

    terms = [t for t in (search_text or "").split() if t]
    chrome_start: int | None = None
    chrome_end: int | None = None
    if today:
        chrome_start, chrome_end = _chrome_time_bounds_today()

    query, params = _history_query(terms, limit, chrome_start=chrome_start, chrome_end=chrome_end)

    conn = sqlite3.connect(db_copy)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(query, params).fetchall()
    finally:
        conn.close()

    history: list[HistoryRow] = []
    for row in rows:
        history.append(
            HistoryRow(
                id=int(row["id"]),
                url=str(row["url"] or ""),
                title=str(row["title"] or ""),
                last_visited_at=str(row["lastVisitedAt"] or ""),
            )
        )
    return history


def _iter_bookmark_nodes(node: dict, folder: str) -> Iterable[Bookmark]:
    node_type = str(node.get("type") or "")
    if node_type == "url" and node.get("url"):
        yield Bookmark(
            id=str(node.get("id") or ""),
            name=str(node.get("name") or "Untitled"),
            url=str(node.get("url") or ""),
            date_added=_chrome_microseconds_to_iso_date(node.get("date_added")),
            folder=folder or None,
        )

    children = node.get("children") or []
    if not isinstance(children, list):
        return

    current_folder = str(node.get("name") or folder)
    for child in children:
        if isinstance(child, dict):
            yield from _iter_bookmark_nodes(child, current_folder)


def get_bookmarks(limit: int, search_text: str | None) -> list[Bookmark]:
    bookmarks_path = get_bookmarks_path()
    data = json.loads(bookmarks_path.read_text(encoding="utf-8"))

    roots = data.get("roots") or {}
    ordered_roots = [
        ("Bookmarks Bar", roots.get("bookmark_bar") or {}),
        ("Other Bookmarks", roots.get("other") or {}),
        ("Synced Bookmarks", roots.get("synced") or {}),
    ]

    bookmarks: list[Bookmark] = []
    for folder_name, root in ordered_roots:
        if isinstance(root, dict):
            bookmarks.extend(_iter_bookmark_nodes(root, folder_name))

    if search_text:
        lowered = search_text.lower()
        bookmarks = [
            b
            for b in bookmarks
            if lowered in b.name.lower() or lowered in b.url.lower() or lowered in (b.folder or "").lower()
        ]

    return bookmarks[:limit]


def _print_table(rows: Iterable[Sequence[object]], headers: Sequence[str]) -> None:
    widths = [len(h) for h in headers]
    materialized = [tuple(str(cell) for cell in row) for row in rows]
    for row in materialized:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))

    def fmt_row(row: Sequence[str]) -> str:
        return "  ".join(cell.ljust(widths[i]) for i, cell in enumerate(row))

    print(fmt_row(headers))
    print(fmt_row(["-" * w for w in widths]))
    for row in materialized:
        print(fmt_row(row))


def _render_tabs(tabs: list[Tab], as_json: bool) -> None:
    if as_json:
        print(json.dumps([asdict(t) for t in tabs], indent=2))
        return

    rows = [
        (
            "*" if t.is_active else " ",
            t.window_id,
            t.tab_index,
            t.title,
            t.url,
        )
        for t in tabs
    ]
    _print_table(rows, headers=["A", "window_id", "tab", "title", "url"])


def _render_history(rows: list[HistoryRow], as_json: bool) -> None:
    if as_json:
        print(json.dumps([asdict(r) for r in rows], indent=2))
        return

    table = [(r.last_visited_at, r.title, r.url) for r in rows]
    _print_table(table, headers=["last_visited_at", "title", "url"])


def _render_bookmarks(rows: list[Bookmark], as_json: bool) -> None:
    if as_json:
        print(json.dumps([asdict(r) for r in rows], indent=2))
        return

    table = [(r.folder or "", r.name, r.url, r.date_added) for r in rows]
    _print_table(table, headers=["folder", "name", "url", "date_added"])


def _parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Control ChatGPT Atlas from the terminal.")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("app-name", help="Print the detected Atlas application name")

    tabs_parser = sub.add_parser("tabs", help="List open Atlas tabs")
    tabs_parser.add_argument("--json", action="store_true", help="Emit JSON instead of a table")

    open_parser = sub.add_parser("open-tab", help="Open a new Atlas tab")
    open_parser.add_argument("url", help="URL to open")

    focus_parser = sub.add_parser("focus-tab", help="Focus a tab by window id and tab index")
    focus_parser.add_argument("window_id", type=int, help="Atlas window id (from tabs output)")
    focus_parser.add_argument("tab_index", type=int, help="Tab index within the window (1-based)")

    close_parser = sub.add_parser("close-tab", help="Close a tab by window id and tab index")
    close_parser.add_argument("window_id", type=int, help="Atlas window id (from tabs output)")
    close_parser.add_argument("tab_index", type=int, help="Tab index within the window (1-based)")

    reload_parser = sub.add_parser("reload-tab", help="Reload a tab by window id and tab index")
    reload_parser.add_argument("window_id", type=int, help="Atlas window id (from tabs output)")
    reload_parser.add_argument("tab_index", type=int, help="Tab index within the window (1-based)")

    history_parser = sub.add_parser("history", help="Search Atlas history")
    history_parser.add_argument("--search", default=None, help="Space-separated search terms")
    history_parser.add_argument("--limit", type=int, default=DEFAULT_HISTORY_LIMIT, help="Max rows to return")
    history_parser.add_argument(
        "--today",
        action="store_true",
        help="Limit results to pages visited today (local time)",
    )
    history_parser.add_argument("--json", action="store_true", help="Emit JSON instead of a table")

    bookmarks_parser = sub.add_parser("bookmarks", help="List Atlas bookmarks")
    bookmarks_parser.add_argument("--search", default=None, help="Filter bookmarks by text")
    bookmarks_parser.add_argument("--limit", type=int, default=DEFAULT_BOOKMARK_LIMIT, help="Max rows to return")
    bookmarks_parser.add_argument("--json", action="store_true", help="Emit JSON instead of a table")

    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv or sys.argv[1:])

    try:
        if args.command == "app-name":
            print(detect_atlas_app_name())
            return 0

        if args.command == "tabs":
            _render_tabs(get_tabs(), as_json=args.json)
            return 0

        if args.command == "open-tab":
            open_new_tab(args.url)
            print(f"Opened tab: {args.url}")
            return 0

        if args.command == "focus-tab":
            focus_tab(args.window_id, args.tab_index)
            print(f"Focused window id {args.window_id}, tab {args.tab_index}")
            return 0

        if args.command == "close-tab":
            close_tab(args.window_id, args.tab_index)
            print(f"Closed window id {args.window_id}, tab {args.tab_index}")
            return 0

        if args.command == "reload-tab":
            reload_tab(args.window_id, args.tab_index)
            print(f"Reloaded window id {args.window_id}, tab {args.tab_index}")
            return 0

        if args.command == "history":
            rows = search_history(args.search, max(1, args.limit), today=args.today)
            _render_history(rows, as_json=args.json)
            return 0

        if args.command == "bookmarks":
            rows = get_bookmarks(max(1, args.limit), args.search)
            _render_bookmarks(rows, as_json=args.json)
            return 0

        raise AtlasError(f"Unknown command: {args.command}")
    except AtlasError as exc:
        print(f"atlas error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
