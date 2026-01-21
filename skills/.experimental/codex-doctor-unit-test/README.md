# LLM Codex Doctor Unit Test

Instruction-first, in-session "doctor" for evaluating AGENTS/PLANS documentation quality without any external APIs or SDKs. All LLM evaluation is performed by the current Codex session. Scripts are deterministic (filesystem scanning + command execution only).

Primary outputs (per run, under `.codex-doctor-unit-test/<timestamp>/`):
- `report.json`
- `report.html`
- `summary.json`
- `logs/*` (execute mode only)

## Scope
All checks run against the current working directory (cwd). No monorepo discovery is performed. Each run writes to `.codex-doctor-unit-test/<timestamp>/` and updates `.codex-doctor-unit-test/latest.json`.

## HOW TO RUN

### Read-only mode
1) Collect evidence (AGENTS plus any referenced skills; `$SkillName` or `.codex/skills/<name>` in AGENTS):

```bash
python skills/codex-doctor-unit-test/bin/collect_evidence.py
```

2) Run deterministic rules (#1, #2). These commands target the latest run automatically:

```bash
python skills/codex-doctor-unit-test/bin/deterministic_rules.py
```

3) Run in-session LLM checks (#3, #4, #5) for the cwd, save results to `.codex-doctor-unit-test/<timestamp>/llm_results.json` (use `.codex-doctor-unit-test/latest.json` to find the run dir).

4) Build report + HTML scorecard:

```bash
python skills/codex-doctor-unit-test/bin/scoring.py --mode read-only
```

### Execute mode
1) Collect evidence + deterministic rules (same as read-only).
2) Build `.codex-doctor-unit-test/<timestamp>/plan.json` with the extracted commands and get whole-plan confirmation.
3) Execute the plan (use `.codex-doctor-unit-test/latest.json` to find the run dir):

```bash
python skills/codex-doctor-unit-test/bin/run_plan.py --plan .codex-doctor-unit-test/<timestamp>/plan.json
```

4) Run in-session LLM checks (#3–#6) and save `.codex-doctor-unit-test/<timestamp>/llm_results.json`.
5) Build report + HTML scorecard:

```bash
python skills/codex-doctor-unit-test/bin/scoring.py --mode execute
```

See `INSTRUCTIONS.md` for the runbook, strict JSON retry loop, and file schemas.
