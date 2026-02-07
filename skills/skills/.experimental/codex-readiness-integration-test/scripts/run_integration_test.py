#!/usr/bin/env python3
import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SCORING_FOCUS_DEFAULT = [
    "correctness",
    "context_usage",
    "builds_tests_pass",
    "maintainability",
    "risk",
]

VALID_STATUSES = {"PASS", "WARN", "FAIL", "NOT_RUN"}
SKILL_REF_PATTERN = re.compile(r"\$([A-Za-z0-9_.-]+)")
SKILL_PATH_PATTERN = re.compile(
    r"(?:\.codex/skills|~/.codex/skills|/\.codex/skills|skills)/([A-Za-z0-9_.-]+)"
)
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


def now_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def resolve_run_dir(base_dir: Path, run_dir_arg: str | None) -> Path:
    if run_dir_arg:
        return Path(run_dir_arg).resolve()
    return base_dir / now_stamp()


def ensure_prompt_template(prompt_path: Path, seed_task: str | None) -> Path:
    if prompt_path.exists():
        return prompt_path
    prompt = {
        "seed_task": seed_task,
        "prompt_origin": "manual",
        "change_prompt": "",
        "acceptance_criteria": [],
        "build_test_plan": [],
        "scoring_focus": SCORING_FOCUS_DEFAULT,
        "approved": False,
        "generated_at": now_iso(),
    }
    write_json(prompt_path, prompt)
    return prompt_path


def approve_prompt(prompt_path: Path) -> dict:
    prompt = load_json(prompt_path)
    prompt["approved"] = True
    prompt["approved_at"] = now_iso()
    write_json(prompt_path, prompt)
    return prompt


def prompt_ready(prompt: dict) -> tuple[bool, str]:
    if not prompt.get("change_prompt"):
        return False, "change_prompt is empty"
    plan = prompt.get("build_test_plan")
    if not isinstance(plan, list) or not plan:
        return False, "build_test_plan is missing or empty"
    return True, "ready"


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        try:
            return path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return ""


def extract_candidate_commands(text: str) -> list[str]:
    commands = []
    in_code_block = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            if stripped and not stripped.startswith("#"):
                commands.append(stripped)
            continue
        inline = re.findall(r"`([^`]+)`", line)
        for cmd in inline:
            cmd_str = cmd.strip()
            if cmd_str:
                commands.append(cmd_str)
        if stripped.startswith("$"):
            cmd = stripped.lstrip("$ ")
            if cmd:
                commands.append(cmd)
    normalized = []
    seen = set()
    for cmd in commands:
        cleaned = cmd.strip()
        if not cleaned or cleaned in seen:
            continue
        seen.add(cleaned)
        normalized.append(cleaned)
    return normalized


def extract_skill_refs(text: str) -> list[str]:
    refs = set(SKILL_REF_PATTERN.findall(text))
    refs.update(SKILL_PATH_PATTERN.findall(text))
    return sorted(refs)


def resolve_skills_roots(repo_root: Path) -> list[Path]:
    candidates = []
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        candidates.append(Path(codex_home) / "skills")
    candidates.append(repo_root / ".codex" / "skills")
    candidates.append(Path.home() / ".codex" / "skills")

    roots = []
    seen = set()
    for candidate in candidates:
        try:
            resolved = candidate.expanduser().resolve()
        except Exception:
            resolved = candidate.expanduser()
        key = str(resolved)
        if key in seen:
            continue
        seen.add(key)
        if resolved.exists():
            roots.append(resolved)
    return roots


def classify_command(cmd: str) -> str | None:
    lower = cmd.lower()
    if any(keyword in lower for keyword in TEST_KEYWORDS):
        return "test"
    if any(keyword in lower for keyword in BUILD_KEYWORDS):
        return "build"
    return None


def infer_build_test_plan(repo_root: Path) -> list[dict]:
    agents_path = repo_root / "AGENTS.md"
    candidate_commands: list[str] = []
    skill_refs: list[str] = []
    if agents_path.exists():
        agents_text = read_text(agents_path)
        if agents_text:
            candidate_commands.extend(extract_candidate_commands(agents_text))
            skill_refs = extract_skill_refs(agents_text)

    if skill_refs:
        skills_roots = resolve_skills_roots(repo_root)
        for skill_name in skill_refs:
            for root in skills_roots:
                skill_path = root / skill_name / "SKILL.md"
                if skill_path.exists():
                    skill_text = read_text(skill_path)
                    if skill_text:
                        candidate_commands.extend(extract_candidate_commands(skill_text))
                    break

    seen = set()
    unique_cmds = []
    for cmd in candidate_commands:
        if cmd in seen:
            continue
        seen.add(cmd)
        unique_cmds.append(cmd)

    build_cmd = None
    test_cmd = None
    for cmd in unique_cmds:
        label = classify_command(cmd)
        if label == "build" and build_cmd is None:
            build_cmd = cmd
        elif label == "test" and test_cmd is None:
            test_cmd = cmd
        if build_cmd and test_cmd:
            break

    plan: list[dict] = []
    if build_cmd:
        plan.append({"label": "build", "cmd": build_cmd})
    if test_cmd:
        plan.append({"label": "test", "cmd": test_cmd})
    return plan


def write_plan_json(run_dir: Path, prompt: dict, cwd: Path) -> Path:
    plan = {
        "cwd": str(cwd),
        "commands": prompt.get("build_test_plan", []),
    }
    plan_path = run_dir / "plan.json"
    write_json(plan_path, plan)
    return plan_path


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


def prepare_codex_home(repo_root: Path) -> Path:
    codex_home = repo_root / ".codex-home"
    cache_root = codex_home / ".cache"
    codex_home.mkdir(parents=True, exist_ok=True)
    cache_root.mkdir(parents=True, exist_ok=True)
    (cache_root / "codex").mkdir(parents=True, exist_ok=True)
    return codex_home


def prompt_for_json(label: str, prompt_text: str, json_fix_text: str) -> dict | None:
    attempts = 0
    while attempts < 3:
        print(f"\n=== {label} ===")
        print(prompt_text.rstrip())
        print("\nPaste JSON result. End with a line containing only END.")
        lines = []
        while True:
            try:
                line = input()
            except EOFError:
                return None
            if line.strip() == "END":
                break
            lines.append(line)
        raw = "\n".join(lines).strip()
        if not raw:
            print("No input received.")
        else:
            try:
                data = json.loads(raw)
            except json.JSONDecodeError as exc:
                print(f"Invalid JSON: {exc}")
                if json_fix_text:
                    print("\n" + json_fix_text.rstrip() + "\n")
            else:
                if valid_llm_result(data):
                    return data
                print("JSON missing required keys or invalid types.")
        attempts += 1
        print("Please retry. End with a line containing only END.")
    return None


def run_llm_evals_manual(run_dir: Path) -> int:
    llm_path = run_dir / "llm_results.json"
    if llm_path.exists():
        return 0
    if not sys.stdin.isatty():
        print("LLM eval skipped: stdin is not a TTY and llm_results.json is missing.")
        return 2

    prompts_dir = Path(__file__).resolve().parents[1] / "references"
    json_fix_path = prompts_dir / "json_fix.md"
    json_fix_text = json_fix_path.read_text(encoding="utf-8") if json_fix_path.exists() else ""

    print("LLM evaluation required. Use evidence and execution summary for context.")
    print(f"Evidence: {run_dir / 'evidence.json'}")
    print(f"Execution summary: {run_dir / 'execution_summary.json'}")

    results = {}
    evals = [
        ("agentic_loop_eval", prompts_dir / "agentic_loop_eval.md"),
        ("change_quality_eval", prompts_dir / "change_quality.md"),
    ]

    for check_id, prompt_path in evals:
        prompt_text = prompt_path.read_text(encoding="utf-8")
        result = prompt_for_json(check_id, prompt_text, json_fix_text)
        if result is None:
            print(f"LLM eval for {check_id} not completed.")
            return 2
        results[check_id] = result

    llm_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    return 0


def run_llm_evals_auto(run_dir: Path, base_dir: Path) -> int:
    llm_path = run_dir / "llm_results.json"
    if llm_path.exists():
        return 0
    cmd = [
        sys.executable,
        str(Path(__file__).resolve().parent / "run_llm_eval.py"),
        "--out-dir",
        str(base_dir),
        "--run-dir",
        str(run_dir),
    ]
    return run_step(cmd)


def run_llm_evals(run_dir: Path, base_dir: Path, manual: bool) -> int:
    if manual:
        return run_llm_evals_manual(run_dir)
    return run_llm_evals_auto(run_dir, base_dir)


def run_step(cmd: list[str]) -> int:
    result = subprocess.run(cmd, text=True)
    return result.returncode


def print_prompt_options(prompt_path: Path) -> None:
    print("\nChoose one of the following options to create the prompt:")
    print("1) Let Codex generate it: use references/generate_prompt.md and save JSON to:")
    print(f"   {prompt_path}")
    print("2) Write it yourself: fill in change_prompt and build_test_plan in:")
    print(f"   {prompt_path}")


def archive_prompt(base_dir: Path, run_dir: Path, prompt: dict) -> Path:
    archive_dir = base_dir / "prompts"
    archive_dir.mkdir(parents=True, exist_ok=True)
    archive_path = archive_dir / f"{run_dir.name}.json"
    write_json(archive_path, prompt)
    return archive_path


def format_prompt_summary(prompt: dict) -> str:
    lines: list[str] = ["Prompt summary", ""]
    origin = prompt.get("prompt_origin") or "unknown"
    seed_task = prompt.get("seed_task")
    change_prompt = str(prompt.get("change_prompt") or "").strip()
    acceptance_criteria = prompt.get("acceptance_criteria") or []
    build_test_plan = prompt.get("build_test_plan") or []
    scoring_focus = prompt.get("scoring_focus") or []

    lines.append(f"origin: {origin}")
    if seed_task is None:
        lines.append("seed_task: none")
    else:
        lines.append(f"seed_task: {seed_task}")
    lines.append("")
    lines.append("change_prompt:")
    if change_prompt:
        lines.append(change_prompt)
    else:
        lines.append("(missing)")
    lines.append("")
    lines.append("acceptance_criteria:")
    if acceptance_criteria:
        for item in acceptance_criteria:
            lines.append(f"- {item}")
    else:
        lines.append("- (none)")
    lines.append("")
    lines.append("build_test_plan:")
    if build_test_plan:
        for step in build_test_plan:
            if isinstance(step, str):
                label = "step"
                cmd = step
            elif isinstance(step, dict):
                label = step.get("label") or "step"
                cmd = step.get("cmd") or ""
            else:
                label = "step"
                cmd = ""
            if cmd:
                lines.append(f"- {label}: {cmd}")
            else:
                lines.append(f"- {label}")
    else:
        lines.append("- (none)")
    lines.append("")
    lines.append("scoring_focus:")
    if scoring_focus:
        for item in scoring_focus:
            lines.append(f"- {item}")
    else:
        lines.append("- (none)")
    return "\n".join(lines) + "\n"


def ensure_prompt_origin(prompt: dict, seed_task: str | None) -> None:
    if "prompt_origin" in prompt:
        return
    if seed_task:
        prompt["prompt_origin"] = "auto"
    else:
        prompt["prompt_origin"] = "manual"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the codex-readiness-integration-test.")
    parser.add_argument(
        "--out-dir", default=".codex-readiness-integration-test", help="Base output directory"
    )
    parser.add_argument("--run-dir", default=None, help="Specific run directory to use")
    parser.add_argument("--seed-task", default=None, help="Optional seed task")
    parser.add_argument(
        "--approve-prompt", action="store_true", help="Mark prompt.json as approved and continue"
    )
    parser.add_argument(
        "--skip-agentic-loop", action="store_true", help="Skip the agentic loop execution"
    )
    parser.add_argument(
        "--skip-llm-eval", action="store_true", help="Skip in-session LLM evaluation prompts"
    )
    parser.add_argument(
        "--manual-llm-eval", action="store_true", help="Prompt for manual LLM evaluation input"
    )
    args = parser.parse_args()

    base_dir = Path(args.out_dir)
    base_dir.mkdir(parents=True, exist_ok=True)
    repo_root = Path.cwd()
    codex_home = prepare_codex_home(repo_root)
    print(f"Initialized Codex home at {codex_home}.")
    cache_home = codex_home / ".cache"
    print(f"Using repo-local Codex home at {codex_home}.")
    print("If you have not authenticated with Codex for this repo, run:")
    print(f"  HOME={codex_home} XDG_CACHE_HOME={cache_home} codex login")
    print(f"  HOME={codex_home} XDG_CACHE_HOME={cache_home} codex login status")
    prompt_path = ensure_prompt_template(base_dir / "prompt.pending.json", args.seed_task)
    prompt = load_json(prompt_path)

    ensure_prompt_origin(prompt, args.seed_task)

    if args.approve_prompt:
        prompt = approve_prompt(prompt_path)

    if not prompt.get("build_test_plan"):
        inferred_plan = infer_build_test_plan(repo_root)
        if inferred_plan:
            prompt["build_test_plan"] = inferred_plan
            write_json(prompt_path, prompt)

    ready, reason = prompt_ready(prompt)
    if not ready:
        print(f"Prompt not ready: {reason}")
        if args.seed_task:
            print(
                "A seed task was provided, but prompt.json still needs a change_prompt and build_test_plan."
            )
        else:
            print("No seed task provided. Generate a prompt using references/generate_prompt.md.")
        print_prompt_options(prompt_path)
        print(f"\nEdit {prompt_path} and re-run with --approve-prompt.")
        return 2

    if not prompt.get("approved"):
        print(f"Prompt not approved. Review {prompt_path} and re-run with --approve-prompt.")
        return 2

    run_dir = resolve_run_dir(base_dir, args.run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)

    latest_path = base_dir / "latest.json"
    write_json(latest_path, {"run_dir": str(run_dir)})

    prompt_run_path = run_dir / "prompt.json"
    write_json(prompt_run_path, prompt)
    archive_prompt(base_dir, run_dir, prompt)
    print("\n" + format_prompt_summary(prompt).rstrip() + "\n")

    plan_path = write_plan_json(run_dir, prompt, Path.cwd())

    if not args.skip_agentic_loop:
        agentic_cmd = [
            sys.executable,
            str(Path(__file__).resolve().parent / "run_agentic_loop.py"),
            "--out-dir",
            str(base_dir),
            "--run-dir",
            str(run_dir),
        ]
        agentic_status = run_step(agentic_cmd)
        if agentic_status != 0:
            print(f"Agentic loop exited with code {agentic_status}.")
            return agentic_status

        agentic_summary_path = run_dir / "agentic_summary.json"
        if agentic_summary_path.exists():
            agentic_summary = load_json(agentic_summary_path)
            if agentic_summary.get("requires_escalation"):
                print(
                    "Agentic loop indicates sandbox-blocked access. "
                    "Re-run the integration test with escalated permissions."
                )
                return 3

    run_plan_cmd = [
        sys.executable,
        str(Path(__file__).resolve().parent / "run_plan.py"),
        "--plan",
        str(plan_path),
        "--out-dir",
        str(base_dir),
        "--run-dir",
        str(run_dir),
    ]
    run_step(run_plan_cmd)

    run_step(
        [
            sys.executable,
            str(Path(__file__).resolve().parent / "collect_evidence.py"),
            "--out-dir",
            str(base_dir),
            "--run-dir",
            str(run_dir),
        ]
    )

    run_step(
        [
            sys.executable,
            str(Path(__file__).resolve().parent / "deterministic_rules.py"),
            "--out-dir",
            str(base_dir),
            "--run-dir",
            str(run_dir),
        ]
    )

    if not args.skip_llm_eval:
        llm_status = run_llm_evals(run_dir, base_dir, args.manual_llm_eval)
        if llm_status != 0:
            return llm_status

    run_step(
        [
            sys.executable,
            str(Path(__file__).resolve().parent / "scoring.py"),
            "--out-dir",
            str(base_dir),
            "--run-dir",
            str(run_dir),
        ]
    )

    print(f"Run complete: {run_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
