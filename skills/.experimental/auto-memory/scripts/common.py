#!/usr/bin/env python3
"""Shared helpers for the auto-memory skill."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from datetime import datetime, timezone
from difflib import SequenceMatcher
import os
from pathlib import Path
from typing import Any

import yaml

REQUIRED_SECTIONS = (
    "Summary",
    "Context",
    "Decision",
    "Rationale",
    "Implementation",
    "Verification",
    "Follow-ups",
    "Changelog",
)

DEFAULT_SECTION_CONTENT = {
    "Summary": "- TODO",
    "Context": "- TODO",
    "Decision": "- TODO",
    "Rationale": "- TODO",
    "Implementation": "- TODO",
    "Verification": "- TODO",
    "Follow-ups": "- TODO",
    "Changelog": "- Initialized.",
}

SECTION_LOOKUP = {name.lower(): name for name in REQUIRED_SECTIONS}

SECRET_PATTERNS = [
    ("openai-key", re.compile(r"\bsk-[A-Za-z0-9]{20,}\b")),
    ("github-token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b")),
    ("aws-access-key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    (
        "credential-assignment",
        re.compile(
            r"(?i)\b(api[_-]?key|token|secret|password|passwd|client[_-]?secret)\b\s*[:=]\s*['\"]?[^'\"\s]{8,}"
        ),
    ),
    (
        "sensitive-var-assignment",
        re.compile(
            r"(?i)\b[A-Z0-9_]*(api[_-]?key|token|secret|password|passwd|client[_-]?secret)[A-Z0-9_]*\b\s*[:=]\s*['\"]?[^'\"\s]{6,}"
        ),
    ),
    ("bearer-token", re.compile(r"(?i)\bbearer\s+[A-Za-z0-9\-_\.=]{20,}")),
    ("high-entropy-token", re.compile(r"\b[A-Za-z0-9+/]{40,}={0,2}\b")),
]

FRONTMATTER_PATTERN = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)
HEADING_PATTERN = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
PLAIN_REQUIRED_HEADING_PATTERN = re.compile(
    r"^(summary|context|decision|rationale|implementation|verification|follow-ups|changelog)$",
    re.IGNORECASE,
)


@dataclass
class NoteRecord:
    path: Path
    frontmatter: dict[str, Any]
    body: str
    title: str
    tags: list[str]
    date: str


class MemoryValidationError(RuntimeError):
    """Raised when user-provided memory inputs are invalid."""


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def get_codex_home() -> Path:
    configured = Path(str(Path.home() / ".codex"))
    env_home = Path(os.environ["CODEX_HOME"]) if "CODEX_HOME" in os.environ else None
    return env_home.expanduser() if env_home else configured


def ensure_project_name(project: str) -> str:
    value = project.strip()
    if not value:
        raise MemoryValidationError("project must not be empty")
    if "/" in value or "\\" in value or "\x00" in value or ".." in value:
        raise MemoryValidationError("project must be a single folder name without path traversal")
    return value


def memory_dir_for_project(project: str) -> Path:
    return get_codex_home() / "memory" / ensure_project_name(project)


def env_dir_for_project(project: str) -> Path:
    return get_codex_home() / "env" / ensure_project_name(project)


def parse_frontmatter(content: str) -> tuple[dict[str, Any], str]:
    match = FRONTMATTER_PATTERN.match(content)
    if not match:
        return {}, content.strip()
    frontmatter = yaml.safe_load(match.group(1)) or {}
    if not isinstance(frontmatter, dict):
        frontmatter = {}
    body = content[match.end() :].strip()
    return frontmatter, body


def render_note(frontmatter: dict[str, Any], body: str) -> str:
    frontmatter_text = yaml.safe_dump(frontmatter, sort_keys=False, allow_unicode=False).strip()
    normalized_body = body.strip() + "\n"
    return f"---\n{frontmatter_text}\n---\n\n{normalized_body}"


def read_note(path: Path) -> NoteRecord:
    content = path.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(content)
    title = str(frontmatter.get("title") or path.stem).strip() or path.stem
    date = str(frontmatter.get("date") or "").strip()
    raw_tags = frontmatter.get("tags") or []
    tags: list[str] = []
    if isinstance(raw_tags, str):
        tags = [tag.strip() for tag in raw_tags.split(",") if tag.strip()]
    elif isinstance(raw_tags, list):
        tags = [str(tag).strip() for tag in raw_tags if str(tag).strip()]
    return NoteRecord(path=path, frontmatter=frontmatter, body=body, title=title, tags=tags, date=date)


def write_note(path: Path, frontmatter: dict[str, Any], body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_note(frontmatter, body), encoding="utf-8")


def list_notes(project_dir: Path) -> list[NoteRecord]:
    if not project_dir.exists():
        return []
    notes: list[NoteRecord] = []
    for path in sorted(project_dir.glob("*.md")):
        try:
            notes.append(read_note(path))
        except Exception:
            continue
    return notes


def slugify_title(title: str) -> str:
    ascii_value = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_value.lower()).strip("-")
    return slug or "memory-note"


def next_note_path(project_dir: Path, title: str) -> Path:
    base = slugify_title(title)
    candidate = project_dir / f"{base}.md"
    index = 2
    while candidate.exists():
        candidate = project_dir / f"{base}-{index}.md"
        index += 1
    return candidate


def normalize_title_for_match(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()


def title_similarity(left: str, right: str) -> float:
    return SequenceMatcher(None, normalize_title_for_match(left), normalize_title_for_match(right)).ratio()


def titles_are_near_duplicates(left: str, right: str, threshold: float = 0.88) -> bool:
    left_normalized = normalize_title_for_match(left)
    right_normalized = normalize_title_for_match(right)
    if not left_normalized or not right_normalized:
        return False
    if left_normalized == right_normalized:
        return True
    similarity = title_similarity(left, right)
    if similarity >= threshold:
        return True
    left_tokens = set(left_normalized.split())
    right_tokens = set(right_normalized.split())
    if not left_tokens or not right_tokens:
        return False
    overlap = len(left_tokens & right_tokens) / len(left_tokens | right_tokens)
    return overlap >= 0.8


def parse_iso_datetime(raw: str | None) -> datetime:
    if not raw:
        return datetime.fromtimestamp(0, timezone.utc)
    text = raw.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return datetime.fromtimestamp(0, timezone.utc)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def choose_latest_note(notes: list[NoteRecord]) -> NoteRecord:
    return max(notes, key=lambda note: parse_iso_datetime(note.date))


def _contains_escaped_headings(text: str) -> bool:
    if "\\n" not in text:
        return False
    markers = ["\\n## "] + [f"\\n{name}" for name in REQUIRED_SECTIONS]
    return any(marker in text for marker in markers)


def _preprocess_body_text(body: str) -> str:
    text = body.strip()
    if _contains_escaped_headings(text):
        text = text.replace("\\r\\n", "\n").replace("\\n", "\n")
    # Recover malformed heading lines like "- ## Summary".
    text = re.sub(r"(?m)^\s*[-*]\s+##\s+", "## ", text)
    return text


def parse_body_sections(body: str) -> tuple[dict[str, str], list[tuple[str, str]]]:
    text = _preprocess_body_text(body)
    if not text:
        return {}, []

    lines = text.splitlines()
    heading_entries: list[tuple[int, str, bool]] = []
    for index, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue

        markdown_match = re.match(r"^##\s+(.+?)\s*$", stripped)
        if markdown_match:
            heading_raw = markdown_match.group(1).strip()
            canonical = SECTION_LOOKUP.get(heading_raw.lower())
            heading_entries.append((index, canonical or heading_raw, canonical is not None))
            continue

        plain_match = PLAIN_REQUIRED_HEADING_PATTERN.match(stripped)
        if plain_match:
            canonical = SECTION_LOOKUP[plain_match.group(1).lower()]
            heading_entries.append((index, canonical, True))

    if not heading_entries:
        return {}, []

    required: dict[str, str] = {}
    extras: list[tuple[str, str]] = []
    for idx, (line_no, heading_name, is_required) in enumerate(heading_entries):
        next_line_no = heading_entries[idx + 1][0] if idx + 1 < len(heading_entries) else len(lines)
        content = "\n".join(lines[line_no + 1 : next_line_no]).strip()
        if is_required:
            existing = required.get(heading_name, "")
            required[heading_name] = f"{existing}\n{content}".strip() if existing else content
            continue
        extras.append((heading_name, content))
    return required, extras


def _default_freeform_sections(body: str) -> dict[str, str]:
    stripped = body.strip()
    first_line = next((line.strip() for line in stripped.splitlines() if line.strip()), "")
    summary = f"- {first_line}" if first_line else DEFAULT_SECTION_CONTENT["Summary"]
    context = stripped if stripped else DEFAULT_SECTION_CONTENT["Context"]
    return {
        "Summary": summary,
        "Context": context,
        "Decision": DEFAULT_SECTION_CONTENT["Decision"],
        "Rationale": DEFAULT_SECTION_CONTENT["Rationale"],
        "Implementation": DEFAULT_SECTION_CONTENT["Implementation"],
        "Verification": DEFAULT_SECTION_CONTENT["Verification"],
        "Follow-ups": DEFAULT_SECTION_CONTENT["Follow-ups"],
        "Changelog": DEFAULT_SECTION_CONTENT["Changelog"],
    }


def normalize_sections(body: str) -> tuple[dict[str, str], list[tuple[str, str]]]:
    required, extras = parse_body_sections(body)
    if not required:
        required = _default_freeform_sections(body)
        return required, []
    for name in REQUIRED_SECTIONS:
        required[name] = required.get(name, "").strip() or DEFAULT_SECTION_CONTENT[name]
    return required, extras


def _is_meaningful_section(section_name: str, content: str) -> bool:
    text = content.strip()
    if not text:
        return False
    return text != DEFAULT_SECTION_CONTENT[section_name]


def merge_required_sections(existing: dict[str, str], incoming: dict[str, str]) -> dict[str, str]:
    merged: dict[str, str] = {}
    for section_name in REQUIRED_SECTIONS:
        if section_name == "Changelog":
            continue
        incoming_value = incoming.get(section_name, "").strip()
        existing_value = existing.get(section_name, "").strip()
        if _is_meaningful_section(section_name, incoming_value):
            merged[section_name] = incoming_value
        elif _is_meaningful_section(section_name, existing_value):
            merged[section_name] = existing_value
        else:
            merged[section_name] = DEFAULT_SECTION_CONTENT[section_name]
    merged["Changelog"] = existing.get("Changelog", "").strip() or DEFAULT_SECTION_CONTENT["Changelog"]
    return merged


def append_changelog_entry(required_sections: dict[str, str], entry: str) -> None:
    current = required_sections.get("Changelog", "").strip()
    entry_line = f"- {entry}"
    if not current or current == DEFAULT_SECTION_CONTENT["Changelog"]:
        required_sections["Changelog"] = entry_line
        return
    required_sections["Changelog"] = f"{current}\n{entry_line}"


def render_sections(required: dict[str, str], extras: list[tuple[str, str]] | None = None) -> str:
    blocks: list[str] = []
    for section_name in REQUIRED_SECTIONS:
        if section_name == "Changelog":
            continue
        content = required.get(section_name, "").strip() or DEFAULT_SECTION_CONTENT[section_name]
        blocks.append(f"## {section_name}\n{content}")

    for heading, content in extras or []:
        cleaned = content.strip() or "- TODO"
        blocks.append(f"## {heading}\n{cleaned}")

    changelog = required.get("Changelog", "").strip() or DEFAULT_SECTION_CONTENT["Changelog"]
    blocks.append(f"## Changelog\n{changelog}")
    return "\n\n".join(blocks).strip() + "\n"


def normalize_tags(raw_tags: list[str]) -> list[str]:
    tags: list[str] = []
    seen: set[str] = set()
    for tag in raw_tags:
        candidate = re.sub(r"\s+", "-", tag.strip().lower())
        if ":" in candidate:
            key_part, value_part = candidate.split(":", 1)
            key = re.sub(r"[^a-z0-9._-]+", "-", key_part).strip("-")
            value = re.sub(r"[^a-z0-9._-]+", "-", value_part).strip("-")
            if key and value:
                normalized = f"{key}:{value}"
            else:
                normalized = key or value
        else:
            normalized = re.sub(r"[^a-z0-9._-]+", "-", candidate).strip("-")
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        tags.append(normalized)
    return tags


def merge_tags(existing: list[str], incoming: list[str]) -> list[str]:
    merged = existing + incoming
    return normalize_tags(merged)


def detect_secret_indicators(text: str) -> list[str]:
    reasons: list[str] = []
    for line in text.splitlines():
        if "redacted" in line.lower():
            continue
        for label, pattern in SECRET_PATTERNS:
            if pattern.search(line):
                reasons.append(label)
    # Keep the list deterministic while preserving first-seen order.
    deduped: list[str] = []
    seen: set[str] = set()
    for reason in reasons:
        if reason in seen:
            continue
        seen.add(reason)
        deduped.append(reason)
    return deduped
