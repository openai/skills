# Minimal Eval Workflow

Run this when you want a fast quality check with minimal overhead.

## Step 1: Pick One Task

- Choose one prompt from `eval-prompts.md`.
- Choose the closest baseline from `case-library.md`.

## Step 2: Execute The Skill

- Run the skill on the target page/codebase.
- Require concrete edits only (no vague guidance text).

## Step 3: Verify Visual Integrity

- If assets exist, run checks from `image-visibility-checks.md`.
- Confirm required tracks when relevant: animal, abstract, business.
- For case-b style dashboard polish checks, run:
  - `node skills/.experimental/ivan-human-ui/scripts/verify_dashboard_polish.mjs <path/to/index.html>`
- For case-c style testimonial checks, run:
  - `node skills/.experimental/ivan-human-ui/scripts/verify_testimonial_tracks.mjs <path/to/index.html>`

## Step 4: Score

- Score with `eval-rubric.md` (0-10).
- Ship bar is `>= 8/10`, with asset integrity mandatory pass.

## Step 5: Log

- Add one row to `eval-results.md`:
  - date
  - prompt id
  - case id
  - score
  - pass/fail
  - short notes

## Step 6: Iterate Once If Needed

- If fail, do one focused iteration and rescore.
- Log the second result as a new row (do not overwrite history).
