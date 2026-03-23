---
name: webapp-testing
description: Test and debug local web applications in the repository by combining route discovery, browser inspection, console and network review, smoke-test flows, and reproducible bug-check workflows. Use when the user asks to verify a local web app, reproduce a UI bug, smoke-test a feature, inspect frontend errors, or validate that a browser flow works end to end.
---

# Webapp Testing

## Overview

Use this skill to validate a running web app with a disciplined workflow instead of ad hoc clicking. Start by figuring out how the app runs locally, then choose the lightest path that can confirm the behavior or reproduce the bug.

## Workflow

1. Determine the app shape:
   - static HTML or simple local file
   - existing local dev server
   - app that needs a start command from the repo
2. Find the right run command from the README, package scripts, framework config, or existing docs before inventing one.
3. Choose the testing mode:
   - quick smoke test for basic rendering and critical clicks
   - bug reproduction for a specific reported issue
   - exploratory inspection for selectors, console errors, and unexpected states
   - regression validation after a code change
4. Use browser automation when needed, but keep the workflow evidence-first: inspect the rendered state, then interact.
5. Convert what you learned into a clear result: pass, fail, repro steps, or follow-up fix.

## Tool Coordination

- Use the `$playwright` skill when real browser automation is required from the terminal.
- Use the screenshot skill or the app's own tooling when a visual capture is helpful.
- Use the `$testing-patterns` skill when the user wants persistent repo tests added, not just manual or exploratory validation.

## Practical Rules

- For dynamic apps, wait for the page to settle before trusting selectors or assertions.
- Prefer accessible selectors and visible behavior over brittle DOM paths.
- Check console errors, failed network requests, and unexpected redirects before assuming the UI bug is purely visual.
- Keep repro steps minimal and deterministic.
- Reuse the repository's existing dev and test scripts instead of inventing parallel workflows.

## Typical Deliverables

- Reproduction steps for the bug or validation flow
- Screenshots or console findings when useful
- The commands used to run the app and the validation
- A clear pass or fail summary
- Follow-up recommendations if the issue belongs in automated tests

## Guardrails

- Do not claim a bug is fixed without re-running the relevant flow.
- Do not add permanent repo tests unless the user wants that outcome.
- Do not ignore server startup, env vars, or API health; many frontend bugs are actually app boot or backend issues.
