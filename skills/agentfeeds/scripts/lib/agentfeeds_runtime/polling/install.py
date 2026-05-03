#!/usr/bin/env python3
"""Install background polling for Agent Feeds v0.3."""

from __future__ import annotations

import os
import argparse
import platform
import plistlib
import shlex
import shutil
import subprocess
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


LABEL = "dev.agentfeeds.fetch"
BEGIN_MARKER = "# BEGIN Agent Feeds polling"
END_MARKER = "# END Agent Feeds polling"
DEFAULT_ROOT = Path.home() / ".agentfeeds"
MIN_INTERVAL_SECONDS = 300
STABLE_PATH = f"{Path.home()}/.local/bin:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"


def load_subscriptions(root: Path) -> dict:
    path = root / "subscriptions.yaml"
    if not path.exists() or yaml is None:
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def poll_interval_seconds(root: Path) -> int:
    config = load_subscriptions(root)
    defaults = config.get("defaults") or {}
    intervals = []
    if defaults.get("poll_interval_seconds"):
        intervals.append(int(defaults["poll_interval_seconds"]))
    for subscription in config.get("subscriptions") or []:
        if subscription.get("poll_interval_seconds"):
            intervals.append(int(subscription["poll_interval_seconds"]))
    return max(min(intervals or [600]), MIN_INTERVAL_SECONDS)


def fetcher_path() -> str:
    venv_candidate = Path.home() / ".agentfeeds" / "runtime-venv" / "bin" / "agentfeeds-fetch"
    if venv_candidate.exists():
        return str(venv_candidate)
    candidate = Path.home() / ".local" / "bin" / "agentfeeds-fetch"
    if candidate.exists():
        return str(candidate)
    command = shutil.which("agentfeeds-fetch")
    if command:
        return command
    raise FileNotFoundError("agentfeeds-fetch not found; run `python3 scripts/setup.py` first")


def install_launchd(root: Path, interval: int, fetcher: str) -> None:
    launch_agents = Path.home() / "Library" / "LaunchAgents"
    launch_agents.mkdir(parents=True, exist_ok=True)
    logs = root / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    plist_path = launch_agents / f"{LABEL}.plist"
    payload = {
        "Label": LABEL,
        "ProgramArguments": [fetcher, "--root", str(root), "--all"],
        "StartInterval": interval,
        "RunAtLoad": True,
        "StandardOutPath": str(logs / "poll.out.log"),
        "StandardErrorPath": str(logs / "poll.err.log"),
        "EnvironmentVariables": {
            "PATH": STABLE_PATH,
        },
    }
    plist_path.write_bytes(plistlib.dumps(payload))

    domain = f"gui/{os.getuid()}"
    subprocess.run(["launchctl", "bootout", domain, str(plist_path)], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["launchctl", "bootstrap", domain, str(plist_path)], check=True)
    subprocess.run(["launchctl", "enable", f"{domain}/{LABEL}"], check=False)
    subprocess.run(["launchctl", "kickstart", "-k", f"{domain}/{LABEL}"], check=False)
    print(f"installed launchd polling: {plist_path}")
    print(f"interval: {interval} seconds")
    print(f"logs: {logs}")


def current_crontab() -> str:
    result = subprocess.run(["crontab", "-l"], check=False, text=True, capture_output=True)
    return "" if result.returncode else result.stdout


def without_existing_block(text: str) -> str:
    lines = text.splitlines()
    output = []
    skipping = False
    for line in lines:
        if line == BEGIN_MARKER:
            skipping = True
            continue
        if line == END_MARKER:
            skipping = False
            continue
        if not skipping:
            output.append(line)
    return "\n".join(output).strip()


def install_cron(root: Path, interval: int, fetcher: str) -> None:
    minutes = max(interval // 60, 5)
    logs = root / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    command = (
        f"*/{minutes} * * * * "
        f"{shlex.quote(fetcher)} --root {shlex.quote(str(root))} --all "
        f">> {shlex.quote(str(logs / 'poll.out.log'))} "
        f"2>> {shlex.quote(str(logs / 'poll.err.log'))}"
    )
    existing = without_existing_block(current_crontab())
    new_crontab = "\n".join(line for line in [existing, BEGIN_MARKER, command, END_MARKER, ""] if line)
    subprocess.run(["crontab", "-"], input=new_crontab + "\n", text=True, check=True)
    print(f"installed cron polling every {minutes} minutes")
    print(f"logs: {logs}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Install Agent Feeds background polling")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="agentfeeds root directory")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = args.root.expanduser()
    root.mkdir(parents=True, exist_ok=True)
    interval = poll_interval_seconds(root)
    fetcher = fetcher_path()
    system = platform.system()
    if system == "Darwin":
        install_launchd(root, interval, fetcher)
        return 0
    if system in {"Linux", "FreeBSD"}:
        install_cron(root, interval, fetcher)
        return 0
    print(f"unsupported platform for polling installer: {system}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
