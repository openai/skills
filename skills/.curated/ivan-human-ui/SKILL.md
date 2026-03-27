---
name: ivan-human-ui
description: Ivan's human-UI polish skill for removing AI-looking web/slides patterns and shipping clearer, more intentional pages. Use when users ask to remove "AI vibe/AI taste", improve visual hierarchy, refine component polish, fix UI media visibility regressions, or enforce explicit layout/typography/color constraints for landing pages, dashboards, and presentation-style sections. Do not trigger for backend-only, data-only, or non-visual refactors.
---

# Ivan Human UI

Apply concrete constraints that make generated UI feel intentional instead of generic, then evaluate the result with measurable checks.

## Workflow

1. Diagnose first.
   - Read current code and identify AI artifacts (default palette drift, center-everything, fake screenshots, generic icon clutter, weak hierarchy).
2. Show, do not tell.
   - Before full rewrite, create 2-3 compact visual directions from `references/style-directions.md`.
   - Let the user react to concrete options instead of abstract adjectives.
3. Apply hard constraints.
   - Use `references/human-ui-constraints.md` as non-negotiable implementation guardrails.
   - Read `references/gotchas.md` before finalizing edits.
   - Implement from structure -> typography -> color -> components -> spacing polish.
4. Enforce concrete edits only.
   - Specify explicit class/token/value changes.
   - Ban vague text like "optimize the logic" or "make it premium."
5. Validate visuals and assets.
   - Run `references/image-visibility-checks.md` when images/logos/testimonials exist.
   - Ensure animal/abstract/business tracks all render when requested.
6. Score quality.
   - Evaluate final output using `references/eval-rubric.md`.
   - Run task prompts from `references/eval-prompts.md` for regression checks.
   - If score is below ship bar, iterate once more before handoff.
7. Log and retain evidence.
   - Pick a closest scenario from `references/case-library.md`.
   - Record one row in `references/eval-results.md` for each eval run.
   - Keep artifact links/paths so future iterations can compare quality over time.

## Enforced Guardrails

- Prefer neutral, product-specific visual direction over common purple/indigo AI defaults.
- Prefer real screenshots/logos over fabricated placeholder UI when source assets exist.
- Prefer crisp outer rings with subtle opacity over muddy solid-border plus heavy-shadow stacks.
- Prefer left-aligned or asymmetrical hierarchy when it improves reading rhythm.
- Keep section spacing and grid rhythm explicit and numerically consistent.
- Keep text wrapping intentional with `text-balance` or `text-pretty` when needed.
- Keep every section visually intentional; remove ornamental effects that do not improve comprehension.

## Deliverable Format

Return:

1. The exact code edits made.
2. The short "before -> after" rationale per section.
3. Which direction was selected and why (if multi-direction exploration was used).
4. A verification checklist showing that images/logos all display, including animal, abstract, and business assets when required.
5. The eval score summary from `references/eval-rubric.md`.
