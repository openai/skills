---
name: ralph-wiggum-loop
description: Run a single-process monolithic orchestrator loop over one repository/problem space with exactly one planned change and one verification pass per iteration, persistent .ralph state, failure-domain logging, and offline demo repair. Use when users want autonomous incremental repair/refactor loops with resumability and strict iteration contracts.
---

# Ralph Wiggum Loop

Run a deterministic, single-process orchestrator that plans one change-set, applies it, verifies once, and records iteration state. Use this skill for goal-driven local repair/refactor loops with resumability and strict per-iteration contracts.

## Workflow

1. Generate or choose a target repository.
2. Prepare a config (or CLI overrides) including `goal`, `repo_path`, `test_command`, and `acceptance_criteria`.
3. Run `scripts/ralph_loop.py` in `auto` or `step` mode.
4. Inspect `.ralph/` artifacts for iteration history, failure domains, and last patch.

## LLM Adapters

- `llm.adapter=stub`:
  - Offline deterministic behavior for demo repair (`RALPH_FIXME:addition_bug` path).
  - No API key required.
- `llm.adapter=openai`:
  - Uses OpenAI Chat Completions with strict JSON change-set parsing.
  - Required env var defaults to `OPENAI_API_KEY` (configurable via `llm.api_key_env`).
  - Configurable fields: `llm.model`, `llm.base_url`, `llm.api_key_env`, `llm.timeout_seconds`.
  - Context controls: `llm.context_max_files`, `llm.context_max_chars_per_file`, `llm.context_max_total_chars`.

## Patch Apply Safety

- `replace_text` first tries exact target matching.
- If exact target is missing, fuzzy fallback is allowed only when:
  - best similarity is `>= fuzzy_min_similarity` (default `0.94`)
  - and best-vs-second score gap is `>= fuzzy_min_gap` (default `0.03`)
- Empty change sets are treated as explicit no-op (`mode=no_op`) instead of failure.

## Commands

```bash
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export RALPH_DIR="$CODEX_HOME/skills/ralph-wiggum-loop"

# Generate offline demo repo with failing tests
python3 "$RALPH_DIR/scripts/demo_repo_generator.py" --output /tmp/ralph-demo

# Run loop against demo
python3 "$RALPH_DIR/scripts/ralph_loop.py" \
  --goal "Make tests pass" \
  --repo_path /tmp/ralph-demo \
  --test_command "python3 -m unittest -q" \
  --mode auto \
  --max_iterations 5

# Or run via config
python3 "$RALPH_DIR/scripts/ralph_loop.py" --config "$RALPH_DIR/references/config.example.yaml"

# OpenAI-backed run (optional)
export OPENAI_API_KEY="<set-your-api-key>"
python3 "$RALPH_DIR/scripts/ralph_loop.py" \
  --config "$RALPH_DIR/references/config.example.yaml"
```

## Independence and Integration

- Standalone: this skill can operate by itself with local verification commands.
- Optional integration with `$auto-memory`: use memory snapshots for richer iteration context.
- Optional integration with `$self-improve`: use one-change + gate decisions as acceptance wrapper around Ralph iterations.

## Read-only audit overlay pilot

Use this when you need a bounded comparison between your normal Ralph control loop and a read-only audit companion.

```bash
export RALPH_DIR="$CODEX_HOME/skills/ralph-wiggum-loop"

python3 "$RALPH_DIR/scripts/evaluate_ralph_readonly_overlay.py" \
  --project ralph-loop-eval \
  --repo-path /path/to/repo \
  --goal "Repair repository until tests pass." \
  --control-runs 6 \
  --readonly-runs 6 \
  --acceptance-criteria tests_pass
```

Each trigger creates:
- one run note named `Ralph Loop Evaluation Run / <run_id>`
- one aggregate note named `Ralph Loop Evaluation Aggregate / <YYYY-MM-DD>`
- an `output-last-message.txt` artifact in `~/.codex/tmp/ralph-readonly-audit-pilot` (or custom `--artifacts-dir`)

`output-last-message.txt` uses additive schema `v1.1` (backward compatible):
- existing keys are preserved
- added keys include:
  - `schema_version`, `timestamp_utc`
  - `decision`, `readonly`, `changed_in_readonly`
  - `search_enabled`, `search_disabled_simulated`
  - `verification_failure_injected`, `compaction_cycle_injected`, `compaction_checkpoint_id`
  - `acceptance_criteria`, `test_command`

Search-disabled simulation metadata is explicit:
- `search_enabled=false` on the configured trigger index
- `search_disabled_simulated=true` only on that trigger

Pilot prompt template for a separate evaluator:
`references/loop_evaluation_agent_prompt.md`

## Behavior Guarantees

- Single-process loop owner for planning, patching, verification, and state.
- Exact per-iteration sequence:
  `load_context()` -> `plan_step()` -> `call_llm()`/`call_tool()` -> `apply_changes()` -> `run_verification()` -> `record_iteration()`.
- Exactly one planned change-set and one verification pass per iteration.
- Persistent `.ralph/` state with resumable execution.
- Failure-domain classification and operator levers appended to `.ralph/failures.md` each iteration.

## Files In This Skill

- `scripts/ralph_loop.py`: Main orchestrator loop.
- `scripts/demo_repo_generator.py`: Offline demo repo creator.
- `references/config.example.yaml`: Config template.
- `references/prompt_template.md`: Prompt composition template used each iteration.
- `references/failure_domains.md`: Failure taxonomy and operator guidance.
- `requirements.txt`: Minimal dependency set.

## Agent Team Protocol Adapter (2026-02-19)

Use this adapter when Ralph runs as a `Builder` under `/Users/maleick/.codex/skills/agent-team-protocol`.

- Keep Ralph as the change executor only.
- Emit protocol-compatible handoff fields after each iteration.
- Keep bounded policy intact: one change-set, one verification pass.
- Route completion through `review` before final acceptance.

Reference: `references/agent-team-protocol-adapter.md`
