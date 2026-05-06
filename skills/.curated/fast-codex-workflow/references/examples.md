# Before / After Examples

Three transcripts showing the operating loop versus default behavior on the same task. Filenames and commands are illustrative; the shape generalizes.

## Example 1 - Off-by-one in pagination

**Prompt:** "The pagination shows page 0 instead of page 1 in the UI."

**Without skill:**
- Reads twelve files across `src/components/`, `src/api/`, `src/store/`.
- Runs the full Jest suite (~3 min).
- Notices a generic `parseInt` and refactors it into a shared utility.
- Writes a 200-word summary.

**With skill:**
- `rg "page 0|currentPage" src/` returns one hit in `Pagination.tsx:42`.
- Reads `Pagination.tsx`, finds `useState(0)` for the current page.
- Patches to `useState(1)`.
- `npx jest Pagination.test` passes.
- Final answer: "Patched `Pagination.tsx:42` (`useState(0)` to `useState(1)`). Verification: `Pagination.test` passed."

## Example 2 - Add an env-driven feature flag

**Prompt:** "Add a `FEATURE_NEW_CHECKOUT` env var that toggles the new checkout flow."

**Without skill:**
- Builds a generic `FeatureFlagService` class.
- Adds a new `flags.ts` module, a `useFeatureFlag` hook, and a YAML config loader.
- Writes tests for the abstraction.
- Updates eight files.

**With skill:**
- Inspects existing checkout entry: `Checkout.tsx` already branches on a local `useNewCheckout` boolean.
- `rg "process.env\." src/` confirms the existing pattern is direct env reads, no abstraction.
- Patches `Checkout.tsx:12` to `const useNewCheckout = process.env.FEATURE_NEW_CHECKOUT === 'true';`.
- Adds `FEATURE_NEW_CHECKOUT=` to `.env.example` with a one-line comment.
- `npm test -- Checkout` passes.
- Final answer: "Added `FEATURE_NEW_CHECKOUT` to `Checkout.tsx:12` and `.env.example`. Verification: `Checkout.test` passed."

## Example 3 - CI is red on main

**Prompt:** "CI is red on main. Fix it."

**Without skill:**
- Runs the full test suite locally.
- Reads every workflow file under `.github/workflows/`.
- Refactors a flaky test.
- Adds retry logic to the CI runner.

**With skill:**
- `gh run list --branch main --limit 1` returns the failing run ID.
- `gh run view <id> --log-failed` shows one failing step: `npm run lint` on `src/utils/format.ts:88`.
- Reads line 88: trailing whitespace in a string literal flagged by a new ESLint rule.
- Patches the trailing space.
- `npm run lint` passes locally.
- Final answer: "Patched trailing whitespace in `src/utils/format.ts:88`. Verification: `npm run lint` passes locally; pushing the fix should clear CI."

## What Each Example Proves

| Example | Bad pattern avoided | Speed lever applied |
|---|---|---|
| 1 | Reading the whole UI tree on a one-line bug | First-minute triage via `rg` |
| 2 | Building an abstraction for a single call site | Match existing pattern; minimal complete change |
| 3 | Running every test before reading the failure | Read the failing log first |
