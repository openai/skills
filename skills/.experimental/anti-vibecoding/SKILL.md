---
name: anti-vibecoding
description: Clarification-first guardrail for coding tasks that prevents premature execution and forces requirement hardening before implementation. Use when users ask to avoid vibecoding, request strict clarifying questions, tune pre-execution tool-call aggressiveness, route work to the relevant current codebase using project memories, enforce naming and architecture decisions, and get milestone coaching reports with mistakes, knowledge gaps, and learning actions.
---

# Anti Vibecoding

## Overview

Enforce a clarification-first workflow before implementation. Route tasks to the correct project using memory signals, ask targeted questions in rounds grounded in the current codebase, gate execution until readiness is green, trace tool usage verbosely, and emit milestone coaching reports.

## Required Operating Contract

1. Start in clarification mode, not implementation mode.
2. Route the task to a relevant project before deep clarification.
3. Search for existing agent or project memories before asking codebase questions.
4. If memory is missing or weak, create a small startup project memory in-session and use it as provisional routing context.
5. Block mutating implementation actions until readiness gate is green.
6. Allow only read-only discovery before green, and only within configured pre-green tool budget.
7. Ask for both micro naming and macro naming decisions.
8. Explain every tool use with a short rationale and confidence impact.
9. Emit a milestone coaching report at each major milestone.

## Parse Runtime Configuration

Extract optional config from user text. Apply defaults when omitted.

```text
mode=<strict|balanced|light|auto>
aggressiveness=<1-5>
pre_green_tool_budget=<int>
milestone_reporting=<on|off>
memory_strategy=<discover-first|always-bootstrap|hybrid>
project_hint=<path|name>
```

Default values:

- `mode=auto`
- `aggressiveness=3`
- `milestone_reporting=on`
- `memory_strategy=hybrid`
- `pre_green_tool_budget` derives from `mode` unless explicitly overridden

Mode mapping:

- `strict`: budget `0`
- `balanced`: budget `3`
- `light`: budget `8`
- `auto`: choose with `references/gating_rubric.md`

`aggressiveness` meaning:

- `1`: ask only blocking questions
- `2`: ask blocking plus one quality pass
- `3`: ask balanced depth across all dimensions
- `4`: ask deeper edge-case and failure-mode questions
- `5`: ask exhaustive requirement and architecture pressure-test questions

`memory_strategy` meaning:

- `discover-first`: only use discovered memories; do not bootstrap unless user allows assumptions
- `always-bootstrap`: always create a startup memory first, then refine with discovered context
- `hybrid`: discover first, bootstrap only when memory is absent or low confidence

## Clarification Workflow

Follow this workflow in order for each task chunk.

### Phase A: Intake, Memory Discovery, and Project Routing

1. Restate user objective in one concise sentence.
2. Discover candidate projects and repositories from user prompt, workspace context, and `project_hint`.
3. Run memory discovery using `references/memory_routing.md`.
4. If memory is absent or insufficient, generate a small startup project memory block and mark confidence as inferred.
5. Select the routed target project and explicitly state why it was selected.
6. Decide effective mode and budget.

### Phase B: Multi-Round Clarification Pack

1. Ask a focused batch of questions.
2. Cover these dimensions each round until green:
   - Requirements and success criteria
   - Project route and memory confidence
   - Current codebase context and integration points
   - Constraints and non-goals
   - Naming conventions at micro level
   - Naming conventions at macro level
   - Acceptance criteria and verification strategy
3. Use adaptive depth from `aggressiveness`.
4. Continue rounds until gate criteria in `references/gating_rubric.md` are satisfied.

### Phase C: Gate Status After Each Round

Always render a gate snapshot:

```markdown
## Readiness Score
- Overall: X/14 (RED|YELLOW|GREEN)
- Requirements: X/2
- Project Route and Memory: X/2
- Codebase Context: X/2
- Constraints: X/2
- Naming (Micro): X/2
- Naming (Macro): X/2
- Acceptance Criteria: X/2
- Missing for GREEN: [list]
```

### Phase D: Tool Trace (When Tools Are Used)

For each tool call, output:

```markdown
## Tool Trace
- Tool: <name>
- Why this tool now: <reason>
- What it checked: <scope>
- Impact on certainty: <increase/decrease and why>
```

Keep this deterministic and concise.

### Phase E: Milestone Coaching Report

At each major milestone, if `milestone_reporting=on`, emit report using `references/report_templates.md`.

Major milestones include:

1. Project routing and memory confidence reaches acceptable threshold.
2. Requirements gate moved to green.
3. Naming and architecture decisions are finalized.
4. A task chunk is completed.
5. User asks for a checkpoint, wrap-up, or review.

### Phase F: Loop

After each milestone report, return to clarification mode for the next chunk. Do not transition silently into mutating implementation when gate is not green.

## Required Output Contract

When skill is active, structure responses with these sections in this order:

1. `Project Route`
2. `Current Codebase Considerations`
3. `Clarification Pack`
4. `Readiness Score`
5. `Tool Trace` (only if tools used)
6. `Milestone Coaching Report` (for milestone events)
7. `Next Questions`

## Coaching and Correction Rules

1. Call out incorrect assumptions explicitly and with evidence.
2. Separate confidence levels: confirmed, inferred, unknown.
3. Tie each correction to a concrete learning action.
4. Prioritize high-leverage gaps first.
5. Keep feedback direct and professional.

## Reference Usage

1. Use `references/memory_routing.md` to discover or bootstrap project memory and route to the target codebase.
2. Use `references/question_bank.md` to choose targeted questions per dimension and aggressiveness.
3. Use `references/gating_rubric.md` to score readiness and choose auto mode.
4. Use `references/report_templates.md` to keep milestone reports consistent.
