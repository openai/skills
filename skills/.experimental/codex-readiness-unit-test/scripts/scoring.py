#!/usr/bin/env python3
import argparse
import json
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path
from typing import Any

VALID_STATUSES = {"PASS", "WARN", "FAIL", "NOT_RUN"}
PRIORITY_MULTIPLIERS = {0: 4, 1: 3, 2: 2, 3: 1}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_run_dir(base_dir: Path, run_dir_arg: str | None) -> Path:
    if run_dir_arg:
        return Path(run_dir_arg).resolve()
    latest_path = base_dir / "latest.json"
    if latest_path.exists():
        try:
            latest = load_json(latest_path)
            run_dir = latest.get("run_dir")
            if run_dir:
                return Path(run_dir)
        except Exception:
            pass
    if (base_dir / "evidence.json").exists():
        return base_dir.resolve()
    return base_dir.resolve()


def round_half_up(value: float) -> int:
    return int(Decimal(value).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def status_points(status: str) -> float:
    if status == "PASS":
        return 1.0
    if status == "WARN":
        return 0.5
    return 0.0


def normalize_priority(value) -> int:
    try:
        priority = int(value)
    except (TypeError, ValueError):
        priority = 3
    if priority in PRIORITY_MULTIPLIERS:
        return priority
    return 3


def priority_label(priority: int) -> str:
    return f"P{priority}"


def validate_result(result: dict) -> dict | None:
    if not isinstance(result, dict):
        return None
    if result.get("status") not in VALID_STATUSES:
        return None
    if (
        "rationale" not in result
        or "evidence_quotes" not in result
        or "recommendations" not in result
        or "confidence" not in result
    ):
        return None
    if not isinstance(result.get("evidence_quotes"), list):
        return None
    if not isinstance(result.get("recommendations"), list):
        return None
    return result


def fallback_invalid_json() -> dict:
    return {
        "status": "WARN",
        "rationale": "Invalid JSON from evaluator after retries.",
        "evidence_quotes": [],
        "recommendations": ["Re-run the evaluator with the json_fix prompt."],
        "confidence": 0.0,
    }


def build_weights(checks: list[dict]) -> dict:
    enabled = [c for c in checks if c.get("enabled_by_default")]
    raw_weights = []
    for check in enabled:
        weight = check.get("weight")
        base_weight = weight if isinstance(weight, (int, float)) else 1.0
        priority = normalize_priority(check.get("priority"))
        raw_weights.append(base_weight * PRIORITY_MULTIPLIERS[priority])
    total = sum(raw_weights) if raw_weights else 1.0
    weights = {}
    for check, raw in zip(enabled, raw_weights):
        weights[check["id"]] = (raw / total) * 100.0
    return weights


def build_results(
    checks: list[dict],
    deterministic_results: dict,
    llm_results: dict,
    execution_summary: dict | None,
    mode: str,
) -> dict:
    results = {}
    execution_status = None
    if execution_summary:
        execution_status = execution_summary.get("overall_status")

    for check in checks:
        if not check.get("enabled_by_default"):
            continue
        check_id = check["id"]
        check_type = check.get("type")

        if check_type == "DETERMINISTIC":
            result = deterministic_results.get(check_id)
            if result:
                valid = validate_result(result)
                results[check_id] = valid if valid else fallback_invalid_json()
            else:
                results[check_id] = {
                    "status": "FAIL",
                    "rationale": "Deterministic result missing for this check.",
                    "evidence_quotes": [],
                    "recommendations": ["Run deterministic_rules.py to populate results."],
                    "confidence": 0.0,
                }
            continue

        if check_type == "LLM":
            llm_result = llm_results.get(check_id)
            if llm_result:
                valid = validate_result(llm_result)
                results[check_id] = valid if valid else fallback_invalid_json()
            else:
                results[check_id] = {
                    "status": "WARN",
                    "rationale": "LLM evaluation missing for this check.",
                    "evidence_quotes": [],
                    "recommendations": ["Run the evaluator prompt for this check."],
                    "confidence": 0.0,
                }
            continue

        if check_type == "HYBRID":
            if mode == "read-only":
                status = "NOT_RUN"
            else:
                status = (
                    execution_status
                    or deterministic_results.get(check_id, {}).get("status")
                    or "NOT_RUN"
                )
            llm_result = llm_results.get(check_id)
            if llm_result:
                valid = validate_result(llm_result) or fallback_invalid_json()
                valid["status"] = status
                results[check_id] = valid
            else:
                results[check_id] = {
                    "status": status,
                    "rationale": "Execution summary present but LLM rationale missing."
                    if status != "NOT_RUN"
                    else "Execution not run.",
                    "evidence_quotes": [],
                    "recommendations": [
                        "Provide execution rationale using the execution_explanation prompt."
                    ],
                    "confidence": 0.0,
                }
            continue

    return results


def render_html(report: dict) -> str:
    score = report["scorecard"]["score_total"]
    status = report["scorecard"]["overall_status"]
    results = report.get("results", {})
    enabled_checks = report.get("enabled_checks", [])
    checks_by_id = {check["id"]: check for check in enabled_checks}
    run_context = report.get("run_context", {})
    file_path = run_context.get("repo_root") or run_context.get("cwd") or ""

    def status_class(value: str) -> str:
        return value.lower()

    html = [
        "<!doctype html>",
        "<html>",
        "<head>",
        "<meta charset='utf-8'>",
        "<title>Codex Readiness Unit Test Report</title>",
        "<style>",
        "body{font-family:Arial,sans-serif;margin:24px;color:#222;background:#fafafa;}",
        ".badge{display:inline-block;padding:4px 10px;border-radius:12px;color:#fff;font-size:12px;text-transform:uppercase;}",
        ".pass{background:#2e7d32;} .warn{background:#f9a825;} .fail{background:#c62828;} .not_run{background:#546e7a;}",
        "table{border-collapse:collapse;width:100%;margin:12px 0 20px;background:#fff;table-layout:fixed;}",
        "th,td{border:1px solid #ddd;padding:8px;font-size:13px;vertical-align:top;word-break:break-word;}",
        "th{background:#f1f1f1;text-align:left;}",
        "h3{margin:12px 0 6px;}",
        "h2{margin-top:24px;}",
        "</style>",
        "</head>",
        "<body>",
        "<h1>Codex Readiness Unit Test Report</h1>",
        f"<h2>{file_path}</h2>" if file_path else "",
        f"<p>Overall score: <strong>{score}</strong> <span class='badge {status_class(status)}'>{status}</span></p>",
        "<h2>Checks</h2>",
    ]
    colgroup = (
        "<colgroup><col style='width:42%'><col style='width:12%'><col style='width:46%'></colgroup>"
    )
    grouped: dict[str, list[str]] = {
        f"P{priority}": [] for priority in sorted(PRIORITY_MULTIPLIERS.keys())
    }
    for check in enabled_checks:
        check_id = check["id"]
        label = check.get("priority_label") or priority_label(
            normalize_priority(check.get("priority"))
        )
        if label in grouped:
            grouped[label].append(check_id)

    for label in ["P0", "P1", "P2", "P3"]:
        check_ids = grouped.get(label, [])
        if not check_ids:
            continue
        html.append(f"<h3>{label}</h3>")
        html.append("<table>")
        html.append(colgroup)
        html.append("<tr><th>Check</th><th>Status</th><th>Rationale</th></tr>")
        for check_id in check_ids:
            result = results.get(check_id, {})
            title = checks_by_id.get(check_id, {}).get("title") or check_id
            rationale = result.get("rationale", "")
            status_value = result.get("status", "WARN")
            html.append(
                f"<tr><td>{title}</td><td><span class='badge {status_class(status_value)}'>{status_value}</span></td><td>{rationale}</td></tr>"
            )
        html.append("</table>")
    html.append("</body></html>")
    return "\n".join(html)


def build_summary(
    checks: list[dict], results: dict, overall_counts: dict, overall_status: str
) -> dict:
    enabled_checks = [c for c in checks if c.get("enabled_by_default")]
    by_status: dict[str, list[dict[str, Any]]] = {"PASS": [], "FAIL": [], "WARN": [], "NOT_RUN": []}
    all_checks = []
    for check in enabled_checks:
        check_id = check["id"]
        result = results.get(check_id, {})
        status = result.get("status", "WARN")
        priority = normalize_priority(check.get("priority"))
        entry = {
            "id": check_id,
            "title": check.get("title") or check_id,
            "status": status,
            "priority": priority,
            "priority_label": priority_label(priority),
        }
        all_checks.append(entry)
        if status == "PASS":
            by_status["PASS"].append(entry)
            continue
        detail = {
            **entry,
            "rationale": result.get("rationale", ""),
            "recommendations": result.get("recommendations", []),
        }
        by_status.get(status, by_status["WARN"]).append(detail)

    return {
        "overall_status": overall_status,
        "counts": overall_counts,
        "checks": all_checks,
        "passed": by_status["PASS"],
        "failed": by_status["FAIL"],
        "warned": by_status["WARN"],
        "not_run": by_status["NOT_RUN"],
    }


def render_summary_text(summary: dict) -> str:
    counts = summary.get("counts", {})
    lines = [
        "Summary",
        f"Overall status: {summary.get('overall_status')}",
        f"Counts: PASS={counts.get('PASS', 0)} WARN={counts.get('WARN', 0)} FAIL={counts.get('FAIL', 0)} NOT_RUN={counts.get('NOT_RUN', 0)}",
    ]

    def render_section(label: str, items: list[dict], include_details: bool = False) -> None:
        if not items:
            return
        lines.append(f"{label}:")
        for item in items:
            title = item.get("title") or item.get("id")
            lines.append(f"- {item.get('priority_label')} {title} ({item.get('id')})")
            if include_details:
                rationale = item.get("rationale", "")
                if rationale:
                    lines.append(f"  Rationale: {rationale}")
                recommendations = item.get("recommendations", [])
                if recommendations:
                    lines.append(f"  Recommendations: {', '.join(recommendations)}")

    render_section("Failed", summary.get("failed", []), include_details=True)
    render_section("Warned", summary.get("warned", []), include_details=True)
    render_section("Not run", summary.get("not_run", []), include_details=True)
    render_section("Passed", summary.get("passed", []), include_details=False)

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute scorecard and render report outputs.")
    parser.add_argument("--mode", choices=["read-only", "execute"], required=True, help="Run mode")
    parser.add_argument(
        "--out-dir", default=".codex-readiness-unit-test", help="Base output directory"
    )
    parser.add_argument("--run-dir", default=None, help="Specific run directory to use")
    parser.add_argument(
        "--checks",
        default=str(
            Path(__file__).resolve().parents[1]
            / "references"
            / "checks"
            / "checks.json"
        ),
        help="Path to checks.json",
    )
    parser.add_argument("--evidence", default=None, help="Path to evidence.json (optional)")
    parser.add_argument(
        "--deterministic", default=None, help="Path to deterministic results (optional)"
    )
    parser.add_argument("--llm", default=None, help="Path to LLM results (optional)")
    args = parser.parse_args()

    base_dir = Path(args.out_dir)
    base_dir.mkdir(parents=True, exist_ok=True)
    run_dir = resolve_run_dir(base_dir, args.run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)

    checks = load_json(Path(args.checks)).get("checks", [])
    evidence_path = Path(args.evidence) if args.evidence else (run_dir / "evidence.json")
    deterministic_path = (
        Path(args.deterministic) if args.deterministic else (run_dir / "deterministic_results.json")
    )
    llm_path = Path(args.llm) if args.llm else (run_dir / "llm_results.json")
    evidence = load_json(evidence_path)
    deterministic_results = (
        load_json(deterministic_path).get("results", {}) if deterministic_path.exists() else {}
    )
    llm_results = load_json(llm_path) if llm_path.exists() else {}

    execution_summary_path = run_dir / "execution_summary.json"
    execution_summary = (
        load_json(execution_summary_path) if execution_summary_path.exists() else None
    )

    weights = build_weights(checks)
    results = build_results(
        checks, deterministic_results, llm_results, execution_summary, args.mode
    )

    overall_counts = {"PASS": 0, "WARN": 0, "FAIL": 0, "NOT_RUN": 0}
    per_check_contributions = {}
    total = 0.0
    for check in checks:
        if not check.get("enabled_by_default"):
            continue
        check_id = check["id"]
        result = results.get(check_id, {})
        status = result.get("status", "WARN")
        overall_counts[status] = overall_counts.get(status, 0) + 1
        weight = weights.get(check_id, 0.0)
        contribution = weight * status_points(status)
        total += contribution
        per_check_contributions[check_id] = {
            "status": status,
            "weight": round(weight, 2),
            "contribution": round(contribution, 2),
            "priority": normalize_priority(check.get("priority")),
            "priority_label": priority_label(normalize_priority(check.get("priority"))),
        }

    overall_status = "PASS"
    if overall_counts.get("FAIL"):
        overall_status = "FAIL"
    elif overall_counts.get("WARN") or overall_counts.get("NOT_RUN"):
        overall_status = "WARN"

    enabled_checks = []
    for check in checks:
        if not check.get("enabled_by_default"):
            continue
        priority = normalize_priority(check.get("priority"))
        enabled_checks.append(
            {
                **check,
                "priority": priority,
                "priority_label": priority_label(priority),
                "priority_multiplier": PRIORITY_MULTIPLIERS[priority],
                "weight": round(weights.get(check["id"], 0.0), 2),
            }
        )

    report = {
        "schema_version": "1.0",
        "tool_name": "codex-readiness-unit-test",
        "tool_version": "0.1.0",
        "run_context": evidence.get("run_context", {}),
        "enabled_checks": enabled_checks,
        "results": results,
        "execution_summary": execution_summary if args.mode == "execute" else None,
        "scorecard": {
            "score_total_raw": round(total, 2),
            "score_total": round_half_up(total),
            "per_check_contributions": per_check_contributions,
            "counts": overall_counts,
            "overall_status": overall_status,
        },
    }

    report_path = run_dir / "report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    html = render_html(report)
    html_path = run_dir / "report.html"
    html_path.write_text(html, encoding="utf-8")

    summary = build_summary(checks, results, overall_counts, overall_status)
    summary_path = run_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(str(report_path))
    print(str(html_path))
    print(str(summary_path))
    print(render_summary_text(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
