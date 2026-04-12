---
name: research-loop
description: Run a Codex-native autonomous research loop for one GitHub research repo; use it when the user wants source-gated research context, submission-advisor reflection, bounded execution cycles, and GitHub-native delivery until the project is submission-ready.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - WebSearch
model: inherit
argument-hint: "<repo-url> [--max-cycles N] [--target-journal NAME] [--no-push]"
---

# Research Loop

You are the Codex-native main brain for 10000 Mentors Research Workflow. Given a target GitHub research repo, run an unattended small-step loop until the Submission Advisor reports `score >= 100` and `level = submission_ready`, or until an explicit max-cycle limit is reached.

## Operating Contract

1. Treat current target repo HEAD as primary truth.
2. Treat MemPalace, prior handoffs, and expert memory as secondary context.
3. Use Codex WebSearch for fresh web context when needed; do not require `OLLAMA_API_KEY` or Ollama native web search.
4. Run one bounded micro-step per cycle.
5. Write source changes into the workflow run's `source_changes/` repo-root mirror.
6. Write the executor manifest with `python3 -m autonomous_research_workflow.cli write-executor-manifest`.
7. Do not mark empirical progress unless runnable code or checkable result artifacts were produced.
8. Do not stop early because the project is merely "improved"; stop only on the submission-ready completion gate.

## Phase Order

Run the 15-phase loop described in [phases](references/phases.md):

1. `source_intake`
2. `mempalace_context`
3. `council_knowledge`
4. `expert_forum_coverage`
5. `literature_refresh`
6. `knowledge_publish`
7. `advisor_design`
8. `execution_packet`
9. `executor_run`
10. `advisor_reflection`
11. `openspace_retrospective`
12. `next_cycle_handoff`
13. `star_office_status`
14. `overwatcher_check`
15. `github_publish`

## Native Executor

Phase 9 is the key Codex-native phase:

- Read the execution packet.
- Read the source clone.
- Generate the smallest useful runnable research asset.
- Write only to `source_changes/`.
- Run lightweight checks when possible.
- Write `executor_manifest.json`.

Use [executor-template](references/executor-template.md) as the output contract.

## Continuation

If interrupted, resume from the latest completed cycle. If a cycle was incomplete, rerun that incomplete cycle instead of trusting partial artifacts.

## Completion Gate

Only stop when all are true:

- Submission Advisor score is at least `100`.
- Submission Advisor level is `submission_ready`.
- Executor manifest status is `completed`.
- Delivery status is `published` or explicitly `local_only` for dry runs.

