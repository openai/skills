#!/usr/bin/env python3
"""Uninstall background polling for Agent Feeds v0.3."""

from __future__ import annotations

import os
import argparse
import platform
import subprocess
from pathlib import Path


LABEL = "dev.agentfeeds.fetch"
BEGIN_MARKER = "# BEGIN Agent Feeds polling"
END_MARKER = "# END Agent Feeds polling"


def uninstall_launchd() -> None:
    plist_path = Path.home() / "Library" / "LaunchAgents" / f"{LABEL}.plist"
    domain = f"gui/{os.getuid()}"
    subprocess.run(["launchctl", "bootout", domain, str(plist_path)], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if plist_path.exists():
        plist_path.unlink()
    print(f"removed launchd polling: {plist_path}")


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


def uninstall_cron() -> None:
    cleaned = without_existing_block(current_crontab())
    subprocess.run(["crontab", "-"], input=(cleaned + "\n") if cleaned else "", text=True, check=True)
    print("removed cron polling")


def build_parser() -> argparse.ArgumentParser:
    return argparse.ArgumentParser(description="Uninstall Agent Feeds background polling")


def main(argv: list[str] | None = None) -> int:
    build_parser().parse_args(argv)
    system = platform.system()
    if system == "Darwin":
        uninstall_launchd()
        return 0
    if system in {"Linux", "FreeBSD"}:
        uninstall_cron()
        return 0
    print(f"unsupported platform for polling uninstaller: {system}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
