#!/usr/bin/env python3
from __future__ import annotations

from memory_utils import ensure_initialized, init_log_path, log_base_dir


def main() -> int:
    base_dir = log_base_dir(create=True)
    init_log = init_log_path(base_dir)
    if init_log.exists():
        print("Initialization already completed.")
        return 0

    ensure_initialized(base_dir)
    print(f"Initialized easy-memory in {base_dir}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
