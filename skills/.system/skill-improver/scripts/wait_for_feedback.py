#!/usr/bin/env python3
"""Wait until an eval review viewer writes complete feedback.json."""

import argparse
import json
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from feedback_to_revision_brief import build_brief


def feedback_is_complete(path: Path) -> bool:
    try:
        data = json.loads(path.read_text())
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return False
    return data.get("status") == "complete"


def write_revision_brief(feedback_path: Path, benchmark_path: Path | None, output_path: Path) -> None:
    brief = build_brief(feedback_path, benchmark_path)
    output_path.write_text(brief)


def main() -> None:
    parser = argparse.ArgumentParser(description="Wait for skill-improver review feedback")
    parser.add_argument("feedback_json", type=Path, help="Path to feedback.json written by the eval viewer")
    parser.add_argument("--poll-seconds", type=float, default=2.0, help="Polling interval (default: 2)")
    parser.add_argument("--timeout-seconds", type=float, default=0.0, help="Optional timeout; 0 waits forever")
    parser.add_argument("--benchmark", type=Path, default=None, help="Optional benchmark.json to summarize in the revision brief")
    parser.add_argument("--revision-brief", type=Path, default=None, help="Write a model-ready revision brief after feedback is complete")
    args = parser.parse_args()

    started = time.monotonic()
    while True:
        if feedback_is_complete(args.feedback_json):
            print(f"Feedback complete: {args.feedback_json}")
            if args.revision_brief:
                write_revision_brief(args.feedback_json, args.benchmark, args.revision_brief)
                print(f"Revision brief: {args.revision_brief}")
            return
        if args.timeout_seconds > 0 and time.monotonic() - started > args.timeout_seconds:
            print(f"Timed out waiting for complete feedback: {args.feedback_json}", file=sys.stderr)
            sys.exit(1)
        time.sleep(args.poll_seconds)


if __name__ == "__main__":
    main()
