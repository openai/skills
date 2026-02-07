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


def sort_checks_by_priority(checks: list[dict]) -> list[dict]:
    return sorted(
        checks,
        key=lambda check: (
            normalize_priority(check.get("priority")),
            check.get("id", ""),
        ),
    )


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
                    "recommendations": ["Provide execution rationale using the evaluator prompt."],
                    "confidence": 0.0,
                }
            continue

    return results


def render_html(report: dict, prompt: dict | None = None, report_path: Path | None = None) -> str:
    score = report["scorecard"]["score_total"]
    status = report["scorecard"]["overall_status"]
    results = report.get("results", {})
    enabled_checks = report.get("enabled_checks", [])
    checks_by_id = {check["id"]: check for check in enabled_checks}
    prompt = prompt or {}
    change_prompt = prompt.get("change_prompt") or ""
    acceptance_criteria = prompt.get("acceptance_criteria") or []

    def status_class(value: str) -> str:
        return value.lower()

    html = [
        "<!doctype html>",
        "<html>",
        "<head>",
        "<meta charset='utf-8'>",
        "<title>Codex Readiness Integration Test Report</title>",
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
        "<h1>Codex Readiness Integration Test Report</h1>",
    ]
    if report_path:
        html.append(f"<h2>{report_path}</h2>")
    html.append(
        f"<p>Overall score: <strong>{score}</strong> <span class='badge {status_class(status)}'>{status}</span></p>"
    )

    if change_prompt:
        html.extend(
            [
                "<h2>Prompt</h2>",
                "<table>",
                "<tr><th>Change prompt</th></tr>",
                f"<tr><td>{change_prompt}</td></tr>",
                "</table>",
            ]
        )

    if isinstance(acceptance_criteria, list) and acceptance_criteria:
        html.extend(
            [
                "<h2>Acceptance criteria</h2>",
                "<table>",
                "<tr><th>Criteria</th></tr>",
            ]
        )
        for item in acceptance_criteria:
            html.append(f"<tr><td>{item}</td></tr>")
        html.append("</table>")

    html.append("<h2>Checks</h2>")

    html.append("<table>")
    html.append("<tr><th>Check</th><th>Status</th><th>Rationale</th></tr>")
    for check_id, result in results.items():
        check = checks_by_id.get(check_id, {})
        title = check.get("title", check_id)
        status_value = result.get("status", "NOT_RUN")
        rationale = result.get("rationale", "")
        html.append(
            "<tr>"
            f"<td>{title}</td>"
            f"<td><span class='badge {status_class(status_value)}'>{status_value}</span></td>"
            f"<td>{rationale}</td>"
            "</tr>"
        )
    html.append("</table>")
    html.append("</body></html>")
    return "\n".join(html)


def summarize_diff(git_diff: str) -> dict[str, Any]:
    files: list[str] = []
    additions = 0
    deletions = 0
    for line in git_diff.splitlines():
        if line.startswith("diff --git "):
            parts = line.split()
            if len(parts) >= 4:
                left = parts[2].removeprefix("a/")
                right = parts[3].removeprefix("b/")
                if left and left not in files:
                    files.append(left)
                if right and right not in files:
                    files.append(right)
            continue
        if line.startswith(("+++ ", "--- ")):
            continue
        if line.startswith("+"):
            additions += 1
        elif line.startswith("-"):
            deletions += 1
    return {"files": files, "additions": additions, "deletions": deletions}


def truncate_text(text: str, limit: int = 200) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def render_summary_text(
    report: dict,
    evidence: dict,
    deterministic_results: dict,
    llm_results: dict,
    execution_summary: dict | None,
    agentic_summary: dict | None,
    summary_path: Path,
) -> str:
    lines = [
        "# Codex Readiness Integration Test Report",
        f"## {summary_path}",
        "",
    ]
    score = report["scorecard"]["score_total"]
    status = report["scorecard"]["overall_status"]
    lines.append(f"Overall: {status} (score {score})")

    prompt = (evidence.get("prompt_json") or {}).get("content") or {}
    change_prompt = prompt.get("change_prompt") or ""
    if change_prompt:
        lines.append(f"Prompt: {truncate_text(change_prompt)}")

    if agentic_summary:
        agentic_status = agentic_summary.get("status", "NOT_RUN")
        exit_code = agentic_summary.get("exit_code")
        duration = agentic_summary.get("duration_seconds")
        lines.append(
            f"Agentic loop: {agentic_status} (exit_code {exit_code}, duration {duration}s)"
        )
    else:
        lines.append("Agentic loop: NOT_RUN")

    diff_stats = summarize_diff(evidence.get("git_diff", ""))
    if diff_stats.get("files"):
        lines.append(
            f"Diff: {len(diff_stats['files'])} file(s), +{diff_stats['additions']}/-{diff_stats['deletions']} lines"
        )

    path_check = deterministic_results.get("repo_root_only_changes", {}).get("status")
    if path_check:
        lines.append(f"Path policy: {path_check}")

    test_status = execution_summary.get("overall_status") if execution_summary else "NOT_RUN"
    lines.append(f"Tests: {test_status}")

    agentic_eval = llm_results.get("agentic_loop_eval", {}).get("status", "NOT_RUN")
    change_eval = llm_results.get("change_quality_eval", {}).get("status", "NOT_RUN")
    lines.append(f"LLM eval: agentic_loop_eval={agentic_eval}, change_quality_eval={change_eval}")

    if agentic_summary:
        questions = agentic_summary.get("clarifying_questions") or []
        if questions:
            last_question = truncate_text(str(questions[-1]))
            lines.append(f"Clarifying questions: {len(questions)}")
            lines.append(f"Last question: {last_question}")

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Score integration test results.")
    parser.add_argument(
        "--out-dir", default=".codex-readiness-integration-test", help="Base output directory"
    )
    parser.add_argument("--run-dir", default=None, help="Specific run directory to use")
    parser.add_argument(
        "--checks",
        default=str(Path(__file__).resolve().parents[1] / "references" / "checks.json"),
    )
    args = parser.parse_args()

    base_dir = Path(args.out_dir)
    run_dir = resolve_run_dir(base_dir, args.run_dir)

    checks_data = load_json(Path(args.checks))
    checks = sort_checks_by_priority(checks_data.get("checks", []))

    deterministic_results = (
        load_json(run_dir / "deterministic_results.json")
        if (run_dir / "deterministic_results.json").exists()
        else {}
    )
    llm_results = (
        load_json(run_dir / "llm_results.json") if (run_dir / "llm_results.json").exists() else {}
    )
    execution_summary = (
        load_json(run_dir / "execution_summary.json")
        if (run_dir / "execution_summary.json").exists()
        else None
    )
    evidence = load_json(run_dir / "evidence.json") if (run_dir / "evidence.json").exists() else {}
    agentic_summary = (
        load_json(run_dir / "agentic_summary.json")
        if (run_dir / "agentic_summary.json").exists()
        else None
    )

    weights = build_weights(checks)
    results = build_results(checks, deterministic_results, llm_results, execution_summary)

    score_items = []
    for check_id, result in results.items():
        weight = weights.get(check_id, 0)
        score_items.append(weight * status_points(result.get("status", "NOT_RUN")))
    score_total = round_half_up(sum(score_items))

    overall_status = "PASS"
    for result in results.values():
        if result["status"] == "FAIL":
            overall_status = "FAIL"
            break
        if result["status"] in {"WARN", "NOT_RUN"}:
            overall_status = "WARN"

    report = {
        "scorecard": {
            "score_total": score_total,
            "overall_status": overall_status,
            "weights": weights,
        },
        "enabled_checks": [check for check in checks if check.get("enabled_by_default")],
        "results": results,
    }

    report_path = run_dir / "report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    prompt_content = (evidence.get("prompt_json") or {}).get("content") or {}
    html_path = run_dir / "report.html"
    html_path.write_text(render_html(report, prompt_content, html_path), encoding="utf-8")

    summary = {
        "overall_status": overall_status,
        "score_total": score_total,
    }
    summary_path = run_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    summary_text_path = run_dir / "summary.txt"
    summary_text = render_summary_text(
        report,
        evidence,
        deterministic_results,
        llm_results,
        execution_summary,
        agentic_summary,
        summary_text_path,
    )
    summary_text_path.write_text(summary_text, encoding="utf-8")
    print(summary_text)

    print(str(report_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
