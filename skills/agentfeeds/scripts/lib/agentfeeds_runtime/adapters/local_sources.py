"""Local filesystem and repository adapters."""

from __future__ import annotations

import subprocess
from datetime import UTC, datetime
from pathlib import Path

from agentfeeds_runtime.adapters.common import envelope, stable_hash


def _iso_mtime(path: Path) -> str:
    return datetime.fromtimestamp(path.stat().st_mtime, UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _resolve_path(value: str) -> Path:
    path = Path(value).expanduser()
    return path if path.is_absolute() else path.resolve()


def _entry_kind(path: Path) -> str:
    if path.is_symlink():
        return "symlink"
    if path.is_file():
        return "file"
    if path.is_dir():
        return "directory"
    return "other"


def _directory_entry(path: Path) -> dict:
    stat = path.stat()
    return {
        "path": str(path),
        "name": path.name,
        "kind": _entry_kind(path),
        "extension": path.suffix.lstrip(".") or None,
        "size_bytes": stat.st_size if path.is_file() else None,
        "modified_at": _iso_mtime(path),
    }


def fetch_filesystem_scan(stream: dict, adapter: dict, stream_uri: str) -> list[dict]:
    root = _resolve_path(adapter["path"])
    if not root.exists():
        raise FileNotFoundError(f"{stream['id']}: local directory not found: {root}")
    if not root.is_dir():
        raise ValueError(f"{stream['id']}: local path is not a directory: {root}")
    limit = int(adapter.get("limit") or 25)
    entries = [_directory_entry(path) for path in root.iterdir()]
    entries.sort(key=lambda item: item["modified_at"], reverse=True)
    return [envelope(stream, stream_uri, stable_hash(item), item, item["modified_at"]) for item in entries[:limit]]


def _parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    raw = text[4:end]
    body = text[end + 5 :]
    data = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip("\"'")
    return data, body


def fetch_markdown_scan(stream: dict, adapter: dict, stream_uri: str) -> list[dict]:
    root = _resolve_path(adapter["path"])
    if not root.exists():
        raise FileNotFoundError(f"{stream['id']}: markdown vault not found: {root}")
    if not root.is_dir():
        raise ValueError(f"{stream['id']}: markdown vault path is not a directory: {root}")
    limit = int(adapter.get("limit") or 25)
    docs = []
    for path in root.rglob("*.md"):
        text = path.read_text(encoding="utf-8", errors="replace")
        frontmatter, body = _parse_frontmatter(text) if adapter.get("parse_frontmatter") else ({}, text)
        title = frontmatter.get("title") or next((line.lstrip("# ").strip() for line in body.splitlines() if line.strip()), path.stem)
        snippet = " ".join(line.strip() for line in body.splitlines() if line.strip())[:500]
        tags = frontmatter.get("tags") or ""
        if isinstance(tags, str):
            tags = [item.strip() for item in tags.strip("[]").split(",") if item.strip()]
        item = {
            "path": str(path),
            "title": title,
            "snippet": snippet,
            "modified_at": _iso_mtime(path),
            "frontmatter": frontmatter,
            "tags": tags,
        }
        docs.append(item)
    docs.sort(key=lambda item: item["modified_at"], reverse=True)
    return [envelope(stream, stream_uri, stable_hash(item), item, item["modified_at"]) for item in docs[:limit]]


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=False, text=True, capture_output=True).stdout.strip()


def fetch_git_status(stream: dict, adapter: dict, stream_uri: str) -> list[dict]:
    repo = _resolve_path(adapter["path"])
    if not (repo / ".git").exists():
        raise ValueError(f"{stream['id']}: path is not a git repository: {repo}")
    branch = _git(repo, "branch", "--show-current") or "HEAD"
    dirty_files = [line[3:] for line in _git(repo, "status", "--porcelain").splitlines() if line]
    ahead = behind = 0
    upstream = _git(repo, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}")
    if upstream:
        counts = _git(repo, "rev-list", "--left-right", "--count", f"{upstream}...HEAD").split()
        if len(counts) == 2:
            behind, ahead = int(counts[0]), int(counts[1])
    data = {
        "path": str(repo),
        "branch": branch,
        "clean": not dirty_files,
        "dirty_files": dirty_files,
        "ahead": ahead,
        "behind": behind,
    }
    return [envelope(stream, stream_uri, stable_hash(data), data)]
