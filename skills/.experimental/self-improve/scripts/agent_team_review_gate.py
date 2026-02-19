#!/usr/bin/env python3
"""Optional agent-team review gate for self-improve workflows."""

from __future__ import annotations

import argparse
import json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--decision", choices=("accept", "reject"), required=True)
    parser.add_argument("--smoke-status", choices=("pass", "fail", "unknown"), required=True)
    parser.add_argument("--regression-status", choices=("pass", "fail", "unknown"), required=True)
    parser.add_argument("--author-id", default="")
    parser.add_argument("--final-reviewer-id", default="")
    parser.add_argument("--enforce-reviewer-separation", action="store_true")
    parser.add_argument(
        "--reviewer-decision",
        action="append",
        default=[],
        help="Repeatable '<reviewer_id>:<accept|reject>' entries used to detect conflicting review outcomes.",
    )
    parser.add_argument("--output", choices=("json", "text"), default="json")
    return parser.parse_args()


def parse_reviewer_decisions(entries: list[str]) -> tuple[list[dict[str, str]], list[str]]:
    parsed: list[dict[str, str]] = []
    errors: list[str] = []
    for entry in entries:
        value = (entry or "").strip()
        if not value:
            continue
        if ":" not in value:
            errors.append(f"invalid reviewer-decision '{value}' (expected reviewer_id:accept|reject)")
            continue
        reviewer_id, decision = value.split(":", 1)
        reviewer_id = reviewer_id.strip()
        decision = decision.strip().lower()
        if not reviewer_id:
            errors.append("reviewer-decision must include reviewer id")
            continue
        if decision not in {"accept", "reject"}:
            errors.append(f"invalid reviewer decision '{decision}' for reviewer '{reviewer_id}'")
            continue
        parsed.append({"reviewer_id": reviewer_id, "decision": decision})
    return parsed, errors


def evaluate(args: argparse.Namespace) -> dict[str, object]:
    reasons: list[str] = []
    blockers: list[str] = []
    escalated = False

    parsed_reviews, parsing_errors = parse_reviewer_decisions(args.reviewer_decision)
    if parsing_errors:
        blockers.extend(parsing_errors)
        escalated = True

    author_id = args.author_id.strip()
    final_reviewer_id = args.final_reviewer_id.strip()

    if args.enforce_reviewer_separation and author_id and final_reviewer_id and author_id == final_reviewer_id:
        blockers.append("reviewer separation violated: final reviewer cannot be the author")
        escalated = True

    review_outcomes = {row["decision"] for row in parsed_reviews}
    if len(review_outcomes) > 1:
        blockers.append("conflicting review outcomes detected")
        escalated = True

    smoke_pass = args.smoke_status == "pass"
    regression_pass = args.regression_status == "pass"
    gate_decision = "accept" if smoke_pass and regression_pass else "reject"

    if gate_decision == "reject":
        reasons.append(
            f"dual-gate rule requires reject when smoke={args.smoke_status} and regression={args.regression_status}"
        )

    if args.decision != gate_decision:
        reasons.append(
            f"input decision '{args.decision}' normalized to '{gate_decision}' by smoke/regression policy"
        )

    final_decision = "reject" if escalated else gate_decision
    final_state = "failed" if escalated else "review"
    if escalated:
        reasons.append("escalation lock applied; no in-iteration retry allowed")

    return {
        "status": "ok",
        "decision": final_decision,
        "gate_decision": gate_decision,
        "final_state": final_state,
        "escalated": escalated,
        "author_id": author_id,
        "final_reviewer_id": final_reviewer_id,
        "reviewer_separation_enforced": args.enforce_reviewer_separation,
        "reviews": parsed_reviews,
        "reasons": reasons,
        "blockers": blockers,
    }


def emit_text(payload: dict[str, object]) -> None:
    print(f"decision={payload['decision']}")
    print(f"gate_decision={payload['gate_decision']}")
    print(f"final_state={payload['final_state']}")
    print(f"escalated={payload['escalated']}")
    if payload.get("reasons"):
        print("reasons:")
        for row in payload["reasons"]:
            print(f"- {row}")
    if payload.get("blockers"):
        print("blockers:")
        for row in payload["blockers"]:
            print(f"- {row}")


def main() -> int:
    args = parse_args()
    try:
        payload = evaluate(args)
        if args.output == "json":
            print(json.dumps(payload, indent=2))
        else:
            emit_text(payload)
        return 1 if payload["escalated"] else 0
    except Exception as exc:
        error_payload = {"status": "error", "error": str(exc)}
        if args.output == "json":
            print(json.dumps(error_payload, indent=2))
        else:
            print(f"review gate error: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
