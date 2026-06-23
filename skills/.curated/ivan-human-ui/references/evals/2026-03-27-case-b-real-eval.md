# Real Eval Report - 2026-03-27 - Prompt 2 / Case B

## Scope

- Prompt: `prompt-2` from `references/eval-prompts.md`
- Case: `case-b` from `references/case-library.md`
- Goal: validate dashboard landing polish constraints with deterministic checks

## Artifact

- Before: `assets/eval-case-b-before/index.html`
- After: `assets/eval-case-b-after/index.html`
- Verifier: `scripts/verify_dashboard_polish.mjs`

## Commands

```bash
node skills/.experimental/ivan-human-ui/scripts/verify_dashboard_polish.mjs skills/.experimental/ivan-human-ui/assets/eval-case-b-before/index.html
node skills/.experimental/ivan-human-ui/scripts/verify_dashboard_polish.mjs skills/.experimental/ivan-human-ui/assets/eval-case-b-after/index.html
```

## Results

### Before (expected fail)

- `FAIL: Hero split layout missing.`
- `FAIL: Hero ratio 3/5 and 2/5 missing.`
- `FAIL: Section heading left alignment signal missing.`
- `FAIL: 8px spacing rhythm signal missing.`
- `FAIL: Outer ring 10% treatment signal missing.`
- `FAIL: Neutral palette signal missing.`
- `FAIL: Disallowed palette tokens found: indigo/emerald/purple.`
- `FAIL: Screenshot reference is missing.`

### After (expected pass)

- `PASS: dashboard polish constraints satisfied (layout, palette, spacing, ring, screenshot asset).`

## Rubric Score

- Hierarchy clarity: 2/2
- Anti-template quality: 2/2
- Typography quality: 2/2
- Component polish: 1/2
- Asset integrity: 2/2
- Total: `9/10` (Ship bar met)
