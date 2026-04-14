#!/usr/bin/env python3
"""Run trigger evaluation for a skill description.

Tests whether a skill's description causes Codex to trigger (read the skill)
for a set of queries. Outputs results as JSON.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import uuid
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.utils import parse_skill_md


def find_project_root() -> Path:
    """Find the project root used as context for temporary Codex evals."""
    current = Path.cwd()
    for parent in [current, *current.parents]:
        if (parent / ".git").is_dir():
            return parent
    return current


def build_agents_md(skill_name: str, skill_description: str, skill_path: Path) -> str:
    description = " ".join(skill_description.splitlines())
    return f"""# AGENTS.md instructions for Codex skill trigger evaluation

<INSTRUCTIONS>
## Skills
A skill is a set of local instructions to follow that is stored in a `SKILL.md` file.

### Available skills
- {skill_name}: {description} (file: {skill_path})

### How to use skills
- Discovery: The list above is the skills available in this session.
- Trigger rules: If the task clearly matches a skill's description, you must use that skill for this turn. Do not use skills that do not match the user request.
- How to use a skill: After deciding to use a skill, open its `SKILL.md` and follow the instructions there.
</INSTRUCTIONS>
"""


def build_sentinel_skill_md(skill_name: str, skill_description: str, sentinel: str) -> str:
    return f"""---
name: {skill_name}
description: {skill_description}
---

# {skill_name}

If you use this skill for the current request, include `{sentinel}` in your final response.
Do not include `{sentinel}` unless you have decided this skill is relevant and have read this file.
"""


def event_text(event: dict) -> str:
    try:
        return json.dumps(event)
    except TypeError:
        return str(event)


def codex_command(query: str, model: str | None, project_root: Path) -> list[str]:
    cmd = [
        "codex",
        "exec",
        "--json",
        "--ephemeral",
        "--skip-git-repo-check",
        "-s",
        "read-only",
        "-C",
        str(project_root),
    ]
    if model:
        cmd.extend(["--model", model])
    cmd.append(query)
    return cmd


def run_single_query(
    query: str,
    skill_name: str,
    skill_description: str,
    timeout: int,
    project_root: str,
    model: str | None = None,
) -> bool:
    """Run a single query and return whether the skill was triggered.

    Creates a temporary project containing an AGENTS.md skill registry and a
    sentinel SKILL.md, then runs `codex exec --json` with the raw query. The
    returned event stream is treated as triggered if Codex reads the sentinel
    skill path or includes the sentinel in its final answer.
    """
    unique_id = uuid.uuid4().hex[:8]
    sentinel = f"SKILL_TRIGGERED_{unique_id}"
    temp_root = Path(tempfile.mkdtemp(prefix="codex-skill-trigger-"))
    skill_path = temp_root / "skills" / skill_name / "SKILL.md"

    try:
        skill_path.parent.mkdir(parents=True, exist_ok=True)
        skill_path.write_text(build_sentinel_skill_md(skill_name, skill_description, sentinel))
        (temp_root / "AGENTS.md").write_text(
            build_agents_md(skill_name, skill_description, skill_path)
        )

        env = os.environ.copy()
        env["CODEX_DISABLE_SHELL_SNAPSHOT"] = "1"
        process = subprocess.run(
            codex_command(query, model, temp_root),
            cwd=project_root,
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )

        for line in process.stdout.splitlines():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            payload = event_text(event)
            if sentinel in payload or str(skill_path) in payload:
                return True
        return sentinel in process.stderr or str(skill_path) in process.stderr
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)


def run_eval(
    eval_set: list[dict],
    skill_name: str,
    description: str,
    num_workers: int,
    timeout: int,
    project_root: Path,
    runs_per_query: int = 1,
    trigger_threshold: float = 0.5,
    model: str | None = None,
) -> dict:
    """Run the full eval set and return results."""
    results = []

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        future_to_info = {}
        for item in eval_set:
            for run_idx in range(runs_per_query):
                future = executor.submit(
                    run_single_query,
                    item["query"],
                    skill_name,
                    description,
                    timeout,
                    str(project_root),
                    model,
                )
                future_to_info[future] = (item, run_idx)

        query_triggers: dict[str, list[bool]] = {}
        query_items: dict[str, dict] = {}
        for future in as_completed(future_to_info):
            item, _ = future_to_info[future]
            query = item["query"]
            query_items[query] = item
            if query not in query_triggers:
                query_triggers[query] = []
            try:
                query_triggers[query].append(future.result())
            except Exception as e:
                print(f"Warning: query failed: {e}", file=sys.stderr)
                query_triggers[query].append(False)

    for query, triggers in query_triggers.items():
        item = query_items[query]
        trigger_rate = sum(triggers) / len(triggers)
        should_trigger = item["should_trigger"]
        if should_trigger:
            did_pass = trigger_rate >= trigger_threshold
        else:
            did_pass = trigger_rate < trigger_threshold
        results.append({
            "query": query,
            "should_trigger": should_trigger,
            "trigger_rate": trigger_rate,
            "triggers": sum(triggers),
            "runs": len(triggers),
            "pass": did_pass,
        })

    passed = sum(1 for r in results if r["pass"])
    total = len(results)

    return {
        "skill_name": skill_name,
        "description": description,
        "results": results,
        "summary": {
            "total": total,
            "passed": passed,
            "failed": total - passed,
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Run trigger evaluation for a skill description")
    parser.add_argument("--eval-set", required=True, help="Path to eval set JSON file")
    parser.add_argument("--skill-path", required=True, help="Path to skill directory")
    parser.add_argument("--description", default=None, help="Override description to test")
    parser.add_argument("--num-workers", type=int, default=10, help="Number of parallel workers")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout per query in seconds")
    parser.add_argument("--runs-per-query", type=int, default=3, help="Number of runs per query")
    parser.add_argument("--trigger-threshold", type=float, default=0.5, help="Trigger rate threshold")
    parser.add_argument("--model", default=None, help="Model to use for codex exec (default: user's configured model)")
    parser.add_argument("--verbose", action="store_true", help="Print progress to stderr")
    args = parser.parse_args()

    eval_set = json.loads(Path(args.eval_set).read_text())
    skill_path = Path(args.skill_path)

    if not (skill_path / "SKILL.md").exists():
        print(f"Error: No SKILL.md found at {skill_path}", file=sys.stderr)
        sys.exit(1)

    name, original_description, content = parse_skill_md(skill_path)
    description = args.description or original_description
    project_root = find_project_root()

    if args.verbose:
        print(f"Evaluating: {description}", file=sys.stderr)

    output = run_eval(
        eval_set=eval_set,
        skill_name=name,
        description=description,
        num_workers=args.num_workers,
        timeout=args.timeout,
        project_root=project_root,
        runs_per_query=args.runs_per_query,
        trigger_threshold=args.trigger_threshold,
        model=args.model,
    )

    if args.verbose:
        summary = output["summary"]
        print(f"Results: {summary['passed']}/{summary['total']} passed", file=sys.stderr)
        for r in output["results"]:
            status = "PASS" if r["pass"] else "FAIL"
            rate_str = f"{r['triggers']}/{r['runs']}"
            print(f"  [{status}] rate={rate_str} expected={r['should_trigger']}: {r['query'][:70]}", file=sys.stderr)

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
