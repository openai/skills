#!/usr/bin/env python3
"""
Fetch GitLab merge request discussions (including inline threads) for the MR
associated with the current git branch, by shelling out to:

  glab api

Requires:
  - `glab auth status` succeeds (uses glab config/keyring or GITLAB_TOKEN)
  - current branch has an associated open MR

Usage:
  python scripts/fetch_comments.py > /tmp/mr_comments.json
  python scripts/fetch_comments.py --open-comments > /tmp/open_threads.json
  python scripts/fetch_comments.py --output /tmp/mr_comments.json
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
import subprocess
import sys
from typing import Any, Iterable
from urllib.parse import quote


def _run(cmd: list[str]) -> str:
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{p.stderr}")
    return p.stdout


def _run_json(cmd: list[str]) -> Any:
    out = _run(cmd)
    try:
        return json.loads(out)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse JSON from command output: {e}\nRaw:\n{out}") from e


def _ensure_glab_authenticated() -> None:
    try:
        _run(["glab", "auth", "status"])
    except RuntimeError as exc:
        raise RuntimeError(
            "glab auth status failed; run `glab auth login` or set GITLAB_TOKEN"
        ) from exc


def _git_current_branch() -> str:
    return _run(["git", "rev-parse", "--abbrev-ref", "HEAD"]).strip()


def _git_origin_url() -> str:
    return _run(["git", "remote", "get-url", "origin"]).strip()


def _strip_dot_git(path: str) -> str:
    return path[:-4] if path.endswith(".git") else path


def _parse_project_path(remote_url: str) -> str:
    """
    Convert a git remote URL into a GitLab project path (group/subgroup/project).
    Supports common SSH and HTTPS formats.
    """
    # HTTPS: https://gitlab.example.com/group/project.git
    https_match = re.match(r"^https?://[^/]+/(.+)$", remote_url)
    if https_match:
        return _strip_dot_git(https_match.group(1))

    # SSH scp-like: git@gitlab.example.com:group/project.git
    ssh_match = re.match(r"^(?:ssh://)?git@[^:/]+[:/](.+)$", remote_url)
    if ssh_match:
        return _strip_dot_git(ssh_match.group(1))

    raise RuntimeError(f"Unable to parse GitLab project path from origin URL: {remote_url}")


def _glab_api_get(endpoint: str, params: dict[str, Any] | None = None) -> Any:
    cmd = ["glab", "api", endpoint, "-X", "GET"]
    for key, value in (params or {}).items():
        if value is None:
            continue
        cmd += ["-F", f"{key}={value}"]
    return _run_json(cmd)


def _paginate(endpoint: str, base_params: dict[str, Any], per_page: int = 100, max_pages: int = 20) -> list[Any]:
    results: list[Any] = []
    page = 1

    while page <= max_pages:
        params = dict(base_params)
        params.update({"per_page": per_page, "page": page})
        chunk = _glab_api_get(endpoint, params=params)

        if not isinstance(chunk, list) or not chunk:
            break

        results.extend(chunk)

        if len(chunk) < per_page:
            break
        page += 1

    return results


def _encode_project_path(project_path: str) -> str:
    # GitLab API accepts URL-encoded project paths in place of numeric IDs.
    return quote(project_path, safe="")


def _find_open_mr_for_branch(project: str, branch: str) -> dict[str, Any]:
    endpoint = f"/projects/{project}/merge_requests"
    mrs = _paginate(
        endpoint,
        base_params={
            "state": "opened",
            "source_branch": branch,
            "order_by": "updated_at",
            "sort": "desc",
        },
    )
    if not mrs:
        raise RuntimeError(f"No open merge request found for source branch: {branch}")
    # Prefer the most recently updated MR for this branch.
    return mrs[0]


def _get_mr(project: str, mr_iid: int) -> dict[str, Any]:
    endpoint = f"/projects/{project}/merge_requests/{mr_iid}"
    mr = _glab_api_get(endpoint)
    if not isinstance(mr, dict):
        raise RuntimeError("Unexpected response when fetching merge request details")
    return mr


def _discussion_notes(discussion: dict[str, Any]) -> list[dict[str, Any]]:
    notes = discussion.get("notes")
    return notes if isinstance(notes, list) else []


def _is_bot_or_system_note(note: dict[str, Any]) -> bool:
    if note.get("system"):
        return True
    author = note.get("author") or {}
    if author.get("bot"):
        return True
    username = str(author.get("username") or "").lower()
    return username.endswith("[bot]") or username.endswith("-bot")


def _filter_bot_notes(notes: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    return [n for n in notes if not _is_bot_or_system_note(n)]


def _discussion_is_open(discussion: dict[str, Any]) -> bool:
    # Prefer the top-level resolved flag if present.
    resolved = discussion.get("resolved")
    if resolved is True:
        return False

    notes = _discussion_notes(discussion)
    resolvable_notes = [n for n in notes if n.get("resolvable")]
    if resolvable_notes:
        # If any resolvable note is still unresolved, treat the discussion as open.
        return any(not bool(n.get("resolved")) for n in resolvable_notes)

    # Fallback: treat unresolved/unknown as open.
    return not bool(resolved)


def _discussion_has_non_bot_content(discussion: dict[str, Any]) -> bool:
    notes = _discussion_notes(discussion)
    return len(_filter_bot_notes(notes)) > 0


def fetch_all(project_path: str, branch: str) -> dict[str, Any]:
    encoded_project = _encode_project_path(project_path)

    mr_hint = _find_open_mr_for_branch(encoded_project, branch)
    mr_iid = int(mr_hint["iid"])
    mr = _get_mr(encoded_project, mr_iid)

    discussions_endpoint = f"/projects/{encoded_project}/merge_requests/{mr_iid}/discussions"
    discussions = _paginate(discussions_endpoint, base_params={})

    # Drop pure bot/system discussions.
    discussions = [d for d in discussions if _discussion_has_non_bot_content(d)]

    open_discussions = [d for d in discussions if _discussion_is_open(d)]

    mr_meta = {
        "iid": mr.get("iid"),
        "project_id": mr.get("project_id"),
        "web_url": mr.get("web_url"),
        "title": mr.get("title"),
        "state": mr.get("state"),
        "source_branch": mr.get("source_branch"),
        "target_branch": mr.get("target_branch"),
        "updated_at": mr.get("updated_at"),
    }

    return {
        "merge_request": mr_meta,
        "project": {
            "path": project_path,
            "encoded_path": encoded_project,
            "branch": branch,
        },
        "discussions": discussions,
        "open_discussions": open_discussions,
    }


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Fetch GitLab MR discussions for the current branch")
    parser.add_argument(
        "--open-comments",
        action="store_true",
        help="emit only unresolved/open discussions (still includes merge_request metadata)",
    )
    parser.add_argument(
        "--output",
        help="optional path to write JSON output; defaults to stdout",
    )
    return parser


def main() -> None:
    parser = _build_arg_parser()
    args = parser.parse_args()

    _ensure_glab_authenticated()

    branch = _git_current_branch()
    origin = _git_origin_url()
    project_path = _parse_project_path(origin)

    result = fetch_all(project_path=project_path, branch=branch)

    if args.open_comments:
        payload: Any = {
            "merge_request": result["merge_request"],
            "project": result["project"],
            "open_discussions": result["open_discussions"],
        }
    else:
        payload = result

    output = json.dumps(payload, indent=2)

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(output)
            f.write("\n")
    else:
        print(output)


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)
