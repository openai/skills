# Real Eval Report - 2026-03-27 - Prompt 3 / Case C

## Scope

- Prompt: `prompt-3` from `references/eval-prompts.md`
- Case: `case-c` from `references/case-library.md`
- Goal: fix missing testimonial media tracks and verify anti-AI polish constraints

## Artifact

- Before: `assets/eval-case-c-before/index.html`
- After: `assets/eval-case-c-after/index.html`
- Verifier: `scripts/verify_testimonial_tracks.mjs`

## Commands

```bash
node skills/ivan-human-ui/scripts/verify_testimonial_tracks.mjs skills/ivan-human-ui/assets/eval-case-c-before/index.html
node skills/ivan-human-ui/scripts/verify_testimonial_tracks.mjs skills/ivan-human-ui/assets/eval-case-c-after/index.html
```

## Results

### Before (expected fail)

- `Track "abstract" asset missing: ./images/abstract.svg`
- `Track "business" asset missing: ./images/business.svg`
- `Track "business" is visually hidden via inline style: display:none`

### After (expected pass)

- `PASS: all required tracks render constraints are satisfied (animal, abstract, business).`

## Rubric Score

- Hierarchy clarity: 2/2
- Anti-template quality: 1/2
- Typography quality: 2/2
- Component polish: 2/2
- Asset integrity: 2/2
- Total: `9/10` (Ship bar met)

## Notes

- This run validates the core reliability claim: "two not showing" is caught and fixed with deterministic checks.
- Next recommended real run: `prompt-2` / `case-b` for dashboard-level layout polish.
