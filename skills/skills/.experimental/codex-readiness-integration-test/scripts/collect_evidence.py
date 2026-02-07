#!/usr/bin/env python3
import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

SKIP_DIRS = {
    ".git",
    ".codex-readiness-integration-test",
    "node_modules",
    "dist",
    "build",
    ".venv",
    "venv",
    "__pycache__",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        try:
            return path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return ""


def extract_snippet(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 3] + "..."


def run_cmd(cmd: list[str]) -> str:
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
        return output.strip()
    except Exception as exc:
        return f"<error> {exc}"


def run_cmd_allow_failure(cmd: list[str]) -> str:
    try:
        result = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=False
        )
        return result.stdout.strip()
    except Exception as exc:
        return f"<error> {exc}"


def should_include_untracked(path: Path) -> bool:
    if path.name == ".DS_Store":
        return False
    return all(not part.startswith(".codex") for part in path.parts)


def build_untracked_diff() -> str:
    raw = run_cmd(["git", "ls-files", "--others", "--exclude-standard"])
    if raw.startswith("<error>"):
        return ""
    diffs = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        path = Path(line)
        if not should_include_untracked(path):
            continue
        diff = run_cmd_allow_failure(["git", "diff", "--no-index", "/dev/null", line])
        if diff and not diff.startswith("<error>"):
            diffs.append(diff)
    return "\n".join(diffs)


def load_json_if_exists(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def resolve_run_dir(base_dir: Path, run_dir_arg: str | None) -> Path:
    if run_dir_arg:
        return Path(run_dir_arg).resolve()
    latest_path = base_dir / "latest.json"
    if latest_path.exists():
        try:
            latest = json.loads(latest_path.read_text(encoding="utf-8"))
            run_dir = latest.get("run_dir")
            if run_dir:
                return Path(run_dir)
        except Exception:
            pass
    if (base_dir / "prompt.json").exists():
        return base_dir.resolve()
    return base_dir.resolve()


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect evidence for integration test.")
    parser.add_argument(
        "--out-dir", default=".codex-readiness-integration-test", help="Base output directory"
    )
    parser.add_argument("--run-dir", default=None, help="Specific run directory to use")
    parser.add_argument("--max-snippet-chars", type=int, default=2000)
    args = parser.parse_args()

    cwd = Path.cwd()
    base_dir = Path(args.out_dir)
    run_dir = resolve_run_dir(base_dir, args.run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)

    agents_path = cwd / "AGENTS.md"
    agents_text = read_text(agents_path) if agents_path.exists() else ""

    prompt_path = run_dir / "prompt.json"
    plan_path = run_dir / "plan.json"
    execution_summary_path = run_dir / "execution_summary.json"
    agentic_summary_path = run_dir / "agentic_summary.json"
    agentic_log_path = run_dir / "logs" / "agentic.log"

    logs_dir = run_dir / "logs"
    logs_index = [str(path) for path in sorted(logs_dir.glob("*.log"))] if logs_dir.exists() else []

    tracked_diff = run_cmd(["git", "diff"])
    untracked_diff = build_untracked_diff()
    if untracked_diff:
        if tracked_diff:
            combined_diff = f"{tracked_diff}\n{untracked_diff}"
        else:
            combined_diff = untracked_diff
    else:
        combined_diff = tracked_diff

    evidence = {
        "timestamp": now_iso(),
        "repo_root": str(cwd),
        "agents_md": {
            "path": str(agents_path),
            "exists": agents_path.exists(),
            "snippet": extract_snippet(agents_text, args.max_snippet_chars),
        },
        "prompt_json": {
            "path": str(prompt_path),
            "exists": prompt_path.exists(),
            "content": load_json_if_exists(prompt_path),
        },
        "plan_json": {
            "path": str(plan_path),
            "exists": plan_path.exists(),
            "content": load_json_if_exists(plan_path),
        },
        "execution_summary": {
            "path": str(execution_summary_path),
            "exists": execution_summary_path.exists(),
            "content": load_json_if_exists(execution_summary_path),
        },
        "agentic_summary": {
            "path": str(agentic_summary_path),
            "exists": agentic_summary_path.exists(),
            "content": load_json_if_exists(agentic_summary_path),
        },
        "agentic_log": {
            "path": str(agentic_log_path),
            "exists": agentic_log_path.exists(),
            "snippet": extract_snippet(read_text(agentic_log_path), args.max_snippet_chars)
            if agentic_log_path.exists()
            else "",
        },
        "logs_index": logs_index,
        "git_status": run_cmd(["git", "status", "--porcelain"]),
        "git_diff": combined_diff,
    }

    output_path = run_dir / "evidence.json"
    output_path.write_text(json.dumps(evidence, indent=2), encoding="utf-8")
    print(str(output_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
