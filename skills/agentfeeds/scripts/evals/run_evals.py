#!/usr/bin/env python3
"""Run AgentSkills-style eval cases with Codex CLI."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import shutil
import subprocess
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_EVALS = ROOT / "evals" / "evals.json"
DEFAULT_WORKSPACE = ROOT.parent / "agentfeeds-eval-workspace"


def slug(value: str) -> str:
    return "".join(ch if ch.isalnum() else "-" for ch in value.lower()).strip("-")


def load_evals(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("skill_name") != "agentfeeds":
        raise SystemExit(f"unexpected skill_name in {path}: {data.get('skill_name')}")
    for item in data.get("evals") or []:
        for file in item.get("files") or []:
            if not (ROOT / file).exists():
                raise SystemExit(f"missing eval input file: {file}")
    return data


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_prompt(case: dict, output_dir: Path, *, with_skill: bool) -> str:
    files = case.get("files") or []
    skill_line = f"- Skill path: {ROOT}" if with_skill else "- Skill path: none; answer without using the Agent Feeds skill instructions."
    file_lines = "\n".join(f"  - {ROOT / file}" for file in files) or "  - none"
    assertions = "\n".join(f"  - {item}" for item in case.get("assertions") or [])
    return f"""Execute this eval task in a clean context.

{skill_line}
- Task: {case["prompt"]}
- Input files:
{file_lines}
- Save any produced files to: {output_dir}

Expected output:
{case["expected_output"]}

Assertions to satisfy:
{assertions}

Keep the final answer concise and include the commands you used when relevant.
Do not edit files in the skill repository. Put all artifacts, temporary Agent Feeds roots, draft templates, reports, logs, and generated files under the output directory above.
"""


def run_case(case: dict, target: Path, *, with_skill: bool, model: str | None) -> dict:
    outputs = target / "outputs"
    outputs.mkdir(parents=True, exist_ok=True)
    prompt = build_prompt(case, outputs, with_skill=with_skill)
    prompt_path = target / "prompt.txt"
    output_path = target / "output.txt"
    prompt_path.write_text(prompt, encoding="utf-8")

    command = [
        "codex",
        "exec",
        "--cd",
        str(ROOT),
        "--sandbox",
        "danger-full-access",
        "--dangerously-bypass-approvals-and-sandbox",
        "--ephemeral",
        "--output-last-message",
        str(output_path),
    ]
    if model:
        command.extend(["--model", model])
    command.append(prompt)

    started = time.monotonic()
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    duration_ms = round((time.monotonic() - started) * 1000)
    (target / "stdout.log").write_text(result.stdout, encoding="utf-8")
    (target / "stderr.log").write_text(result.stderr, encoding="utf-8")
    timing = {"duration_ms": duration_ms, "returncode": result.returncode}
    write_json(target / "timing.json", timing)
    return timing


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Agent Feeds eval cases")
    parser.add_argument("--evals", type=Path, default=DEFAULT_EVALS)
    parser.add_argument("--workspace", type=Path, default=DEFAULT_WORKSPACE)
    parser.add_argument("--iteration", default="iteration-1")
    parser.add_argument("--case", action="append", help="run only this eval id; repeatable")
    parser.add_argument("--with-skill-only", action="store_true", help="skip baseline runs")
    parser.add_argument("--model", help="optional Codex model override")
    parser.add_argument("--jobs", type=int, default=6, help="parallel model runs when --execute is set")
    parser.add_argument("--execute", action="store_true", help="actually run Codex model calls")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    data = load_evals(args.evals)
    selected = set(args.case or [])
    cases = [case for case in data["evals"] if not selected or case["id"] in selected]
    if selected and len(cases) != len(selected):
        found = {case["id"] for case in cases}
        raise SystemExit(f"unknown eval case(s): {', '.join(sorted(selected - found))}")

    iteration = args.workspace / args.iteration
    plan = []
    for case in cases:
        case_dir = iteration / f"eval-{slug(case['id'])}"
        targets = [("with_skill", True)]
        if not args.with_skill_only:
            targets.append(("without_skill", False))
        for name, with_skill in targets:
            target = case_dir / name
            plan.append((case, target, with_skill))

    print(f"workspace: {iteration}")
    print(f"planned runs: {len(plan)}")
    for case, target, with_skill in plan:
        print(f"- {case['id']} -> {target.relative_to(args.workspace)}")
        if not args.execute:
            target.mkdir(parents=True, exist_ok=True)
            (target / "prompt.txt").write_text(build_prompt(case, target / "outputs", with_skill=with_skill), encoding="utf-8")

    if not args.execute:
        print("dry run only; pass --execute to spend model calls")
        return 0

    if not shutil.which("codex"):
        raise SystemExit("codex CLI not found on PATH")

    jobs = max(1, args.jobs)
    results = []
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        futures = {}
        for case, target, with_skill in plan:
            label = "with_skill" if with_skill else "without_skill"
            print(f"starting {case['id']} ({label})")
            future = pool.submit(run_case, case, target, with_skill=with_skill, model=args.model)
            futures[future] = (case, target, label)
        for future in as_completed(futures):
            case, target, label = futures[future]
            timing = future.result()
            print(f"finished {case['id']} ({label}) returncode={timing['returncode']} duration_ms={timing['duration_ms']}")
            results.append({"id": case["id"], "variant": label, "target": str(target), **timing})
    results.sort(key=lambda item: (item["id"], item["variant"]))
    write_json(iteration / "run-summary.json", {"runs": results})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
