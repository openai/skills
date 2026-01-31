from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from functools import lru_cache
from pathlib import Path
from typing import Any

ATLAS_APP_NAME = "ChatGPT Atlas"

LOCAL_STATE_PATH = (
    Path.home()
    / "Library"
    / "Application Support"
    / "com.openai.atlas"
    / "browser-data"
    / "host"
    / "Local State"
)


class AtlasError(RuntimeError):
    """Raised when Atlas-specific operations fail."""


def _app_bundle_paths(app_name: str) -> list[Path]:
    return [
        Path("/Applications") / f"{app_name}.app",
        Path.home() / "Applications" / f"{app_name}.app",
    ]


def is_app_installed(app_name: str) -> bool:
    return any(path.exists() for path in _app_bundle_paths(app_name))


@lru_cache(maxsize=1)
def detect_atlas_app_name() -> str:
    """Return the Atlas app name when it is installed."""
    if is_app_installed(ATLAS_APP_NAME):
        return ATLAS_APP_NAME

    raise AtlasError("Could not find ChatGPT Atlas. Install the ChatGPT Atlas app.")


def _ensure_local_state_path(path: Path = LOCAL_STATE_PATH) -> Path:
    if not path.exists():
        raise AtlasError(f"Local State file not found at: {path}")
    return path


def read_local_state(path: Path = LOCAL_STATE_PATH) -> dict[str, Any]:
    local_state_path = _ensure_local_state_path(path)
    try:
        return json.loads(local_state_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise AtlasError(f"Failed to parse Local State JSON at: {local_state_path}") from exc


def get_active_profile_path() -> Path:
    """Resolve the active Atlas profile directory, falling back to Default."""
    local_state = read_local_state()
    host_root = LOCAL_STATE_PATH.parent

    last_used = local_state.get("profile", {}).get("last_used")
    if isinstance(last_used, str) and last_used:
        candidate = host_root / last_used
        if candidate.exists():
            return candidate

    default_profile = host_root / "Default"
    if default_profile.exists():
        return default_profile

    raise AtlasError(
        "Unable to resolve an Atlas profile directory. "
        f"Checked last_used={last_used!r} and Default under: {host_root}"
    )


def get_history_path() -> Path:
    return get_active_profile_path() / "History"


def get_bookmarks_path() -> Path:
    return get_active_profile_path() / "Bookmarks"


def copy_sqlite_db(path: Path) -> Path:
    """Copy a SQLite DB to a temp location to avoid lock errors."""
    if not path.exists():
        raise AtlasError(f"SQLite database not found at: {path}")

    tmp_dir = Path(tempfile.mkdtemp(prefix="atlas-db-"))
    dest = tmp_dir / path.name
    shutil.copy2(path, dest)
    return dest


def _run_applescript_raw(script: str) -> subprocess.CompletedProcess[str]:
    if shutil.which("osascript") is None:
        raise AtlasError("osascript is not available on PATH; Atlas control requires macOS")

    return subprocess.run(
        ["osascript", "-e", script],
        check=False,
        capture_output=True,
        text=True,
    )


def _applescript_hint(stderr: str) -> str | None:
    lower = stderr.lower()
    if "-1743" in stderr or "not authorized" in lower or "not permitted" in lower:
        return (
            "Grant Automation permission in System Settings > Privacy & Security > Automation, "
            "and allow your terminal to control ChatGPT Atlas."
        )
    return None


def run_applescript(script: str) -> str:
    """Execute AppleScript via osascript and return stdout."""
    completed = _run_applescript_raw(script)
    if completed.returncode != 0:
        stderr = (completed.stderr or "").strip()
        hint = _applescript_hint(stderr)
        if hint:
            stderr = f"{stderr} (Hint: {hint})"
        raise AtlasError(f"AppleScript failed: {stderr}")
    return (completed.stdout or "").strip()


@lru_cache(maxsize=4)
def is_tab_capable(app_name: str) -> bool:
    """Return True if the app supports basic window/tab AppleScript queries."""
    if not is_app_installed(app_name):
        return False

    probe = f'tell application "{app_name}" to get count of windows'
    completed = _run_applescript_raw(probe)
    if completed.returncode != 0:
        stderr = (completed.stderr or "").strip()
        hint = _applescript_hint(stderr)
        if hint:
            raise AtlasError(f"AppleScript probe failed: {stderr} (Hint: {hint})")
        return False
    return True


@lru_cache(maxsize=1)
def detect_tab_capable_app_name() -> str:
    """Return the Atlas app name when it supports tab scripting."""
    app_name = detect_atlas_app_name()
    if not is_tab_capable(app_name):
        raise AtlasError(
            "ChatGPT Atlas is installed but does not appear to expose window/tab scripting."
        )
    return app_name


def tell_atlas(script_body: str, app_name: str | None = None) -> str:
    """Wrap a script body in a tell application block for the detected Atlas app."""
    target_app = app_name or detect_atlas_app_name()
    script = f'tell application "{target_app}"\n{script_body}\nend tell'
    return run_applescript(script)
