"""Subprocess wrapper that swallows missing-binary errors into a structured result."""
from __future__ import annotations

import subprocess
from dataclasses import dataclass
from typing import Optional, Sequence


@dataclass
class ToolResult:
    exit_code: int
    stdout: str
    stderr: str

    @property
    def ok(self) -> bool:
        return self.exit_code == 0


def run(cmd: Sequence[str], cwd: Optional[str] = None, timeout: int = 120) -> ToolResult:
    """Run a command and return ToolResult.

    Returns exit_code=127 with stderr "binary not found: <cmd>" if the executable is missing.
    Returns exit_code=124 on timeout.
    """
    try:
        proc = subprocess.run(
            list(cmd),
            cwd=cwd,
            timeout=timeout,
            capture_output=True,
            text=True,
            check=False,
        )
        return ToolResult(proc.returncode, proc.stdout or "", proc.stderr or "")
    except FileNotFoundError:
        return ToolResult(127, "", f"binary not found: {cmd[0]}")
    except subprocess.TimeoutExpired as e:
        return ToolResult(124, e.stdout or "", (e.stderr or "") + f"\ntimeout after {timeout}s")
    except OSError as e:
        return ToolResult(126, "", f"os error: {e}")
