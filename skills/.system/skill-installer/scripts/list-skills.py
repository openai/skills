#!/usr/bin/env python3
"""List skills from a GitHub repo path."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error

from github_utils import github_api_contents_url, github_request

DEFAULT_REPO = "openai/skills"
DEFAULT_PATH = "skills/.curated"
DEFAULT_REF = "main"


class ListError(Exception):
    pass


class Args(argparse.Namespace):
    repo: str
    path: str
    ref: str
    format: str
    show_path: bool


def _request(url: str) -> bytes:
    return github_request(url, "codex-skill-list")


def _codex_home() -> str:
    return os.environ.get("CODEX_HOME", os.path.expanduser("~/.codex"))


def _installed_skills() -> set[str]:
    root = os.path.join(_codex_home(), "skills")
    if not os.path.isdir(root):
        return set()
    entries = set()
    for name in os.listdir(root):
        path = os.path.join(root, name)
        if os.path.isdir(path):
            entries.add(name)
    return entries


def _installed_skills_detail() -> dict[str, dict[str, str]]:
    """Return installed skills with path and health status."""
    root = os.path.join(_codex_home(), "skills")
    if not os.path.isdir(root):
        return {}
    detail: dict[str, dict[str, str]] = {}
    for name in sorted(os.listdir(root)):
        path = os.path.join(root, name)
        if not os.path.isdir(path):
            continue
        skill_md = os.path.join(path, "SKILL.md")
        status = "ok" if os.path.isfile(skill_md) else "broken (missing SKILL.md)"
        detail[name] = {"path": path, "status": status}
    return detail


def _list_skills(repo: str, path: str, ref: str) -> list[str]:
    api_url = github_api_contents_url(repo, path, ref)
    try:
        payload = _request(api_url)
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            raise ListError(
                "Skills path not found: "
                f"https://github.com/{repo}/tree/{ref}/{path}"
            ) from exc
        raise ListError(f"Failed to fetch skills: HTTP {exc.code}") from exc
    data = json.loads(payload.decode("utf-8"))
    if not isinstance(data, list):
        raise ListError("Unexpected skills listing response.")
    skills = [item["name"] for item in data if item.get("type") == "dir"]
    return sorted(skills)


def _parse_args(argv: list[str]) -> Args:
    parser = argparse.ArgumentParser(description="List skills.")
    parser.add_argument("--repo", default=DEFAULT_REPO)
    parser.add_argument(
        "--path",
        default=DEFAULT_PATH,
        help="Repo path to list (default: skills/.curated)",
    )
    parser.add_argument("--ref", default=DEFAULT_REF)
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format",
    )
    parser.add_argument(
        "--show-path",
        action="store_true",
        default=False,
        help="Show install path and health status for installed skills.",
    )
    return parser.parse_args(argv, namespace=Args())


def main(argv: list[str]) -> int:
    args = _parse_args(argv)
    try:
        skills = _list_skills(args.repo, args.path, args.ref)
        installed = _installed_skills()
        detail = _installed_skills_detail() if args.show_path else {}
        if args.format == "json":
            payload = []
            for name in skills:
                entry: dict[str, object] = {
                    "name": name,
                    "installed": name in installed,
                }
                if args.show_path and name in detail:
                    entry["path"] = detail[name]["path"]
                    entry["status"] = detail[name]["status"]
                payload.append(entry)
            print(json.dumps(payload))
        else:
            for idx, name in enumerate(skills, start=1):
                if name in installed:
                    info = detail.get(name, {})
                    if args.show_path and info:
                        status = info.get("status", "")
                        path_str = info.get("path", "")
                        status_hint = f" [{status}]" if status != "ok" else ""
                        suffix = f" (installed: {path_str}{status_hint})"
                    else:
                        suffix = " (already installed)"
                else:
                    suffix = ""
                print(f"{idx}. {name}{suffix}")
        return 0
    except ListError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
