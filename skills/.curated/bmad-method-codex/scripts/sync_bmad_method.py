#!/usr/bin/env python3
"""Synchronize BMAD-METHOD references and run first-run health checks for Codex."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import ssl
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

REPO = "bmad-code-org/BMAD-METHOD"
DEFAULT_LATEST_RELEASE_API = f"https://api.github.com/repos/{REPO}/releases/latest"
DEFAULT_RAW_BASE = f"https://raw.githubusercontent.com/{REPO}/main/"
USER_AGENT = "codex-skill-sync/1.5"

SKILL_NAME = "bmad-method-codex"
REQUEST_TIMEOUT = 30
SUMMARY_MAX_CHARS = 6000
DEFAULT_MAX_RETRIES = 3
DEFAULT_RETRY_DELAY = 1.0

ROOT = Path(__file__).resolve().parents[1]
STATE_FILE = ROOT / "state" / "bmad-release-state.json"
SNAPSHOT_DIR = ROOT / "references" / "upstream"
MANIFEST_FILE = ROOT / "references" / "skill-manifest.json"

TRACKED_FILES: List[Tuple[str, str]] = [
    ("CHANGELOG.md", "CHANGELOG.md"),
    ("package.json", "package_json.md"),
    ("docs/reference/commands.md", "docs_reference_commands.md"),
    ("docs/reference/agents.md", "docs_reference_agents.md"),
    ("docs/reference/modules.md", "docs_reference_modules.md"),
    ("docs/reference/workflow-map.md", "docs_reference_workflow_map.md"),
    ("docs/how-to/install-bmad.md", "how_to_install_bmad.md"),
    ("docs/how-to/upgrade-to-v6.md", "how_to_upgrade_to_v6.md"),
]


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _header_int(headers, name: str, default: int = 0) -> int:
    if not headers:
        return default
    value = headers.get(name)
    if value is None:
        return default
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return default


def _http_retry_delay(error: urllib.error.HTTPError, fallback: float) -> float:
    retry_after = error.headers.get("Retry-After") if error.headers else None
    if retry_after:
        retry_after = str(retry_after).strip()
        if retry_after.isdigit():
            return float(retry_after)
        try:
            dt = datetime.strptime(retry_after, "%a, %d %b %Y %H:%M:%S %Z")
            wait = (dt.replace(tzinfo=timezone.utc) - datetime.now(timezone.utc)).total_seconds()
            if wait > 0:
                return wait
        except ValueError:
            pass

    reset_epoch = _header_int(error.headers, "X-RateLimit-Reset")
    if reset_epoch:
        wait = reset_epoch - int(datetime.now(timezone.utc).timestamp())
        if wait > 0:
            return float(wait + 1)

    return max(0.0, float(fallback))


def _is_retryable_http(error: urllib.error.HTTPError) -> bool:
    code = getattr(error, "code", None)
    if code in {429, 500, 502, 503, 504}:
        return True
    if code == 403 and error.headers:
        remaining = error.headers.get("X-RateLimit-Remaining")
        if str(remaining).strip() == "0":
            return True
    return False


def request_text(url: str, *, max_retries: int = DEFAULT_MAX_RETRIES, retry_delay: float = DEFAULT_RETRY_DELAY) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": USER_AGENT,
        },
    )
    attempt = 0
    delay = retry_delay

    while True:
        try:
            with urllib.request.urlopen(
                request,
                context=ssl.create_default_context(),
                timeout=REQUEST_TIMEOUT,
            ) as response:
                return response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            if _is_retryable_http(exc) and attempt < max_retries:
                wait = _http_retry_delay(exc, delay)
                if wait > 0:
                    time.sleep(wait)
                attempt += 1
                delay = max(delay * 2, 1.0)
                continue
            raise RuntimeError(f"Request failed for {url}: HTTP {getattr(exc, 'code', 'error')}") from exc
        except urllib.error.URLError as exc:
            if attempt < max_retries:
                if delay > 0:
                    time.sleep(delay)
                attempt += 1
                delay = max(delay * 2, 1.0)
                continue
            raise RuntimeError(f"Request failed for {url}: {exc}") from exc


def request_json(
    url: str,
    *,
    max_retries: int = DEFAULT_MAX_RETRIES,
    retry_delay: float = DEFAULT_RETRY_DELAY,
) -> dict:
    data = request_text(url, max_retries=max_retries, retry_delay=retry_delay)
    try:
        payload = json.loads(data)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid JSON payload from {url}") from exc
    if not isinstance(payload, dict):
        raise RuntimeError(f"Unexpected payload type from {url}")
    return payload


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def read_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    body = dict(payload)
    body["last_updated_at"] = _now_iso()
    path.write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")


def read_manifest(path: Path) -> dict:
    data = read_json(path, {})
    return data if isinstance(data, dict) else {}


def read_skill_version(path: Path) -> str:
    manifest = read_manifest(path)
    value = manifest.get("skill_version")
    return value if isinstance(value, str) and value.strip() else "0.0.0"


def codex_runtime_version() -> str:
    codex_home = os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))
    version_file = Path(codex_home) / "version.json"
    data = read_json(version_file, {})
    if not isinstance(data, dict):
        return ""
    latest = data.get("latest_version")
    return latest if isinstance(latest, str) else ""


def resolve_candidate_skill_path() -> Path:
    base = Path(__file__).resolve().parents[1]
    candidates = [
        Path.home() / ".codex" / "skills" / SKILL_NAME,
    ]
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        candidates.insert(0, Path(codex_home) / "skills" / SKILL_NAME)
    if base not in candidates:
        candidates.append(base)

    for candidate in candidates:
        if candidate.exists() and (candidate / "SKILL.md").is_file():
            return candidate
    return base


def read_agent_version(agent_path: Path) -> Tuple[str, str]:
    manifest_path = agent_path / "references" / "skill-manifest.json"
    return read_skill_version(manifest_path), str(manifest_path)


def read_skill_health(agent_path: Path) -> dict:
    local_version = read_skill_version(MANIFEST_FILE)
    agent_version, agent_manifest = read_agent_version(agent_path)
    local_manifest_data = read_manifest(MANIFEST_FILE)
    runtime_profile = local_manifest_data.get("target_codex_profile", "unknown")

    return {
        "local_version": local_version,
        "agent_version": agent_version,
        "local_manifest": str(MANIFEST_FILE),
        "agent_manifest": agent_manifest,
        "versions_match": local_version == agent_version,
        "agent_path": str(agent_path),
        "runtime_profile": runtime_profile,
        "runtime_version": codex_runtime_version(),
    }


def is_first_invocation(state: dict) -> bool:
    return not STATE_FILE.exists() or not isinstance(state.get("release"), dict)


def sync_snapshots(*, raw_base: str, max_retries: int, retry_delay: float) -> Tuple[Dict[str, str], List[str]]:
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    checksums: Dict[str, str] = {}
    downloaded: List[str] = []

    for source_path, local_name in TRACKED_FILES:
        source_url = f"{raw_base}{source_path}"
        content = request_text(source_url, max_retries=max_retries, retry_delay=retry_delay)
        checksums[local_name] = sha256_text(content)
        output_path = SNAPSHOT_DIR / local_name
        output_path.write_text(
            f"<!-- Auto-generated by sync_bmad_method.py -->\n"
            f"<!-- source: {source_url} -->\n\n"
            f"{content}\n",
            encoding="utf-8",
        )
        downloaded.append(local_name)

    return checksums, downloaded


def compute_delta(current: Dict[str, str], previous: Dict[str, str]) -> List[str]:
    changed: List[str] = []
    all_files = set(current) | set(previous)
    for name in sorted(all_files):
        if current.get(name) != previous.get(name):
            changed.append(name)
    return changed


def write_release_summary(release: dict) -> None:
    summary_path = SNAPSHOT_DIR / "latest-release-summary.md"
    body = (release.get("body") or "").strip()
    if len(body) > SUMMARY_MAX_CHARS:
        body = body[:SUMMARY_MAX_CHARS] + "\n\n...(truncated release body)"

    lines = [
        "# BMAD-METHOD latest release",
        "",
        f"- tag: {release.get('tag_name')}",
        f"- name: {release.get('name')}",
        f"- published: {release.get('published_at')}",
        f"- url: {release.get('html_url')}",
        "",
        "## Release notes",
        "",
        body or "(empty)",
        "",
    ]
    summary_path.write_text("\n".join(lines), encoding="utf-8")


def build_warnings(
    health: dict,
    first_run: bool,
    runtime_before: str,
    release_changed: bool,
    mode: str,
) -> List[str]:
    warnings: List[str] = []

    if not health["versions_match"]:
        warnings.append(
            "Wersja skilla w aktywnym agencie różni się od wersji z bieżącego checkoutu. "
            "Rozważ aktualizację lub ponowną instalację skilla przed kontynuacją."
        )

    if runtime_before and health["runtime_version"] and runtime_before != health["runtime_version"]:
        warnings.append(
            "Wersja Codex runtime zmieniła się od ostatniego zapisu stanu skilla. "
            "Sprawdź kompatybilność odpowiedzi i uruchom sync, jeśli wskazują na to zmiany."
        )

    if (not first_run) and release_changed and mode in {"check", "report"}:
        warnings.append(
            "Wykryto nowe wydanie BMAD-METHOD od ostatniego pełnego sync. "
            "Uruchom sync (lub uruchom jeszcze raz check po autoupdate)."
        )

    return warnings


def build_report(
    mode: str,
    latest: dict,
    state: dict,
    health: dict,
    first_run: bool,
    release_changed: bool,
    warnings: List[str],
    synced_files: List[str],
    tracked_delta: List[str],
) -> dict:
    return {
        "mode": mode,
        "first_run": first_run,
        "latest_release": {
            "tag": latest.get("tag_name"),
            "name": latest.get("name"),
            "published_at": latest.get("published_at"),
            "url": latest.get("html_url"),
        },
        "previous_release": (state.get("release") or {}).get("tag_name"),
        "release_changed": release_changed,
        "synced_files": synced_files,
        "tracked_file_changes": tracked_delta,
        "health": {
            "agent_path": health["agent_path"],
            "local_version": health["local_version"],
            "agent_version": health["agent_version"],
            "versions_match": health["versions_match"],
            "runtime_profile": health["runtime_profile"],
            "runtime_version": health["runtime_version"],
            "local_manifest": health["local_manifest"],
            "agent_manifest": health["agent_manifest"],
        },
        "warnings": warnings,
        "is_optimal": len(warnings) == 0,
        "action": "needs_attention" if warnings else "ok",
        "state_path": str(STATE_FILE),
        "snapshot_path": str(SNAPSHOT_DIR),
    }


def print_report_text(report: dict) -> None:
    print(f"Mode: {report['mode']}")
    print(f"First run: {'yes' if report['first_run'] else 'no'}")
    print("---")
    latest = report['latest_release']
    print(f"Latest BMAD release: {latest.get('tag')} ({latest.get('published_at')})")
    print(f"Previously seen release: {report['previous_release']}")

    health = report['health']
    print("---")
    print(f"Skill local version: {health['local_version']}")
    print(f"Agent skill version: {health['agent_version']}")
    print(f"Versions match: {'yes' if health['versions_match'] else 'no'}")
    print(f"Codex profile: {health['runtime_profile']}")
    print(f"Codex runtime version: {health['runtime_version'] or 'unknown'}")

    if report['release_changed']:
        print("Release delta: detected")
    if report['synced_files']:
        print(f"Synced files: {', '.join(report['synced_files'])}")
    if report['tracked_file_changes']:
        print("Changed tracked files:")
        for name in report['tracked_file_changes']:
            print(f"- {name}")

    if report['warnings']:
        print("---")
        print("SKILL_NOTICE:")
        for warning in report['warnings']:
            print(f"- {warning}")
        print("Suggested step: python3 scripts/sync_bmad_method.py sync")

    print("---")
    print(f"SKILL_STATUS={'optimal' if report['is_optimal'] else 'requires_update'}")


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync BMAD-METHOD references and run health checks")
    parser.add_argument(
        "mode",
        nargs="?",
        default="check",
        choices=("check", "report", "sync", "refresh"),
        help="check: status; report: short status; sync/refresh: force snapshot sync",
    )
    parser.add_argument("--json", action="store_true", help="print JSON report")
    parser.add_argument(
        "--force-sync",
        action="store_true",
        help="force snapshot sync even when release is unchanged",
    )
    parser.add_argument(
        "--release-url",
        default=os.environ.get("BMAD_RELEASE_API", DEFAULT_LATEST_RELEASE_API),
        help="Override releases endpoint (default from BMAD upstream or BMAD_RELEASE_API)",
    )
    parser.add_argument(
        "--raw-base",
        default=os.environ.get("BMAD_RAW_BASE", DEFAULT_RAW_BASE),
        help="Override upstream raw base URL (default from BMAD upstream or BMAD_RAW_BASE)",
    )
    parser.add_argument(
        "--max-retries",
        type=int,
        default=int(os.environ.get("BMAD_MAX_RETRIES", DEFAULT_MAX_RETRIES)),
        help="Max retry attempts for transient network errors",
    )
    parser.add_argument(
        "--retry-delay",
        type=float,
        default=float(os.environ.get("BMAD_RETRY_DELAY", DEFAULT_RETRY_DELAY)),
        help="Initial retry delay in seconds (exponential backoff)",
    )
    parser.add_argument(
        "--request-timeout",
        type=float,
        default=float(os.environ.get("BMAD_REQUEST_TIMEOUT", REQUEST_TIMEOUT)),
        help="Per-request network timeout in seconds",
    )
    args = parser.parse_args(argv)
    if args.max_retries < 0:
        parser.error("--max-retries must be 0 or greater")
    if args.retry_delay < 0:
        parser.error("--retry-delay must be 0 or greater")
    if args.request_timeout <= 0:
        parser.error("--request-timeout must be greater than 0")
    return args


def main(argv: List[str] | None = None) -> int:
    args = parse_args(argv)

    global REQUEST_TIMEOUT
    REQUEST_TIMEOUT = args.request_timeout

    try:
        latest = request_json(
            args.release_url,
            max_retries=args.max_retries,
            retry_delay=args.retry_delay,
        )
    except RuntimeError as exc:
        error = {"error": str(exc), "mode": args.mode}
        if args.json:
            print(json.dumps(error, indent=2))
        else:
            print(f"Failed to fetch BMAD release metadata: {exc}")
        return 1

    state = read_json(STATE_FILE, {}) if STATE_FILE.exists() else {}
    if not isinstance(state, dict):
        state = {}
    previous_state = dict(state)
    previous = previous_state.get("release") if isinstance(previous_state.get("release"), dict) else {}

    first_run = is_first_invocation(state)
    previous_runtime = state.get("runtime_version", "") if isinstance(state.get("runtime_version"), str) else ""
    latest_tag = latest.get("tag_name")
    previous_tag = previous.get("tag_name") if isinstance(previous, dict) else None
    release_changed = bool(previous_tag and latest_tag and previous_tag != latest_tag)

    agent_path = resolve_candidate_skill_path()
    health = read_skill_health(agent_path)
    warnings = build_warnings(health, first_run, previous_runtime, release_changed, args.mode)

    prior_checksums = state.get("tracked_checksums") if isinstance(state.get("tracked_checksums"), dict) else {}
    synced_files: List[str] = []
    tracked_delta: List[str] = []

    should_sync = args.mode in {"sync", "refresh"} or args.force_sync or first_run or release_changed

    if should_sync:
        try:
            new_checksums, synced_files = sync_snapshots(
                raw_base=args.raw_base,
                max_retries=args.max_retries,
                retry_delay=args.retry_delay,
            )
            tracked_delta = compute_delta(new_checksums, prior_checksums if isinstance(prior_checksums, dict) else {})
            write_release_summary(latest)
            state["tracked_checksums"] = new_checksums
        except RuntimeError as exc:
            error = {"error": str(exc), "mode": args.mode}
            if args.json:
                print(json.dumps(error, indent=2))
            else:
                print(f"Failed to sync snapshots: {exc}")
            return 1

    release_changed = release_changed or bool(tracked_delta)

    state["release"] = {
        "tag_name": latest_tag,
        "name": latest.get("name"),
        "published_at": latest.get("published_at"),
        "html_url": latest.get("html_url"),
        "body_sha": sha256_text((latest.get("body") or "")),
    }
    state["runtime_version"] = health["runtime_version"]
    state["agent_health"] = {
        "local_version": health["local_version"],
        "agent_version": health["agent_version"],
        "agent_path": health["agent_path"],
        "versions_match": health["versions_match"],
    }
    state["last_checked_at"] = _now_iso()
    state["last_check_mode"] = args.mode
    state["tracked_changes_last_sync"] = tracked_delta
    write_json(STATE_FILE, state)

    report = build_report(
        args.mode,
        latest,
        previous_state,
        health,
        first_run,
        release_changed,
        warnings,
        synced_files,
        tracked_delta,
    )

    if args.mode == "report":
        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print(f"Mode: {report['mode']}")
            print(f"Latest BMAD release: {report['latest_release'].get('tag')}")
            print(f"Known status: {report['action']}")
            if report['warnings']:
                print("SKILL_NOTICE: review first-run and sync guidance")
        return 0

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_report_text(report)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
