#!/usr/bin/env python3
"""Run release hygiene checks for the ProjectGraph skill."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


REQUIRED_FILES = [
    "SKILL.md",
    "LICENSE.txt",
    "scripts/bootstrap_projectgraph.py",
    "scripts/capture_codex_trace.py",
    "scripts/validate_projectgraph.py",
    "templates/AGENTS_PROJECTGRAPH_SNIPPET.md",
    "templates/PROJECT_GRAPH.template.json",
    "templates/PROJECT_GRAPH.template.md",
    "templates/TRACE_INDEX.template.json",
    "templates/TRACE_LOCATOR_TEMPLATE.md",
    "templates/SEED_TRACE_TEMPLATE.md",
    "assets/PROJECT_GRAPH.html",
    "assets/vendor/markmap-0.18.12/VENDOR_MANIFEST.json",
]

FORBIDDEN_PATTERNS = [
    re.compile("/" + r"Users/[^/\s]+/"),
    re.compile(r"\b019e[0-9a-f]{4}-[0-9a-f-]{20,}\b", re.IGNORECASE),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\b[A-Z0-9_]*(?:SECRET|TOKEN|KEY)\s*=\s*['\"]?[^'\"\s]{8,}", re.IGNORECASE),
]

TEXT_SUFFIXES = {".md", ".py", ".json", ".html", ".css"}


def run(command: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(
            f"command failed ({result.returncode}): {' '.join(command)}\n{result.stdout}"
        )
    return result


def check_required_files(skill_root: Path) -> None:
    missing = [item for item in REQUIRED_FILES if not (skill_root / item).exists()]
    if missing:
        raise SystemExit("missing required release files:\n- " + "\n- ".join(missing))


def check_forbidden_text(skill_root: Path) -> None:
    hits: list[str] = []
    for path in skill_root.rglob("*"):
        if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
            continue
        rel = path.relative_to(skill_root)
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in FORBIDDEN_PATTERNS:
            if pattern.search(text):
                hits.append(f"{rel}: matches {pattern.pattern!r}")
    if hits:
        raise SystemExit("release source contains local or secret-looking text:\n- " + "\n- ".join(hits))


def check_templates(skill_root: Path) -> None:
    graph_template = json.loads((skill_root / "templates" / "PROJECT_GRAPH.template.json").read_text(encoding="utf-8"))
    views = graph_template.get("display", {}).get("views", [])
    if not views:
        raise SystemExit("PROJECT_GRAPH.template.json must include at least one display view")
    for view in views:
        if not view.get("id") or not view.get("title"):
            raise SystemExit("each display view must include id and title")


def check_scripts(skill_root: Path) -> None:
    scripts = skill_root / "scripts"
    for script in ("bootstrap_projectgraph.py", "capture_codex_trace.py", "validate_projectgraph.py", "check_release.py"):
        script_path = scripts / script
        compile(script_path.read_text(encoding="utf-8"), str(script_path), "exec")
    for script in ("bootstrap_projectgraph.py", "capture_codex_trace.py", "validate_projectgraph.py"):
        run([sys.executable, str(scripts / script), "--help"])


def check_bootstrap_and_capture(skill_root: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="projectgraph-release-") as temp_name:
        target = Path(temp_name) / "TargetProject"
        target.mkdir()
        run(
            [
                sys.executable,
                str(skill_root / "scripts" / "bootstrap_projectgraph.py"),
                "--target",
                str(target),
                "--project-name",
                "ReleaseSmoke",
            ]
        )
        run([sys.executable, str(target / "tools" / "projectgraph" / "validate_projectgraph.py"), "--root", str(target)])

        transcript = Path(temp_name) / "session.jsonl"
        transcript.write_text(
            "\n".join(
                [
                    json.dumps(
                        {
                            "timestamp": "2026-01-01T00:00:00Z",
                            "type": "session_meta",
                            "payload": {
                                "id": "release-smoke-session",
                                "cwd": str(target),
                            },
                        }
                    ),
                    json.dumps(
                        {
                            "timestamp": "2026-01-01T00:00:01Z",
                            "type": "event_msg",
                            "payload": {
                                "type": "task_started",
                                "turn_id": "release-smoke-turn",
                            },
                        }
                    ),
                    json.dumps(
                        {
                            "timestamp": "2026-01-01T00:00:02Z",
                            "type": "response_item",
                            "payload": {
                                "type": "message",
                                "role": "user",
                                "content": [{"type": "input_text", "text": "release smoke"}],
                            },
                        }
                    ),
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        capture = target / "tools" / "projectgraph" / "capture_codex_trace.py"
        first = run(
            [
                sys.executable,
                str(capture),
                "--root",
                str(target),
                "--transcript-path",
                str(transcript),
                "--title",
                "release-smoke",
            ]
        ).stdout.strip()
        second = run(
            [
                sys.executable,
                str(capture),
                "--root",
                str(target),
                "--transcript-path",
                str(transcript),
                "--title",
                "release-smoke",
            ]
        ).stdout.strip()
        if first == second:
            raise SystemExit("capture script did not create a unique trace path on repeated runs")
        if not Path(first).exists() or not Path(second).exists():
            raise SystemExit("capture script did not write expected trace files")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-root", default=".", help="Path to skills/projectgraph")
    args = parser.parse_args()

    skill_root = Path(args.skill_root).resolve()
    if not skill_root.exists():
        raise SystemExit(f"skill root does not exist: {skill_root}")
    if not shutil.which(sys.executable):
        raise SystemExit("python executable is not available")

    check_required_files(skill_root)
    check_forbidden_text(skill_root)
    check_templates(skill_root)
    check_scripts(skill_root)
    check_bootstrap_and_capture(skill_root)

    print(f"ProjectGraph skill release check passed: {skill_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
