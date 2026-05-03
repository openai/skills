#!/usr/bin/env python3
"""Run the Agent Feeds management CLI from the skill checkout."""

from __future__ import annotations

import sys
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VENV_PYTHON = Path.home() / ".agentfeeds" / "runtime-venv" / "bin" / "python"
if VENV_PYTHON.exists() and Path(sys.executable).resolve() != VENV_PYTHON.resolve():
    os.execv(str(VENV_PYTHON), [str(VENV_PYTHON), __file__, *sys.argv[1:]])
LIB = ROOT / "scripts" / "lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from agentfeeds_runtime.commands import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main())
