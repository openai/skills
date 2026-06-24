---
name: ai-native-software-engineering
description: "Use when applying the AI Native Software Engineering lifecycle across problem definition, planning, foundation, implementation, and improvement."
---

# AI Native Software Engineering

Use this umbrella skill when the user asks to apply the methodology broadly or does not specify which lifecycle phase they are in.

## Phase Router

Choose the narrowest phase skill that matches the user's current need:

1. Use `ai-native-problem-definition` when the project is still an idea, problem, opportunity, or vague solution direction.
2. Use `ai-native-implementation-plan` when the problem is clear and the user needs an MVP-first phased roadmap.
3. Use `ai-native-project-foundation` when a plan exists and the user needs a controlled workspace, persisted plan, plan review, and version-control readiness.
4. Use `ai-native-controlled-implementation` when the user is ready to implement from `docs/implementation-plan.md`.
5. Use `ai-native-structured-improvement` when an MVP works and the user wants hardening, review, technical debt, or guidelines.
6. Use `ai-native-context-discipline` when the session is long, confusing, drifting, or needs a reset.

## Lifecycle Rules

- Specification precedes implementation.
- Constraints precede generation.
- Verification precedes merge.
- Clarity precedes speed.
- Ambiguity compounds.
- Structure scales.

## Artifact Model

Prefer durable project artifacts over conversational state:

- `docs/implementation-plan.md`
- `docs/progress.md`
- `docs/project-guidelines.md`
- `docs/technical-debt.md`

## Output

State the detected phase, the selected skill or workflow, and the next concrete action. If phase is ambiguous, ask one concise clarification or make the safest conservative assumption.

See `references/lifecycle.md` for the full phase map.
