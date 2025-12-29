#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime

from memory_utils import (
    ensure_single_line,
    format_entry_line,
    format_timestamp,
    list_log_files,
    log_base_dir,
    normalize_bool,
    parse_entry_line,
    require_initialized,
    validate_ref_level,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Update a memory entry by ID across all logs."
    )
    parser.add_argument("--id", required=True, help="Entry ID to update.")
    parser.add_argument(
        "--content",
        help="New content (English preferred; UTF-8 accepted).",
    )
    parser.add_argument(
        "--factual",
        help="Whether the entry is factual: true or false.",
    )
    parser.add_argument(
        "--ref-level",
        help="Reference level (e.g., low, medium, high, critical).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    base_dir = log_base_dir(create=True)
    require_initialized(base_dir)

    if not any([args.content, args.factual, args.ref_level]):
        raise SystemExit("Provide at least one field to update.")

    matches: list[tuple] = []
    for log_path in list_log_files(base_dir):
        text = log_path.read_text(encoding="utf-8")
        lines = text.splitlines()
        for idx, line in enumerate(lines):
            entry = parse_entry_line(line)
            if entry and entry["id"] == args.id:
                matches.append((log_path, lines, idx, entry))

    if not matches:
        raise SystemExit("Entry ID not found.")
    if len(matches) > 1:
        raise SystemExit("Entry ID appears multiple times. Refine the logs manually.")

    log_path, lines, idx, entry = matches[0]

    content = entry["content"]
    if args.content is not None:
        content = args.content.strip()
        if not content:
            raise SystemExit("content must not be empty.")
        ensure_single_line(content, "content")

    factual = entry["factual"]
    if args.factual is not None:
        factual = normalize_bool(args.factual)

    ref_level = entry["ref"]
    if args.ref_level is not None:
        ref_level = validate_ref_level(args.ref_level)

    timestamp = format_timestamp(datetime.now())
    lines[idx] = format_entry_line(args.id, ref_level, factual, content, timestamp)

    output = "\n".join(lines) + "\n"
    log_path.write_text(output, encoding="utf-8")

    print(f"Updated entry ID: {args.id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
