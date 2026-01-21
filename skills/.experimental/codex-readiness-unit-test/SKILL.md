---
name: codex-readiness-unit-test
description: Run the Codex Readiness unit test report. Use when you need deterministic checks plus in-session LLM evals for AGENTS.md/PLANS.md.
metadata:
  short-description: Run Codex Readiness unit test report
---

# LLM Codex Readiness Unit Test

Follow the runbook in `INSTRUCTIONS.md`. All checks run against the current working directory. Each run writes to `.codex-readiness-unit-test/<timestamp>/` and updates `.codex-readiness-unit-test/latest.json`. Keep execution deterministic (filesystem scanning + local command execution only). All LLM evaluation happens in-session and must output strict JSON via the provided prompts.

## Quick Start

1) Collect evidence:
   - `python skills/codex-readiness-unit-test/bin/collect_evidence.py`
2) Run deterministic checks:
   - `python skills/codex-readiness-unit-test/bin/deterministic_rules.py`
3) Run LLM checks using prompts in `prompts/` and store `.codex-readiness-unit-test/<timestamp>/llm_results.json`.
4) If execute mode is requested, build a plan, get confirmation, run:
   - `python skills/codex-readiness-unit-test/bin/run_plan.py --plan .codex-readiness-unit-test/<timestamp>/plan.json`
5) Generate the report:
   - `python skills/codex-readiness-unit-test/bin/scoring.py --mode read-only|execute`

Outputs (per run, under `.codex-readiness-unit-test/<timestamp>/`):
- `report.json`
- `report.html`
- `logs/*` (execute mode)
