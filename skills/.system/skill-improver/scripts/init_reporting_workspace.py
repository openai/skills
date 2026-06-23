#!/usr/bin/env python3
"""Scaffold and maintain a reporting workspace for skill-improver runs.

Creates a stable per-skill reporting directory with:
- evals.json as the canonical editable eval definition
- report.md for side-by-side artifact review and rubric notes
- status.md for simple run status and test coverage
- slack-post.md for a team-facing summary once the iteration is ready to share

When an improver workspace is provided, the script also syncs the canonical
evals.json into <workspace>/runs/evals/evals.json so execution uses the exact
definition stored in skill-reporting/.
"""

import argparse
import json
import shutil
import time
from pathlib import Path


def slugify(value: str) -> str:
    return "".join(ch if ch.isalnum() or ch in {"-", "_"} else "-" for ch in value).strip("-").lower()


def write_if_missing(path: Path, content: str) -> None:
    if not path.exists():
        path.write_text(content)


def default_evals(skill_name: str) -> dict:
    return {
        "skill_name": skill_name,
        "evals": [],
    }


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def format_test_coverage(evals_path: Path, run_dir: Path | None) -> str:
    eval_count = 0
    if evals_path.exists():
        try:
            eval_count = len(load_json(evals_path).get("evals", []))
        except (json.JSONDecodeError, OSError, AttributeError):
            eval_count = 0

    if not run_dir:
        return f"{eval_count} prompts drafted" if eval_count else "not started"

    with_skill = 0
    without_skill = 0
    for eval_dir in sorted(path for path in run_dir.iterdir() if path.is_dir()) if run_dir.exists() else []:
        if (eval_dir / "with_skill").is_dir():
            with_skill += 1
        if (eval_dir / "without_skill").is_dir():
            without_skill += 1

    if with_skill or without_skill:
        return f"{eval_count} prompts configured; {with_skill} with-skill runs and {without_skill} baseline runs present"
    return f"{eval_count} prompts configured"


def format_overall_performance(benchmark_path: Path | None) -> str:
    if not benchmark_path or not benchmark_path.exists():
        return "not yet assessed"

    try:
        benchmark = load_json(benchmark_path)
    except (json.JSONDecodeError, OSError):
        return "benchmark present but unreadable"

    summary = benchmark.get("run_summary") or {}
    with_skill = summary.get("with_skill", {}).get("pass_rate", {}).get("mean")
    without_skill = summary.get("without_skill", {}).get("pass_rate", {}).get("mean")
    delta = summary.get("delta", {}).get("pass_rate")

    if with_skill is None and without_skill is None:
        return "benchmark generated but pass-rate summary missing"

    parts: list[str] = []
    if with_skill is not None:
        parts.append(f"with-skill pass rate {with_skill:.0%}")
    if without_skill is not None:
        parts.append(f"baseline pass rate {without_skill:.0%}")
    if delta is not None:
        parts.append(f"delta {delta}")
    return "; ".join(parts)


def status_template(
    skill_name: str,
    reporting_dir: Path,
    improver_workspace: Path | None,
    plugin_skill_path: Path | None,
    installed_skill_path: Path | None,
    evals_path: Path,
    run_dir: Path | None = None,
    benchmark_path: Path | None = None,
    run_status: str = "draft",
) -> str:
    improver_line = str(improver_workspace) if improver_workspace else "TBD"
    plugin_line = str(plugin_skill_path) if plugin_skill_path else "TBD"
    installed_line = str(installed_skill_path) if installed_skill_path else "TBD"
    timestamp = time.strftime("%Y-%m-%d %H:%M %Z", time.localtime())
    return f"""# {skill_name} Eval Status

- Last updated: {timestamp}
- Status: {run_status}
- Test coverage: {format_test_coverage(evals_path, run_dir)}
- Overall performance: {format_overall_performance(benchmark_path)}
- Reporting workspace: {reporting_dir}
- Improver workspace: {improver_line}
- Repo-local fork: {plugin_line}
- Installed skill source: {installed_line}

## What to update

- Set `Status` to one of: `draft`, `approved`, `running`, `under review`, `update ready`, `complete`.
- Replace `Test coverage` with a short note on how many prompts were run and whether they cover connector and non-connector cases.
- Replace `Overall performance` with a short statement on how the skill compared to baseline.
"""


def report_template(skill_name: str) -> str:
    return f"""# {skill_name} Evaluation Report

## Scope

- Skill:
- Current revision:
- Comparison:
- Date range:
- Owner:

## Eval Status

- Stage:
- Coverage summary:
- Overall outcome:

## Rubric

| Dimension | Weight | What it checks | 1 | 3 | 5 | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Task success | 35% | Did the skill solve the task and produce the requested outcome? | Failed, off-target, or unusable. | Partially solved; usable but missing important pieces. | Fully solved; directly useful in a real workflow. | Include qualitative details for the score. |
| Output quality | 35% | Correctness, completeness, and output formatting. | Major errors or weak recommendations. | Mostly sound but shallow, uneven, or missing depth. | High-quality, well-reasoned, and decision-useful. | Include qualitative details for the score. |
| Context retrieval quality | 10% | Whether it pulled the right sources or clearly asked for missing context. | Missed obvious context or used weak sources. | Retrieved some relevant context but not enough. | Retrieved the right context with strong source selection. | |
| Skill orchestration | 10% | Whether it used the right skills and sequence of actions. | Did not use expected skills. | Mixed execution quality. | Well-executed skill use. | |
| Efficiency | 10% | Perceived time and effort relative to task complexity. | Slow, bloated, or clearly did unnecessary work. | Acceptable efficiency for the task. | Fast and appropriately scoped. | Include time-to-completion notes. |

## Eval Matrix

Use 3-5 hero prompts per use case. Where appropriate, include a few that avoid connectors and instead use uploaded files or public information. Map each prompt to expected skills to make debugging easier.

| Eval prompt | Use case | Expected skills | With skill output | Without skill output | Preference | Rubric notes | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Prompt 1 |  |  |  |  |  |  | draft |
| Prompt 2 |  |  |  |  |  |  | draft |
| Prompt 3 |  |  |  |  |  |  | draft |

## Hero Artifacts

Document 3-5 side-by-side examples worth sharing. For each one:

1. Link the with-skill artifact.
2. Link the baseline artifact.
3. State why one is better.
4. Note whether the difference is due to context retrieval, orchestration, quality, or efficiency.

## Iteration Notes

- What changed in the skill:
- What improved:
- What still regressed or remains weak:
- What to test next:
"""


def slackpost_template(skill_name: str) -> str:
    return f"""# {skill_name} Slack Post

## Draft

We just iterated on `{skill_name}` and compared it against a no-skill baseline on a small set of realistic prompts.

What the skill does:
- 

How it compared to baseline:
- 

Useful iteration insights:
- 

What changed in this revision:
- 

Recommended next step:
- 
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a reporting workspace for a skill-improver run")
    parser.add_argument("root", type=Path, help="Repo root or working directory that should contain skill-reporting/")
    parser.add_argument("--skill-name", required=True, help="Skill name")
    parser.add_argument("--improver-workspace", type=Path, default=None, help="Associated skill-improver workspace")
    parser.add_argument("--plugin-skill-path", type=Path, default=None, help="Path to a repo-local fork of the skill")
    parser.add_argument("--installed-skill-path", type=Path, default=None, help="Original installed skill path")
    parser.add_argument("--evals-source", type=Path, default=None, help="Optional existing evals.json to copy in")
    parser.add_argument("--run-dir", type=Path, default=None, help="Optional run directory such as <workspace>/runs/original")
    parser.add_argument("--benchmark", type=Path, default=None, help="Optional benchmark.json used to summarize status")
    parser.add_argument("--status", default="draft", help="Simple run status for status.md")
    parser.add_argument("--replace", action="store_true", help="Replace existing scaffolded files")
    args = parser.parse_args()

    reporting_dir = args.root.resolve() / "skill-reporting" / slugify(args.skill_name)
    reporting_dir.mkdir(parents=True, exist_ok=True)

    evals_path = reporting_dir / "evals.json"
    report_path = reporting_dir / "report.md"
    status_path = reporting_dir / "status.md"
    slackpost_path = reporting_dir / "slack-post.md"

    if args.evals_source:
        if not args.evals_source.exists():
            parser.error(f"evals source does not exist: {args.evals_source}")
        if args.replace or not evals_path.exists():
            shutil.copyfile(args.evals_source, evals_path)
    elif args.replace or not evals_path.exists():
        evals_path.write_text(json.dumps(default_evals(args.skill_name), indent=2) + "\n")

    if args.improver_workspace:
        synced_evals_path = args.improver_workspace.resolve() / "runs" / "evals" / "evals.json"
        synced_evals_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(evals_path, synced_evals_path)

    if args.replace:
        report_path.write_text(report_template(args.skill_name))
        status_path.write_text(
            status_template(
                args.skill_name,
                reporting_dir,
                args.improver_workspace.resolve() if args.improver_workspace else None,
                args.plugin_skill_path.resolve() if args.plugin_skill_path else None,
                args.installed_skill_path.resolve() if args.installed_skill_path else None,
                evals_path,
                args.run_dir.resolve() if args.run_dir else None,
                args.benchmark.resolve() if args.benchmark else None,
                args.status,
            )
        )
        slackpost_path.write_text(slackpost_template(args.skill_name))
    else:
        write_if_missing(report_path, report_template(args.skill_name))
        write_if_missing(
            status_path,
            status_template(
                args.skill_name,
                reporting_dir,
                args.improver_workspace.resolve() if args.improver_workspace else None,
                args.plugin_skill_path.resolve() if args.plugin_skill_path else None,
                args.installed_skill_path.resolve() if args.installed_skill_path else None,
                evals_path,
                args.run_dir.resolve() if args.run_dir else None,
                args.benchmark.resolve() if args.benchmark else None,
                args.status,
            ),
        )
        write_if_missing(slackpost_path, slackpost_template(args.skill_name))

    print(reporting_dir)


if __name__ == "__main__":
    main()
