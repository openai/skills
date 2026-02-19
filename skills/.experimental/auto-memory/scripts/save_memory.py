#!/usr/bin/env python3
"""Persist project-scoped markdown memory notes with deduplication."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from common import (
    DEFAULT_SECTION_CONTENT,
    MemoryValidationError,
    append_changelog_entry,
    choose_latest_note,
    detect_secret_indicators,
    ensure_project_name,
    list_notes,
    memory_dir_for_project,
    merge_required_sections,
    merge_tags,
    next_note_path,
    normalize_sections,
    normalize_tags,
    normalize_title_for_match,
    now_iso,
    parse_iso_datetime,
    render_sections,
    titles_are_near_duplicates,
    write_note,
)
from protocol_tags import build_protocol_tags


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Save or update a durable project memory note.")
    parser.add_argument("--project", required=True, help="Project scope for memory operations.")
    parser.add_argument("--title", required=True, help="Memory note title.")
    body_group = parser.add_mutually_exclusive_group(required=True)
    body_group.add_argument("--body", help="Memory body content.")
    body_group.add_argument("--body-file", help="Path to a file containing body content.")
    parser.add_argument("--tags", default="", help="Comma-separated tags.")
    parser.add_argument(
        "--tag",
        action="append",
        default=[],
        help="Add a single tag (repeatable).",
    )
    parser.add_argument("--protocol-task-id", default="", help="Protocol task id for standardized tagging.")
    parser.add_argument("--protocol-state", default="", help="Protocol lifecycle state for standardized tagging.")
    parser.add_argument("--protocol-owner-role", default="", help="Protocol owner role for standardized tagging.")
    parser.add_argument("--protocol-handoff-id", default="", help="Protocol handoff id for standardized tagging.")
    parser.add_argument(
        "--protocol-project",
        default="",
        help="Optional protocol project tag value (defaults to --project).",
    )
    parser.add_argument(
        "--strict-sections",
        action="store_true",
        help=(
            "Reject writes when Decision/Rationale/Implementation/Verification/Follow-ups "
            "resolve to placeholder content."
        ),
    )
    return parser.parse_args()


def load_body(args: argparse.Namespace) -> str:
    if args.body is not None:
        return args.body
    return Path(args.body_file).read_text(encoding="utf-8")


def parse_tag_inputs(tags_csv: str, explicit_tags: list[str]) -> list[str]:
    raw: list[str] = []
    if tags_csv:
        raw.extend([piece.strip() for piece in tags_csv.split(",") if piece.strip()])
    raw.extend([tag.strip() for tag in explicit_tags if tag.strip()])
    return normalize_tags(raw)


def parse_protocol_tag_inputs(args: argparse.Namespace, project: str) -> list[str]:
    has_protocol_args = any(
        [
            args.protocol_task_id.strip(),
            args.protocol_state.strip(),
            args.protocol_owner_role.strip(),
            args.protocol_handoff_id.strip(),
            args.protocol_project.strip(),
        ]
    )
    if not has_protocol_args:
        return []

    protocol_project = args.protocol_project.strip() or project
    return build_protocol_tags(
        task_id=args.protocol_task_id,
        state=args.protocol_state,
        owner_role=args.protocol_owner_role,
        handoff_id=args.protocol_handoff_id,
        project=protocol_project,
    )


def mark_superseded(note_path: Path, canonical_filename: str, timestamp: str) -> None:
    from common import read_note

    note = read_note(note_path)
    marker = f"> Superseded by `{canonical_filename}` on {timestamp}."
    lines = note.body.splitlines()
    if lines and lines[0].startswith("> Superseded by `"):
        lines[0] = marker
        new_body = "\n".join(lines).strip() + "\n"
    else:
        new_body = f"{marker}\n\n{note.body.strip()}\n"

    new_frontmatter = dict(note.frontmatter)
    new_frontmatter["superseded_by"] = canonical_filename
    new_frontmatter["superseded_at"] = timestamp
    write_note(note.path, new_frontmatter, new_body)


def clear_superseded_marker(note_path: Path) -> None:
    from common import read_note

    note = read_note(note_path)
    frontmatter = dict(note.frontmatter)
    body_lines = note.body.splitlines()
    changed = False
    if "superseded_by" in frontmatter:
        frontmatter.pop("superseded_by", None)
        changed = True
    if "superseded_at" in frontmatter:
        frontmatter.pop("superseded_at", None)
        changed = True
    if body_lines and body_lines[0].startswith("> Superseded by `"):
        body_lines = body_lines[1:]
        if body_lines and body_lines[0].strip() == "":
            body_lines = body_lines[1:]
        changed = True
    if changed:
        new_body = "\n".join(body_lines).strip() + "\n"
        write_note(note.path, frontmatter, new_body)


def latest_by_declared_date(notes):
    return max(notes, key=lambda note: parse_iso_datetime(note.date))


STRICT_SECTION_NAMES = (
    "Decision",
    "Rationale",
    "Implementation",
    "Verification",
    "Follow-ups",
)


def _is_placeholder_section(section_name: str, value: str) -> bool:
    text = value.strip()
    if not text:
        return True

    normalized = text.lower()
    default = DEFAULT_SECTION_CONTENT[section_name].strip().lower()
    if normalized == default:
        return True
    return normalized in {"todo", "- todo", "- to do", "tbd", "- tbd"}


def strict_section_violations(required_sections: dict[str, str]) -> list[str]:
    violations: list[str] = []
    for section_name in STRICT_SECTION_NAMES:
        if _is_placeholder_section(section_name, required_sections.get(section_name, "")):
            violations.append(section_name)
    return violations


def main() -> int:
    args = parse_args()
    try:
        project = ensure_project_name(args.project)
    except MemoryValidationError as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, indent=2))
        return 2

    title = args.title.strip()
    if not title:
        print(json.dumps({"status": "error", "error": "title must not be empty"}, indent=2))
        return 2

    body = load_body(args)
    secret_reasons = detect_secret_indicators(f"{title}\n{body}")
    if secret_reasons:
        print(
            json.dumps(
                {
                    "status": "blocked",
                    "error": "Potential secret-like content detected. Do not store secrets in markdown memory notes.",
                    "secret_indicators": secret_reasons,
                    "next_step": "Persist secret values with store_secret_env.py and keep only variable names + redacted hints in memory notes.",
                },
                indent=2,
            )
        )
        return 2

    memory_dir = memory_dir_for_project(project)
    memory_dir.mkdir(parents=True, exist_ok=True)

    incoming_tags = parse_tag_inputs(args.tags, args.tag)
    try:
        protocol_tags = parse_protocol_tag_inputs(args, project)
    except Exception as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, indent=2))
        return 2
    incoming_tags = merge_tags(incoming_tags, protocol_tags)
    notes = list_notes(memory_dir)
    normalized_title = normalize_title_for_match(title)
    exact_matches = [note for note in notes if normalize_title_for_match(note.title) == normalized_title]

    timestamp = now_iso()
    action = "created"
    updated_path: Path
    extras = []

    incoming_sections, incoming_extras = normalize_sections(body)
    if exact_matches:
        canonical = choose_latest_note(exact_matches)
        existing_sections, existing_extras = normalize_sections(canonical.body)
        merged = merge_required_sections(existing_sections, incoming_sections)
        append_changelog_entry(merged, f"{timestamp}: updated via save_memory.")
        merged_tags = merge_tags(canonical.tags, incoming_tags)
        updated_path = canonical.path
        action = "updated"
        # Keep historical extra headings while allowing incoming extras to add new headings.
        existing_extra_names = [name for name, _ in existing_extras]
        extras = list(existing_extras)
        for name, content in incoming_extras:
            if name not in existing_extra_names:
                extras.append((name, content))
    else:
        merged = incoming_sections
        append_changelog_entry(merged, f"{timestamp}: created via save_memory.")
        merged_tags = incoming_tags
        updated_path = next_note_path(memory_dir, title)
        extras = incoming_extras

    if args.strict_sections:
        invalid_sections = strict_section_violations(merged)
        if invalid_sections:
            print(
                json.dumps(
                    {
                        "status": "error",
                        "error": "strict-sections validation failed",
                        "invalid_sections": invalid_sections,
                    },
                    indent=2,
                )
            )
            return 2

    frontmatter = {
        "title": title,
        "date": timestamp,
        "project": project,
        "tags": merged_tags,
    }
    write_note(updated_path, frontmatter, render_sections(merged, extras=extras))

    # Reconcile near-duplicate titles and mark non-canonical files as superseded.
    all_notes = list_notes(memory_dir)
    duplicate_cluster = [note for note in all_notes if titles_are_near_duplicates(note.title, title)]
    superseded_files: list[str] = []
    canonical_file = updated_path.name
    if len(duplicate_cluster) > 1:
        canonical = latest_by_declared_date(duplicate_cluster)
        canonical_file = canonical.path.name
        clear_superseded_marker(canonical.path)
        for note in duplicate_cluster:
            if note.path == canonical.path:
                continue
            mark_superseded(note.path, canonical.path.name, timestamp)
            superseded_files.append(note.path.name)

    print(
        json.dumps(
            {
                "status": "ok",
                "project": project,
                "action": action,
                "file": str(updated_path),
                "canonical_file": canonical_file,
                "reconciled_superseded_files": superseded_files,
                "tags": merged_tags,
                "protocol_tags": protocol_tags,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
