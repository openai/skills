#!/usr/bin/env python3
"""Search a Codex plugin index."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


TOKEN_RE = re.compile(r"[a-zA-Z0-9\u4e00-\u9fff]+")
STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "build",
    "by",
    "can",
    "create",
    "do",
    "does",
    "for",
    "from",
    "generate",
    "help",
    "in",
    "into",
    "is",
    "make",
    "of",
    "on",
    "or",
    "the",
    "to",
    "use",
    "using",
    "with",
}
MATCH_FIELDS = (
    "name",
    "display_name",
    "description",
    "category",
    "keywords",
    "capabilities",
    "companion_surfaces",
)


def tokenize(text: str) -> list[str]:
    """Return lowercase search tokens from text."""
    return [match.group(0).lower() for match in TOKEN_RE.finditer(text)]


def normalize_token(token: str) -> str:
    """Normalize simple English plural forms for lightweight matching."""
    if not token.isascii():
        return token
    if len(token) > 4 and token.endswith("ies"):
        return token[:-3] + "y"
    if (
        len(token) > 4
        and token.endswith("es")
        and token.endswith(("ses", "xes", "zes", "ches", "shes"))
    ):
        return token[:-2]
    if len(token) > 3 and token.endswith("s") and not token.endswith(("ss", "is", "us")):
        return token[:-1]
    return token


def normalized_tokens(text: str) -> list[str]:
    """Return lowercase tokens with simple plural normalization."""
    return [normalize_token(token) for token in tokenize(text)]


def significant_terms(text: str) -> dict[str, str]:
    """Return normalized query terms mapped to display terms."""
    terms = {}
    for display_token in tokenize(text):
        normalized = normalize_token(display_token)
        if normalized in STOPWORDS:
            continue
        if len(normalized) == 1 and normalized.isascii():
            continue
        terms.setdefault(normalized, display_token)
    return terms


def load_index(path: Path) -> dict[str, Any]:
    """Read a plugin index from JSON."""
    return json.loads(path.read_text(encoding="utf-8"))


def field_text(value: Any) -> str:
    """Normalize scalar or list metadata fields into searchable text."""
    if isinstance(value, list):
        return " ".join(str(item) for item in value if item is not None)
    if value is None:
        return ""
    return str(value)


def matched_fields(plugin: dict[str, Any], query_terms: dict[str, str]) -> dict[str, list[str]]:
    """Return field-level token matches for one plugin."""
    matches = {}
    for field in MATCH_FIELDS:
        field_terms = set(normalized_tokens(field_text(plugin.get(field))))
        matched = sorted(display for term, display in query_terms.items() if term in field_terms)
        if matched:
            matches[field] = matched
    return matches


def format_matched_fields(fields: dict[str, list[str]]) -> str:
    """Render field-level matches in a stable order."""
    parts = []
    for field in MATCH_FIELDS:
        terms = fields.get(field)
        if terms:
            parts.append(f"{field} ({', '.join(terms)})")
    return ", ".join(parts) if parts else "indexed metadata"


def positive_int(value: str) -> int:
    """Argparse type for positive integer limits."""
    parsed = int(value)
    if parsed < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return parsed


def search(index: dict[str, Any], query: str, limit: int = 5) -> list[dict[str, Any]]:
    """Search plugins by significant query terms contained in metadata fields."""
    if limit < 1:
        raise ValueError("limit must be positive")

    query_terms = significant_terms(query)
    if not query_terms:
        return []

    results = []

    for plugin in index.get("plugins", []):
        fields = matched_fields(plugin, query_terms)
        if not fields:
            continue

        matched_terms = sorted({term for terms in fields.values() for term in terms})
        result = dict(plugin)
        result["score"] = len(matched_terms)
        result["matched_terms"] = matched_terms
        result["matched_fields"] = fields
        results.append(result)

    results.sort(
        key=lambda item: (
            -item["score"],
            str(item.get("display_name") or item.get("name") or "").lower(),
        )
    )
    return results[:limit]


def render_results(results: list[dict[str, Any]], index: dict[str, Any]) -> str:
    """Render search results as Markdown-ish recommendations."""
    boundary = "Results only cover openai/plugins"
    source = index.get("source") or {}
    commit = source.get("commit")
    lines = [boundary]
    if commit:
        lines[0] = f"{lines[0]} (commit: {commit})"

    if not results:
        lines.extend(
            [
                "",
                "No strong match was found in openai/plugins.",
                "Try broadening the query or manually inspecting https://github.com/openai/plugins.",
            ]
        )
        return "\n".join(lines)

    lines.append("")
    for position, plugin in enumerate(results, start=1):
        display_name = plugin.get("display_name") or plugin.get("name") or "Unknown plugin"
        name = plugin.get("name") or display_name
        category = plugin.get("category") or "Uncategorized"
        matched_terms = ", ".join(plugin.get("matched_terms") or [])
        fields = format_matched_fields(plugin.get("matched_fields") or {})
        location = plugin.get("repository") or plugin.get("homepage") or plugin.get("plugin_path") or ""
        score = plugin.get("score", 0)

        lines.append(f"{position}. {display_name} ({name})")
        lines.append(f"   Category: {category}")
        lines.append(f"   Why it matches: matched query terms {matched_terms or 'none'} in indexed plugin metadata.")
        lines.append(f"   Matched fields: {fields}")
        lines.append(f"   Source: {location}")
        lines.append(f"   Confidence: {score} matched term(s); inspect the manifest before installing.")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query")
    parser.add_argument("--index", type=Path, default=Path("index/plugins-index.json"))
    parser.add_argument("--limit", type=positive_int, default=5)
    args = parser.parse_args()

    index = load_index(args.index)
    print(render_results(search(index, args.query, limit=args.limit), index))


if __name__ == "__main__":
    main()
