#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_ROOT = ROOT / "assets" / "templates"


@dataclass(frozen=True)
class TemplateFile:
    source: str
    destination: str


TEMPLATE_FILES = (
    TemplateFile("AGENTS.md", "AGENTS.md"),
    TemplateFile("WORKFLOW.md", "WORKFLOW.md"),
    TemplateFile("PROGRESS.md", "PROGRESS.md"),
    TemplateFile("docs-boards-README.md", "docs/boards/README.md"),
    TemplateFile("phase-board.md", "docs/boards/phase-board.template.md"),
    TemplateFile("phase-spec.md", "docs/specs/phase-spec.template.md"),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scaffold Phasekeeper workflow files into a repository."
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Repository root to initialize. Defaults to the current directory.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing workflow files.",
    )
    return parser.parse_args()


def copy_template(target_root: Path, template_file: TemplateFile, *, force: bool) -> str:
    source = TEMPLATE_ROOT / template_file.source
    destination = target_root / template_file.destination
    existed = destination.exists()

    if existed and not force:
        return f"SKIPPED {template_file.destination} (already exists)"

    destination.parent.mkdir(parents=True, exist_ok=True)
    content = source.read_text(encoding="utf-8")
    destination.write_text(content, encoding="utf-8")

    if existed and force:
        return f"OVERWROTE {template_file.destination}"
    return f"CREATED {template_file.destination}"


def init_phasekeeper(target: Path, *, force: bool) -> list[str]:
    target_root = target.resolve()
    target_root.mkdir(parents=True, exist_ok=True)
    return [
        copy_template(target_root, template_file, force=force)
        for template_file in TEMPLATE_FILES
    ]


def main() -> int:
    args = parse_args()
    messages = init_phasekeeper(Path(args.target), force=args.force)
    for message in messages:
        print(message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
