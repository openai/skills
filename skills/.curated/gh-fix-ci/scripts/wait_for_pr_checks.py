#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from shutil import which
from typing import Any

FAILURE_BUCKETS = {"fail", "cancel"}
FAILURE_STATES = {
    "failure",
    "error",
    "cancelled",
    "timed_out",
    "action_required",
    "startup_failure",
}
PENDING_BUCKETS = {"pending"}
PENDING_STATES = {"pending", "in_progress", "queued", "waiting", "requested"}
LONG_RUNNING_MARKERS = ("shows_slow", "coverage", "staging", "deploy", "railway")

DEFAULT_TIMEOUT_SECONDS = 2 * 60 * 60
DEFAULT_MIN_INTERVAL_SECONDS = 20
DEFAULT_MAX_INTERVAL_SECONDS = 75
DEFAULT_STABLE_POLLS = 2
DEFAULT_HEARTBEAT_POLLS = 4


@dataclass(frozen=True)
class CheckRecord:
    name: str
    bucket: str
    state: str
    link: str


def run_gh_json(*, args: list[str], cwd: Path) -> tuple[int, Any, str]:
    process = subprocess.run(
        ["gh", *args],
        cwd=cwd,
        text=True,
        capture_output=True,
    )
    stderr = (process.stderr or process.stdout or "").strip()
    if process.returncode != 0:
        return process.returncode, None, stderr
    try:
        return 0, json.loads(process.stdout or "null"), ""
    except json.JSONDecodeError:
        return 1, None, "Failed to parse gh JSON output."


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Wait for GitHub PR checks to complete with adaptive polling. "
            "Returns non-zero immediately if a failing check is detected."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--repo", default=".", help="Path inside the target Git repository.")
    parser.add_argument(
        "--pr",
        default=None,
        help="PR number or URL (defaults to current branch PR).",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=DEFAULT_TIMEOUT_SECONDS,
        help="Maximum time to wait before returning non-zero.",
    )
    parser.add_argument(
        "--min-interval-seconds",
        type=int,
        default=DEFAULT_MIN_INTERVAL_SECONDS,
        help="Minimum polling interval.",
    )
    parser.add_argument(
        "--max-interval-seconds",
        type=int,
        default=DEFAULT_MAX_INTERVAL_SECONDS,
        help="Maximum polling interval.",
    )
    parser.add_argument(
        "--stable-polls",
        type=int,
        default=DEFAULT_STABLE_POLLS,
        help="Number of consecutive no-pending polls before declaring success.",
    )
    parser.add_argument(
        "--heartbeat-polls",
        type=int,
        default=DEFAULT_HEARTBEAT_POLLS,
        help="Print status when unchanged for this many polls.",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON summary on exit.")
    return parser.parse_args()


def find_git_root(*, start: Path) -> Path | None:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=start,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        return None
    return Path(result.stdout.strip())


def ensure_gh_ready(*, repo_root: Path) -> bool:
    if which("gh") is None:
        print("Error: gh is not installed or not on PATH.", file=sys.stderr)
        return False
    process = subprocess.run(
        ["gh", "auth", "status"],
        cwd=repo_root,
        text=True,
        capture_output=True,
    )
    if process.returncode == 0:
        return True
    message = (process.stderr or process.stdout or "").strip()
    print(message or "Error: gh is not authenticated.", file=sys.stderr)
    return False


def resolve_pr(*, pr_value: str | None, repo_root: Path) -> str | None:
    if pr_value:
        return pr_value
    returncode, payload, error = run_gh_json(
        args=["pr", "view", "--json", "number"],
        cwd=repo_root,
    )
    if returncode != 0:
        print(error or "Error: unable to resolve PR.", file=sys.stderr)
        return None
    if not isinstance(payload, dict) or payload.get("number") is None:
        print("Error: no PR number found.", file=sys.stderr)
        return None
    return str(payload["number"])


def fetch_checks(*, pr_value: str, repo_root: Path) -> tuple[list[CheckRecord] | None, str]:
    returncode, payload, error = run_gh_json(
        args=["pr", "checks", pr_value, "--json", "name,bucket,state,link"],
        cwd=repo_root,
    )
    if returncode != 0:
        return None, error or "Error: gh pr checks failed."
    if not isinstance(payload, list):
        return None, "Error: unexpected checks payload."

    checks: list[CheckRecord] = []
    for item in payload:
        if not isinstance(item, dict):
            continue
        checks.append(
            CheckRecord(
                name=str(item.get("name") or ""),
                bucket=normalize(item.get("bucket")),
                state=normalize(item.get("state")),
                link=str(item.get("link") or ""),
            )
        )
    return checks, ""


def normalize(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip().lower()


def classify_checks(
    *,
    checks: list[CheckRecord],
) -> tuple[list[CheckRecord], list[CheckRecord], list[CheckRecord]]:
    failures: list[CheckRecord] = []
    pending: list[CheckRecord] = []
    completed: list[CheckRecord] = []

    for check in checks:
        if check.bucket in FAILURE_BUCKETS or check.state in FAILURE_STATES:
            failures.append(check)
            continue
        if check.bucket in PENDING_BUCKETS or check.state in PENDING_STATES:
            pending.append(check)
            continue
        completed.append(check)
    return failures, pending, completed


def has_long_running_pending(*, pending: list[CheckRecord]) -> bool:
    for check in pending:
        lowered = check.name.lower()
        if any(marker in lowered for marker in LONG_RUNNING_MARKERS):
            return True
    return False


def adaptive_interval_seconds(
    *,
    pending_count: int,
    unchanged_polls: int,
    long_running_pending: bool,
    min_seconds: int,
    max_seconds: int,
) -> int:
    if pending_count >= 6:
        base = 20
    elif pending_count >= 3:
        base = 30
    elif pending_count == 2:
        base = 40
    else:
        base = 30

    if long_running_pending and pending_count <= 2:
        base = max(base, 50)
    if unchanged_polls >= 5:
        base += 15
    if unchanged_polls >= 10:
        base += 10

    return max(min_seconds, min(max_seconds, base))


def snapshot_signature(*, checks: list[CheckRecord]) -> tuple[tuple[str, str, str], ...]:
    return tuple(sorted((check.name, check.bucket, check.state) for check in checks))


def print_status(
    *,
    pr_value: str,
    failures: list[CheckRecord],
    pending: list[CheckRecord],
    completed: list[CheckRecord],
    stable_hits: int,
    stable_target: int,
    elapsed_seconds: int,
) -> None:
    print(
        f"[t+{elapsed_seconds}s] PR #{pr_value}: "
        f"pending={len(pending)} fail={len(failures)} pass_or_other={len(completed)} "
        f"stable={stable_hits}/{stable_target}"
    )
    if pending:
        for check in pending:
            print(f"  - pending: {check.name}")
    if failures:
        for check in failures:
            print(f"  - fail: {check.name} ({check.link})")


def main() -> int:
    args = parse_args()

    if args.timeout_seconds <= 0:
        print("Error: --timeout-seconds must be greater than 0.", file=sys.stderr)
        return 1
    if args.min_interval_seconds <= 0 or args.max_interval_seconds <= 0:
        print("Error: poll intervals must be greater than 0.", file=sys.stderr)
        return 1
    if args.min_interval_seconds > args.max_interval_seconds:
        print("Error: min interval cannot be greater than max interval.", file=sys.stderr)
        return 1
    if args.stable_polls <= 0:
        print("Error: --stable-polls must be greater than 0.", file=sys.stderr)
        return 1
    if args.heartbeat_polls <= 0:
        print("Error: --heartbeat-polls must be greater than 0.", file=sys.stderr)
        return 1

    repo_root = find_git_root(start=Path(args.repo))
    if repo_root is None:
        print("Error: not inside a Git repository.", file=sys.stderr)
        return 1
    if not ensure_gh_ready(repo_root=repo_root):
        return 1

    pr_value = resolve_pr(pr_value=args.pr, repo_root=repo_root)
    if pr_value is None:
        return 1

    start_ts = time.time()
    stable_hits = 0
    unchanged_polls = 0
    poll_count = 0
    last_signature: tuple[tuple[str, str, str], ...] | None = None
    last_status: dict[str, Any] | None = None

    while True:
        checks, error = fetch_checks(pr_value=pr_value, repo_root=repo_root)
        if checks is None:
            print(error, file=sys.stderr)
            return 1

        failures, pending, completed = classify_checks(checks=checks)
        signature = snapshot_signature(checks=checks)
        changed = signature != last_signature
        if changed:
            unchanged_polls = 0
            stable_hits = 0 if pending else 1
        else:
            unchanged_polls += 1
            if not pending:
                stable_hits += 1

        elapsed_seconds = int(time.time() - start_ts)
        should_print = changed or unchanged_polls % args.heartbeat_polls == 0
        if should_print:
            print_status(
                pr_value=pr_value,
                failures=failures,
                pending=pending,
                completed=completed,
                stable_hits=stable_hits,
                stable_target=args.stable_polls,
                elapsed_seconds=elapsed_seconds,
            )

        last_status = {
            "pr": pr_value,
            "elapsedSeconds": elapsed_seconds,
            "pending": [check.__dict__ for check in pending],
            "failures": [check.__dict__ for check in failures],
            "completedCount": len(completed),
            "stableHits": stable_hits,
            "stableTarget": args.stable_polls,
            "pollCount": poll_count + 1,
        }

        if failures:
            if args.json:
                print(json.dumps(last_status, indent=2))
            return 1
        if not pending and stable_hits >= args.stable_polls:
            if args.json:
                print(json.dumps(last_status, indent=2))
            print(f"PR #{pr_value}: checks stabilized and are green.")
            return 0
        if elapsed_seconds >= args.timeout_seconds:
            print(
                f"Timeout after {elapsed_seconds}s while waiting for PR #{pr_value} checks.",
                file=sys.stderr,
            )
            if args.json and last_status is not None:
                print(json.dumps(last_status, indent=2))
            return 1

        poll_count += 1
        wait_seconds = adaptive_interval_seconds(
            pending_count=len(pending),
            unchanged_polls=unchanged_polls,
            long_running_pending=has_long_running_pending(pending=pending),
            min_seconds=args.min_interval_seconds,
            max_seconds=args.max_interval_seconds,
        )
        time.sleep(wait_seconds)
        last_signature = signature


if __name__ == "__main__":
    raise SystemExit(main())
