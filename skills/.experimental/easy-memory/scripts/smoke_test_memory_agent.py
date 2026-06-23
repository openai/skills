#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

from memory_agent_client import SUMMARY_PREFIX
from memory_agent_config import (
    default_local_config_file,
    installed_skill_dir,
    load_memory_agent_config,
)
from memory_agent_failure_log import agent_failure_log_path
from memory_utils import log_base_dir, require_initialized


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run a small end-to-end smoke test for the easy-memory "
            "memory-agent integration in the current project."
        )
    )
    parser.add_argument(
        "--task-context",
        default=(
            "Smoke test for the current easy-memory memory-agent "
            "configuration in this project."
        ),
        help="Task context passed to both read_today_log.py and search_memory.py.",
    )
    parser.add_argument(
        "--search-keyword",
        action="append",
        dest="search_keywords",
        default=[],
        help=(
            "Keyword passed to search_memory.py. Repeat to provide multiple "
            "keywords. Defaults to easy-memory, memory-agent, and codex."
        ),
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=3,
        help="Maximum results passed to search_memory.py (default: 3).",
    )
    parser.add_argument(
        "--command-timeout",
        type=float,
        default=90.0,
        help="Per-command timeout in seconds (default: 90).",
    )
    parser.add_argument(
        "--strict-no-new-failures",
        action="store_true",
        help=(
            "Fail the smoke test if the shared installation-directory "
            "agent failure log grows during this test run."
        ),
    )
    parser.add_argument(
        "--json-output-file",
        help=(
            "Optional path to write the final smoke-test JSON report. "
            "Relative paths are resolved from the current working directory."
        ),
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help=(
            "Suppress successful stdout output. Errors still surface normally. "
            "Use with --json-output-file when another tool will read the report."
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.max_results <= 0:
        raise SystemExit("--max-results must be a positive integer.")
    if args.command_timeout <= 0:
        raise SystemExit("--command-timeout must be a positive number.")

    base_dir = log_base_dir(create=True)
    require_initialized(base_dir)
    output_file = resolve_optional_output_file(args.json_output_file)

    config_file = default_local_config_file()
    if not config_file.exists():
        raise SystemExit(
            f"Project-local memory-agent config file not found: {config_file}"
        )

    keywords = args.search_keywords or [
        "easy-memory",
        "memory-agent",
        "codex",
    ]
    config = load_memory_agent_config()
    failure_log = agent_failure_log_path(installed_skill_dir())
    failure_log_before = count_log_lines(failure_log)

    tests = [
        run_cli_test(
            script_name="search_memory.py",
            mode="search_memory",
            script_args=[
                *keywords,
                "--max-results",
                str(args.max_results),
                "--task-context",
                args.task_context,
            ],
            timeout_seconds=args.command_timeout,
        ),
        run_cli_test(
            script_name="read_today_log.py",
            mode="read_today_log",
            script_args=[
                "--task-context",
                args.task_context,
            ],
            timeout_seconds=args.command_timeout,
        ),
    ]
    failure_log_after = count_log_lines(failure_log)

    if args.strict_no_new_failures and failure_log_after > failure_log_before:
        last_record_preview = read_last_log_line(failure_log)
        raise SystemExit(
            "Smoke test detected new agent failure log entries during the test run.\n"
            f"failure_log: {failure_log}\n"
            f"before: {failure_log_before}\n"
            f"after: {failure_log_after}\n"
            f"last_record: {last_record_preview}"
        )

    report = {
        "status": "ok",
        "cwd": str(Path.cwd()),
        "config_file": str(config_file),
        "json_output_file": str(output_file) if output_file else None,
        "agent_config": {
            "enabled": config.enabled,
            "api_style": config.api_style,
            "model": config.model,
            "base_url": config.base_url,
            "codex_binary": config.codex_binary,
            "codex_profile": config.codex_profile,
            "codex_service_tier": config.codex_service_tier,
            "codex_reasoning_effort": config.codex_reasoning_effort,
            "disable_thinking": config.disable_thinking,
            "timeout_seconds": config.timeout_seconds,
        },
        "failure_log": {
            "path": str(failure_log),
            "before_lines": failure_log_before,
            "after_lines": failure_log_after,
            "strict_no_new_failures": args.strict_no_new_failures,
        },
        "tests": tests,
    }
    rendered_report = json.dumps(report, ensure_ascii=False, indent=2)
    if output_file is not None:
        write_report_file(output_file, rendered_report)
    if not args.quiet:
        print(rendered_report)
    return 0


def run_cli_test(
    *,
    script_name: str,
    mode: str,
    script_args: list[str],
    timeout_seconds: float,
) -> dict[str, object]:
    script_path = Path(__file__).resolve().parent / script_name
    started_at = time.monotonic()
    try:
        completed = subprocess.run(
            [sys.executable, str(script_path), *script_args],
            cwd=Path.cwd(),
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise SystemExit(
            f"{script_name} timed out after {timeout_seconds:.1f}s."
        ) from exc
    elapsed_seconds = round(time.monotonic() - started_at, 2)

    if completed.returncode != 0:
        stderr_text = completed.stderr.strip()
        stdout_text = completed.stdout.strip()
        raise SystemExit(
            f"{script_name} exited with code {completed.returncode}.\n"
            f"stdout:\n{stdout_text}\n"
            f"stderr:\n{stderr_text}"
        )

    stderr_text = completed.stderr.strip()
    if "Memory-agent fallback:" in stderr_text:
        raise SystemExit(
            f"{script_name} fell back to raw output.\n"
            f"stdout:\n{completed.stdout.strip()}\n"
            f"stderr:\n{stderr_text}"
        )

    stdout_text = completed.stdout.strip()
    if not stdout_text:
        raise SystemExit(
            f"{script_name} returned empty stdout."
        )
    summary_line = extract_summary_line(
        stdout_text=stdout_text,
        script_name=script_name,
    )

    return {
        "script": script_name,
        "mode": mode,
        "elapsed_seconds": elapsed_seconds,
        "status": "ok",
        "summary": summary_line.removeprefix(SUMMARY_PREFIX).strip(),
    }


def extract_summary_line(
    *,
    stdout_text: str,
    script_name: str,
) -> str:
    nonempty_lines = [
        line.strip()
        for line in stdout_text.splitlines()
        if line.strip()
    ]
    if not nonempty_lines:
        raise SystemExit(
            f"{script_name} did not return any non-empty output.\n"
            f"stdout:\n{stdout_text}\n"
        )
    summary_line = nonempty_lines[-1]
    if not summary_line.startswith(SUMMARY_PREFIX):
        raise SystemExit(
            f"{script_name} did not end with the expected summary line.\n"
            f"stdout:\n{stdout_text}\n"
        )
    return summary_line


def count_log_lines(log_path: Path) -> int:
    if not log_path.exists():
        return 0
    with log_path.open("r", encoding="utf-8") as handle:
        return sum(1 for _ in handle)


def read_last_log_line(log_path: Path) -> str:
    if not log_path.exists():
        return ""
    last_line = ""
    with log_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if stripped:
                last_line = stripped
    return last_line


def resolve_optional_output_file(raw_value: str | None) -> Path | None:
    if raw_value is None:
        return None
    candidate = Path(raw_value).expanduser()
    if not candidate.is_absolute():
        candidate = (Path.cwd() / candidate).resolve()
    return candidate


def write_report_file(output_file: Path, rendered_report: str) -> None:
    try:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(f"{rendered_report}\n", encoding="utf-8")
    except OSError as exc:
        raise SystemExit(
            f"Failed to write smoke-test report file: {output_file}"
        ) from exc


if __name__ == "__main__":
    raise SystemExit(main())
