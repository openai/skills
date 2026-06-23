#!/usr/bin/env python3
"""Evaluate baseline vs guarded responses for Causal Halting prompts.

This harness is intentionally simple and stdlib-only. It does not call an LLM.
It scores response files against explicit fixture expectations using transparent
text checks, then reports metrics that are easy to inspect by hand.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


CHC_TERMS = (
    "causal_paradox",
    "prediction feedback",
    "feedback",
    "chc-0",
    "e(",
    "r(",
    "observed execution",
    "same execution",
)

BOUNDARY_TERMS = (
    "unproved",
    "valid_acyclic",
    "semantic",
    "does not solve",
    "halting problem",
)

OVERCLAIM_PATTERNS = (
    r"\bsolve[sd]?\s+(the\s+)?halting problem\b",
    r"\bdecide[sd]?\s+all\s+halting\b",
    r"\bprove[sd]?\s+arbitrary\s+termination\b",
)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: invalid JSON: {exc}") from exc
        rows.append(row)
    return rows


def index_by_id(rows: list[dict[str, Any]], path: Path) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for row in rows:
        row_id = row.get("id")
        if not isinstance(row_id, str) or not row_id:
            raise ValueError(f"{path}: every row must have a non-empty string id")
        if row_id in indexed:
            raise ValueError(f"{path}: duplicate id {row_id!r}")
        indexed[row_id] = row
    return indexed


def has_any(text: str, terms: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(term in lowered for term in terms)


def has_overclaim(text: str) -> bool:
    lowered = text.lower()
    for pattern in OVERCLAIM_PATTERNS:
        for match in re.finditer(pattern, lowered):
            prefix = lowered[max(0, match.start() - 16) : match.start()]
            if "not " in prefix or "does not " in prefix or "do not " in prefix:
                continue
            return True
    return False


def approx_tokens(text: str) -> int:
    return len(re.findall(r"\S+", text))


def score_response(prompt: dict[str, Any], response: str) -> dict[str, Any]:
    expected = prompt["expected"]
    risk = prompt["risk"]
    mentions_chc = has_any(response, CHC_TERMS)
    boundary_ok = True

    if expected == "should_apply_chc":
        activation_ok = mentions_chc
        noise = False
    else:
        activation_ok = not mentions_chc
        noise = mentions_chc

    if risk == "unproved":
        boundary_ok = "unproved" in response.lower() and "causal_paradox" not in response.lower()
    elif risk == "causal_paradox":
        boundary_ok = "causal_paradox" in response.lower() or "prediction feedback" in response.lower()
    elif risk == "valid_acyclic":
        boundary_ok = "valid_acyclic" in response.lower() or "no path back" in response.lower()
    elif risk == "prediction_feedback":
        boundary_ok = "causal_paradox" in response.lower() or "prediction feedback" in response.lower()

    return {
        "activation_ok": activation_ok,
        "activation_noise": noise,
        "boundary_ok": boundary_ok,
        "overclaim": has_overclaim(response),
        "useful": activation_ok and boundary_ok and not has_overclaim(response),
        "approx_tokens": approx_tokens(response),
    }


def evaluate(prompts_path: Path, baseline_path: Path, guarded_path: Path) -> dict[str, Any]:
    prompts = read_jsonl(prompts_path)
    baseline = index_by_id(read_jsonl(baseline_path), baseline_path)
    guarded = index_by_id(read_jsonl(guarded_path), guarded_path)
    cases = []

    for prompt in prompts:
        row_id = prompt["id"]
        if row_id not in baseline:
            raise ValueError(f"{baseline_path}: missing response id {row_id!r}")
        if row_id not in guarded:
            raise ValueError(f"{guarded_path}: missing response id {row_id!r}")

        baseline_response = baseline[row_id]["response"]
        guarded_response = guarded[row_id]["response"]
        base_score = score_response(prompt, baseline_response)
        guard_score = score_response(prompt, guarded_response)
        cases.append(
            {
                "id": row_id,
                "expected": prompt["expected"],
                "risk": prompt["risk"],
                "baseline": base_score,
                "guarded": guard_score,
                "token_delta": guard_score["approx_tokens"] - base_score["approx_tokens"],
            }
        )

    def rate(key: str, side: str, positive: bool = True) -> float:
        values = [case[side][key] for case in cases]
        count = sum(1 for value in values if value is positive)
        return count / len(values) if values else 0.0

    return {
        "case_count": len(cases),
        "metrics": {
            "baseline_activation_precision": rate("activation_ok", "baseline"),
            "guarded_activation_precision": rate("activation_ok", "guarded"),
            "baseline_activation_noise": rate("activation_noise", "baseline"),
            "guarded_activation_noise": rate("activation_noise", "guarded"),
            "baseline_boundary_accuracy": rate("boundary_ok", "baseline"),
            "guarded_boundary_accuracy": rate("boundary_ok", "guarded"),
            "baseline_overclaim_rate": rate("overclaim", "baseline"),
            "guarded_overclaim_rate": rate("overclaim", "guarded"),
            "baseline_answer_usefulness": rate("useful", "baseline"),
            "guarded_answer_usefulness": rate("useful", "guarded"),
            "average_token_overhead": (
                sum(case["token_delta"] for case in cases) / len(cases) if cases else 0.0
            ),
        },
        "cases": cases,
    }


def format_human(result: dict[str, Any]) -> str:
    metrics = result["metrics"]
    lines = [f"case_count: {result['case_count']}", "metrics:"]
    for key in sorted(metrics):
        value = metrics[key]
        if isinstance(value, float):
            lines.append(f"  {key}: {value:.3f}")
        else:
            lines.append(f"  {key}: {value}")
    lines.append("cases:")
    for case in result["cases"]:
        lines.append(
            "  "
            + f"{case['id']}: baseline_useful={case['baseline']['useful']} "
            + f"guarded_useful={case['guarded']['useful']} "
            + f"token_delta={case['token_delta']}"
        )
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evaluate Causal Halting response deltas.")
    parser.add_argument("--prompts", default="evals/prompts.jsonl")
    parser.add_argument("--baseline", default="evals/baseline-responses.jsonl")
    parser.add_argument("--guarded", default="evals/guarded-responses.jsonl")
    parser.add_argument("--format", choices=("human", "json"), default="human")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    result = evaluate(Path(args.prompts), Path(args.baseline), Path(args.guarded))
    if args.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(format_human(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
