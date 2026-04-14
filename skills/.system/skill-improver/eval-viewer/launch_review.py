#!/usr/bin/env python3
"""Launch generate_review.py as a detached background server and verify readiness."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
import webbrowser
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Launch the eval review viewer in the background")
    parser.add_argument("workspace", type=Path, help="Path to the iteration workspace directory")
    parser.add_argument("--port", "-p", type=int, default=3117, help="Preferred server port (default: 3117)")
    parser.add_argument("--skill-name", "-n", type=str, default=None, help="Skill name for viewer header")
    parser.add_argument(
        "--previous-workspace",
        type=Path,
        default=None,
        help="Path to previous iteration workspace for side-by-side review context",
    )
    parser.add_argument(
        "--benchmark",
        type=Path,
        default=None,
        help="Optional path to benchmark.json for the Benchmark tab",
    )
    parser.add_argument(
        "--log-file",
        type=Path,
        default=None,
        help="Log destination. Defaults to <workspace>/viewer.log",
    )
    parser.add_argument(
        "--startup-timeout",
        type=float,
        default=10.0,
        help="Seconds to wait for the viewer URL to appear in the log (default: 10)",
    )
    parser.add_argument(
        "--no-open-url",
        action="store_true",
        help="Do not open the viewer URL in a browser after startup succeeds.",
    )
    return parser.parse_args()


def build_command(args: argparse.Namespace, script_path: Path) -> list[str]:
    command = [
        sys.executable,
        "-u",
        str(script_path),
        str(args.workspace),
        "--port",
        str(args.port),
        "--no-browser-open",
    ]
    if args.skill_name:
        command.extend(["--skill-name", args.skill_name])
    if args.previous_workspace:
        command.extend(["--previous-workspace", str(args.previous_workspace)])
    if args.benchmark:
        command.extend(["--benchmark", str(args.benchmark)])
    return command


def wait_for_url(log_path: Path, process: subprocess.Popen[bytes], timeout_seconds: float) -> str | None:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        if process.poll() is not None:
            return None
        try:
            text = log_path.read_text(errors="replace")
        except OSError:
            text = ""
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("URL:"):
                return stripped.split("URL:", 1)[1].strip()
        time.sleep(0.2)
    return None


def main() -> int:
    args = parse_args()
    workspace = args.workspace.resolve()
    if not workspace.is_dir():
        print(f"Error: {workspace} is not a directory", file=sys.stderr)
        return 1

    log_path = args.log_file.resolve() if args.log_file else workspace / "viewer.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)

    script_path = Path(__file__).with_name("generate_review.py")
    command = build_command(args, script_path)

    with log_path.open("wb") as log_file, open(os.devnull, "rb") as devnull:
        process = subprocess.Popen(
            command,
            stdin=devnull,
            stdout=log_file,
            stderr=subprocess.STDOUT,
            start_new_session=True,
            cwd=str(workspace),
        )

    url = wait_for_url(log_path, process, args.startup_timeout)
    if url is None:
        returncode = process.poll()
        if returncode is None:
            process.terminate()
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=2)
            reason = f"viewer did not report a URL within {args.startup_timeout:.1f}s"
        else:
            reason = f"viewer exited early with code {returncode}"
        print(f"Error: {reason}", file=sys.stderr)
        print(f"Log: {log_path}", file=sys.stderr)
        return 1

    if not args.no_open_url:
        try:
            webbrowser.open(url)
        except Exception:
            pass

    print(f"URL: {url}")
    print(f"PID: {process.pid}")
    print(f"Log: {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
