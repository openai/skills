from __future__ import annotations

import os
import re
from datetime import date, datetime
from pathlib import Path
from typing import Optional

ENTRY_RE = re.compile(
    r"^\[ID:(?P<id>[^\]]+)\] "
    r"\[REF:(?P<ref>[^\]]+)\] "
    r"\[FACT:(?P<factual>true|false)\] "
    r"(?P<content>.*) "
    r"\[TIME:(?P<ts>\d{4}-\d{2}-\d{2}:\d{2}:\d{2})\]$"
)

_REF_LEVEL_RE = re.compile(r"^[A-Za-z0-9._-]+$")


def skill_dir() -> Path:
    return Path(__file__).resolve().parent.parent


def ensure_local_install(skill_path: Path) -> None:
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    global_skills_dir = codex_home / "skills"
    if global_skills_dir in skill_path.parents:
        raise SystemExit(
            "This skill must be used from a project-local directory, not CODEX_HOME."
        )


def log_path_for_date(log_date: date, base_dir: Path) -> Path:
    return base_dir / f"{log_date.strftime('%Y-%m-%d')}.log"


def list_log_files(base_dir: Path) -> list[Path]:
    return sorted(base_dir.glob("*.log"), reverse=True)


def ensure_ascii_english(text: str, label: str) -> None:
    if any(ord(ch) >= 128 for ch in text):
        raise SystemExit(f"{label} must be English ASCII only.")


def ensure_single_line(text: str, label: str) -> None:
    if "\n" in text or "\r" in text:
        raise SystemExit(f"{label} must be a single line.")


def normalize_bool(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized == "true":
        return True
    if normalized == "false":
        return False
    raise SystemExit("factual must be 'true' or 'false'.")


def validate_ref_level(value: str) -> str:
    if not value:
        raise SystemExit("ref-level must be a non-empty string.")
    if not _REF_LEVEL_RE.match(value):
        raise SystemExit("ref-level must match [A-Za-z0-9._-]+.")
    return value


def format_timestamp(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d:%H:%M")


def format_entry_line(
    entry_id: str,
    ref_level: str,
    factual: bool,
    content: str,
    timestamp: str,
) -> str:
    fact_value = "true" if factual else "false"
    return (
        f"[ID:{entry_id}] [REF:{ref_level}] [FACT:{fact_value}] {content} "
        f"[TIME:{timestamp}]"
    )


def parse_entry_line(line: str) -> Optional[dict]:
    match = ENTRY_RE.match(line.strip())
    if not match:
        return None
    return {
        "id": match.group("id"),
        "ref": match.group("ref"),
        "factual": match.group("factual") == "true",
        "content": match.group("content"),
        "timestamp": match.group("ts"),
    }
