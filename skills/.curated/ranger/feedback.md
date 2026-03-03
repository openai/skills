# Addressing Reviewer Feedback

When a reviewer leaves comments on scenarios, a new version (v2) of the scenario is created to incorporate the feedback. The reviewer's comments were left on the **previous version** (v1), but they are the reason this v2 scenario exists. Use this workflow to understand what the reviewer wants, fix the code, and re-verify.

v2+ scenarios inherit comments from their parent version. Run `get-review` to see them.

## When This Applies

- Scenarios show as v2/v3 with `[has reviewer feedback]` tag
- `ranger resume` prints a warning about unaddressed comments

## Step 1: Read the Feedback

```bash
ranger get-review
```

This shows ALL reviewer comments across all scenarios, including:
- The specific comment content and who wrote it
- The previous version description (what changed from v1 to v2)
- The expected flow from prior verification (canonical flow)
- **Annotated screenshots** — when a reviewer annotated a screenshot, the image is downloaded locally and the annotation coordinates are shown

### Example Output

```
📋 Feedback for: User Authentication (feat_abc123)

Scenario 1: "User can log in" (v2) — 2 unaddressed comments (from previous version)
  Previous version: "User can log in with email"
  This scenario was created to address the following reviewer feedback:
  💬 Jane (Feb 5): "This button is misaligned"
     📷 Screenshot: /path/to/.ranger/feedback-images/comment_abc123.png
     📍 Annotation: point at (0.45, 0.32)
  💬 Bob (Feb 5): "Error message not visible on failed login"
  Expected flow:
    1. Navigate to /login
    2. Enter email and password
    3. Click Submit
    4. Verify dashboard appears

Scenario 2: "Dashboard loads" — 0 comments
  ✅ No feedback to address
```

### Reading Annotated Screenshots

When the output includes `📷 Screenshot:` lines with a local file path, **use the `Read` tool on that file path** to see the screenshot the reviewer was commenting on. The `📍 Annotation:` line shows the normalized (0-1) coordinates where the reviewer placed their comment — this tells you exactly where on the screen the reviewer is pointing. Use both the visual screenshot and the coordinates to understand the spatial context of the feedback.

## Step 2: Fix the Code

For each unaddressed comment:
1. Read the comment carefully — what is the reviewer asking for?
2. If a screenshot path is shown (`📷 Screenshot:`), **read the image file** to see what the reviewer sees. Correlate the annotation coordinates with the comment text to understand exactly which UI element the reviewer is referring to.
3. Look at the "previous version" description to understand what changed
4. If a canonical flow is provided, that's the expected user journey to verify against
5. Make the code changes that address each concern

## Step 3: Re-verify

```bash
ranger go --scenario <N>
```

The verification agent **automatically receives the reviewer comments** in its prompt. It will specifically check that each reviewer concern was addressed in the current implementation.

## Key Points

- Always run `get-review` **before** making code changes — understand what the reviewer wants first
- v2+ scenarios inherit their parent's comments — those comments are the reason this version exists
- The go command auto-injects feedback into the browser agent's prompt, so you don't need to manually include comments in your `--notes` description
- Address ALL unaddressed comments before re-verifying — partial fixes may result in another review round
