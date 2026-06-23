#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime

from memory_utils import (
    clear_related_path_entry,
    clone_related_paths,
    ensure_single_line,
    format_related_path_lines,
    format_entry_line,
    format_timestamp,
    list_log_files,
    log_base_dir,
    normalize_related_paths,
    normalize_bool,
    parse_entry_line,
    replace_related_path_entry,
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
    parser.add_argument(
        "--related-path",
        action="append",
        default=None,
        help=(
            "Replace the stored related-path list with project-local paths, "
            "external absolute local paths, or URL/document addresses. "
            "Repeat to store multiple references."
        ),
    )
    parser.add_argument(
        "--clear-related-paths",
        action="store_true",
        help="Replace all stored related reference metadata with an empty list.",
    )
    parser.add_argument(
        "--path-update",
        action="append",
        default=None,
        help=(
            "Replace one stored reference in the form "
            "PATH_ID=<project/path|/absolute/path|https://url>. The existing "
            "path ID is preserved."
        ),
    )
    parser.add_argument(
        "--path-clear",
        action="append",
        default=None,
        help=(
            "Clear one stored related reference by PATH_ID while preserving the path ID "
            "for future updates."
        ),
    )
    return parser.parse_args()


def parse_path_update(raw_value: str) -> tuple[str, str]:
    path_id, separator, path_value = raw_value.partition("=")
    if not separator or not path_id or not path_value:
        raise SystemExit(
            "path-update must use the form PATH_ID=<project/path|/absolute/path|https://url>."
        )
    return path_id, path_value


def main() -> int:
    args = parse_args()
    base_dir = log_base_dir(create=True)
    require_initialized(base_dir)

    if args.related_path is not None and args.clear_related_paths:
        raise SystemExit("Use either --related-path or --clear-related-paths, not both.")
    if args.related_path is not None and (args.path_update or args.path_clear):
        raise SystemExit(
            "Use --related-path for whole-list replacement, or --path-update/--path-clear "
            "for per-reference changes, but not both together."
        )

    has_updates = any(
        [
            args.content is not None,
            args.factual is not None,
            args.ref_level is not None,
            args.related_path is not None,
            args.clear_related_paths,
            bool(args.path_update),
            bool(args.path_clear),
        ]
    )
    if not has_updates:
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

    has_paths_metadata = entry["has_paths_metadata"]
    path_entries = clone_related_paths(entry["path_entries"])
    if args.related_path is not None:
        path_entries = normalize_related_paths(args.related_path)
        has_paths_metadata = True
    elif args.clear_related_paths:
        path_entries = []
        has_paths_metadata = True
    elif args.path_update or args.path_clear:
        if not entry["has_paths_metadata"]:
            raise SystemExit("Entry does not contain related reference metadata.")
        update_pairs = [parse_path_update(item) for item in (args.path_update or [])]
        update_ids = {path_id for path_id, _ in update_pairs}
        clear_ids = set(args.path_clear or [])
        overlap = update_ids & clear_ids
        if overlap:
            overlap_text = ", ".join(sorted(overlap))
            raise SystemExit(
                f"path-update and path-clear cannot target the same related resource IDs: {overlap_text}"
            )
        for path_id, new_path in update_pairs:
            replace_related_path_entry(path_entries, path_id, new_path)
        for path_id in args.path_clear or []:
            clear_related_path_entry(path_entries, path_id)

    timestamp = format_timestamp(datetime.now())
    lines[idx] = format_entry_line(
        args.id,
        ref_level,
        factual,
        content,
        timestamp,
        path_entries=path_entries if has_paths_metadata else None,
    )

    output = "\n".join(lines) + "\n"
    log_path.write_text(output, encoding="utf-8")

    print(f"Updated entry ID: {args.id}")
    for line in format_related_path_lines(path_entries if has_paths_metadata else None):
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
