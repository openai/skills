---
name: linear-plan-and-implement
description: End-to-end flow that starts with Linear ticket triage, creates an approved plan, and implements the ticket.
---

# Linear → Plan → Implement

## Overview
- Use this when a user wants to pick a Linear ticket, get a code-change plan, and implement it.
- Explicitly depends on the `linear` skill.
- Leverages existing skills: Linear (ticket listing/context) and create-plan (plan+approval).

## Prereqs
- Git repo ready for edits.

## Workflow
1) List candidate tickets
- Ask for filters (team, status, labels, priority, `--unassigned`, `--assignee @me`, limit).
- Use the Linear skill; prefer JSON -> render a compact table.

2) User picks a ticket
- Offer a quick briefing with and share the summary.
- If attachments are present, list them explicitly (title + URL) in the briefing.
- If the description or attachments include image links (e.g., `![...](https://uploads.linear.app/...)`), fetch them and view them with so visual context is reflected in the briefing.
- Confirm the ticket identifier, title, and acceptance criteria before planning.

3) Plan the code change
- Feed the ticket title/description into create-plan; include any repo findings needed to scope the work.
- Show a concise plan (steps, risks, tests) and ask for explicit approval before edits.

4) Execute after approval
- Implement the approved plan; keep changes scoped to the plan.
- Run the tests/checks promised in the plan; capture results.

5) Summarize the change
- Provide a short summary (what changed, why), files/areas touched, test results, and the Linear ticket link/ID.

## Notes
- If the user switches tickets, restart at step 2 with the new identifier.
- Keep each step brief and actionable; avoid mixing planning with editing.