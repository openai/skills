#!/usr/bin/env python3
from __future__ import annotations

import argparse

from memory_utils import (
    ensure_local_install,
    list_log_files,
    parse_entry_line,
    skill_dir,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Delete a memory entry by ID across all logs."
    )
    parser.add_argument("--id", required=True, help="Entry ID to delete.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    base_dir = skill_dir()
    ensure_local_install(base_dir)

    matches: list[tuple] = []
    for log_path in list_log_files(base_dir):
        text = log_path.read_text(encoding="utf-8")
        lines = text.splitlines()
        for idx, line in enumerate(lines):
            entry = parse_entry_line(line)
            if entry and entry["id"] == args.id:
                matches.append((log_path, lines, idx))

    if not matches:
        raise SystemExit("Entry ID not found.")
    if len(matches) > 1:
        raise SystemExit("Entry ID appears multiple times. Refine the logs manually.")

    log_path, lines, idx = matches[0]
    del lines[idx]

    output = "\n".join(lines)
    if output:
        output += "\n"
    log_path.write_text(output, encoding="utf-8")

    print(f"Deleted entry ID: {args.id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
