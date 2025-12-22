#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime

from memory_utils import (
    ensure_ascii_english,
    ensure_local_install,
    list_log_files,
    parse_entry_line,
    skill_dir,
)

_REF_LEVEL_SCORES = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}

_TIME_FORMAT = "%Y-%m-%d:%H:%M"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Search memory logs in the easy-memory directory."
    )
    parser.add_argument(
        "keywords",
        nargs="+",
        help="English keywords (space-separated).",
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
    base_dir = skill_dir()
    ensure_local_install(base_dir)

    for keyword in args.keywords:
        ensure_ascii_english(keyword, "keyword")

    keywords = [k.lower() for k in args.keywords]
    max_results = args.max_results
    if max_results <= 0:
        raise SystemExit("max-results must be a positive integer.")

    matches = []
    order = 0
    for log_path in list_log_files(base_dir):
        for line in log_path.read_text(encoding="utf-8").splitlines():
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

    if not matches:
        print("No matching entries found.")
        return 0

    matches.sort(key=lambda item: (item["factual"], item["ref"], item["timestamp"]), reverse=True)
    results = [f"{item['log']}: {item['line']}" for item in matches[:max_results]]
    print("\n".join(results))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
