#!/usr/bin/env python3
from __future__ import annotations

from datetime import date

from memory_utils import log_base_dir, log_path_for_date


def main() -> int:
    base_dir = log_base_dir()

    log_path = log_path_for_date(date.today(), base_dir)
    if not log_path.exists():
        print(f"No log file for today: {log_path.name}")
        return 0

    print(log_path.read_text(encoding="utf-8"), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
