#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STATE_SCHEMA_VERSION = 2
DEFAULT_WORK_SOURCES = [
    "local_tests",
    "ci_failures",
    "runtime_failures",
    "todo_fixme",
    "docs_handoff_gaps",
    "github_issues",
    "github_pr_reviews",
    "github_discussions",
]
DEFAULT_PRIORITY_BUCKETS = {
    "ci_failure": 1,
    "runtime_failure": 1,
    "verification_failure": 1,
    "github_pr_review": 2,
    "github_issue": 2,
    "github_discussion": 2,
    "carryover": 3,
    "plan_decomposition": 3,
    "todo_fixme": 4,
    "docs_handoff_gap": 4,
    "cleanup": 5,
}
PERSISTENT_PENDING_SOURCES = {
    "carryover",
    "plan_decomposition",
    "runtime_failure",
    "verification_failure",
}
DEFAULT_STOP_REASONS = {
    "needs_user_decision",
    "external_blocker",
    "risk_budget_exceeded",
    "no_safe_work",
    "mission_complete",
}
SKIP_DIR_NAMES = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "node_modules",
    "dist",
    "build",
    "generated",
    ".next",
    ".turbo",
    "__pycache__",
    ".operator",
}
TEXT_SIGNAL_EXTENSIONS = {".md", ".mdx", ".txt", ".rst", ".adoc"}
COMMENT_TOKENS = {
    ".c": ("//", "/*", "*"),
    ".cc": ("//", "/*", "*"),
    ".cpp": ("//", "/*", "*"),
    ".cs": ("//", "/*", "*"),
    ".go": ("//", "/*", "*"),
    ".java": ("//", "/*", "*"),
    ".js": ("//", "/*", "*"),
    ".jsx": ("//", "/*", "*"),
    ".kt": ("//", "/*", "*"),
    ".lua": ("--",),
    ".py": ("#",),
    ".rb": ("#",),
    ".rs": ("//", "/*", "*"),
    ".sh": ("#",),
    ".sql": ("--",),
    ".swift": ("//", "/*", "*"),
    ".ts": ("//", "/*", "*"),
    ".tsx": ("//", "/*", "*"),
    ".yaml": ("#",),
    ".yml": ("#",),
}
ACTIONABLE_TODO_PATTERN = re.compile(r"^(TODO|FIXME|HACK|XXX)\b(?::|\s+)", re.IGNORECASE)
ACTIONABLE_HANDOFF_PATTERN = re.compile(
    r"^(next step|next steps|follow[- ]up|known blocker|known blockers|remaining work)\b",
    re.IGNORECASE,
)


@dataclass
class SignalItem:
    source: str
    title: str
    evidence: list[str]
    impact: str
    effort: str
    risk: str
    next_action: str
    fingerprint: str


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "item"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        return {}, text

    match = re.match(r"^---\n(.*?)\n---\n?", text, re.DOTALL)
    if not match:
        return {}, text

    data: dict[str, Any] = {}
    current_key: str | None = None
    for raw_line in match.group(1).splitlines():
        if raw_line.startswith("  - ") and current_key:
            data.setdefault(current_key, [])
            data[current_key].append(raw_line[4:].strip())
            continue
        if ":" not in raw_line:
            current_key = None
            continue
        key, value = raw_line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"')
        if value == "":
            data[key] = []
        else:
            data[key] = value
        current_key = key

    return data, text[match.end() :]


def render_mission(repo_name: str, goal: str, github_repo: str | None) -> str:
    github_line = github_repo or "unknown"
    return (
        "---\n"
        f"title: Improve {repo_name}\n"
        f"goal: {goal}\n"
        "autonomy_mode: aggressive_in_scope\n"
        "continuity: cross_thread_cross_day\n"
        "publish_mode: checkpoint_commit\n"
        "risk_budget: medium\n"
        f"github_repo: {github_line}\n"
        "work_sources:\n"
        "  - local_tests\n"
        "  - ci_failures\n"
        "  - runtime_failures\n"
        "  - todo_fixme\n"
        "  - docs_handoff_gaps\n"
        "  - github_issues\n"
        "  - github_pr_reviews\n"
        "  - github_discussions\n"
        "stop_reasons:\n"
        "  - needs_user_decision\n"
        "  - external_blocker\n"
        "  - risk_budget_exceeded\n"
        "  - no_safe_work\n"
        "  - mission_complete\n"
        "---\n\n"
        "# Mission\n\n"
        "## In Scope\n\n"
        "- Repository code, tests, docs, CI, and backlog items directly related to the current project.\n"
        "- Follow-up work discovered through repo signals or GitHub signals.\n\n"
        "## Out Of Scope\n\n"
        "- New product lines or marketing tracks not implied by the current repository.\n"
        "- Large irreversible architecture shifts without evidence.\n\n"
        "## Success Signals\n\n"
        "- The current mission is moving through verified checkpoints.\n"
        "- `next_action` always points at the next safe, high-leverage task.\n"
    )


def run_command(args: list[str], cwd: Path | None = None) -> tuple[int, str, str]:
    result = subprocess.run(
        args,
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode, result.stdout, result.stderr


def infer_goal(repo_path: Path) -> str:
    readme = repo_path / "README.md"
    if not readme.exists():
        return f"Improve {repo_path.name} through verified high-leverage iterations."

    text = read_text(readme)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for line in lines:
        if line.startswith("#"):
            continue
        return line
    return f"Improve {repo_path.name} through verified high-leverage iterations."


def infer_github_repo(repo_path: Path) -> str | None:
    code, stdout, _ = run_command(["git", "-C", str(repo_path), "remote", "get-url", "origin"])
    if code != 0:
        return None

    remote = stdout.strip()
    https_match = re.search(r"github\.com[:/](?P<owner>[^/]+)/(?P<repo>[^/.]+)(?:\.git)?$", remote)
    if not https_match:
        return None
    return f"{https_match.group('owner')}/{https_match.group('repo')}"


def operator_paths(repo_path: Path) -> dict[str, Path]:
    root = repo_path / ".operator"
    return {
        "root": root,
        "mission": root / "mission.md",
        "backlog": root / "backlog.json",
        "state": root / "state.json",
        "checkpoints": root / "checkpoints",
    }


def default_state(github_repo: str | None = None) -> dict[str, Any]:
    return {
        "schema_version": STATE_SCHEMA_VERSION,
        "status": "active",
        "current_item_id": None,
        "next_action": "Run scan, choose the next item, and continue executing.",
        "last_scan_at": None,
        "last_checkpoint_at": None,
        "last_stop_reason": None,
        "last_completed_item_id": None,
        "verification": {
            "status": "unknown",
            "summary": None,
            "updated_at": None,
        },
        "github_repo": github_repo,
        "publish_mode": "checkpoint_commit",
    }


def bootstrap_state(repo_path: Path, goal: str | None = None, github_repo: str | None = None) -> dict[str, Any]:
    paths = operator_paths(repo_path)
    paths["checkpoints"].mkdir(parents=True, exist_ok=True)
    github_repo = github_repo or infer_github_repo(repo_path)
    if not paths["mission"].exists():
        mission_goal = goal or infer_goal(repo_path)
        write_text(paths["mission"], render_mission(repo_path.name, mission_goal, github_repo))
    if not paths["backlog"].exists():
        write_json(paths["backlog"], {"schema_version": STATE_SCHEMA_VERSION, "items": []})
    if not paths["state"].exists():
        write_json(paths["state"], default_state(github_repo))
    return load_state(repo_path)


def load_mission(repo_path: Path) -> dict[str, Any]:
    mission_path = operator_paths(repo_path)["mission"]
    if not mission_path.exists():
        bootstrap_state(repo_path)
    frontmatter, body = parse_frontmatter(read_text(mission_path))
    frontmatter["body"] = body.strip()
    return frontmatter


def load_state(repo_path: Path) -> dict[str, Any]:
    return read_json(operator_paths(repo_path)["state"], default_state())


def load_backlog(repo_path: Path) -> dict[str, Any]:
    return read_json(operator_paths(repo_path)["backlog"], {"schema_version": STATE_SCHEMA_VERSION, "items": []})


def signal_to_item(signal: SignalItem) -> dict[str, Any]:
    bucket = DEFAULT_PRIORITY_BUCKETS.get(signal.source, 5)
    digest = hashlib.sha1(f"{signal.source}:{signal.fingerprint}".encode("utf-8")).hexdigest()[:10]
    return {
        "id": f"{slugify(signal.source)}-{digest}",
        "title": signal.title,
        "source": signal.source,
        "evidence": signal.evidence,
        "impact": signal.impact,
        "effort": signal.effort,
        "risk": signal.risk,
        "priority_bucket": bucket,
        "status": "pending",
        "next_action": signal.next_action,
        "updated_at": utc_now(),
    }


def existing_item_map(items: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {item["id"]: item for item in items}


def merge_items(existing: list[dict[str, Any]], incoming: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged = existing_item_map(existing)
    for item in incoming:
        current = merged.get(item["id"])
        if current and current.get("status") == "completed":
            continue
        if current:
            current.update(item)
            current.setdefault("status", "pending")
        else:
            merged[item["id"]] = item
    items = list(merged.values())
    items.sort(key=lambda item: (item["priority_bucket"], item["title"]))
    return items


def iter_candidate_files(repo_path: Path) -> list[Path]:
    files: list[Path] = []
    for root, dirs, filenames in os.walk(repo_path):
        dirs[:] = [name for name in dirs if name not in SKIP_DIR_NAMES]
        for filename in filenames:
            path = Path(root) / filename
            if path.is_file():
                files.append(path)
    return files


def strip_doc_prefix(line: str) -> str:
    return re.sub(r"^\s*(?:[#>*-]+|\d+[.)])\s*", "", line).strip()


def extract_comment_text(path: Path, line: str) -> str | None:
    stripped = line.strip()
    tokens = COMMENT_TOKENS.get(path.suffix.lower(), ())
    for token in tokens:
        index = line.find(token)
        if index == -1:
            continue
        prefix = line[:index].strip()
        if prefix:
            continue
        return line[index + len(token) :].strip()
    if path.suffix.lower() in TEXT_SIGNAL_EXTENSIONS:
        return strip_doc_prefix(stripped)
    return None


def actionable_todo_text(path: Path, line: str) -> str | None:
    candidate = extract_comment_text(path, line)
    if candidate and ACTIONABLE_TODO_PATTERN.search(candidate):
        return candidate
    return None


def actionable_handoff_text(path: Path, line: str) -> str | None:
    if path.suffix.lower() not in TEXT_SIGNAL_EXTENSIONS:
        return None
    candidate = strip_doc_prefix(line)
    if candidate and ACTIONABLE_HANDOFF_PATTERN.search(candidate):
        return candidate
    return None


def scan_todo_signals(repo_path: Path) -> list[SignalItem]:
    signals: list[SignalItem] = []
    for path in iter_candidate_files(repo_path):
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf", ".zip"}:
            continue
        try:
            text = read_text(path)
        except UnicodeDecodeError:
            continue
        for index, line in enumerate(text.splitlines(), start=1):
            candidate = actionable_todo_text(path, line)
            if candidate:
                relpath = str(path.relative_to(repo_path))
                fingerprint = f"{relpath}:{index}:{candidate}"
                signals.append(
                    SignalItem(
                        source="todo_fixme",
                        title=f"Resolve TODO in {relpath}:{index}",
                        evidence=[f"{relpath}:{index}: {candidate}"],
                        impact="medium",
                        effort="small",
                        risk="low",
                        next_action=f"Inspect {relpath}:{index} and decide whether to implement, remove, or formalize the follow-up.",
                        fingerprint=fingerprint,
                    )
                )
    return signals


def scan_handoff_signals(repo_path: Path) -> list[SignalItem]:
    signals: list[SignalItem] = []
    for path in iter_candidate_files(repo_path):
        if path.suffix.lower() not in {".md", ".txt"}:
            continue
        try:
            text = read_text(path)
        except UnicodeDecodeError:
            continue
        for index, line in enumerate(text.splitlines(), start=1):
            candidate = actionable_handoff_text(path, line)
            if candidate:
                relpath = str(path.relative_to(repo_path))
                fingerprint = f"{relpath}:{index}:{candidate}"
                signals.append(
                    SignalItem(
                        source="docs_handoff_gap",
                        title=f"Review follow-up note in {relpath}:{index}",
                        evidence=[f"{relpath}:{index}: {candidate}"],
                        impact="medium",
                        effort="small",
                        risk="low",
                        next_action=f"Confirm whether the follow-up in {relpath}:{index} is still true and either execute it or update the doc.",
                        fingerprint=fingerprint,
                    )
                )
    return signals


def command_available(name: str) -> bool:
    return shutil.which(name) is not None


def github_json(repo: str, args: list[str]) -> Any | None:
    if not command_available("gh"):
        return None
    code, stdout, _ = run_command(["gh", *args, "-R", repo])
    if code != 0 or not stdout.strip():
        return None
    return json.loads(stdout)


def scan_github_issue_signals(github_repo: str | None) -> list[SignalItem]:
    if not github_repo:
        return []
    payload = github_json(github_repo, ["issue", "list", "--state", "open", "--limit", "20", "--json", "number,title,url,labels"])
    if not payload:
        return []

    signals: list[SignalItem] = []
    for issue in payload:
        fingerprint = f"issue:{issue['number']}"
        labels = ", ".join(label["name"] for label in issue.get("labels", [])) or "no labels"
        signals.append(
            SignalItem(
                source="github_issue",
                title=f"Resolve GitHub issue #{issue['number']}: {issue['title']}",
                evidence=[issue["url"], f"labels: {labels}"],
                impact="high",
                effort="medium",
                risk="medium",
                next_action=f"Inspect GitHub issue #{issue['number']} and decide whether it should become the next active work item.",
                fingerprint=fingerprint,
            )
        )
    return signals


def scan_github_pr_review_signals(github_repo: str | None) -> list[SignalItem]:
    if not github_repo:
        return []
    payload = github_json(
        github_repo,
        ["pr", "list", "--state", "open", "--limit", "20", "--json", "number,title,url,reviewDecision,isDraft"],
    )
    if not payload:
        return []

    signals: list[SignalItem] = []
    for pr in payload:
        decision = pr.get("reviewDecision") or "UNKNOWN"
        if decision not in {"CHANGES_REQUESTED", "REVIEW_REQUIRED"}:
            continue
        fingerprint = f"pr:{pr['number']}:{decision}"
        signals.append(
            SignalItem(
                source="github_pr_review",
                title=f"Address PR #{pr['number']} review state: {pr['title']}",
                evidence=[pr["url"], f"reviewDecision: {decision}"],
                impact="high",
                effort="medium",
                risk="medium",
                next_action=f"Inspect PR #{pr['number']} and resolve requested review work before lower-priority tasks.",
                fingerprint=fingerprint,
            )
        )
    return signals


def scan_github_run_signals(github_repo: str | None) -> list[SignalItem]:
    if not github_repo:
        return []
    payload = github_json(
        github_repo,
        ["run", "list", "--limit", "20", "--json", "databaseId,workflowName,displayTitle,conclusion,url"],
    )
    if not payload:
        return []

    signals: list[SignalItem] = []
    for run in payload:
        if run.get("conclusion") != "failure":
            continue
        fingerprint = f"run:{run['databaseId']}"
        title = run.get("displayTitle") or run.get("workflowName") or "Failing workflow"
        signals.append(
            SignalItem(
                source="ci_failure",
                title=f"Fix failing CI run: {title}",
                evidence=[run["url"], f"workflow: {run.get('workflowName') or 'unknown'}"],
                impact="high",
                effort="medium",
                risk="medium",
                next_action=f"Inspect the failing run for {title} and turn it into the next active repair task.",
                fingerprint=fingerprint,
            )
        )
    return signals


def scan_github_discussion_signals(github_repo: str | None) -> list[SignalItem]:
    if not github_repo or not command_available("gh"):
        return []
    code, stdout, _ = run_command(["gh", "api", f"repos/{github_repo}/discussions?per_page=10"])
    if code != 0 or not stdout.strip():
        return []
    try:
        payload = json.loads(stdout)
    except json.JSONDecodeError:
        return []

    signals: list[SignalItem] = []
    for discussion in payload:
        fingerprint = f"discussion:{discussion.get('number')}"
        title = discussion.get("title") or "GitHub discussion"
        signals.append(
            SignalItem(
                source="github_discussion",
                title=f"Review actionable discussion #{discussion.get('number')}: {title}",
                evidence=[discussion.get("html_url", ""), f"category: {discussion.get('category', {}).get('name', 'unknown')}"],
                impact="medium",
                effort="medium",
                risk="low",
                next_action=f"Check whether discussion #{discussion.get('number')} implies a concrete backlog item.",
                fingerprint=fingerprint,
            )
        )
    return signals


def carry_over_items(backlog: dict[str, Any]) -> list[dict[str, Any]]:
    items = []
    for item in backlog.get("items", []):
        status = item.get("status")
        source = item.get("source", "carryover")
        keep_pending = status == "pending" and source in PERSISTENT_PENDING_SOURCES
        if status in {"in_progress", "blocked"} or keep_pending:
            item = dict(item)
            item["source"] = source
            item["priority_bucket"] = DEFAULT_PRIORITY_BUCKETS.get(source, item.get("priority_bucket", 5))
            items.append(item)
    return items


def refresh_backlog(repo_path: Path) -> dict[str, Any]:
    bootstrap_state(repo_path)
    mission = load_mission(repo_path)
    state = load_state(repo_path)
    existing_backlog = load_backlog(repo_path)
    github_repo = mission.get("github_repo") or state.get("github_repo") or infer_github_repo(repo_path)

    incoming: list[dict[str, Any]] = carry_over_items(existing_backlog)
    for scanner in (
        scan_todo_signals,
        scan_handoff_signals,
    ):
        incoming.extend(signal_to_item(item) for item in scanner(repo_path))

    for scanner in (
        scan_github_run_signals,
        scan_github_pr_review_signals,
        scan_github_issue_signals,
        scan_github_discussion_signals,
    ):
        incoming.extend(signal_to_item(item) for item in scanner(github_repo))

    completed_items = [item for item in existing_backlog.get("items", []) if item.get("status") == "completed"]
    merged = merge_items(completed_items, incoming)
    payload = {"schema_version": STATE_SCHEMA_VERSION, "items": merged}
    write_json(operator_paths(repo_path)["backlog"], payload)
    state["last_scan_at"] = utc_now()
    state["github_repo"] = github_repo
    write_json(operator_paths(repo_path)["state"], state)
    return payload


def choose_next_item(repo_path: Path) -> dict[str, Any] | None:
    backlog = load_backlog(repo_path)
    state = load_state(repo_path)
    pending = [item for item in backlog.get("items", []) if item.get("status") == "pending"]
    pending.sort(key=lambda item: (item.get("priority_bucket", 99), item.get("title", "")))
    next_item = pending[0] if pending else None
    if next_item:
        next_item["status"] = "in_progress"
        state["current_item_id"] = next_item["id"]
        state["next_action"] = next_item["next_action"]
        state["last_stop_reason"] = None
    else:
        state["current_item_id"] = None
        state["next_action"] = "No safe pending work found. Stop only after recording `no_safe_work` or a more specific stop reason."
        state["last_stop_reason"] = "no_safe_work"
    write_json(operator_paths(repo_path)["backlog"], backlog)
    write_json(operator_paths(repo_path)["state"], state)
    return next_item


def parse_plan_items(plan_text: str) -> list[str]:
    items: list[str] = []
    for raw_line in plan_text.splitlines():
        match = re.match(r"^\s*(?:[-*]|\d+\.)\s+(.*)$", raw_line)
        if match:
            text = match.group(1).strip()
            if text:
                items.append(text)
    return items


def ingest_plan(repo_path: Path, plan_text: str) -> dict[str, Any]:
    backlog = refresh_backlog(repo_path)
    new_items = []
    for line in parse_plan_items(plan_text):
        signal = SignalItem(
            source="plan_decomposition",
            title=line,
            evidence=["decomposed from a broad plan"],
            impact="high",
            effort="medium",
            risk="low",
            next_action=f"Execute the planned step: {line}",
            fingerprint=line,
        )
        new_items.append(signal_to_item(signal))
    payload = {"schema_version": STATE_SCHEMA_VERSION, "items": merge_items(backlog["items"], new_items)}
    write_json(operator_paths(repo_path)["backlog"], payload)
    return payload


def current_branch(repo_path: Path) -> str | None:
    code, stdout, _ = run_command(["git", "-C", str(repo_path), "branch", "--show-current"])
    return stdout.strip() if code == 0 and stdout.strip() else None


def default_branch(repo_path: Path) -> str | None:
    for branch_name in ("main", "master"):
        code, _, _ = run_command(["git", "-C", str(repo_path), "rev-parse", "--verify", branch_name])
        if code == 0:
            return branch_name
    return None


def ensure_checkpoint_branch(repo_path: Path, item: dict[str, Any]) -> None:
    branch = current_branch(repo_path)
    default = default_branch(repo_path)
    if branch and default and branch == default:
        checkpoint_branch = f"codex/checkpoint/{datetime.now().strftime('%Y%m%d-%H%M%S')}-{slugify(item['title'])[:32]}"
        run_command(["git", "-C", str(repo_path), "checkout", "-b", checkpoint_branch])


def maybe_commit_checkpoint(repo_path: Path, item: dict[str, Any]) -> None:
    code, stdout, _ = run_command(["git", "-C", str(repo_path), "status", "--short"])
    if code != 0 or not stdout.strip():
        return
    ensure_checkpoint_branch(repo_path, item)
    run_command(["git", "-C", str(repo_path), "add", "-A"])
    run_command(["git", "-C", str(repo_path), "commit", "-m", f"checkpoint: {item['title']}"])


def write_checkpoint(
    repo_path: Path,
    item: dict[str, Any],
    summary: str,
    verification_status: str,
    verification_summary: str,
    stop_reason: str | None,
) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    checkpoint_path = operator_paths(repo_path)["checkpoints"] / f"{timestamp}-{slugify(item['title'])}.md"
    content = (
        f"# Checkpoint: {item['title']}\n\n"
        f"- Time: {utc_now()}\n"
        f"- Item ID: {item['id']}\n"
        f"- Verification: {verification_status}\n"
        f"- Stop reason: {stop_reason or 'none'}\n\n"
        "## Summary\n\n"
        f"{summary.strip()}\n\n"
        "## Verification\n\n"
        f"{verification_summary.strip()}\n"
    )
    write_text(checkpoint_path, content)
    return checkpoint_path


def apply_checkpoint(
    repo_path: Path,
    item_id: str,
    summary: str,
    verification_status: str,
    verification_summary: str,
    stop_reason: str | None,
    publish_checkpoint: bool,
) -> dict[str, Any]:
    if stop_reason and stop_reason not in DEFAULT_STOP_REASONS:
        raise SystemExit(f"Unsupported stop reason: {stop_reason}")

    backlog = load_backlog(repo_path)
    state = load_state(repo_path)
    item = next((candidate for candidate in backlog["items"] if candidate["id"] == item_id), None)
    if not item:
        raise SystemExit(f"Unknown backlog item: {item_id}")

    checkpoint_path = write_checkpoint(repo_path, item, summary, verification_status, verification_summary, stop_reason)
    if verification_status == "passed":
        item["status"] = "completed"
        state["last_completed_item_id"] = item_id
    elif verification_status == "failed":
        item["status"] = "blocked"
        failure_signal = signal_to_item(
            SignalItem(
                source="verification_failure",
                title=f"Repair failed verification for {item['title']}",
                evidence=[verification_summary.strip()],
                impact="high",
                effort="medium",
                risk="medium",
                next_action=f"Fix the failed verification for {item['title']} and rerun validation.",
                fingerprint=f"verification:{item_id}:{verification_summary.strip()}",
            )
        )
        backlog["items"] = merge_items(backlog["items"], [failure_signal])
    else:
        item["status"] = "completed"
        state["last_completed_item_id"] = item_id

    state["verification"] = {
        "status": verification_status,
        "summary": verification_summary.strip(),
        "updated_at": utc_now(),
    }
    state["last_checkpoint_at"] = utc_now()
    state["last_stop_reason"] = stop_reason
    state["current_item_id"] = None
    write_json(operator_paths(repo_path)["backlog"], backlog)
    write_json(operator_paths(repo_path)["state"], state)

    if publish_checkpoint:
        maybe_commit_checkpoint(repo_path, item)

    refresh_backlog(repo_path)
    next_item = choose_next_item(repo_path)
    state = load_state(repo_path)
    state["next_action"] = next_item["next_action"] if next_item else "Wait for a user decision or a new safe signal before continuing."
    write_json(operator_paths(repo_path)["state"], state)
    return {
        "checkpoint": str(checkpoint_path),
        "next_item": next_item,
    }


def status_payload(repo_path: Path) -> dict[str, Any]:
    mission = load_mission(repo_path)
    backlog = load_backlog(repo_path)
    state = load_state(repo_path)
    counts: dict[str, int] = {}
    for item in backlog.get("items", []):
        status = item.get("status", "pending")
        counts[status] = counts.get(status, 0) + 1
    return {
        "mission_title": mission.get("title"),
        "goal": mission.get("goal"),
        "github_repo": state.get("github_repo"),
        "current_item_id": state.get("current_item_id"),
        "next_action": state.get("next_action"),
        "last_stop_reason": state.get("last_stop_reason"),
        "counts": counts,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Persistent runtime for the self-improving operator.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    bootstrap_parser = subparsers.add_parser("bootstrap")
    bootstrap_parser.add_argument("--repo", required=True)
    bootstrap_parser.add_argument("--goal")
    bootstrap_parser.add_argument("--github-repo")

    scan_parser = subparsers.add_parser("scan")
    scan_parser.add_argument("--repo", required=True)

    next_parser = subparsers.add_parser("next")
    next_parser.add_argument("--repo", required=True)

    status_parser = subparsers.add_parser("status")
    status_parser.add_argument("--repo", required=True)

    ingest_parser = subparsers.add_parser("ingest-plan")
    ingest_parser.add_argument("--repo", required=True)
    ingest_parser.add_argument("--plan-file")
    ingest_parser.add_argument("--plan-text")

    checkpoint_parser = subparsers.add_parser("checkpoint")
    checkpoint_parser.add_argument("--repo", required=True)
    checkpoint_parser.add_argument("--item-id", required=True)
    checkpoint_parser.add_argument("--summary", required=True)
    checkpoint_parser.add_argument("--verification-status", choices=["passed", "failed", "unknown"], required=True)
    checkpoint_parser.add_argument("--verification-summary", required=True)
    checkpoint_parser.add_argument("--stop-reason")
    checkpoint_parser.add_argument("--publish-checkpoint", action="store_true")

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_path = Path(getattr(args, "repo")).resolve()

    if args.command == "bootstrap":
        state = bootstrap_state(repo_path, goal=args.goal, github_repo=args.github_repo)
        print(json.dumps(state, indent=2))
        return 0
    if args.command == "scan":
        payload = refresh_backlog(repo_path)
        print(json.dumps(payload, indent=2))
        return 0
    if args.command == "next":
        next_item = choose_next_item(repo_path)
        print(json.dumps(next_item or {"stop_reason": "no_safe_work"}, indent=2))
        return 0
    if args.command == "status":
        print(json.dumps(status_payload(repo_path), indent=2))
        return 0
    if args.command == "ingest-plan":
        if not args.plan_file and not args.plan_text:
            raise SystemExit("Provide --plan-file or --plan-text.")
        plan_text = args.plan_text or read_text(Path(args.plan_file))
        payload = ingest_plan(repo_path, plan_text)
        print(json.dumps(payload, indent=2))
        return 0
    if args.command == "checkpoint":
        payload = apply_checkpoint(
            repo_path=repo_path,
            item_id=args.item_id,
            summary=args.summary,
            verification_status=args.verification_status,
            verification_summary=args.verification_summary,
            stop_reason=args.stop_reason,
            publish_checkpoint=args.publish_checkpoint,
        )
        print(json.dumps(payload, indent=2))
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
