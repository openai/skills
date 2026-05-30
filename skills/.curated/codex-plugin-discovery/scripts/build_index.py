#!/usr/bin/env python3
"""Build a searchable index for OpenAI Codex plugins."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any


REPOSITORY_URL = "https://github.com/openai/plugins"


def run_git(args: list[str], cwd: Path | None = None) -> str:
    """Run a git command and return stdout."""
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.strip()


def remote_head() -> str:
    """Return the current HEAD SHA from the upstream repository."""
    output = run_git(["ls-remote", REPOSITORY_URL, "HEAD"])
    return output.split()[0]


def ensure_repo(cache_dir: Path) -> Path:
    """Ensure the upstream plugin repository is cached and checked out."""
    repo_dir = cache_dir / "openai-plugins"
    cache_dir.mkdir(parents=True, exist_ok=True)

    if not repo_dir.exists():
        run_git(["clone", "--depth", "1", REPOSITORY_URL, str(repo_dir)])
    else:
        run_git(["fetch", "--depth", "1", "origin", "HEAD"], cwd=repo_dir)
        run_git(["checkout", "--detach", "FETCH_HEAD"], cwd=repo_dir)

    return repo_dir


def scan_manifest_paths(repo_dir: Path) -> list[Path]:
    """Return direct plugin manifests, excluding nested fixtures."""
    return sorted((repo_dir / "plugins").glob("*/.codex-plugin/plugin.json"))


def read_json(path: Path) -> Any:
    """Read UTF-8 JSON from path."""
    return json.loads(path.read_text(encoding="utf-8"))


def as_list(value: Any) -> list[str]:
    """Normalize a scalar, list, or empty value into a list of strings."""
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return [str(item) for item in value if item is not None and item != ""]
    return [str(value)]


def companion_surfaces(plugin_dir: Path) -> list[str]:
    """Detect companion surfaces adjacent to a plugin manifest."""
    surfaces = []
    for name in (
        "skills",
        "agents",
        "commands",
        "assets",
        ".app.json",
        ".mcp.json",
        "hooks.json",
    ):
        if (plugin_dir / name).exists():
            surfaces.append(name)
    return surfaces


def build_plugin_record(manifest_path: Path, repo_dir: Path) -> dict[str, Any]:
    """Build the recommendation fields for one plugin manifest."""
    manifest = read_json(manifest_path)
    interface = manifest.get("interface") or {}
    plugin_dir = manifest_path.parents[1]

    name = str(manifest.get("name") or plugin_dir.name)
    display_name = str(
        interface.get("displayName")
        or interface.get("display_name")
        or manifest.get("displayName")
        or manifest.get("display_name")
        or name
    )
    description = str(
        manifest.get("description")
        or interface.get("longDescription")
        or interface.get("shortDescription")
        or ""
    )
    category = str(interface.get("category") or manifest.get("category") or "")
    keywords = as_list(manifest.get("keywords"))
    capabilities = as_list(interface.get("capabilities") or manifest.get("capabilities"))
    repository = manifest.get("repository") or ""
    homepage = manifest.get("homepage") or ""
    plugin_path = plugin_dir.relative_to(repo_dir).as_posix()
    manifest_rel_path = manifest_path.relative_to(repo_dir).as_posix()
    surfaces = companion_surfaces(plugin_dir)

    search_parts = [
        name,
        display_name,
        description,
        category,
        *keywords,
        *capabilities,
        str(interface.get("shortDescription") or ""),
        str(interface.get("longDescription") or ""),
    ]

    return {
        "name": name,
        "display_name": display_name,
        "description": description,
        "category": category,
        "keywords": keywords,
        "capabilities": capabilities,
        "repository": repository,
        "homepage": homepage,
        "plugin_path": plugin_path,
        "manifest_path": manifest_rel_path,
        "companion_surfaces": surfaces,
        "search_text": " ".join(part for part in search_parts if part).lower(),
    }


def build_index(repo_dir: Path, output_path: Path, upstream_sha: str) -> dict[str, Any]:
    """Build and write the plugin index."""
    manifest_paths = scan_manifest_paths(repo_dir)
    if not manifest_paths:
        raise ValueError(f"No direct plugin manifests found under {repo_dir / 'plugins'}")

    plugins = [
        build_plugin_record(manifest_path, repo_dir)
        for manifest_path in manifest_paths
    ]
    index = {
        "source": {
            "repository": REPOSITORY_URL,
            "commit": upstream_sha,
            "scope": "plugins/*/.codex-plugin/plugin.json",
        },
        "plugins": plugins,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(index, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return index


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache-dir", type=Path, default=Path(".cache"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--repo-dir", type=Path)
    args = parser.parse_args()

    if args.repo_dir:
        upstream_sha = "local"
        repo_dir = args.repo_dir
    else:
        upstream_sha = remote_head()
        repo_dir = ensure_repo(args.cache_dir)
    index = build_index(repo_dir=repo_dir, output_path=args.output, upstream_sha=upstream_sha)
    print(f"indexed {len(index['plugins'])} plugins from {upstream_sha}")


if __name__ == "__main__":
    main()
