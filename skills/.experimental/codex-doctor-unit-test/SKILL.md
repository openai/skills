---
name: codex-doctor-unit-test
description: Run the Codex Doctor unit test report. Use when you need deterministic checks plus in-session LLM evals for AGENTS.md/PLANS.md.
metadata:
  short-description: Run Codex Doctor unit test report
---

# LLM Codex Doctor Unit Test

Follow the runbook in `INSTRUCTIONS.md`. All checks run against the current working directory. Each run writes to `.codex-doctor-unit-test/<timestamp>/` and updates `.codex-doctor-unit-test/latest.json`. Keep execution deterministic (filesystem scanning + local command execution only). All LLM evaluation happens in-session and must output strict JSON via the provided prompts.

## Quick Start

1) Collect evidence:
   - `python skills/codex-doctor-unit-test/bin/collect_evidence.py`
2) Run deterministic checks:
   - `python skills/codex-doctor-unit-test/bin/deterministic_rules.py`
3) Run LLM checks using prompts in `prompts/` and store `.codex-doctor-unit-test/<timestamp>/llm_results.json`.
4) If execute mode is requested, build a plan, get confirmation, run:
   - `python skills/codex-doctor-unit-test/bin/run_plan.py --plan .codex-doctor-unit-test/<timestamp>/plan.json`
5) Generate the report:
   - `python skills/codex-doctor-unit-test/bin/scoring.py --mode read-only|execute`

Outputs (per run, under `.codex-doctor-unit-test/<timestamp>/`):
- `report.json`
- `report.html`
- `logs/*` (execute mode)
