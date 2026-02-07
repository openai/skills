#!/usr/bin/env python3
import argparse
import json
import re
import shlex
import subprocess
from pathlib import Path
from typing import Any

VALID_STATUSES = {"PASS", "WARN", "FAIL", "NOT_RUN"}
ANSI_ESCAPE_PATTERN = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
ERROR_MARKERS = [
    "error:",
    "failed",
    "exception",
    "traceback",
    "segmentation fault",
]
PLANNING_SIGNAL_PATTERNS = [
    re.compile(r"\bupdate_plan\b", re.IGNORECASE),
    re.compile(r"^\s*plan\s*[:\-]", re.IGNORECASE),
    re.compile(r"^\s*plan\s+update\b", re.IGNORECASE),
    re.compile(r"^\s*\*\*planning\b", re.IGNORECASE),
    re.compile(r"^\s*steps?\s*[:\-]", re.IGNORECASE),
    re.compile(r"^\s*approach\s*[:\-]", re.IGNORECASE),
    re.compile(r"\bhere(?:'s| is)\s+(?:the\s+)?plan\b", re.IGNORECASE),
]
COMMAND_LINE_PATTERNS = [
    re.compile(r"^\s*\$\s+(.+)$"),
    re.compile(r"^\s*!\s*(.+)$"),
    re.compile(r"^\s*running(?: command)?\s*:\s+(.+)$", re.IGNORECASE),
    re.compile(r"^\s*cmd\s*:\s+(.+)$", re.IGNORECASE),
]
# Match shell "-lc '<cmd>'" forms even when prefixed by a path like /bin/zsh.
SHELL_LC_PATTERN = re.compile(r"(?:^|\s)-lc\s+(?P<quote>['\"])(?P<cmd>.+?)(?P=quote)")
VERIFICATION_KEYWORDS = [
    " test",
    "pytest",
    "npm test",
    "pnpm test",
    "yarn test",
    "node --test",
    "go test",
    "cargo test",
    "mvn test",
    "gradle test",
    "./gradlew test",
    "lint",
    "eslint",
    "ruff",
    "flake8",
    "black --check",
    "prettier --check",
    "typecheck",
    "tsc",
    " build",
    "compile",
    "mvn package",
    "gradle build",
    "./gradlew build",
    "go build",
    "cargo build",
    "make build",
    "make test",
    "make lint",
    "make verify",
    "verify",
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


def is_doc_path(path: str) -> bool:
    return path.lower().endswith(".md")


def strip_ansi(text: str) -> str:
    return ANSI_ESCAPE_PATTERN.sub("", text)


def command_binary(cmd: str) -> str:
    try:
        parts = shlex.split(cmd)
    except ValueError:
        parts = cmd.split()
    if not parts:
        return ""
    return Path(parts[0]).name.lower()


def is_codex_invocation(cmd: str) -> bool:
    binary = command_binary(cmd)
    return binary in {"codex", "codex.exe"}


def extract_command_events(log_text: str) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for idx, raw_line in enumerate(log_text.splitlines()):
        clean_line = strip_ansi(raw_line).strip()
        if not clean_line:
            continue

        # First handle common "command-like" prefixes such as "$ npm test".
        for pattern in COMMAND_LINE_PATTERNS:
            match = pattern.match(clean_line)
            if not match:
                continue
            cmd = match.group(1).strip()
            if not cmd:
                continue
            if is_codex_invocation(cmd):
                # Ignore runner-level codex invocations; they are not verification steps.
                continue
            events.append(
                {
                    "line_index": idx,
                    "cmd": cmd,
                    "raw_line": clean_line,
                }
            )
            break

        else:
            # Fall back to extracting the inner command from shell "-lc" invocations
            # such as: /bin/zsh -lc 'npm test' ... succeeded in 64ms
            lc_match = SHELL_LC_PATTERN.search(clean_line)
            if not lc_match:
                continue
            cmd = lc_match.group("cmd").strip()
            if not cmd:
                continue
            if is_codex_invocation(cmd):
                continue
            events.append(
                {
                    "line_index": idx,
                    "cmd": cmd,
                    "raw_line": clean_line,
                }
            )
    return events


def prompt_command_candidates(prompt: dict[str, Any]) -> list[str]:
    candidates: list[str] = []
    plan = prompt.get("build_test_plan")
    if not isinstance(plan, list):
        return candidates
    for entry in plan:
        if isinstance(entry, dict):
            cmd = entry.get("cmd")
        elif isinstance(entry, str):
            cmd = entry
        else:
            cmd = None
        if isinstance(cmd, str) and cmd.strip():
            candidates.append(cmd.strip().lower())
    return candidates


def is_verification_command(cmd: str, prompt_cmds: list[str]) -> bool:
    lower = cmd.lower()
    if any(keyword in lower for keyword in VERIFICATION_KEYWORDS):
        return True
    return any(prompt_cmd and prompt_cmd in lower for prompt_cmd in prompt_cmds)


def first_code_change_event(events: list[dict[str, Any]]) -> dict[str, Any] | None:
    code_events: list[dict[str, Any]] = []
    for event in events:
        path = str(event.get("path", ""))
        try:
            line_index = int(event.get("line_index"))
        except Exception:
            continue
        if not path:
            continue
        if path.startswith(".codex/"):
            continue
        if is_doc_path(path):
            continue
        code_events.append({"path": path, "line_index": line_index})
    if not code_events:
        return None
    return min(code_events, key=lambda item: item["line_index"])


def file_update_line_indexes(events: list[dict[str, Any]]) -> set[int]:
    indexes: set[int] = set()
    for event in events:
        try:
            indexes.add(int(event.get("line_index")))
        except Exception:
            continue
    return indexes


def find_first_planning_signal_index(lines: list[str], skip_indexes: set[int]) -> int | None:
    for idx, line in enumerate(lines):
        if idx in skip_indexes:
            continue
        for pattern in PLANNING_SIGNAL_PATTERNS:
            if pattern.search(line):
                return idx
    return None


def check_exec_plan_before_code_changes(run_dir: Path, params: dict[str, Any]) -> dict:
    prompt_path = run_dir / params.get("prompt_path", "prompt.json")
    if not prompt_path.exists():
        return result("FAIL", "prompt.json is missing.")
    try:
        _prompt = load_json(prompt_path)
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

    code_event = first_code_change_event(events)
    if code_event is None:
        return result(
            "WARN",
            "No non-doc, non-.codex file changes found; ordering not evaluated.",
            [{"path": str(log_path), "quote": "no code updates"}],
        )
    code_line = int(code_event["line_index"])

    skip_indexes = file_update_line_indexes(events)
    plan_line = find_first_planning_signal_index(lines, skip_indexes)
    if plan_line is None:
        return result(
            "FAIL",
            "No planning signal detected in agentic.log before code changes.",
            [
                {"path": str(log_path), "quote": "planning signal not detected"},
                {
                    "path": str(log_path),
                    "quote": lines[code_line] if code_line < len(lines) else "",
                },
            ],
            ["Emit a short plan (for example: 'Plan:' or use update_plan) before code edits."],
        )

    if plan_line <= code_line:
        return result(
            "PASS",
            "Planning signal appears before code changes.",
            [
                {
                    "path": str(log_path),
                    "quote": lines[plan_line] if plan_line < len(lines) else "",
                },
                {
                    "path": str(log_path),
                    "quote": lines[code_line] if code_line < len(lines) else "",
                },
            ],
        )

    return result(
        "FAIL",
        "Planning signal appears after code changes.",
        [
            {"path": str(log_path), "quote": lines[code_line] if code_line < len(lines) else ""},
            {"path": str(log_path), "quote": lines[plan_line] if plan_line < len(lines) else ""},
        ],
        ["Emit a short plan (for example: 'Plan:' or use update_plan) before code edits."],
    )


def check_verification_after_code_changes(run_dir: Path, params: dict[str, Any]) -> dict:
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
    lines = [strip_ansi(line) for line in log_text.splitlines()]
    file_events = parse_agentic_file_update_events(log_text)
    if not file_events:
        return result("WARN", "No file update entries found in agentic.log.")

    code_event = first_code_change_event(file_events)
    if code_event is None:
        return result(
            "WARN",
            "No non-doc, non-.codex file changes found; verification ordering not evaluated.",
            [{"path": str(log_path), "quote": "no code updates"}],
        )
    code_line = int(code_event["line_index"])

    command_events = extract_command_events(log_text)
    prompt_cmds = prompt_command_candidates(prompt)
    verification_events = [
        event
        for event in command_events
        if int(event["line_index"]) > code_line
        and is_verification_command(str(event.get("cmd", "")), prompt_cmds)
    ]

    code_quote = lines[code_line] if code_line < len(lines) else str(code_event.get("path", ""))
    if not verification_events:
        return result(
            "FAIL",
            "No build/test/lint verification command detected after code changes in agentic.log.",
            [{"path": str(log_path), "quote": code_quote}],
            [
                "Run at least one build, test, or lint command after code changes within the agentic loop."
            ],
        )

    evidence: list[dict[str, str]] = [{"path": str(log_path), "quote": code_quote}]
    for event in verification_events[:2]:
        idx = int(event["line_index"])
        quote = lines[idx] if idx < len(lines) else str(event.get("raw_line", event.get("cmd", "")))
        evidence.append({"path": str(log_path), "quote": quote})

    return result(
        "PASS",
        "Verification command(s) appear after code changes in agentic.log.",
        evidence,
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
    "verification_after_code_changes": check_verification_after_code_changes,
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
