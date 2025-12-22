from __future__ import annotations

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
INIT_LOG_NAME = "init.log"
AGENTS_FILE_NAME = "AGENTS.MD"


def log_base_dir(create: bool = False) -> Path:
    base_dir = Path.cwd() / "easy-memory"
    if create:
        base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir


def log_path_for_date(log_date: date, base_dir: Path) -> Path:
    return base_dir / f"{log_date.strftime('%Y-%m-%d')}.log"


def list_log_files(base_dir: Path) -> list[Path]:
    if not base_dir.exists():
        return []
    return sorted(base_dir.glob("*.log"), reverse=True)


def init_log_path(base_dir: Path) -> Path:
    return base_dir / INIT_LOG_NAME


def skill_install_dir() -> Path:
    return Path(__file__).resolve().parents[1]


def init_rules_block(blocked_path: Path) -> str:
    blocked_text = str(blocked_path)
    return "\n".join(
        [
            "## easy-memory rules",
            "- Before executing any task, you must use the `easy-memory` skill "
            "and strictly follow all rules and constraints in its `SKILL.md`.",
            f"- The absolute usage path for easy-memory scripts is `{blocked_text}`.",
        ]
    )


def ensure_initialized(base_dir: Path) -> None:
    init_log = init_log_path(base_dir)
    if init_log.exists():
        return

    base_dir.mkdir(parents=True, exist_ok=True)

    rules_block = init_rules_block(skill_install_dir())
    agents_path = Path.cwd() / AGENTS_FILE_NAME
    if agents_path.exists():
        existing = agents_path.read_text(encoding="utf-8")
        if existing and not existing.endswith("\n"):
            existing += "\n"
        if existing.strip():
            existing += "\n"
        existing += f"{rules_block}\n"
        agents_path.write_text(existing, encoding="utf-8")
    else:
        agents_path.write_text(f"{rules_block}\n", encoding="utf-8")

    date_stamp = date.today().isoformat()
    init_log_content = f"{rules_block}\nDate: {date_stamp}\n"
    init_log.write_text(init_log_content, encoding="utf-8")


def require_initialized(base_dir: Path) -> None:
    init_log = init_log_path(base_dir)
    if not base_dir.exists() or not init_log.exists():
        raise SystemExit(
            "Initialization required. Run `python3 scripts/init_memory.py` "
            "from the project root."
        )


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
