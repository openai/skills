#!/usr/bin/env python3
import argparse
import json
import os
import shlex
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

VALID_STATUSES = {"PASS", "WARN", "FAIL", "NOT_RUN"}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


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


def build_command(
    config: dict[str, Any],
    eval_prompt_path: Path,
    eval_input_path: Path,
    eval_schema_path: Path,
    eval_output_path: Path,
    repo_root: Path,
    run_dir: Path,
    check_id: str,
) -> tuple[list[str], int]:
    cmd = config.get("cmd") or "codex"
    raw_args = config.get("args") or [
        "exec",
        "--output-schema",
        "{eval_schema_path}",
        "--output-last-message",
        "{eval_output_path}",
        "--color",
        "never",
        "--sandbox",
        "read-only",
        "-C",
        "{repo_root}",
        "-",
    ]
    args = normalize_args(raw_args)
    mapping = {
        "{eval_prompt_path}": str(eval_prompt_path),
        "{eval_input_path}": str(eval_input_path),
        "{eval_schema_path}": str(eval_schema_path),
        "{eval_output_path}": str(eval_output_path),
        "{run_dir}": str(run_dir),
        "{repo_root}": str(repo_root),
        "{check_id}": check_id,
    }
    args = substitute_args(args, mapping)
    timeout = int(config.get("timeout_seconds") or 600)
    return [cmd] + args, timeout


def extract_json_blob(text: str) -> str | None:
    stripped = text.strip()
    if stripped.startswith("{") and stripped.endswith("}"):
        return stripped
    start = stripped.find("{")
    end = stripped.rfind("}")
    if start != -1 and end != -1 and end > start:
        return stripped[start : end + 1]
    return None


def valid_llm_result(result: dict) -> bool:
    if not isinstance(result, dict):
        return False
    if result.get("status") not in VALID_STATUSES:
        return False
    if "rationale" not in result or "confidence" not in result:
        return False
    if not isinstance(result.get("evidence_quotes"), list):
        return False
    if not isinstance(result.get("recommendations"), list):
        return False
    return True


def fallback_result(reason: str) -> dict:
    return {
        "status": "WARN",
        "rationale": reason,
        "evidence_quotes": [],
        "recommendations": ["Re-run the evaluator with json_fix prompt."],
        "confidence": 0.0,
    }


def run_eval_command(
    cmd: list[str], cwd: Path, env: dict, timeout: int, input_text: str | None = None
) -> tuple[int | None, str]:
    try:
        result = subprocess.run(
            cmd,
            cwd=str(cwd),
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            input=input_text,
            timeout=timeout,
        )
    except FileNotFoundError as exc:
        return None, f"Command not found: {exc}\n"
    except subprocess.TimeoutExpired:
        return None, f"Command timed out after {timeout} seconds.\n"
    return result.returncode, result.stdout or ""


def build_stdin_prompt(prompt_path: Path, input_path: Path) -> str:
    prompt_text = prompt_path.read_text(encoding="utf-8").rstrip()
    input_text = input_path.read_text(encoding="utf-8").strip()
    return f"{prompt_text}\n\nInput JSON:\n{input_text}\n"


def prepare_codex_env(repo_root: Path, env: dict) -> dict:
    codex_home = repo_root / ".codex-home"
    cache_root = codex_home / ".cache" / "codex"
    cache_root.mkdir(parents=True, exist_ok=True)
    env = dict(env)
    env["HOME"] = str(codex_home)
    env.setdefault("XDG_CACHE_HOME", str(codex_home / ".cache"))
    env.setdefault("CODEX_NO_UPDATE", "1")
    return env


def parse_llm_output(raw: str) -> dict | None:
    candidate = raw.strip()
    for text in [candidate, extract_json_blob(candidate)]:
        if not text:
            continue
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            continue
        if valid_llm_result(parsed):
            return parsed
    return None


def render_json_fix_prompt(prompt_text: str, raw_output: str) -> str:
    return prompt_text.replace("{{RAW_OUTPUT}}", raw_output)


def build_eval_input(run_dir: Path, check_id: str) -> dict:
    evidence_path = run_dir / "evidence.json"
    evidence = load_json(evidence_path) if evidence_path.exists() else {}
    agentic_summary_path = run_dir / "agentic_summary.json"
    agentic_summary = load_json(agentic_summary_path) if agentic_summary_path.exists() else None
    execution_summary_path = run_dir / "execution_summary.json"
    execution_summary = (
        load_json(execution_summary_path) if execution_summary_path.exists() else None
    )

    return {
        "check_id": check_id,
        "prompt": (evidence.get("prompt_json") or {}).get("content") or {},
        "evidence": evidence,
        "git_diff": evidence.get("git_diff", ""),
        "execution_summary": execution_summary,
        "agentic_summary": agentic_summary,
    }


def run_single_eval(
    run_dir: Path,
    repo_root: Path,
    check_id: str,
    prompt_path: Path,
    config: dict[str, Any],
    prompts_dir: Path,
) -> dict:
    logs_dir = run_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    input_payload = build_eval_input(run_dir, check_id)
    eval_input_path = run_dir / f"llm_input_{check_id}.json"
    eval_input_path.write_text(json.dumps(input_payload, indent=2), encoding="utf-8")

    eval_schema_path = prompts_dir / "llm_eval_schema.json"
    eval_output_path = run_dir / f"llm_output_{check_id}.json"

    cmd, timeout = build_command(
        config,
        prompt_path,
        eval_input_path,
        eval_schema_path,
        eval_output_path,
        repo_root,
        run_dir,
        check_id,
    )
    env = prepare_codex_env(repo_root, os.environ.copy())
    input_text = build_stdin_prompt(prompt_path, eval_input_path) if "-" in cmd else None
    exit_code, output = run_eval_command(cmd, repo_root, env, timeout, input_text=input_text)
    log_path = logs_dir / f"llm_eval_{check_id}.log"
    log_path.write_text(output, encoding="utf-8")

    output_text = (
        eval_output_path.read_text(encoding="utf-8") if eval_output_path.exists() else output
    )
    parsed = parse_llm_output(output_text)
    if parsed:
        return parsed

    json_fix_path = prompts_dir / "json_fix.md"
    json_fix_prompt = json_fix_path.read_text(encoding="utf-8") if json_fix_path.exists() else ""
    if not json_fix_prompt:
        return fallback_result(
            "LLM evaluator returned invalid JSON and json_fix prompt is missing."
        )

    fix_prompt_path = run_dir / f"json_fix_{check_id}.md"
    fix_prompt_path.write_text(render_json_fix_prompt(json_fix_prompt, output), encoding="utf-8")
    fix_input_path = run_dir / f"json_fix_input_{check_id}.json"
    fix_input_path.write_text(json.dumps({"raw_output": output}, indent=2), encoding="utf-8")

    fix_output_path = run_dir / f"llm_output_{check_id}_fix.json"
    cmd, timeout = build_command(
        config,
        fix_prompt_path,
        fix_input_path,
        eval_schema_path,
        fix_output_path,
        repo_root,
        run_dir,
        check_id,
    )
    fix_input_text = build_stdin_prompt(fix_prompt_path, fix_input_path) if "-" in cmd else None
    exit_code, fix_output = run_eval_command(
        cmd, repo_root, env, timeout, input_text=fix_input_text
    )
    log_path = logs_dir / f"llm_eval_{check_id}_fix.log"
    log_path.write_text(fix_output, encoding="utf-8")

    fix_output_text = (
        fix_output_path.read_text(encoding="utf-8") if fix_output_path.exists() else fix_output
    )
    parsed = parse_llm_output(fix_output_text)
    if parsed:
        return parsed

    return fallback_result("LLM evaluator returned invalid JSON after json_fix.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run automatic LLM evaluations via Codex CLI.")
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
    run_dir.mkdir(parents=True, exist_ok=True)
    repo_root = Path.cwd()

    prompt_path = run_dir / "prompt.json"
    prompt_config = load_json(prompt_path) if prompt_path.exists() else {}
    raw_llm_config = prompt_config.get("llm_eval")
    llm_config: dict[str, Any] = raw_llm_config if isinstance(raw_llm_config, dict) else {}

    checks_data = load_json(Path(args.checks))
    prompts_dir = Path(__file__).resolve().parents[1] / "references"

    results = {}
    for check in sort_checks_by_priority(checks_data.get("checks", [])):
        if not check.get("enabled_by_default"):
            continue
        if check.get("type") != "LLM":
            continue
        check_id = check.get("id")
        prompt_id = check.get("evaluator_prompt_id")
        if not prompt_id:
            continue
        prompt_file = prompts_dir / f"{prompt_id}.md"
        if not prompt_file.exists():
            results[check_id] = fallback_result(f"Evaluator prompt missing: {prompt_file}")
            continue
        results[check_id] = run_single_eval(
            run_dir, repo_root, check_id, prompt_file, llm_config, prompts_dir
        )

    llm_path = run_dir / "llm_results.json"
    write_json(llm_path, results)
    print(str(llm_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
