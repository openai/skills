#!/usr/bin/env python3
"""Convert eval viewer feedback into a concise skill-revision brief."""

import argparse
import json
from collections import defaultdict
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def review_kind(run_id: str) -> str:
    if run_id.startswith("compare:") and ":artifact:" in run_id:
        return "artifact_compare"
    if run_id.startswith("compare:"):
        return "eval_compare"
    return "run"


def group_reviews(feedback: dict) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for review in feedback.get("reviews", []):
        kind = review_kind(review.get("run_id", ""))
        grouped[kind].append(review)
    return grouped


def render_feedback_section(grouped: dict[str, list[dict]]) -> list[str]:
    lines: list[str] = []

    compare_reviews = [r for r in grouped["eval_compare"] if r.get("feedback", "").strip()]
    if compare_reviews:
        lines.extend(["## Pairwise Preferences", ""])
        for review in compare_reviews:
            lines.extend([
                f"### {review['run_id']}",
                review["feedback"].strip(),
                "",
            ])

    artifact_reviews = [r for r in grouped["artifact_compare"] if r.get("feedback", "").strip()]
    if artifact_reviews:
        lines.extend(["## Artifact-Specific Notes", ""])
        for review in artifact_reviews:
            lines.extend([
                f"### {review['run_id']}",
                review["feedback"].strip(),
                "",
            ])

    run_reviews = [r for r in grouped["run"] if r.get("feedback", "").strip()]
    if run_reviews:
        lines.extend(["## Per-Run Feedback", ""])
        for review in run_reviews:
            lines.extend([
                f"### {review['run_id']}",
                review["feedback"].strip(),
                "",
            ])

    approved_runs = [r["run_id"] for r in grouped["run"] if not r.get("feedback", "").strip()]
    if approved_runs:
        lines.extend([
            "## Runs With Empty Feedback",
            "",
            "Empty feedback means the reviewer submitted the run without notes. Treat these as acceptable unless pairwise feedback says otherwise.",
            "",
            ", ".join(approved_runs),
            "",
        ])

    return lines


def render_score_section(grouped: dict[str, list[dict]]) -> list[str]:
    scored = [
        review
        for review in grouped["run"]
        if review.get("score") not in (None, "")
    ]
    if not scored:
        return []

    lines = [
        "## Reviewer Scores",
        "",
        "Scores use a 1-5 blocker-first rubric: 5 is super excited / use directly; 1 means did not work.",
        "",
    ]
    for review in scored:
        lines.append(f"- {review['run_id']}: {review['score']}/10")
    lines.append("")
    return lines


def render_benchmark_summary(benchmark: dict) -> list[str]:
    summary = benchmark.get("run_summary") or {}
    if not summary:
        return []

    lines = ["## Benchmark Summary", ""]
    for name, metrics in summary.items():
        if name == "delta":
            continue
        pass_rate = metrics.get("pass_rate", {})
        mean = pass_rate.get("mean")
        if mean is None:
            continue
        lines.append(f"- {name}: pass_rate mean {mean:.0%}")

    delta = summary.get("delta") or {}
    if delta:
        lines.append(f"- delta: pass_rate {delta.get('pass_rate', 'unknown')}, time {delta.get('time_seconds', 'unknown')}, tokens {delta.get('tokens', 'unknown')}")
    lines.append("")
    return lines


def build_brief(feedback_path: Path, benchmark_path: Path | None) -> str:
    feedback = load_json(feedback_path)
    grouped = group_reviews(feedback)

    lines = [
        "# Skill Revision Brief",
        "",
        "Use this brief to revise the skill. Preserve what the reviewer preferred, fix repeated complaints, and generalize the underlying instruction rather than overfitting to one eval output.",
        "",
        "## Review Status",
        "",
        f"- feedback_file: {feedback_path}",
        f"- status: {feedback.get('status', 'unknown')}",
        f"- review_entries: {len(feedback.get('reviews', []))}",
        "",
    ]

    if benchmark_path and benchmark_path.exists():
        lines.extend(render_benchmark_summary(load_json(benchmark_path)))

    lines.extend(render_score_section(grouped))
    lines.extend(render_feedback_section(grouped))

    lines.extend([
        "## Revision Instructions For Codex",
        "",
        "1. Briefly restate the pairwise preferences and concrete complaints.",
        "2. Inspect the relevant outputs/transcripts before editing if a comment references an artifact or behavior.",
        "3. Edit SKILL.md or bundled resources to address the general failure mode.",
        "4. Do not delete useful existing guidance only because one eval did not exercise it.",
        "5. Snapshot the revised skill before rerunning evals.",
        "",
    ])

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a model-friendly revision brief from feedback.json")
    parser.add_argument("feedback_json", type=Path, help="Completed feedback.json from the review viewer")
    parser.add_argument("--benchmark", type=Path, default=None, help="Optional benchmark.json from the same iteration")
    parser.add_argument("--output", type=Path, default=None, help="Output Markdown file; defaults to <feedback-dir>/revision_brief.md")
    args = parser.parse_args()

    output = args.output or (args.feedback_json.parent / "revision_brief.md")
    brief = build_brief(args.feedback_json, args.benchmark)
    output.write_text(brief)
    print(output)


if __name__ == "__main__":
    main()
