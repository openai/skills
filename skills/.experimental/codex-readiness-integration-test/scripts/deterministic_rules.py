#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any

VALID_STATUSES = {"PASS", "WARN", "FAIL", "NOT_RUN"}
ERROR_MARKERS = [
    "error:",
    "failed",
    "exception",
    "traceback",
    "segmentation fault",
]


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
    if (base_dir / "prompt.json").exists():
        return base_dir.resolve()
    return base_dir.resolve()


def normalize_priority(value) -> int:
    try:
        priority = int(value)
    except (TypeError, ValueError):
        return 3
    return priority if priority in {0, 1, 2, 3} else 3


def sort_checks_by_priority(checks: list[dict]) -> list[dict]:
    return sorted(
        checks,
        key=lambda check: (
            normalize_priority(check.get("priority")),
            check.get("id", ""),
        ),
    )


def run_cmd(cmd: list[str]) -> str:
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
        return output.strip()
    except Exception as exc:
        return f"<error> {exc}"


def result(
    status: str,
    rationale: str,
    evidence: list[dict] | None = None,
    recs: list[str] | None = None,
    confidence: float = 0.7,
) -> dict:
    return {
        "status": status,
        "rationale": rationale,
        "evidence_quotes": evidence or [],
        "recommendations": recs or [],
        "confidence": confidence,
    }


def check_prompt_json_present(run_dir: Path, params: dict[str, Any]) -> dict:
    path = run_dir / params.get("path", "prompt.json")
    if path.exists():
        return result("PASS", "prompt.json exists.", [{"path": str(path), "quote": "present"}])
    return result(
        "FAIL",
        "prompt.json is missing.",
        recs=["Generate prompt.json before running deterministic checks."],
    )


def check_build_test_plan_present(run_dir: Path, params: dict[str, Any]) -> dict:
    path = run_dir / params.get("path", "prompt.json")
    if not path.exists():
        return result("FAIL", "prompt.json is missing.")
    try:
        prompt = load_json(path)
    except Exception:
        return result("FAIL", "prompt.json could not be parsed.")
    plan = prompt.get("build_test_plan")
    if not isinstance(plan, list) or not plan:
        return result(
            "FAIL",
            "build_test_plan is missing or empty.",
            [{"path": str(path), "quote": "build_test_plan"}],
        )
    commands = [entry.get("cmd") for entry in plan if isinstance(entry, dict)]
    commands = [cmd for cmd in commands if isinstance(cmd, str) and cmd.strip()]
    if not commands:
        return result(
            "WARN",
            "build_test_plan has no valid commands.",
            [{"path": str(path), "quote": "build_test_plan"}],
        )
    return result(
        "PASS",
        "build_test_plan contains commands.",
        [{"path": str(path), "quote": "build_test_plan"}],
    )


def check_execution_summary_status(run_dir: Path, params: dict[str, Any]) -> dict:
    summary_path = run_dir / params.get("summary_path", "execution_summary.json")
    if not summary_path.exists():
        return result("FAIL", "execution_summary.json is missing.")
    try:
        summary = load_json(summary_path)
    except Exception:
        return result("FAIL", "execution_summary.json could not be parsed.")
    status = summary.get("overall_status")
    if status in {"PASS", "WARN"}:
        return result(
            "PASS" if status == "PASS" else "WARN",
            f"execution summary status is {status}.",
            [{"path": str(summary_path), "quote": status}],
        )
    return result(
        "FAIL",
        f"execution summary status is {status}.",
        [{"path": str(summary_path), "quote": str(status)}],
    )


def check_execution_logs_no_errors(run_dir: Path, params: dict[str, Any]) -> dict:
    logs_dir = run_dir / params.get("logs_dir", "logs")
    if not logs_dir.exists():
        return result("WARN", "logs directory is missing.")
    matches = []
    log_paths = sorted(logs_dir.glob("[0-9][0-9]-*.log"))
    if not log_paths:
        log_paths = sorted(logs_dir.glob("*.log"))
    for log_path in log_paths:
        try:
            content = log_path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        lower = content.lower()
        for marker in ERROR_MARKERS:
            if marker in lower:
                snippet_index = lower.find(marker)
                snippet = content[snippet_index : snippet_index + 200].splitlines()[0]
                matches.append({"path": str(log_path), "quote": snippet})
                break
    if matches:
        return result(
            "WARN",
            "Execution logs contain error markers.",
            matches,
            ["Review build/test logs for failures."],
        )
    return result("PASS", "No obvious error markers found in execution logs.")


def parse_agentic_file_update_events(log_text: str) -> list[dict]:
    events = []
    lines = log_text.splitlines()
    for idx, line in enumerate(lines):
        if line.strip() != "file update":
            continue
        next_line = lines[idx + 1] if idx + 1 < len(lines) else ""
        next_line = next_line.strip()
        if not next_line:
            continue
        parts = next_line.split(" ", 1)
        path = parts[1].strip() if len(parts) == 2 else parts[0].strip()
        line_index = idx + 1 if idx + 1 < len(lines) else idx
        events.append({"path": path, "line_index": line_index})
    return events


def resolve_repo_root() -> Path | None:
    repo_root_raw = run_cmd(["git", "rev-parse", "--show-toplevel"])
    if repo_root_raw.startswith("<error>"):
        return None
    return Path(repo_root_raw).resolve()


def exec_plan_path_candidates(
    exec_plan_path: str, run_dir: Path, repo_root: Path | None
) -> list[str]:
    candidates: set[str] = set()
    exec_plan_path = exec_plan_path.strip()
    if exec_plan_path:
        candidates.add(exec_plan_path)
        candidates.add(exec_plan_path.lstrip("./"))

    plan_path = Path(exec_plan_path)
    if not plan_path.is_absolute():
        if repo_root:
            candidates.add(str((repo_root / plan_path).resolve()))
        candidates.add(str((run_dir / plan_path).resolve()))
        candidates.add(str((run_dir.parent / plan_path).resolve()))

    return sorted(candidates)


def find_exec_plan_command_index(lines: list[str], candidates: list[str]) -> int | None:
    patterns = []
    for path in candidates:
        if not path:
            continue
        escaped = re.escape(path)
        patterns.append(re.compile(rf">>?\s*{escaped}(?:$|\\s|\"|')"))
        patterns.append(re.compile(rf"\\btee\\b(?:\\s+-a)?\\s+{escaped}(?:$|\\s|\"|')"))

    for idx, line in enumerate(lines):
        for pattern in patterns:
            if pattern.search(line):
                return idx
    return None


def is_doc_path(path: str) -> bool:
    return path.lower().endswith(".md")


def is_exec_plan_candidate(path: str) -> bool:
    if not is_doc_path(path):
        return False
    name = Path(path).name.lower()
    if name == "plans.md":
        return False
    return "plan" in name


def infer_exec_plan_paths(log_text: str) -> list[str]:
    candidates: set[str] = set()
    events = parse_agentic_file_update_events(log_text)
    for event in events:
        path = event.get("path")
        if path and is_exec_plan_candidate(path):
            candidates.add(path)

    for match in re.finditer(r"([\w./-]*plan[\w./-]*\.md)", log_text, re.IGNORECASE):
        path = match.group(1)
        if is_exec_plan_candidate(path):
            candidates.add(path)

    return sorted(candidates)


def select_existing_plan_file(candidates: list[str]) -> Path | None:
    for candidate in candidates:
        try:
            path = Path(candidate)
        except Exception:
            continue
        if path.exists():
            return path
    return None


def check_exec_plan_before_code_changes(run_dir: Path, params: dict[str, Any]) -> dict:
    prompt_path = run_dir / params.get("prompt_path", "prompt.json")
    if not prompt_path.exists():
        return result("FAIL", "prompt.json is missing.")
    try:
        prompt = load_json(prompt_path)
    except Exception:
        return result("FAIL", "prompt.json could not be parsed.")

    log_path = run_dir / params.get("agentic_log_path", "logs/agentic.log")
    if not log_path.exists():
        return result("FAIL", "agentic.log is missing.")

    log_text = log_path.read_text(encoding="utf-8", errors="ignore")
    lines = log_text.splitlines()
    events = parse_agentic_file_update_events(log_text)
    if not events:
        return result("WARN", "No file update entries found in agentic.log.")

    repo_root = resolve_repo_root()
    exec_plan_path = prompt.get("exec_plan_path")
    candidates: list[str] = []
    if isinstance(exec_plan_path, str) and exec_plan_path.strip():
        exec_plan_path = exec_plan_path.strip()
        candidates.extend(exec_plan_path_candidates(exec_plan_path, run_dir, repo_root))
    else:
        inferred = infer_exec_plan_paths(log_text)
        for inferred_path in inferred:
            candidates.extend(exec_plan_path_candidates(inferred_path, run_dir, repo_root))

    candidates = [path for path in candidates if path]
    if not candidates:
        return result(
            "FAIL",
            "ExecPlan path missing from prompt.json and could not be inferred from agentic.log.",
            [{"path": str(log_path), "quote": "exec plan not detected"}],
            ["Create the ExecPlan and ensure it is referenced in logs before code changes."],
        )

    plan_line = None
    code_line = None
    for event in events:
        path = event["path"]
        line_index = event["line_index"]
        if any(path == cand or path.endswith(cand) for cand in candidates):
            if plan_line is None or line_index < plan_line:
                plan_line = line_index
            continue
        if path.startswith(".codex/"):
            continue
        if is_doc_path(path):
            continue
        if code_line is None:
            code_line = line_index

    command_line = find_exec_plan_command_index(lines, candidates)
    if command_line is not None and (plan_line is None or command_line < plan_line):
        plan_line = command_line

    if plan_line is None:
        return result(
            "FAIL",
            "ExecPlan file was not created before code changes.",
            [{"path": str(log_path), "quote": "missing exec plan update"}],
            ["Create the ExecPlan before making code changes."],
        )

    if code_line is None:
        return result(
            "WARN",
            "No non-doc, non-.codex file changes found; ordering not evaluated.",
            [{"path": str(log_path), "quote": "no code updates"}],
        )

    plan_file = select_existing_plan_file(candidates)
    if plan_file is None or not plan_file.exists():
        return result(
            "FAIL",
            "ExecPlan file is missing on disk.",
            [{"path": "candidate_paths", "quote": ", ".join(candidates)}],
            ["Create the ExecPlan file before making code changes."],
        )

    try:
        plan_text = plan_file.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        plan_text = ""

    required_headings = [
        "# ",
        "## Purpose / Big Picture",
        "## Progress",
        "## Decision Log",
        "## Outcomes & Retrospective",
    ]
    missing = [heading for heading in required_headings if heading not in plan_text]
    if missing:
        return result(
            "FAIL",
            "ExecPlan file is missing required sections.",
            [{"path": str(plan_file), "quote": ", ".join(missing)}],
            ["Ensure the ExecPlan follows PLANS.md headings."],
        )

    if plan_line <= code_line:
        return result(
            "PASS",
            "ExecPlan update appears before code changes.",
            [
                {
                    "path": str(log_path),
                    "quote": lines[plan_line] if plan_line < len(lines) else "",
                },
                {"path": str(plan_file), "quote": "exec plan used"},
            ],
        )

    return result(
        "FAIL",
        "ExecPlan update appears after code changes.",
        [
            {"path": str(log_path), "quote": lines[code_line] if code_line < len(lines) else ""},
            {"path": str(log_path), "quote": lines[plan_line] if plan_line < len(lines) else ""},
        ],
        ["Create the ExecPlan before making code changes."],
    )


def check_agentic_run_success(run_dir: Path, params: dict[str, Any]) -> dict:
    summary_path = run_dir / params.get("path", "agentic_summary.json")
    if not summary_path.exists():
        return result("FAIL", "agentic_summary.json is missing.")
    try:
        summary = load_json(summary_path)
    except Exception:
        return result("FAIL", "agentic_summary.json could not be parsed.")
    status = summary.get("status")
    exit_code = summary.get("exit_code")
    if status == "PASS" and exit_code == 0:
        return result(
            "PASS",
            "Agentic loop completed successfully.",
            [{"path": str(summary_path), "quote": "PASS"}],
        )
    return result(
        "FAIL",
        "Agentic loop did not complete successfully.",
        [{"path": str(summary_path), "quote": str(status)}],
    )


def check_repo_root_only_changes(run_dir: Path, params: dict[str, Any]) -> dict:
    repo_root_raw = run_cmd(["git", "rev-parse", "--show-toplevel"])
    if repo_root_raw.startswith("<error>"):
        return result("FAIL", f"Unable to resolve repo root: {repo_root_raw}")
    repo_root = Path(repo_root_raw).resolve()

    files_raw = run_cmd(["git", "diff", "--name-only"])
    if files_raw.startswith("<error>"):
        return result("FAIL", f"Unable to list git diff files: {files_raw}")
    files = [line.strip() for line in files_raw.splitlines() if line.strip()]
    if not files:
        return result("WARN", "No git diff detected; path policy not evaluated.")

    bad_paths = []
    for rel in files:
        if rel.startswith(("/", "..")):
            bad_paths.append(rel)
            continue
        abs_path = (repo_root / rel).resolve()
        try:
            abs_path.relative_to(repo_root)
        except ValueError:
            bad_paths.append(rel)

    if bad_paths:
        evidence = [{"path": str(repo_root), "quote": ", ".join(bad_paths[:5])}]
        return result(
            "FAIL",
            "Git diff includes paths outside repo root.",
            evidence,
            ["Ensure all changes stay under repo root."],
        )

    return result(
        "PASS",
        "All git diff paths resolve under repo root.",
        [{"path": str(repo_root), "quote": "repo root"}],
    )


RULES = {
    "prompt_json_present": check_prompt_json_present,
    "build_test_plan_present": check_build_test_plan_present,
    "execution_summary_status": check_execution_summary_status,
    "execution_logs_no_errors": check_execution_logs_no_errors,
    "agentic_run_success": check_agentic_run_success,
    "exec_plan_before_code_changes": check_exec_plan_before_code_changes,
    "repo_root_only_changes": check_repo_root_only_changes,
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Run deterministic checks for integration test.")
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

    checks_path = Path(args.checks)
    checks_data = load_json(checks_path)
    results: dict[str, dict] = {}

    for check in sort_checks_by_priority(checks_data.get("checks", [])):
        if not check.get("enabled_by_default"):
            continue
        rule_id = check.get("deterministic_rule_id")
        if not rule_id:
            continue
        rule = RULES.get(rule_id)
        if not rule:
            results[check["id"]] = result("FAIL", f"Unknown deterministic rule: {rule_id}.")
            continue
        params = check.get("deterministic_rule_params", {})
        results[check["id"]] = rule(run_dir, params)

    output_path = run_dir / "deterministic_results.json"
    output_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(str(output_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
