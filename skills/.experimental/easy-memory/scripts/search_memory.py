#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import date, datetime

from memory_utils import (
    log_base_dir,
    log_path_for_date,
    list_log_files,
    parse_entry_line,
    require_initialized,
)

_REF_LEVEL_SCORES = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}

_TIME_FORMAT = "%Y-%m-%d:%H:%M"

EMPTY_LOG_MESSAGE = (
    "No log entries for today. Created an empty log file; "
    "please continue with the remaining task steps."
)
NO_MATCH_MESSAGE = "No matching entries found for the provided keywords."
IMPORTANT_REMINDER = (
    "IMPORTANT NOTICE: The foregoing search history may be used as material reference "
    "for this task; however, should any subsequent work disclose new information "
    "inconsistent with, superseding, or rendering any entry outdated, you are hereby "
    "required, prior to writing new logs or submitting this task, to correct or update "
    "the relevant entries using the appropriate tool scripts, or to delete them."
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Search memory logs in the easy-memory directory."
    )
    parser.add_argument(
        "keywords",
        nargs="+",
        help="Keywords (English preferred; space-separated).",
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=5,
        help="Maximum number of entries to return (default: 5).",
    )
    return parser.parse_args()


def ref_level_score(value: str) -> int:
    normalized = value.strip().lower()
    if normalized in _REF_LEVEL_SCORES:
        return _REF_LEVEL_SCORES[normalized]
    try:
        return int(normalized)
    except ValueError:
        return 0


def parse_timestamp(value: str) -> datetime:
    try:
        return datetime.strptime(value, _TIME_FORMAT)
    except ValueError:
        return datetime.min


def main() -> int:
    args = parse_args()
    base_dir = log_base_dir(create=True)
    require_initialized(base_dir)

    keywords = [k.lower() for k in args.keywords]
    max_results = args.max_results
    if max_results <= 0:
        raise SystemExit("max-results must be a positive integer.")

    log_paths = list_log_files(base_dir)
    if not log_paths:
        log_path_for_date(date.today(), base_dir).touch()
        print(EMPTY_LOG_MESSAGE)
        return 0

    matches = []
    order = 0
    has_any_entries = False
    for log_path in log_paths:
        lines = log_path.read_text(encoding="utf-8").splitlines()
        if lines:
            has_any_entries = True
        for line in lines:
            entry = parse_entry_line(line)
            haystack = entry["content"] if entry else line
            if any(k in haystack.lower() for k in keywords):
                factual_score = 0
                ref_score = 0
                timestamp = datetime.min
                if entry:
                    factual_score = 1 if entry["factual"] else 0
                    ref_score = ref_level_score(entry["ref"])
                    timestamp = parse_timestamp(entry["timestamp"])
                matches.append(
                    {
                        "log": log_path.name,
                        "line": line,
                        "factual": factual_score,
                        "ref": ref_score,
                        "timestamp": timestamp,
                        "order": order,
                    }
                )
                order += 1

    if not has_any_entries:
        log_path = log_path_for_date(date.today(), base_dir)
        if not log_path.exists():
            log_path.touch()
        print(EMPTY_LOG_MESSAGE)
        return 0

    if not matches:
        print(NO_MATCH_MESSAGE)
        return 0

    matches.sort(key=lambda item: (item["factual"], item["ref"], item["timestamp"]), reverse=True)
    results = [f"{item['log']}: {item['line']}" for item in matches[:max_results]]
    results.append(IMPORTANT_REMINDER)
    print("\n".join(results))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
