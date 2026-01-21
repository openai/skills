# LLM Codex Doctor Unit Test Runbook

This skill produces a deterministic evidence file plus an in-session LLM evaluation, then compiles a JSON report and HTML scorecard. It requires no OpenAI API key and makes no external HTTP calls.

## Minimal Inputs
- `mode`: `read-only` or `execute` (required)
- `soft_timeout_seconds`: optional (default 600)

## Modes (Read-only vs Execute)
- **Read-only**: Collect evidence, run deterministic rules, and run LLM checks #3–#5. No commands are executed, check #6 is marked `NOT_RUN`, and no execution logs/summary are produced.
- **Execute**: Everything in read-only **plus** a confirmed `plan.json` is executed via `run_plan.py`. This enables check #6 and produces execution logs + `execution_summary.json` for scoring.

Always ask the user which mode to run (read-only vs. execute) before proceeding.

## Check Types
- **Deterministic**: filesystem-only checks (#1 AGENTS.md exists, #2 PLANS.md exists, #3 AGENTS.md <= 300 lines, #4 config.toml exists at repo root, repo .codex/, or user .codex/)
- **LLM**: in-session Codex evaluation (#3 project context, #4 commands, #5 loops; commands may live in AGENTS or referenced skills)
- **Hybrid**: deterministic execution + LLM rationale (#6 execution)

Skill references are discovered from AGENTS.md via `$SkillName` or `.codex/skills/<name>` patterns; their `SKILL.md` files are added to evidence for the LLM checks.

All checks run relative to the current working directory and are defined in `skills/codex-doctor-unit-test/checks/checks.json`, weighted equally by default. Each run writes outputs to `.codex-doctor-unit-test/<timestamp>/` and updates `.codex-doctor-unit-test/latest.json`.
The helper scripts read `.codex-doctor-unit-test/latest.json` by default to locate the latest run directory.

## Strict JSON + Retry Loop (Required)
For each LLM/HYBRID check:
1) Run the specialized prompt expecting **strict JSON**.
2) If JSON is invalid or missing keys, run `skills/codex-doctor-unit-test/prompts/json_fix.md` with the raw output.
3) Retry up to **2 additional attempts** (max 3 total).
4) If still invalid: mark the check as **WARN** with rationale: "Invalid JSON from evaluator after retries".

The JSON schema is:
```json
{
  "status": "PASS|WARN|FAIL|NOT_RUN",
  "rationale": "string",
  "evidence_quotes": [{"path":"...","quote":"..."}],
  "recommendations": ["..."],
  "confidence": 0.0
}
```

## Single Confirmation (Required)
Combine the command summary and execute plan into **one** concise confirmation step. Present:
- The extracted build/test/dev loop commands (human-readable, labeled).
- The planned execute details (cwd, ordered commands, soft timeout policy, env).
Ask for a single confirmation to proceed. **Do not** paste raw JSON, full evidence, or the full `plan.json`. If declined, mark execute-required checks as `NOT_RUN`.

## Required Files
- `.codex-doctor-unit-test/<timestamp>/evidence.json` (from `collect_evidence.py`)
- `.codex-doctor-unit-test/<timestamp>/deterministic_results.json` (from `deterministic_rules.py`)
- `.codex-doctor-unit-test/<timestamp>/llm_results.json` (from in-session prompts)
- `.codex-doctor-unit-test/<timestamp>/execution_summary.json` (execute mode only)
- `.codex-doctor-unit-test/<timestamp>/report.json` and `.codex-doctor-unit-test/<timestamp>/report.html` (from `scoring.py`)
- `.codex-doctor-unit-test/<timestamp>/summary.json` (structured pass/fail summary from `scoring.py`)
- `.codex-doctor-unit-test/latest.json` (stable pointer to the latest run directory)

## Prompt Mapping
- #3 `project_context_specified` → `skills/codex-doctor-unit-test/prompts/project_context.md`
- #4 `build_test_commands_exist` → `skills/codex-doctor-unit-test/prompts/commands.md`
- #5 `dev_build_test_loops_documented` → `skills/codex-doctor-unit-test/prompts/loop_quality.md`
- #6 `dev_build_test_loop_execution` → `skills/codex-doctor-unit-test/prompts/execution_explanation.md`

## plan.json schema (execute mode)
```json
{
  "project_dir": "relative/or/absolute/path (optional)",
  "cwd": "optional/absolute/path (defaults to current directory)",
  "commands": [
    {"label": "setup", "cmd": "npm install"},
    {"label": "build", "cmd": "npm run build"},
    {"label": "test", "cmd": "npm test"}
  ],
  "env": {
    "EXAMPLE": "value"
  }
}
```
Place `plan.json` inside the run directory (e.g., `.codex-doctor-unit-test/<timestamp>/plan.json`).

## llm_results.json schema
```json
{
  "project_context_specified": {"status":"PASS","rationale":"...","evidence_quotes":[],"recommendations":[],"confidence":0.7},
  "build_test_commands_exist": {"status":"PASS","rationale":"...","evidence_quotes":[],"recommendations":[],"confidence":0.7},
  "dev_build_test_loops_documented": {"status":"WARN","rationale":"...","evidence_quotes":[],"recommendations":[],"confidence":0.6},
  "dev_build_test_loop_execution": {"status":"PASS","rationale":"...","evidence_quotes":[],"recommendations":[],"confidence":0.6}
}
```

## Scoring Rules
- PASS = 100% of weight
- WARN = 50% of weight
- FAIL/NOT_RUN = 0%
- Overall status: FAIL if any FAIL; else WARN if any WARN or NOT_RUN; else PASS.

## Safety + Timeouts
- Denylisted commands are **not executed** and marked FAIL.
- Soft timeout defaults to 600s; hard cap defaults to 3x soft timeout.
- Execution logs are written to `.codex-doctor-unit-test/<timestamp>/logs/`.
