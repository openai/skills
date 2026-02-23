#!/usr/bin/env python3
"""Build a Swift Evolution implemented-concurrency proposal index.

Usage:
  scripts/build_implemented_proposals_index.py --output references/implemented-proposals.md
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


EVOLUTION_JSON_URL = "https://download.swift.org/swift-evolution/v1/evolution.json"

# These proposals are concurrency-relevant but do not match link-based keywords.
MANUAL_INCLUDE_IDS = {"SE-0282", "SE-0310", "SE-0430"}

# Link filename keyword filter keeps relevance high and avoids summary false positives.
LINK_KEYWORD_RE = re.compile(
    r"(async|await|actor|concurr|sendable|isolat|task|executor|clock|stream|continuation|distributed)",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Proposal:
    proposal_id: str
    version: str
    title: str
    link: str

    @property
    def number(self) -> int:
        try:
            return int(self.proposal_id.split("-")[1])
        except Exception as exc:  # pragma: no cover - defensive parsing
            raise ValueError(f"Unexpected proposal id format: {self.proposal_id}") from exc

    @property
    def github_url(self) -> str:
        return f"https://github.com/swiftlang/swift-evolution/blob/main/proposals/{self.link}"


def fetch_json(source: str) -> dict:
    if os.path.exists(source):
        return json.loads(Path(source).read_text(encoding="utf-8"))

    try:
        with urllib.request.urlopen(source, timeout=30) as response:
            return json.load(response)
    except Exception:
        # Fallback for environments where Python networking is restricted but curl works.
        result = subprocess.run(
            ["curl", "-sS", source],
            check=True,
            capture_output=True,
            text=True,
        )
        return json.loads(result.stdout)


def is_relevant(entry: dict) -> bool:
    if entry.get("status", {}).get("state") != "implemented":
        return False

    proposal_id = entry.get("id", "")
    if proposal_id in MANUAL_INCLUDE_IDS:
        return True

    link = entry.get("link", "")
    return bool(LINK_KEYWORD_RE.search(link))


def iter_relevant_proposals(payload: dict) -> Iterable[Proposal]:
    for entry in payload.get("proposals", []):
        if not is_relevant(entry):
            continue
        yield Proposal(
            proposal_id=entry["id"],
            version=entry.get("status", {}).get("version", ""),
            title=entry["title"],
            link=entry["link"],
        )


def render_markdown(payload: dict, proposals: list[Proposal]) -> str:
    lines: list[str] = []
    lines.append("# Implemented Concurrency-Relevant Swift Evolution Proposals")
    lines.append("")
    lines.append(
        "Snapshot source: `https://download.swift.org/swift-evolution/v1/evolution.json`"
    )
    lines.append(f"- `creationDate`: `{payload.get('creationDate', 'unknown')}`")
    lines.append(f"- `commit`: `{payload.get('commit', 'unknown')}`")
    lines.append(f"- `selected proposals`: `{len(proposals)}`")
    lines.append("")
    lines.append("Selection rules:")
    lines.append("- Include only proposals where `status.state == implemented`.")
    lines.append(
        "- Include proposals whose `link` filename matches concurrency keywords (`async`, `actor`, `task`, `sendable`, `isolat`, `executor`, `stream`, `clock`, `continuation`, `distributed`, `concurr`)."
    )
    lines.append("- Also include manual IDs: `SE-0282`, `SE-0310`, `SE-0430`.")
    lines.append("")
    lines.append("| Proposal | Implemented | Title | Link |")
    lines.append("|---|---:|---|---|")
    for proposal in proposals:
        lines.append(
            f"| `{proposal.proposal_id}` | `{proposal.version}` | {proposal.title} | [view]({proposal.github_url}) |"
        )
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        required=True,
        help="Output markdown file path (e.g. references/implemented-proposals.md)",
    )
    parser.add_argument(
        "--source",
        default=EVOLUTION_JSON_URL,
        help=(
            "Swift Evolution JSON source URL or local file path "
            f"(default: {EVOLUTION_JSON_URL})"
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_path = Path(args.output)

    try:
        payload = fetch_json(args.source)
    except Exception as exc:
        print(f"Failed to fetch evolution JSON: {exc}", file=sys.stderr)
        return 1

    proposals = sorted(iter_relevant_proposals(payload), key=lambda p: p.number)
    markdown = render_markdown(payload, proposals)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")
    print(f"Wrote {output_path} ({len(proposals)} proposals)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
