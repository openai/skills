#!/usr/bin/env python3
"""Copy a skill into a revision snapshot directory."""

import argparse
import json
import shutil
import time
from pathlib import Path

EXCLUDE_DIRS = {"__pycache__", "node_modules", "evals"}
EXCLUDE_SUFFIXES = {".pyc", ".skill"}


def ignore_names(_dir: str, names: list[str]) -> set[str]:
    ignored: set[str] = set()
    for name in names:
        if name in EXCLUDE_DIRS or name == ".DS_Store":
            ignored.add(name)
        elif any(name.endswith(suffix) for suffix in EXCLUDE_SUFFIXES):
            ignored.add(name)
    return ignored


def write_manifest(dest: Path, skill_path: Path, label: str, parent_label: str | None, note: str) -> None:
    manifest = {
        "label": label,
        "parent": parent_label,
        "skill_path": str(dest),
        "source_skill_path": str(skill_path),
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "note": note,
    }
    (dest / "snapshot_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Snapshot a skill for later comparison")
    parser.add_argument("skill_path", type=Path, help="Skill directory to snapshot")
    parser.add_argument("workspace", type=Path, help="Skill improver workspace root")
    parser.add_argument("--label", required=True, help="Revision label, e.g. original, iteration-1, iteration-2")
    parser.add_argument("--parent", default=None, help="Parent revision label")
    parser.add_argument("--note", default="", help="Short human-readable note for the manifest")
    parser.add_argument("--replace", action="store_true", help="Replace the snapshot if it already exists")
    args = parser.parse_args()

    skill_path = args.skill_path.resolve()
    if skill_path.is_file() and skill_path.name == "SKILL.md":
        skill_path = skill_path.parent
    if not (skill_path / "SKILL.md").exists():
        parser.error(f"No SKILL.md found in {skill_path}")

    dest = args.workspace.resolve() / "skill-revisions" / args.label
    if dest.exists():
        if not args.replace:
            parser.error(f"Snapshot already exists: {dest}")
        shutil.rmtree(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(skill_path, dest, ignore=ignore_names)
    write_manifest(dest, skill_path, args.label, args.parent, args.note)
    print(dest)


if __name__ == "__main__":
    main()
