---
name: ai-native-context-discipline
description: "Use in long AI coding sessions to prevent context rot: re-anchor artifacts, summarize state, detect drift, and restore phase boundaries."
---

# AI Native Context Discipline

Use this skill when a session is getting long, the agent may be drifting, or the user asks to re-anchor, summarize, resume, or restore coherence.

## Workflow

1. Detect the current phase.
   - Identify whether the project is in problem definition, planning, foundation, implementation, or improvement.
   - Do not assume the phase from recent conversation alone.

2. Reload durable artifacts.
   - Prefer `docs/implementation-plan.md`, `docs/progress.md`, `docs/project-guidelines.md`, and `docs/technical-debt.md` when present.
   - Read relevant source files or tests only as needed.
   - Avoid flooding context with unrelated files.

3. Produce a structured re-anchor summary.
   - Current objective
   - Current phase
   - Completed work
   - Active constraints
   - Decisions already made
   - Open questions
   - Next safe action

4. Detect context rot symptoms.
   - Drift from original problem
   - Inconsistent naming
   - Silent architectural shifts
   - Redundant abstractions
   - Scope expansion without intent
   - Reintroduction of rejected decisions

5. Restore boundaries.
   - Recommend the correct next phase or skill.
   - If implementation is ongoing, return to the smallest valid batch.
   - If planning is unstable, return to problem definition or plan refinement.

## Rules

- Maximize signal, not token volume.
- Prefer durable artifacts over conversational memory.
- Do not make code changes unless the user explicitly asks for action after re-anchoring.
- When summarizing, separate confirmed facts from assumptions.

See `references/context-rot-checklist.md` for symptoms and recovery prompts.
