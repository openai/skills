#!/usr/bin/env python3
from __future__ import annotations

from datetime import date

from memory_utils import log_base_dir, log_path_for_date, require_initialized

EMPTY_LOG_MESSAGE = (
    "No log entries for today. Created an empty log file; "
    "please continue with the remaining task steps."
)


def main() -> int:
    base_dir = log_base_dir(create=True)
    require_initialized(base_dir)

    log_path = log_path_for_date(date.today(), base_dir)
    if not log_path.exists():
        log_path.touch()
        print(EMPTY_LOG_MESSAGE)
        return 0

    content = log_path.read_text(encoding="utf-8")
    if not content.strip():
        print(EMPTY_LOG_MESSAGE)
        return 0

    print(content, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
