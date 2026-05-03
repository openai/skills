#!/usr/bin/env python3
"""Install the Agent Feeds runtime into a local virtual environment."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import venv
from pathlib import Path


DEFAULT_VENV = Path.home() / ".agentfeeds" / "runtime-venv"


def venv_python(path: Path) -> Path:
    if sys.platform == "win32":
        return path / "Scripts" / "python.exe"
    return path / "bin" / "python"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Install Agent Feeds skill runtime")
    parser.add_argument("--venv", type=Path, default=DEFAULT_VENV, help="runtime virtualenv path")
    return parser


def create_venv(path: Path) -> None:
    if venv_python(path).exists():
        return
    try:
        venv.EnvBuilder(with_pip=True).create(path)
        return
    except Exception:
        if path.exists():
            import shutil as _shutil

            _shutil.rmtree(path)
        uv = shutil.which("uv")
        if not uv:
            raise
        subprocess.run([uv, "venv", "--python", sys.executable, str(path)], check=True)


def install_runtime(python: Path, root: Path) -> None:
    has_pip = subprocess.run(
        [str(python), "-m", "pip", "--version"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    ).returncode == 0
    if has_pip:
        subprocess.run([str(python), "-m", "pip", "install", "--upgrade", "pip"], check=True)
        subprocess.run([str(python), "-m", "pip", "install", "-e", str(root)], check=True)
        return
    uv = shutil.which("uv")
    if not uv:
        raise RuntimeError(f"pip is unavailable in {python}; install pip or install uv")
    subprocess.run([uv, "pip", "install", "--python", str(python), "-e", str(root)], check=True)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(__file__).resolve().parents[1]
    venv_path = args.venv.expanduser()
    venv_path.parent.mkdir(parents=True, exist_ok=True)
    create_venv(venv_path)
    python = venv_python(venv_path)
    install_runtime(python, root)
    print(f"installed Agent Feeds runtime: {venv_path}")
    print(f"management CLI: {python} {root / 'scripts' / 'agentfeeds.py'}")
    print(f"refresh worker: {python} {root / 'scripts' / 'agentfeeds_fetch.py'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
