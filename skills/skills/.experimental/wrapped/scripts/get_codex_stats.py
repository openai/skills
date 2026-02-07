#!/usr/bin/env python3
"""
Aggregate Codex usage metrics for the Wrapped report.

Outputs JSON with rolling windows:
- all_time
- last_30_days
- last_7_days
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

CODEX_HOME = Path.home() / ".codex"
SESSION_DIRS = ["sessions", "archived_sessions"]
DEFAULT_TIMEZONE = None
DEFAULT_OUTPUT_PATH = Path(__file__).with_name("wrapped_stats.json")
WINDOW_DELTAS = {
    "all_time": None,
    "last_30_days": 30,
    "last_7_days": 7,
}


@dataclass
class WindowAccumulator:
    name: str
    start: datetime | None
    session_count: int = 0
    total_assistant_messages: int = 0
    total_user_messages: int = 0
    turn_usage_seconds: float = 0.0
    session_span_seconds: float = 0.0
    day_tokens: dict[datetime.date, int] = field(default_factory=lambda: defaultdict(int))
    active_days: set[datetime.date] = field(default_factory=set)
    hour_usage: dict[int, int] = field(default_factory=lambda: defaultdict(int))
    repo_usage: dict[str, int] = field(default_factory=lambda: defaultdict(int))
    longest_turn_duration: float = 0.0
    longest_turn_timestamp: datetime | None = None
    longest_turn_session: str | None = None


def parse_timestamp(ts: str) -> datetime:
    if not ts:
        raise ValueError("Empty timestamp")
    if ts.endswith("Z"):
        ts = ts[:-1] + "+00:00"
    return datetime.fromisoformat(ts)


def iter_session_files() -> Iterable[Path]:
    for rel in SESSION_DIRS:
        root = CODEX_HOME / rel
        if not root.exists():
            continue
        yield from root.rglob("*.jsonl")


def format_tokens(value: int) -> str:
    if value <= 0:
        return "0"
    if value >= 1_000_000:
        scaled = value / 1_000_000
        return f"{scaled:.1f}M".replace(".0M", "M")
    if value >= 1_000:
        scaled = value / 1_000
        return f"{scaled:.1f}k".replace(".0k", "k")
    return f"{value:,}"


def render_usage_hours(seconds: float) -> str:
    if seconds <= 0:
        return "0 minutes"
    hours = seconds / 3600
    if hours < 1:
        minutes = int(round(seconds / 60))
        minutes = max(minutes, 1)
        return f"{minutes} minute{'s' if minutes != 1 else ''}"
    rounded_hours = int(round(hours))
    rounded_hours = max(rounded_hours, 1)
    return f"{rounded_hours} hour{'s' if rounded_hours != 1 else ''}"


def build_contrib_lines(active_days: set[datetime.date]) -> list[str]:
    if not active_days:
        return []

    day_set = set(active_days)
    first_date = min(day_set)
    last_date = max(day_set)

    def to_sunday(dt: datetime.date) -> datetime.date:
        offset = (dt.weekday() + 1) % 7
        return dt - timedelta(days=offset)

    def to_saturday(dt: datetime.date) -> datetime.date:
        offset = 6 - ((dt.weekday() + 1) % 7)
        return dt + timedelta(days=offset)

    start = to_sunday(first_date)
    end = to_saturday(last_date)
    total_days = (end - start).days + 1
    total_weeks = total_days // 7

    weekday_labels = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    line_chars: list[list[str]] = [[] for _ in range(7)]

    for week_index in range(total_weeks):
        week_start = start + timedelta(days=week_index * 7)
        for day_offset in range(7):
            current_day = week_start + timedelta(days=day_offset)
            char = "•" if current_day in day_set else "◦"
            line_chars[day_offset].append(char)

    contrib_lines = [
        f"{weekday_labels[idx]}  {''.join(chars)}" for idx, chars in enumerate(line_chars) if chars
    ]
    return contrib_lines


def local_timezone_name() -> str:
    local_tz = datetime.now().astimezone().tzinfo
    if hasattr(local_tz, "key") and local_tz.key:
        return local_tz.key
    if local_tz:
        return str(local_tz)
    return "UTC"


def get_timezone(tz_name: str) -> ZoneInfo:
    try:
        return ZoneInfo(tz_name)
    except ZoneInfoNotFoundError:
        fallback = local_timezone_name()
        try:
            return ZoneInfo(fallback)
        except ZoneInfoNotFoundError:
            return ZoneInfo("UTC")


def classify_hour(hour: int | None) -> str:
    if hour is None:
        return "unknown"
    if 22 <= hour or hour <= 3:
        return "owl"
    if 4 <= hour <= 9:
        return "bird"
    if 10 <= hour <= 16:
        return "day"
    return "eve"


def longest_streak(active_days: set[datetime.date]) -> int:
    if not active_days:
        return 0
    sorted_days = sorted(active_days)
    longest = 1
    current = 1
    prev_day = sorted_days[0]
    for day in sorted_days[1:]:
        if day == prev_day + timedelta(days=1):
            current += 1
        elif day == prev_day:
            pass
        else:
            longest = max(longest, current)
            current = 1
        prev_day = day
    longest = max(longest, current)
    return longest


def window_stats(window: WindowAccumulator, tz_abbrev: str) -> dict[str, object]:
    total_tokens = sum(window.day_tokens.values())
    active_days_count = len(window.active_days)
    peak_hour = None
    if window.hour_usage:
        peak_hour = max(window.hour_usage.items(), key=lambda item: item[1])[0]

    peak_hour_display = f"{peak_hour:02d}:00" if peak_hour is not None else "unknown"
    peak_hour_label = classify_hour(peak_hour)
    if peak_hour is not None:
        peak_hour_slot = f"{peak_hour_display} {peak_hour_label}"
    else:
        peak_hour_slot = "unknown"

    biggest_day_date = None
    biggest_day_tokens = 0
    if window.day_tokens:
        biggest_day_date, biggest_day_tokens = max(
            window.day_tokens.items(), key=lambda item: item[1]
        )
    if biggest_day_date:
        biggest_day_display = f"{biggest_day_date.day} {biggest_day_date.strftime('%b')}"
    else:
        biggest_day_display = "unknown"

    top_repo = None
    if window.repo_usage:
        top_repo = max(window.repo_usage.items(), key=lambda item: item[1])[0]
    if top_repo:
        repo_path = Path(top_repo)
        top_repo_label = repo_path.name or str(repo_path)
    else:
        top_repo_label = "unknown"

    usage_seconds = max(window.session_span_seconds, window.turn_usage_seconds)
    usage_hours_display = render_usage_hours(usage_seconds)

    streak_days = longest_streak(window.active_days)
    usage_streak_display = (
        f"{streak_days} day" if streak_days == 1 else f"{streak_days} days" if streak_days else "unknown"
    )

    longest_turn_display = "unknown"
    if window.longest_turn_timestamp is not None:
        minutes = int(window.longest_turn_duration // 60)
        seconds = int(round(window.longest_turn_duration % 60))
        longest_turn_display = f"{minutes}m {seconds}s"

    return {
        "sessions": window.session_count,
        "sessions_display": f"{window.session_count:,}",
        "assistant_messages": window.total_assistant_messages,
        "assistant_messages_display": f"{window.total_assistant_messages:,}",
        "user_messages": window.total_user_messages,
        "user_messages_display": f"{window.total_user_messages:,}",
        "active_days": active_days_count,
        "active_days_display": f"{active_days_count:,}",
        "total_tokens": total_tokens,
        "total_tokens_display": format_tokens(total_tokens),
        "usage_hours_display": usage_hours_display,
        "peak_hour": peak_hour,
        "peak_hour_display": peak_hour_display,
        "peak_hour_label": peak_hour_label,
        "peak_hour_slot": peak_hour_slot,
        "timezone_abbrev": tz_abbrev,
        "usage_streak_days": streak_days,
        "usage_streak_display": usage_streak_display,
        "biggest_day_display": biggest_day_display,
        "biggest_day_tokens": biggest_day_tokens,
        "top_repo_display": top_repo_label,
        "longest_turn_display": longest_turn_display,
    }


def gather_metrics(tz_name: str) -> dict[str, object]:
    target_tz = get_timezone(tz_name)
    now_local = datetime.now(target_tz)

    windows: dict[str, WindowAccumulator] = {}
    for name, delta in WINDOW_DELTAS.items():
        start = None if delta is None else now_local - timedelta(days=delta)
        windows[name] = WindowAccumulator(name=name, start=start)

    joined_at: datetime | None = None

    for session_path in iter_session_files():
        current_turn_start: datetime | None = None
        session_start: datetime | None = None
        session_end: datetime | None = None
        session_workspace: str | None = None

        try:
            with session_path.open("r", encoding="utf-8") as handle:
                for raw_line in handle:
                    raw_line = raw_line.strip()
                    if not raw_line:
                        continue
                    try:
                        record = json.loads(raw_line)
                    except json.JSONDecodeError:
                        continue

                    ts_str = record.get("timestamp")
                    if not ts_str:
                        ts_str = record.get("payload", {}).get("timestamp")
                        if not ts_str:
                            continue
                    try:
                        ts = parse_timestamp(ts_str)
                    except ValueError:
                        continue

                    local_ts = ts.astimezone(target_tz)
                    if session_start is None:
                        session_start = local_ts
                    session_end = local_ts

                    rec_type = record.get("type")
                    payload = record.get("payload", {})

                    for window in windows.values():
                        if window.start is None or local_ts >= window.start:
                            window.active_days.add(local_ts.date())

                    if rec_type == "response_item" and payload.get("type") == "message":
                        role = payload.get("role")
                        for window in windows.values():
                            if window.start is None or local_ts >= window.start:
                                if role == "assistant":
                                    window.total_assistant_messages += 1
                                elif role == "user":
                                    window.total_user_messages += 1
                                window.hour_usage[local_ts.hour] += 1

                    if rec_type == "session_meta":
                        session_workspace = (
                            payload.get("workspacePath")
                            or payload.get("workspace_path")
                            or payload.get("cwd")
                            or session_workspace
                        )

                    if rec_type == "turn_context":
                        session_workspace = (
                            payload.get("workspacePath")
                            or payload.get("workspace_path")
                            or payload.get("cwd")
                            or session_workspace
                        )
                        current_turn_start = ts
                        continue

                    if rec_type == "event_msg" and payload.get("type") == "token_count":
                        info = payload.get("info")
                        if not info or current_turn_start is None:
                            continue
                        duration = (ts - current_turn_start).total_seconds()
                        if duration < 0:
                            duration = 0
                        usage = info.get("last_token_usage") or info.get("total_token_usage")
                        tokens = 0
                        if usage and usage.get("total_tokens"):
                            tokens = usage["total_tokens"]

                        for window in windows.values():
                            if window.start is None or local_ts >= window.start:
                                window.turn_usage_seconds += duration
                                if duration > window.longest_turn_duration:
                                    window.longest_turn_duration = duration
                                    window.longest_turn_timestamp = local_ts
                                    window.longest_turn_session = session_path.name
                                if tokens:
                                    window.day_tokens[local_ts.date()] += tokens
                        current_turn_start = None

        except OSError:
            continue

        if session_start and (joined_at is None or session_start < joined_at):
            joined_at = session_start

        if session_start and session_end:
            for window in windows.values():
                if window.start is None:
                    window_start = session_start
                else:
                    window_start = max(window.start, session_start)
                window_end = min(session_end, now_local)
                overlap = (window_end - window_start).total_seconds()
                if overlap > 0:
                    window.session_span_seconds += overlap
                    window.session_count += 1
                    if session_workspace:
                        window.repo_usage[session_workspace] += 1

    tz_abbrev = now_local.strftime("%Z")
    if joined_at:
        joined_str = joined_at.date().isoformat()
        joined_label = joined_at.strftime("%b %d")
        days_diff = (now_local.date() - joined_at.date()).days
        days_ago = f"{days_diff} day{'s' if days_diff != 1 else ''} ago"
        joined_display = f"{joined_label} ({days_ago})"
    else:
        joined_str = "unknown"
        days_ago = "unknown"
        joined_display = "unknown"

    metrics: dict[str, object] = {
        "timezone": tz_name,
        "timezone_abbrev": tz_abbrev,
        "generated_at": now_local.isoformat(),
        "joined_date": joined_str,
        "joined_days_ago": days_ago,
        "joined_display": joined_display,
        "joined_relative_display": days_ago,
        "windows": {name: window_stats(win, tz_abbrev) for name, win in windows.items()},
        "contrib_lines": build_contrib_lines(windows["all_time"].active_days),
    }

    return metrics


def print_text(metrics: dict[str, object]) -> None:
    all_time = metrics.get("windows", {}).get("all_time", {})
    print(f"Joined Codex: {metrics.get('joined_display', 'unknown')}")
    print(f"Sessions: {all_time.get('sessions_display', '0')}")
    print(f"Assistant messages: {all_time.get('assistant_messages_display', '0')}")
    print(f"Prompts: {all_time.get('user_messages_display', '0')}")
    print(f"Tokens: {all_time.get('total_tokens_display', '0')}")
    print(f"Usage time: {all_time.get('usage_hours_display', 'unknown')}")
    print(f"Peak hour: {all_time.get('peak_hour_slot', 'unknown')}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute Codex Wrapped usage metrics.")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit metrics as JSON for scripting.",
    )
    parser.add_argument(
        "--timezone",
        default=local_timezone_name(),
        help="IANA timezone name for local stats (defaults to system timezone).",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT_PATH),
        help=f"Path to save metrics JSON (default: {DEFAULT_OUTPUT_PATH}).",
    )
    args = parser.parse_args()

    metrics = gather_metrics(args.timezone)

    output_path = Path(args.output).expanduser()
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(metrics, handle, indent=2)
        handle.write("\n")

    if args.json:
        json.dump(metrics, fp=sys.stdout, indent=2)
        print()
        return

    print(f"Wrote stats to {output_path}")
    print_text(metrics)


if __name__ == "__main__":
    main()
