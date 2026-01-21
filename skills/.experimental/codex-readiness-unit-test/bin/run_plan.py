#!/usr/bin/env python3
import argparse
import io
import json
import os
import re
import selectors
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, TypedDict

DENYLIST_PATTERNS = [
    r"\brm\s+-rf\b",
    r"\brm\s+-fr\b",
    r"\brm\s+-r\b",
    r"\bgit\s+clean\s+-xfd\b",
    r"\bmkfs\b",
    r"\bdd\s+if=",
    r"\bdiskutil\s+erase\b",
    r"\b:;\s*\b",  # basic fork bomb patterns
    r"\bmkfs\.[a-z0-9]+\b",
]
TEST_KEYWORDS = [
    " test",
    "pytest",
    "node --test",
    "go test",
    "cargo test",
    "mvn test",
    "gradle test",
    "./gradlew test",
]
BUILD_KEYWORDS = [
    " build",
    "compile",
    "mvn package",
    "gradle build",
    "./gradlew build",
    "go build",
    "cargo build",
]


class PlanCommand(TypedDict, total=False):
    label: str
    cmd: str
    timeout_soft_seconds: int
    timeout_hard_seconds: int


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


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def is_denylisted(cmd: str) -> bool:
    lower = cmd.lower()
    return any(re.search(pattern, lower) for pattern in DENYLIST_PATTERNS)


def normalize_plan(plan_data: dict[str, Any]) -> dict[str, Any]:
    if "commands" not in plan_data:
        plan_data["commands"] = []
    commands: list[PlanCommand] = []
    for entry in plan_data.get("commands", []):
        if isinstance(entry, str):
            command_str: PlanCommand = {"label": "step", "cmd": entry}
            commands.append(command_str)
        elif isinstance(entry, dict):
            cmd = entry.get("cmd")
            if not cmd:
                raise ValueError("Each command entry must include 'cmd'.")
            command: PlanCommand = {
                "label": entry.get("label") or "step",
                "cmd": cmd,
            }
            soft = entry.get("timeout_soft_seconds")
            hard = entry.get("timeout_hard_seconds")
            if soft is not None:
                command["timeout_soft_seconds"] = int(soft)
            if hard is not None:
                command["timeout_hard_seconds"] = int(hard)
            commands.append(command)
        else:
            raise ValueError("Commands must be strings or objects with 'cmd'.")
    plan_data["commands"] = commands
    return plan_data


def classify_command(cmd: str) -> str | None:
    lower = cmd.lower()
    if any(keyword in lower for keyword in TEST_KEYWORDS):
        return "test"
    if any(keyword in lower for keyword in BUILD_KEYWORDS):
        return "build"
    return None


def infer_plan_commands(run_dir: Path) -> list[PlanCommand]:
    evidence_path = run_dir / "evidence.json"
    if not evidence_path.exists():
        return []
    evidence = load_json(evidence_path)
    candidates = (
        evidence.get("inferred", {}).get("candidate_commands") if isinstance(evidence, dict) else []
    )
    if not isinstance(candidates, list):
        return []

    build_cmd = None
    test_cmd = None
    for cmd in candidates:
        if not isinstance(cmd, str):
            continue
        label = classify_command(cmd)
        if label == "build" and build_cmd is None:
            build_cmd = cmd
        elif label == "test" and test_cmd is None:
            test_cmd = cmd
        if build_cmd and test_cmd:
            break

    commands: list[PlanCommand] = []
    if build_cmd:
        commands.append({"label": "build", "cmd": build_cmd})
    if test_cmd:
        commands.append({"label": "test", "cmd": test_cmd})
    return commands


def run_command(
    cmd: str, cwd: Path, env: dict, soft_timeout: int, hard_timeout: int, log_path: Path
) -> dict:
    started_at = now_iso()
    start_time = time.time()
    soft_exceeded = False
    hard_exceeded = False
    exit_code = None

    with log_path.open("w", encoding="utf-8") as log_file:
        proc = subprocess.Popen(
            cmd,
            shell=True,
            cwd=str(cwd),
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        selector = selectors.DefaultSelector()
        if proc.stdout:
            selector.register(proc.stdout, selectors.EVENT_READ)

        while True:
            now = time.time()
            if not soft_exceeded and now - start_time > soft_timeout:
                soft_exceeded = True
            if now - start_time > hard_timeout:
                hard_exceeded = True
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    proc.kill()
                break
            events = selector.select(timeout=0.2)
            for key, _ in events:
                file_obj = key.fileobj
                if isinstance(file_obj, io.TextIOBase):
                    line = file_obj.readline()
                    if line:
                        log_file.write(line)
            if proc.poll() is not None:
                break

        # Drain remaining output
        if proc.stdout:
            for line in proc.stdout:
                log_file.write(line)

        exit_code = proc.returncode

    ended_at = now_iso()
    duration = time.time() - start_time

    if hard_exceeded:
        status = "FAIL"
    elif exit_code == 0:
        status = "WARN" if soft_exceeded else "PASS"
    else:
        status = "FAIL"

    return {
        "cmd": cmd,
        "status": status,
        "exit_code": exit_code,
        "duration_seconds": round(duration, 2),
        "soft_timeout_seconds": soft_timeout,
        "hard_timeout_seconds": hard_timeout,
        "soft_timeout_exceeded": soft_exceeded,
        "hard_timeout_exceeded": hard_exceeded,
        "log_path": str(log_path),
        "started_at": started_at,
        "ended_at": ended_at,
    }


def sanitize_label(label: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_.-]+", "-", label.strip().lower())
    return cleaned.strip("-") or "step"


def main() -> int:
    parser = argparse.ArgumentParser(description="Execute a documented dev/build/test plan.")
    parser.add_argument("--plan", required=True, help="Path to plan JSON")
    parser.add_argument(
        "--out-dir", default=".codex-readiness-unit-test", help="Base output directory"
    )
    parser.add_argument("--run-dir", default=None, help="Specific run directory to use")
    parser.add_argument(
        "--soft-timeout-seconds", type=int, default=600, help="Soft timeout per command"
    )
    parser.add_argument(
        "--hard-timeout-multiplier", type=int, default=3, help="Hard timeout multiplier"
    )
    args = parser.parse_args()

    plan_path = Path(args.plan)
    if not plan_path.exists():
        raise SystemExit(f"Plan file not found: {plan_path}")

    plan_data = normalize_plan(load_json(plan_path))

    cwd = Path(plan_data.get("cwd") or plan_data.get("project_dir") or Path.cwd())
    if not cwd.is_absolute():
        cwd = (Path.cwd() / cwd).resolve()

    env = os.environ.copy()
    env.update(plan_data.get("env", {}))

    base_dir = Path(args.out_dir)
    base_dir.mkdir(parents=True, exist_ok=True)
    run_dir = resolve_run_dir(base_dir, args.run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    logs_dir = run_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    if not plan_data.get("commands"):
        inferred = infer_plan_commands(run_dir)
        if inferred:
            plan_data["commands"] = inferred
        else:
            raise ValueError(
                "Plan JSON has no commands and no build/test commands could be inferred from skills."
            )

    steps = []
    for index, entry in enumerate(plan_data.get("commands", []), start=1):
        label = entry.get("label") or f"step-{index}"
        cmd = entry.get("cmd", "").strip()
        soft_timeout = entry.get("timeout_soft_seconds") or args.soft_timeout_seconds
        hard_timeout = entry.get("timeout_hard_seconds") or (
            soft_timeout * args.hard_timeout_multiplier
        )

        log_path = logs_dir / f"{index:02d}-{sanitize_label(label)}.log"
        if is_denylisted(cmd):
            steps.append(
                {
                    "label": label,
                    "cmd": cmd,
                    "status": "FAIL",
                    "exit_code": None,
                    "duration_seconds": 0,
                    "soft_timeout_seconds": soft_timeout,
                    "hard_timeout_seconds": hard_timeout,
                    "soft_timeout_exceeded": False,
                    "hard_timeout_exceeded": False,
                    "denylisted": True,
                    "log_path": str(log_path),
                    "started_at": now_iso(),
                    "ended_at": now_iso(),
                }
            )
            continue

        result = run_command(cmd, cwd, env, soft_timeout, hard_timeout, log_path)
        result["label"] = label
        result["denylisted"] = False
        steps.append(result)

    overall_status = "PASS"
    for step in steps:
        if step["status"] == "FAIL":
            overall_status = "FAIL"
            break
        if step["status"] == "WARN":
            overall_status = "WARN"

    summary = {
        "plan_path": str(plan_path),
        "project_dir": str(plan_data.get("project_dir", cwd)),
        "cwd": str(cwd),
        "soft_timeout_seconds": args.soft_timeout_seconds,
        "hard_timeout_multiplier": args.hard_timeout_multiplier,
        "steps": steps,
        "overall_status": overall_status,
        "started_at": steps[0]["started_at"] if steps else now_iso(),
        "ended_at": steps[-1]["ended_at"] if steps else now_iso(),
    }

    summary_path = run_dir / "execution_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(str(summary_path))

    return 0 if overall_status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
