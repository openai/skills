#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import date, datetime
from uuid import uuid4

from memory_utils import (
    ensure_ascii_english,
    ensure_single_line,
    format_entry_line,
    format_timestamp,
    log_base_dir,
    log_path_for_date,
    normalize_bool,
    validate_ref_level,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Append a memory entry to today's log."
    )
    parser.add_argument("--content", required=True, help="English log content.")
    parser.add_argument(
        "--factual",
        required=True,
        help="Whether the entry is factual: true or false.",
    )
    parser.add_argument(
        "--ref-level",
        required=True,
        help="Reference level (e.g., low, medium, high, critical).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    base_dir = log_base_dir(create=True)

    content = args.content.strip()
    if not content:
        raise SystemExit("content must not be empty.")

    ensure_single_line(content, "content")
    ensure_ascii_english(content, "content")

    factual = normalize_bool(args.factual)
    ref_level = validate_ref_level(args.ref_level)

    entry_id = uuid4().hex
    timestamp = format_timestamp(datetime.now())

    entry_line = format_entry_line(entry_id, ref_level, factual, content, timestamp)

    log_path = log_path_for_date(date.today(), base_dir)
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(entry_line)
        handle.write("\n")

    print(f"Appended entry ID: {entry_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
