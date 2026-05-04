#!/usr/bin/env python3
"""Gate 1 - Discovery Constitution audit.

Checks PRODUCT.md, SPEC.md, PLAN.md, TASKS.md, COMPETITIVE_BENCHMARK.md exist,
have valid frontmatter, required sections, single-sentence Golden Path,
and that all 14 mandatory discovery questions are answered.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.report import Report, Severity  # noqa: E402

try:
    import frontmatter  # python-frontmatter
except ImportError:
    frontmatter = None


REQUIRED_FILES = {
    "PRODUCT.md": ["Golden Path", "Persona", "Outcome Metric"],
    "SPEC.md": ["Scope", "Acceptance"],
    "PLAN.md": ["Appetite", "Kill Criteria", "Deferred"],
    "TASKS.md": ["Tasks"],
    "COMPETITIVE_BENCHMARK.md": ["Benchmark"],
}

QUESTIONS = [
    ("Q1", r"golden\s*path"),
    ("Q2", r"persona"),
    ("Q3", r"current\s*alternative"),
    ("Q4", r"10[- ]?min(ute)?\s*success"),
    ("Q5", r"outcome\s*metric"),
    ("Q6", r"riskiest\s*assumption"),
    ("Q7", r"(four[- ]?risk|value.*usability.*feasibility.*viability)"),
    ("Q8", r"appetite"),
    ("Q9", r"kill\s*criteria"),
    ("Q10", r"rabbit\s*hole"),
    ("Q11", r"deferred"),
    ("Q12", r"(competitive\s*benchmark|v0|bolt|lovable|railway)"),
    ("Q13", r"(discovery\s*cadence|weekly\s*touchpoint)"),
    ("Q14", r"golden_path_step"),
]


def load_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def has_frontmatter(text: str) -> bool:
    if frontmatter is not None:
        try:
            post = frontmatter.loads(text)
            return bool(post.metadata)
        except Exception:
            return False
    return text.lstrip().startswith("---")


def extract_section(text: str, heading: str) -> str:
    # Match any heading line whose visible text contains `heading` (case-insensitive substring).
    heading_line_re = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*$", re.MULTILINE)
    needle = heading.lower()
    match = None
    for m in heading_line_re.finditer(text):
        title = m.group(2).strip()
        if needle in title.lower():
            match = m
            break
    if not match:
        return ""
    matched_level = len(match.group(1))
    start = match.end()
    # Next "section boundary" is a heading at the same or higher level (fewer-or-equal #s).
    boundary_pattern = r"^#{1," + str(matched_level) + r"}[ \t]+"
    nxt = re.search(boundary_pattern, text[start:], re.MULTILINE)
    return text[start: start + nxt.start()] if nxt else text[start:]


def is_filled(body: str) -> bool:
    cleaned = re.sub(r"\[FILL[^\]]*\]", "", body, flags=re.IGNORECASE).strip()
    return len(cleaned) > 5


def audit(project_dir: Path) -> Report:
    rep = Report(name="gate1-discovery-constitution")
    gate = "Gate 1: Discovery"

    for fname, sections in REQUIRED_FILES.items():
        path = project_dir / fname
        if not path.exists():
            rep.add_finding(
                Severity.CRITICAL,
                gate,
                f"file-exists:{fname}",
                f"missing {path}",
                f"Create {fname} from templates/",
            )
            continue
        text = load_text(path)
        if not has_frontmatter(text):
            rep.add_finding(
                Severity.HIGH,
                gate,
                f"frontmatter:{fname}",
                "no YAML frontmatter detected",
                "Add `---` block with name/description/version",
            )
        for sec in sections:
            body = extract_section(text, sec)
            if not body or not is_filled(body):
                rep.add_finding(
                    Severity.HIGH,
                    gate,
                    f"section:{fname}#{sec}",
                    "section missing or unfilled",
                    f"Fill `## {sec}` in {fname}",
                )

    # Golden Path single-sentence check
    product_path = project_dir / "PRODUCT.md"
    if product_path.exists():
        body = extract_section(load_text(product_path), "Golden Path")
        sentence = body.strip().split("\n")
        sentence = [s for s in sentence if s.strip() and not s.strip().startswith("#")]
        joined = " ".join(sentence).strip()
        # one sentence: exactly one sentence terminator
        terminators = re.findall(r"[.!?](\s|$)", joined)
        if not joined:
            rep.add_finding(
                Severity.CRITICAL, gate,
                "golden-path:one-sentence",
                "Golden Path empty",
                "Write exactly one sentence describing user-to-deployed-product flow.",
            )
        elif len(terminators) != 1:
            rep.add_finding(
                Severity.HIGH, gate,
                "golden-path:one-sentence",
                f"found {len(terminators)} sentence terminators",
                "Reduce Golden Path to exactly one sentence.",
            )

    # 14 questions
    aggregate = "\n\n".join(
        load_text(project_dir / f) for f in REQUIRED_FILES if (project_dir / f).exists()
    ).lower()
    for qid, pat in QUESTIONS:
        if not re.search(pat, aggregate, re.IGNORECASE):
            rep.add_finding(
                Severity.HIGH, gate,
                f"question:{qid}",
                f"no match for /{pat}/ in discovery docs",
                f"Answer {qid} explicitly in PRODUCT.md/PLAN.md.",
            )
    return rep


def main() -> int:
    p = argparse.ArgumentParser(description="Gate 1: Discovery Constitution audit")
    p.add_argument("--project-dir", default=".")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    rep = audit(Path(args.project_dir).resolve())
    print(rep.to_json() if args.json else rep.to_markdown())
    return rep.exit_code


if __name__ == "__main__":
    sys.exit(main())
