#!/usr/bin/env python3
"""Check or copy the portable causal-halting skill package."""

from __future__ import annotations

import argparse
import filecmp
import json
import shutil
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PORTABLE_SKILL = ROOT if (ROOT / "SKILL.md").is_file() else ROOT / "skills" / "causal-halting"
DEFAULT_LOCAL_SKILL = Path.home() / ".codex" / "skills" / "causal-halting"


def plugin_version() -> str:
    manifest = ROOT / ".codex-plugin" / "plugin.json"
    if not manifest.is_file():
        return "unknown"
    data = json.loads(manifest.read_text(encoding="utf-8"))
    return str(data.get("version", "unknown"))


def skill_version(path: Path) -> str:
    readme = path / "README.md"
    if not readme.exists():
        return "missing"
    text = readme.read_text(encoding="utf-8", errors="ignore")
    for marker in ("v4.0", "4.0.0", "v3.1", "3.1.0", "v3.0", "3.0.0", "v2.0", "2.0.0"):
        if marker in text:
            return marker.strip("v")
    return "unknown"


def compare_dirs(left: Path, right: Path) -> list[str]:
    if not right.exists():
        return [f"missing target: {right}"]
    mismatches: list[str] = []
    for source in left.rglob("*"):
        if source.is_dir():
            continue
        rel = source.relative_to(left)
        target = right / rel
        if not target.exists():
            mismatches.append(f"missing {rel}")
        elif not filecmp.cmp(source, target, shallow=False):
            mismatches.append(f"different {rel}")
    return mismatches


def copy_skill(target: Path) -> None:
    source = PORTABLE_SKILL.resolve()
    destination = target.expanduser().resolve()
    if not source.is_dir():
        raise FileNotFoundError(f"portable skill source does not exist: {source}")
    if source == destination:
        return
    if source in destination.parents:
        raise ValueError(f"refusing to copy portable skill into its own tree: {destination}")
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination)


def status(targets: list[Path]) -> dict[str, Any]:
    return {
        "plugin_version": plugin_version(),
        "portable_skill": str(PORTABLE_SKILL),
        "targets": [
            {
                "path": str(target),
                "version": skill_version(target),
                "mismatches": compare_dirs(PORTABLE_SKILL, target),
            }
            for target in targets
        ],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Synchronize the causal-halting portable skill package.")
    parser.add_argument("--check", action="store_true", help="Compare portable skill with targets.")
    parser.add_argument("--install-local", action="store_true", help="Copy skill to ~/.codex/skills/causal-halting.")
    parser.add_argument("--target", action="append", help="Additional target skill directory.")
    parser.add_argument("--format", choices=("human", "json"), default="human")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    targets = [Path(path).expanduser() for path in (args.target or [])]
    if args.install_local:
        copy_skill(DEFAULT_LOCAL_SKILL)
        targets.append(DEFAULT_LOCAL_SKILL)
    if not targets:
        targets = [PORTABLE_SKILL]
    result = status(targets)
    failed = any(target["mismatches"] for target in result["targets"])
    if args.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"plugin_version: {result['plugin_version']}")
        for target in result["targets"]:
            print(f"target: {target['path']}")
            print(f"version: {target['version']}")
            print("status: " + ("different" if target["mismatches"] else "synced"))
            for mismatch in target["mismatches"]:
                print(f"  - {mismatch}")
    return 1 if args.check and failed else 0


if __name__ == "__main__":
    sys.exit(main())
