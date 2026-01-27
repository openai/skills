#!/usr/bin/env python3
import argparse
import json
import os
import pty
import re
import selectors
import shlex
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SESSION_ID_PATTERN = re.compile(r"session id:\s*([0-9a-fA-F-]{8,})")
ANSI_ESCAPE_PATTERN = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
QUESTION_PREFIXES = (
    "please ",
    "could you",
    "can you",
    "would you",
    "which ",
    "what ",
    "where ",
)
QUESTION_SUBSTRINGS = (
    "please provide",
    "please paste",
    "please point me",
    "provide ",
    "paste ",
    "point me",
    "clarify",
    "i can't find",
    "i can’t find",
)
IGNORE_LINE_PREFIXES = (
    "openai codex",
    "--------",
    "workdir:",
    "model:",
    "provider:",
    "approval:",
    "sandbox:",
    "reasoning",
    "session id:",
    "mcp startup:",
    "thinking",
    "exec",
    "tokens used",
)
MAX_FOLLOWUP_ROUNDS = 5
TAIL_LINE_LIMIT = 400
QUESTION_TERMINATE_GRACE_SECONDS = 2.0

SANDBOX_BLOCK_SUBSTRINGS = [
    "sandbox-blocked",
    "shell tool is sandbox-blocked",
    "sandbox_apply: operation not permitted",
    "operation not permitted",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


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


def normalize_args(raw_args: Any) -> list[str]:
    if raw_args is None:
        return []
    if isinstance(raw_args, str):
        return shlex.split(raw_args)
    if isinstance(raw_args, list):
        return [str(arg) for arg in raw_args]
    return []


def substitute_args(args: list[str], mapping: dict[str, str]) -> list[str]:
    resolved = []
    for arg in args:
        updated = arg
        for key, value in mapping.items():
            updated = updated.replace(key, value)
        resolved.append(updated)
    return resolved


def sanitize_agentic_args(args: list[str]) -> list[str]:
    """Remove unsafe or runner-managed flags from prompt-supplied args."""
    sanitized: list[str] = []
    skip_next = False
    # Flags that should not be controlled by the prompt in this runner.
    deny_flags_with_value = {"--sandbox", "--ask-for-approval", "-C", "--cd"}
    deny_flags = {
        "--dangerously-bypass-approvals-and-sandbox",
        "--full-auto",
        "exec",
        "resume",
        "{change_prompt}",
    }
    for arg in args:
        if skip_next:
            skip_next = False
            continue
        if arg in deny_flags_with_value:
            skip_next = True
            continue
        if arg in deny_flags:
            continue
        sanitized.append(arg)
    return sanitized


def build_command(
    prompt: dict[str, Any], agents_path: Path, prompt_path: Path, repo_root: Path
) -> tuple[list[str], int]:
    agentic_config = prompt.get("agentic_loop")
    config: dict[str, Any] = agentic_config if isinstance(agentic_config, dict) else {}
    cmd = config.get("cmd") or "codex"
    prompt_args = sanitize_agentic_args(normalize_args(config.get("args")))
    # Hardcode a safe, broadly supported permission model at the runner level,
    # while allowing other prompt-supplied flags (e.g., model selection).
    raw_args = ["exec", "--full-auto"] + prompt_args + ["-C", "{repo_root}", "{change_prompt}"]
    args = normalize_args(raw_args)
    change_prompt = str(prompt.get("change_prompt") or "").strip()
    plan_instruction = str(prompt.get("plan_instruction") or "").strip()
    if plan_instruction:
        change_prompt = f"{plan_instruction} {change_prompt}".strip()
    mapping = {
        "{agents_path}": str(agents_path),
        "{change_prompt}": change_prompt,
        "{prompt_path}": str(prompt_path),
        "{run_dir}": str(prompt_path.parent),
        "{repo_root}": str(repo_root),
    }
    args = substitute_args(args, mapping)
    timeout = int(config.get("timeout_seconds") or 1800)
    return [cmd] + args, timeout


def filter_resume_args(args: list[str]) -> list[str]:
    filtered: list[str] = []
    skip_next = False
    for arg in args:
        if skip_next:
            skip_next = False
            continue
        if arg == "exec":
            continue
        if arg in {"-C", "--cd"}:
            skip_next = True
            continue
        if arg == "{change_prompt}":
            continue
        filtered.append(arg)
    return filtered


def build_resume_command(
    prompt: dict[str, Any],
    session_id: str,
    resume_prompt: str,
    agents_path: Path,
    prompt_path: Path,
    repo_root: Path,
) -> tuple[list[str], int]:
    agentic_config = prompt.get("agentic_loop")
    config: dict[str, Any] = agentic_config if isinstance(agentic_config, dict) else {}
    cmd = config.get("cmd") or "codex"
    prompt_args = sanitize_agentic_args(normalize_args(config.get("args")))
    raw_args = ["exec", "--full-auto"] + prompt_args
    args = normalize_args(raw_args)
    mapping = {
        "{agents_path}": str(agents_path),
        "{prompt_path}": str(prompt_path),
        "{run_dir}": str(prompt_path.parent),
        "{repo_root}": str(repo_root),
    }
    filtered_args = substitute_args(filter_resume_args(args), mapping)
    timeout = int(config.get("timeout_seconds") or 1800)
    resume_args = ["exec", "resume"] + filtered_args + [session_id, resume_prompt]
    return [cmd] + resume_args, timeout


def run_command(
    cmd: list[str],
    cwd: Path,
    env: dict,
    timeout: int,
    log_path: Path,
    *,
    append: bool,
    attempt_label: str,
) -> dict:
    started_at = now_iso()
    start_time = time.time()
    exit_code = None
    status = "FAIL"
    mode = "a" if append else "w"
    timed_out = False
    error_message = None
    master_fd = None
    cmd_display = " ".join(shlex.quote(part) for part in cmd)

    try:
        with log_path.open(mode, encoding="utf-8") as log_file:
            if append:
                log_file.write("\n\n")
            log_file.write(f"===== {attempt_label} =====\n")
            log_file.write(f"$ {cmd_display}\n")
            log_file.flush()

            if not sys.stdin.isatty():
                error_message = "Interactive mode requires a TTY on stdin."
                raise RuntimeError(error_message)

            master_fd, slave_fd = pty.openpty()
            proc = subprocess.Popen(
                cmd,
                cwd=str(cwd),
                env=env,
                stdin=slave_fd,
                stdout=slave_fd,
                stderr=slave_fd,
                close_fds=True,
            )
            os.close(slave_fd)

            sel = selectors.DefaultSelector()
            sel.register(master_fd, selectors.EVENT_READ)
            sel.register(sys.stdin, selectors.EVENT_READ)
            stdin_fd = sys.stdin.fileno()
            old_tty = termios.tcgetattr(stdin_fd)
            deadline = time.time() + timeout

            try:
                tty.setraw(stdin_fd)
                master_closed = False
                while True:
                    if proc.poll() is not None:
                        break
                    if time.time() > deadline:
                        timed_out = True
                        proc.terminate()
                        break
                    events = sel.select(timeout=0.1)
                    for key, _ in events:
                        if key.fileobj == master_fd:
                            data = os.read(master_fd, 1024)
                            if data:
                                os.write(sys.stdout.fileno(), data)
                                log_file.buffer.write(data)
                                log_file.flush()
                            else:
                                master_closed = True
                                break
                        else:
                            data = os.read(stdin_fd, 1024)
                            if data:
                                os.write(master_fd, data)
                    if master_closed:
                        break
                if timed_out:
                    try:
                        proc.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        proc.kill()
                        proc.wait(timeout=5)
                exit_code = proc.wait()
            finally:
                termios.tcsetattr(stdin_fd, termios.TCSADRAIN, old_tty)
                sel.close()
    except FileNotFoundError as exc:
        error_message = f"Command not found: {exc}"
    except subprocess.TimeoutExpired:
        error_message = f"Command timed out after {timeout} seconds."
    except RuntimeError as exc:
        error_message = str(exc)
    except KeyboardInterrupt:
        error_message = "Interrupted by user."
    finally:
        if master_fd is not None:
            os.close(master_fd)
        if error_message:
            with log_path.open("a", encoding="utf-8") as log_file:
                log_file.write(f"{error_message}\n")
        if timed_out:
            status = "FAIL"
        else:
            if exit_code == 0:
                status = "PASS"
            else:
                status = "FAIL"

    ended_at = now_iso()
    duration = round(time.time() - start_time, 2)

    return {
        "cmd": cmd_display,
        "status": status,
        "exit_code": exit_code,
        "duration_seconds": duration,
        "started_at": started_at,
        "ended_at": ended_at,
    }


def prepare_codex_env(repo_root: Path, env: dict) -> dict:
    codex_home = repo_root / ".codex-home"
    cache_root = codex_home / ".cache" / "codex"
    cache_root.mkdir(parents=True, exist_ok=True)
    env = dict(env)
    env["HOME"] = str(codex_home)
    env.setdefault("XDG_CACHE_HOME", str(codex_home / ".cache"))
    env.setdefault("CODEX_NO_UPDATE", "1")
    return env


def extract_session_id(log_text: str) -> str | None:
    matches = SESSION_ID_PATTERN.findall(log_text)
    if not matches:
        return None
    return matches[-1]


def strip_ansi(text: str) -> str:
    return ANSI_ESCAPE_PATTERN.sub("", text)


def is_question_line(line: str) -> bool:
    lower = line.strip().lower()
    if not lower:
        return False
    # Codex often ends with friendly follow-up headings like 'what changed:'
    # or 'what i verified:'. Treat these as non-blocking in non-interactive runs.
    if lower.startswith("what changed"):
        return False
    if lower.startswith("what ") and lower.endswith(":"):
        return False
    if lower.endswith("?"):
        return True
    if lower.startswith(QUESTION_PREFIXES):
        return True
    return any(fragment in lower for fragment in QUESTION_SUBSTRINGS)


def extract_last_attempt_log(log_text: str) -> str:
    sections = re.split(r"^===== .* =====$", log_text, flags=re.MULTILINE)
    if not sections:
        return log_text
    return sections[-1]


def extract_clarifying_question(log_text: str) -> str | None:
    lines = [line.strip() for line in log_text.splitlines()]
    for line in reversed(lines):
        if not line:
            continue
        lower = line.lower()
        if lower.startswith(IGNORE_LINE_PREFIXES):
            continue
        if is_question_line(line):
            return line
    return None


def prompt_for_answer(question: str) -> str:
    print("\nCodex asked:")
    print(question)
    if not sys.stdin.isatty():
        auto = os.environ.get(
            "CODEX_INTEGRATION_AUTOANSWER",
            "Proceed with best effort using the repository context. Do not ask follow-up questions.",
        ).strip()
        print(f"Auto-answering (non-interactive): {auto}")
        return auto
    while True:
        answer = input("Answer: ").strip()
        if answer:
            return answer
        print("Please provide an answer to continue.")


def detect_sandbox_block(log_text: str) -> str | None:
    for raw_line in log_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        lower = line.lower()
        for marker in SANDBOX_BLOCK_SUBSTRINGS:
            if marker in lower:
                return line
    return None


def append_tail_lines(tail_lines: list[str], line: str) -> None:
    tail_lines.append(line)
    if len(tail_lines) > TAIL_LINE_LIMIT:
        del tail_lines[: len(tail_lines) - TAIL_LINE_LIMIT]


def run_non_interactive(
    cmd: list[str],
    cwd: Path,
    env: dict,
    timeout: int,
    log_path: Path,
    *,
    append: bool,
    attempt_label: str,
) -> dict:
    started_at = now_iso()
    start_time = time.time()
    exit_code = None
    status = "FAIL"
    mode = "a" if append else "w"
    timed_out = False
    error_message = None
    question_detected = None
    session_id = None
    terminated_for_question = False
    log_buffer = ""
    tail_lines: list[str] = []
    cmd_display = " ".join(shlex.quote(part) for part in cmd)

    try:
        with log_path.open(mode, encoding="utf-8") as log_file:
            if append:
                log_file.write("\n\n")
            log_file.write(f"===== {attempt_label} =====\n")
            log_file.write(f"$ {cmd_display}\n")
            log_file.flush()

            proc = subprocess.Popen(
                cmd,
                cwd=str(cwd),
                env=env,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                close_fds=True,
            )

            if proc.stdout is None:
                raise RuntimeError("Failed to capture stdout for non-interactive mode.")

            sel = selectors.DefaultSelector()
            sel.register(proc.stdout, selectors.EVENT_READ)
            deadline = time.time() + timeout

            try:
                while True:
                    if proc.poll() is not None:
                        break
                    if time.time() > deadline:
                        timed_out = True
                        proc.terminate()
                        break
                    events = sel.select(timeout=0.1)
                    for key, _ in events:
                        data = os.read(key.fileobj.fileno(), 1024)
                        if not data:
                            continue
                        log_file.buffer.write(data)
                        log_file.flush()

                        text = data.decode("utf-8", errors="ignore")
                        log_buffer += text
                        while "\n" in log_buffer:
                            line, log_buffer = log_buffer.split("\n", 1)
                            clean = strip_ansi(line)
                            append_tail_lines(tail_lines, clean)
                            if session_id is None:
                                match = SESSION_ID_PATTERN.search(clean)
                                if match:
                                    session_id = match.group(1)
                            if question_detected is None and is_question_line(clean):
                                question_detected = clean.strip()
                                if session_id:
                                    terminated_for_question = True
                                    proc.terminate()
                                    break
                        if terminated_for_question:
                            break
                    if terminated_for_question:
                        break

                if log_buffer:
                    clean = strip_ansi(log_buffer)
                    append_tail_lines(tail_lines, clean)
                    if session_id is None:
                        match = SESSION_ID_PATTERN.search(clean)
                        if match:
                            session_id = match.group(1)
                    if question_detected is None and is_question_line(clean):
                        question_detected = clean.strip()
                if terminated_for_question:
                    deadline = time.time() + QUESTION_TERMINATE_GRACE_SECONDS
                    while time.time() < deadline and proc.poll() is None:
                        time.sleep(0.05)
                if timed_out:
                    try:
                        proc.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        proc.kill()
                        proc.wait(timeout=5)
                else:
                    exit_code = proc.wait()
            finally:
                sel.close()
    except FileNotFoundError as exc:
        error_message = f"Command not found: {exc}"
    except subprocess.TimeoutExpired:
        error_message = f"Command timed out after {timeout} seconds."
    except RuntimeError as exc:
        error_message = str(exc)
    except KeyboardInterrupt:
        error_message = "Interrupted by user."
    finally:
        if error_message:
            with log_path.open("a", encoding="utf-8") as log_file:
                log_file.write(f"{error_message}\n")
        if timed_out:
            status = "FAIL"
        else:
            if exit_code == 0 or terminated_for_question:
                status = "PASS"
            else:
                status = "FAIL"

    ended_at = now_iso()
    duration = round(time.time() - start_time, 2)

    return {
        "cmd": cmd_display,
        "status": status,
        "exit_code": exit_code,
        "duration_seconds": duration,
        "started_at": started_at,
        "ended_at": ended_at,
        "mode": "non_interactive",
        "question_detected": question_detected,
        "question_handled": False,
        "session_id": session_id,
        "terminated_for_question": terminated_for_question,
    }


def run_safe_interactive(
    cmd: list[str],
    cwd: Path,
    env: dict,
    timeout: int,
    log_path: Path,
    *,
    append: bool,
    attempt_label: str,
) -> dict:
    started_at = now_iso()
    start_time = time.time()
    exit_code = None
    status = "FAIL"
    mode = "a" if append else "w"
    timed_out = False
    error_message = None
    master_fd = None
    question_detected = None
    session_id = None
    questions_handled: list[str] = []
    log_buffer = ""
    tail_lines: list[str] = []
    cmd_display = " ".join(shlex.quote(part) for part in cmd)

    try:
        with log_path.open(mode, encoding="utf-8") as log_file:
            if append:
                log_file.write("\n\n")
            log_file.write(f"===== {attempt_label} =====\n")
            log_file.write(f"$ {cmd_display}\n")
            log_file.flush()

            if not sys.stdin.isatty():
                error_message = "Safe-interactive mode requires a TTY on stdin."
                raise RuntimeError(error_message)

            master_fd, slave_fd = pty.openpty()
            proc = subprocess.Popen(
                cmd,
                cwd=str(cwd),
                env=env,
                stdin=slave_fd,
                stdout=slave_fd,
                stderr=slave_fd,
                close_fds=True,
            )
            os.close(slave_fd)

            sel = selectors.DefaultSelector()
            sel.register(master_fd, selectors.EVENT_READ)
            deadline = time.time() + timeout

            try:
                master_closed = False
                while True:
                    if proc.poll() is not None:
                        break
                    if time.time() > deadline:
                        timed_out = True
                        proc.terminate()
                        break
                    events = sel.select(timeout=0.1)
                    for key, _ in events:
                        if key.fileobj == master_fd:
                            data = os.read(master_fd, 1024)
                            if data:
                                log_file.buffer.write(data)
                                log_file.flush()

                                text = data.decode("utf-8", errors="ignore")
                                log_buffer += text
                                while "\n" in log_buffer:
                                    line, log_buffer = log_buffer.split("\n", 1)
                                    clean = strip_ansi(line)
                                    append_tail_lines(tail_lines, clean)
                                    if session_id is None:
                                        match = SESSION_ID_PATTERN.search(clean)
                                        if match:
                                            session_id = match.group(1)
                                    if is_question_line(clean):
                                        question_detected = clean.strip()
                                        if (
                                            question_detected
                                            and question_detected not in questions_handled
                                        ):
                                            answer = prompt_for_answer(question_detected)
                                            os.write(master_fd, (answer + "\n").encode())
                                            questions_handled.append(question_detected)
                            else:
                                master_closed = True
                                break
                    if master_closed:
                        break
                if timed_out:
                    try:
                        proc.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        proc.kill()
                        proc.wait(timeout=5)
                exit_code = proc.wait()
            finally:
                sel.close()
    except FileNotFoundError as exc:
        error_message = f"Command not found: {exc}"
    except subprocess.TimeoutExpired:
        error_message = f"Command timed out after {timeout} seconds."
    except RuntimeError as exc:
        error_message = str(exc)
    except KeyboardInterrupt:
        error_message = "Interrupted by user."
    finally:
        if master_fd is not None:
            os.close(master_fd)
        if error_message:
            with log_path.open("a", encoding="utf-8") as log_file:
                log_file.write(f"{error_message}\n")
        if timed_out:
            status = "FAIL"
        else:
            if exit_code == 0:
                status = "PASS"
            else:
                status = "FAIL"

    ended_at = now_iso()
    duration = round(time.time() - start_time, 2)

    return {
        "cmd": cmd_display,
        "status": status,
        "exit_code": exit_code,
        "duration_seconds": duration,
        "started_at": started_at,
        "ended_at": ended_at,
        "mode": "safe_interactive",
        "question_detected": question_detected,
        "question_handled": bool(questions_handled),
        "session_id": session_id,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the agentic loop via Codex CLI.")
    parser.add_argument(
        "--out-dir", default=".codex-readiness-integration-test", help="Base output directory"
    )
    parser.add_argument("--run-dir", default=None, help="Specific run directory to use")
    args = parser.parse_args()

    base_dir = Path(args.out_dir)
    run_dir = resolve_run_dir(base_dir, args.run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    logs_dir = run_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    prompt_path = run_dir / "prompt.json"
    if not prompt_path.exists():
        summary = {
            "cmd": "",
            "status": "FAIL",
            "exit_code": None,
            "duration_seconds": 0,
            "started_at": now_iso(),
            "ended_at": now_iso(),
            "error": "prompt.json missing",
        }
        summary_path = run_dir / "agentic_summary.json"
        summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        print(str(summary_path))
        return 2

    prompt = load_json(prompt_path)
    repo_root = Path.cwd()
    agents_path = repo_root / "AGENTS.md"

    log_path = logs_dir / "agentic.log"
    env = prepare_codex_env(repo_root, os.environ.copy())

    questions: list[str] = []
    attempts: list[dict] = []
    session_id: str | None = None
    resume_prompt: str | None = None
    append_log = False
    summary: dict | None = None
    auto_answer_count = 0
    last_auto_answer_text: str | None = None

    for attempt in range(1, MAX_FOLLOWUP_ROUNDS + 1):
        if resume_prompt:
            if session_id is None:
                break
            cmd, timeout = build_resume_command(
                prompt,
                session_id,
                resume_prompt,
                agents_path,
                prompt_path,
                repo_root,
            )
            attempt_label = f"resume-attempt-{attempt}"
        else:
            cmd, timeout = build_command(prompt, agents_path, prompt_path, repo_root)
            attempt_label = f"agentic-attempt-{attempt}"

        if resume_prompt and sys.stdin.isatty():
            summary = run_safe_interactive(
                cmd,
                repo_root,
                env,
                timeout,
                log_path,
                append=append_log,
                attempt_label=attempt_label,
            )
        else:
            summary = run_non_interactive(
                cmd,
                repo_root,
                env,
                timeout,
                log_path,
                append=append_log,
                attempt_label=attempt_label,
            )
        attempts.append(dict(summary))
        append_log = True

        if summary.get("question_handled"):
            break

        log_text = log_path.read_text(encoding="utf-8", errors="ignore")
        if session_id is None:
            session_id = summary.get("session_id") or extract_session_id(log_text)
        attempt_log = extract_last_attempt_log(log_text)
        question = summary.get("question_detected") or extract_clarifying_question(attempt_log)
        if question:
            questions.append(question)
            if not sys.stdin.isatty():
                if session_id is None:
                    summary["status"] = "FAIL"
                    summary["error"] = "session id missing for auto-answer resume"
                    break
                resume_prompt = prompt_for_answer(question)
                auto_answer_count += 1
                last_auto_answer_text = resume_prompt
                summary["question_detected"] = question
                summary["auto_answer_used"] = True
                summary["auto_answer_text"] = resume_prompt
                summary["auto_answer_count"] = auto_answer_count
                summary["non_interactive_question_ignored"] = False
                continue
            if session_id is None:
                summary["status"] = "FAIL"
                summary["error"] = "session id missing for resume"
                break
            resume_prompt = prompt_for_answer(question)
            continue
        break

    if summary is None:
        summary = {
            "cmd": "",
            "status": "FAIL",
            "exit_code": None,
            "duration_seconds": 0,
            "started_at": now_iso(),
            "ended_at": now_iso(),
            "error": "agentic loop did not run",
        }

    log_text = log_path.read_text(encoding="utf-8", errors="ignore")
    sandbox_block_evidence = detect_sandbox_block(log_text)
    if sandbox_block_evidence:
        summary["status"] = "FAIL"
        summary["error"] = (
            "Codex tool access appears to be sandbox-blocked. "
            "Re-run the integration test with escalated permissions."
        )
        summary["sandbox_blocked"] = True
        summary["sandbox_block_evidence"] = sandbox_block_evidence
        summary["requires_escalation"] = True
        print("Detected sandbox-blocked tool access; escalate permissions and re-run.")

    if auto_answer_count:
        summary["auto_answer_count"] = auto_answer_count
        if last_auto_answer_text:
            summary["auto_answer_text"] = last_auto_answer_text

    summary_path = run_dir / "agentic_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(str(summary_path))
    if summary.get("requires_escalation"):
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
