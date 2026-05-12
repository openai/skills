#!/usr/bin/env python3
"""Bootstrap ProjectGraph files into a target Codex Project."""

from __future__ import annotations

import argparse
import shutil
from datetime import datetime
from pathlib import Path


def read_template(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def render(template: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", value)
    return template


def write_rendered(path: Path, template_path: Path, values: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render(read_template(template_path), values), encoding="utf-8")


def append_agents_snippet(target: Path, snippet_path: Path) -> None:
    agents_path = target / "AGENTS.md"
    snippet = snippet_path.read_text(encoding="utf-8").strip()
    if agents_path.exists():
        current = agents_path.read_text(encoding="utf-8")
        if "ProjectGraph" in current and ".projectgraph/" in current:
            return
        agents_path.write_text(current.rstrip() + "\n\n" + snippet + "\n", encoding="utf-8")
    else:
        agents_path.write_text(snippet + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, help="Target Project root.")
    parser.add_argument("--project-name", help="Human-readable Project name.")
    parser.add_argument(
        "--timezone",
        default="local",
        help="Timezone string to write into bootstrap trace. Defaults to 'local'.",
    )
    parser.add_argument(
        "--append-agents",
        action="store_true",
        help="Append the ProjectGraph AGENTS.md section to the target Project.",
    )
    args = parser.parse_args()

    target = Path(args.target).expanduser().resolve()
    if not target.exists() or not target.is_dir():
        raise SystemExit(f"target does not exist or is not a directory: {target}")

    projectgraph = target / ".projectgraph"
    if projectgraph.exists():
        raise SystemExit(f"refusing to overwrite existing ProjectGraph: {projectgraph}")

    skill_root = Path(__file__).resolve().parents[1]
    templates = skill_root / "templates"
    assets = skill_root / "assets"
    project_name = args.project_name or target.name
    today = datetime.now().astimezone().date().isoformat()
    trace_filename = f"{today}-ProjectGraph-initialization.md"
    values = {
        "PROJECT_NAME": project_name,
        "PROJECT_ROOT": str(target),
        "DATE": today,
        "TIMEZONE": args.timezone,
        "TRACE_FILENAME": trace_filename,
    }

    (projectgraph / "TRACES").mkdir(parents=True)
    (projectgraph / "templates").mkdir(parents=True)
    (target / "tools" / "projectgraph").mkdir(parents=True)

    write_rendered(
        projectgraph / "PROJECT_GRAPH.json",
        templates / "PROJECT_GRAPH.template.json",
        values,
    )
    write_rendered(
        projectgraph / "TRACE_INDEX.json",
        templates / "TRACE_INDEX.template.json",
        values,
    )
    write_rendered(
        projectgraph / "PROJECT_GRAPH.md",
        templates / "PROJECT_GRAPH.template.md",
        values,
    )
    write_rendered(
        projectgraph / "TRACES" / trace_filename,
        templates / "SEED_TRACE_TEMPLATE.md",
        values,
    )

    for template_path in templates.iterdir():
        if template_path.is_file():
            shutil.copy2(template_path, projectgraph / "templates" / template_path.name)

    shutil.copy2(assets / "PROJECT_GRAPH.html", projectgraph / "PROJECT_GRAPH.html")
    shutil.copytree(assets / "vendor", projectgraph / "vendor")
    shutil.copy2(
        skill_root / "scripts" / "validate_projectgraph.py",
        target / "tools" / "projectgraph" / "validate_projectgraph.py",
    )
    shutil.copy2(
        skill_root / "scripts" / "capture_codex_trace.py",
        target / "tools" / "projectgraph" / "capture_codex_trace.py",
    )

    if args.append_agents:
        append_agents_snippet(target, templates / "AGENTS_PROJECTGRAPH_SNIPPET.md")
    else:
        shutil.copy2(
            templates / "AGENTS_PROJECTGRAPH_SNIPPET.md",
            projectgraph / "AGENTS_PROJECTGRAPH_SNIPPET.md",
        )

    print(f"ProjectGraph bootstrapped at {projectgraph}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
