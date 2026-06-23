# Ivan Human UI

Curated Codex skill for removing generic AI-looking UI patterns and shipping more intentional product-facing pages.

## When to Use

- User explicitly asks to remove "AI 味道", "AI vibe", or "template feel".
- UI needs hierarchy, spacing, typography, color, and component polish.
- There are visual regressions in screenshots/logos/testimonials that must render correctly.

## When Not to Use

- Backend-only refactors.
- Data-pipeline tasks with no visual output.
- Pure infra, CI, or API-only changes.

## Quick Workflow

1. Diagnose current UI artifacts first.
2. Propose 2-3 concrete style directions.
3. Apply hard constraints from `references/human-ui-constraints.md`.
4. Validate image/logo/testimonial visibility (`references/image-visibility-checks.md`).
5. Run rubric evaluation and log results (`references/eval-rubric.md`, `references/eval-results.md`).

## Contributor Guide

- Add new repeat failure patterns into `references/gotchas.md`.
- Keep examples small and reproducible in `assets/`.
- Record every real eval in `references/eval-results.md` so quality can be tracked over time.
- Prefer explicit, testable UI constraints over style adjectives.
