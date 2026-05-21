---
name: ai-native-structured-improvement
description: "Use after a functional MVP to harden durability without scope creep: guidelines, verification, expert review, code review, and technical debt."
---

# AI Native Structured Improvement

Use this skill after the MVP works. The objective is durability, not new capability.

## Workflow

1. Re-anchor on the working MVP.
   - Confirm what behavior is already functional.
   - Identify current tests, critical paths, and known risks.
   - Do not add features unless the user explicitly asks for a new planning cycle.

2. Generate and curate `docs/project-guidelines.md`.
   - Draft constraints from the real codebase.
   - Remove generic advice, boilerplate, and redundant rules.
   - Keep only project-specific architectural invariants and non-negotiable constraints.

3. Strengthen verification before risky changes.
   - Add or improve tests around critical behavior when practical.
   - Prefer tests before refactoring behavior.
   - If tests are not feasible, state the residual risk.

4. Run targeted expert review passes.
   - Use focused lenses such as performance, maintainability, security, refactoring, data model, or UX.
   - Ask for risks and simplifications, not broad rewrites.

5. Perform AI-assisted pre-merge review when on a feature branch.
   - Compare the branch against main or the appropriate base branch.
   - Prioritize logical errors, behavioral regressions, architectural inconsistency, guideline violations, hidden complexity, and missing tests.
   - Do not rewrite code during the review pass unless the user asks to fix findings.

6. Generate `docs/technical-debt.md`.
   - Convert review findings into a technical backlog.
   - Include description, risk level, expected benefit, estimated complexity, and priority.

## Required Output

- Concise project guidelines, if requested or missing
- Verification gaps and test improvements
- Targeted review findings
- Technical debt roadmap
- Recommended next improvement batch

## Boundary Rule

Improvement must strengthen the existing system. It must not expand product scope.

See `references/improvement-playbook.md` for review prompts and debt templates.
