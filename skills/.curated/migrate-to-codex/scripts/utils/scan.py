from __future__ import annotations

from collections.abc import Callable, Sequence
from pathlib import Path


def should_skip_inventory_child(child: Path) -> bool:
    return child.name in {".DS_Store", "__pycache__"}


def command_file_inventory(
    source_root: Path,
    command_file_sources: Sequence[tuple[Path, str, str]],
) -> tuple[tuple[str, tuple[str, ...]], ...]:
    inventory: list[tuple[str, tuple[str, ...]]] = []
    for relative_root, _name_prefix, provider in command_file_sources:
        absolute_root = source_root / relative_root
        if not absolute_root.exists():
            continue
        command_names = tuple(
            sorted(
                source_file.relative_to(absolute_root).with_suffix("").as_posix()
                for source_file in absolute_root.rglob("*.md")
            )
        )
        if command_names:
            inventory.append((provider, command_names))
    return tuple(inventory)


def render_named_inventory(
    lines: list[str],
    label: str,
    values: Sequence[str],
) -> None:
    if not values:
        lines.append(f"  inactive: {label} - none found")
        return
    lines.append(f"  active: {label} - {len(values)} found")
    for value in values:
        lines.append(f"    - {value}")


def skill_inventory_name(source_file: Path) -> str:
    if source_file.name == "SKILL.md":
        return source_file.parent.name
    return source_file.stem


def render_scope_inventory(
    source_root: Path,
    instruction_source_candidates: Sequence[Path],
    command_file_sources: Sequence[tuple[Path, str, str]],
    skill_source_roots: Sequence[Path],
    agent_source_roots: Sequence[Path],
    iter_skill_files: Callable[[Path], Sequence[Path]],
    iter_agent_files: Callable[[Path], Sequence[Path]],
    path_exists_with_exact_case: Callable[[Path], bool],
) -> str:
    lines = ["", "Migration inventory:"]
    instruction_candidates = tuple(
        candidate.as_posix()
        for candidate in instruction_source_candidates
        if path_exists_with_exact_case(source_root / candidate)
    )
    skill_names = tuple(
        sorted(
            {
                skill_inventory_name(source_file)
                for relative_root in skill_source_roots
                for source_file in iter_skill_files(source_root / relative_root)
            }
        )
    )
    agent_names = tuple(
        sorted(
            {
                source_file.stem
                for relative_root in agent_source_roots
                for source_file in iter_agent_files(source_root / relative_root)
            }
        )
    )

    render_named_inventory(lines, "instruction files", instruction_candidates)
    render_named_inventory(lines, "skills", skill_names)

    command_inventory = command_file_inventory(source_root, command_file_sources)
    if not command_inventory:
        lines.append("  inactive: command sources - none found")
    else:
        total_commands = sum(
            len(command_names) for _, command_names in command_inventory
        )
        lines.append(f"  active: command sources - {total_commands} found")
        for provider, command_names in command_inventory:
            lines.append(f"    provider: {provider} ({len(command_names)})")
            for command_name in command_names:
                lines.append(f"      - {command_name}")

    render_named_inventory(lines, "subagents", agent_names)
    return "\n".join(lines)


def render_source_inventory(
    source_root: Path,
    source_scan_roots: Sequence[tuple[Path, str]],
    path_exists_with_exact_case: Callable[[Path], bool],
) -> str:
    lines = ["", "Source inventory:"]
    discovered = False

    for relative_root, label in source_scan_roots:
        absolute_root = source_root / relative_root
        if not path_exists_with_exact_case(absolute_root):
            continue
        discovered = True
        lines.append(f"  detected: {relative_root.as_posix()} - {label}")
        try:
            children = sorted(
                absolute_root.iterdir(), key=lambda child: child.name.lower()
            )
        except FileNotFoundError:
            continue
        for child in children:
            if should_skip_inventory_child(child):
                continue
            child_kind = "dir" if child.is_dir() else "file"
            lines.append(f"    {child_kind}: {(relative_root / child.name).as_posix()}")

    if not discovered:
        lines.append("  inactive: No supported source directories found.")

    return "\n".join(lines)
