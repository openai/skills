#!/usr/bin/env python3
from __future__ import annotations

from datetime import date

from memory_utils import ensure_local_install, log_path_for_date, skill_dir


def main() -> int:
    base_dir = skill_dir()
    ensure_local_install(base_dir)

    log_path = log_path_for_date(date.today(), base_dir)
    if not log_path.exists():
        print(f"No log file for today: {log_path.name}")
        return 0

    print(log_path.read_text(encoding="utf-8"), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
