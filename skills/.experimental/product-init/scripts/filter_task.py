#!/usr/bin/env python3
"""Golden-path filter. Score a task description against 7 golden_path_steps.

Step 1 intake; 2 spec; 3 code; 4 test; 5 deploy; 6 handoff; 7 support.
If max score < 0.3 -> DEFER. Else print matched step + confidence.
"""
from __future__ import annotations

import argparse
import re
import sys

KEYWORDS = {
    1: {"intake", "discovery", "interview", "persona", "idea", "brief", "kickoff", "intake-form"},
    2: {"spec", "specification", "requirements", "ac", "acceptance", "user-story", "design", "wireframe", "mockup", "figma"},
    3: {"code", "implement", "build", "refactor", "feature", "endpoint", "component", "frontend", "backend", "api"},
    4: {"test", "tests", "unit", "integration", "e2e", "playwright", "vitest", "jest", "pytest", "coverage", "mutation"},
    5: {"deploy", "release", "preview", "staging", "production", "vercel", "netlify", "ship", "rollback", "smoke"},
    6: {"handoff", "documentation", "docs", "runbook", "credentials", "walkthrough", "knowledge", "transfer", "onboarding"},
    7: {"support", "incident", "warranty", "monitor", "alert", "bugfix", "hotfix", "patch", "maintenance", "follow-up"},
}

STEP_NAMES = {
    1: "Intake",
    2: "Spec",
    3: "Code",
    4: "Test",
    5: "Deploy",
    6: "Handoff",
    7: "Support",
}


def tokenize(text: str):
    return [t.lower() for t in re.findall(r"[A-Za-z][A-Za-z0-9-]+", text)]


def score(tokens, keys):
    if not tokens:
        return 0.0
    hits = sum(1 for t in tokens if t in keys)
    return hits / max(len(tokens), 1) * 5  # boost so single hit on short input passes


def main() -> int:
    p = argparse.ArgumentParser(description="Golden Path filter")
    p.add_argument("task", nargs="+", help="task description")
    args = p.parse_args()
    text = " ".join(args.task)
    tokens = tokenize(text)
    scored = {step: score(tokens, kws) for step, kws in KEYWORDS.items()}
    best_step, best_score = max(scored.items(), key=lambda kv: kv[1])
    if best_score < 0.3:
        print("DEFER: no golden_path_step match")
        return 1
    print(f"golden_path_step={best_step} ({STEP_NAMES[best_step]}) confidence={best_score:.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
