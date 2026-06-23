#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import date, datetime
from uuid import uuid4

from memory_utils import (
    ensure_single_line,
    format_related_path_lines,
    format_entry_line,
    format_timestamp,
    log_base_dir,
    log_path_for_date,
    normalize_related_paths,
    normalize_bool,
    require_initialized,
    validate_ref_level,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Append a memory entry to today's log."
    )
    parser.add_argument(
        "--content",
        required=True,
        help="Log content (English preferred; UTF-8 accepted).",
    )
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
    parser.add_argument(
        "--related-path",
        action="append",
        default=None,
        help=(
            "Project-local path, external absolute local path, or "
            "URL/document address for the current or highly related file, "
            "directory, page, or document. Repeat this option to store "
            "multiple references."
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    base_dir = log_base_dir(create=True)
    require_initialized(base_dir)

    content = args.content.strip()
    if not content:
        raise SystemExit("content must not be empty.")

    ensure_single_line(content, "content")

    factual = normalize_bool(args.factual)
    ref_level = validate_ref_level(args.ref_level)
    path_entries = None
    if args.related_path is not None:
        path_entries = normalize_related_paths(args.related_path)

    entry_id = uuid4().hex
    timestamp = format_timestamp(datetime.now())

    entry_line = format_entry_line(
        entry_id,
        ref_level,
        factual,
        content,
        timestamp,
        path_entries=path_entries,
    )

    log_path = log_path_for_date(date.today(), base_dir)
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(entry_line)
        handle.write("\n")

    print(f"Appended entry ID: {entry_id}")
    for line in format_related_path_lines(path_entries):
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
