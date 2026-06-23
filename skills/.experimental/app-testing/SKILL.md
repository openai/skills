---
name: app-testing
description: Create a tailored app test checklist and then run in-depth testing for web apps, mobile apps, desktop apps, internal tools, and API-backed products. Use when Codex is asked to QA an app, test a feature or release, perform smoke, regression, or end-to-end testing, hunt bugs, validate UX or edge cases, or systematically explore product behavior before sign-off.
---

# App Testing

## Overview

Create a context-specific checklist before interacting with the app. Then execute deep testing against that checklist, expand coverage when risk appears, and report findings with reproduction steps, impact, and residual risk.

## Workflow

1. Gather context fast
   - Inspect the repo, run instructions, routes or screens, auth roles, data model, feature flags, recent changes, and existing tests.
   - Identify what "app" means in context: web UI, mobile app, desktop app, API-backed workflow, or a mixed system.
   - Note blockers early: missing credentials, unavailable services, absent fixtures, or platform limits.

2. Build the checklist first
   - Start from `references/checklist-template.md`.
   - Keep only relevant sections and add app-specific flows.
   - Include both requested scope and nearby regression risk.
   - Make the checklist visible in the response or working notes before deep testing.
   - Mark each item as `pending`, `passed`, `failed`, or `blocked` as testing progresses.

3. Run testing in deliberate passes
   - Start with a smoke pass to confirm the app boots and the main entry path works.
   - Cover primary user journeys end to end before spending time on polish issues.
   - Run negative and edge-case passes after the happy path is stable.
   - Validate integrations, persistence, permissions, and state transitions.
   - Finish with broader quality passes such as responsiveness, accessibility, security sanity checks, and performance observations when applicable.

4. Go deep when issues appear
   - Minimize repro steps.
   - Check whether the problem is isolated or systemic.
   - Probe adjacent states, roles, inputs, and recovery paths.
   - Record the smallest reliable reproduction and the broadest credible impact.
   - Use `references/test-depth-guide.md` for additional heuristics.

5. Report outcomes clearly
   - List findings ordered by severity.
   - For each confirmed issue include: title, severity, setup or account used, steps to reproduce, expected result, actual result, and evidence.
   - Separate confirmed bugs from weak signals, assumptions, and untested areas.
   - End with checklist coverage, blocked items, and the highest remaining risks.

## Coverage Priorities

Prefer this order unless the user gives tighter scope:

1. App start-up and environment sanity
2. Authentication, authorization, and role boundaries
3. Core value paths
4. Data creation, editing, deletion, and persistence
5. Validation, empty states, and error handling
6. Navigation, back, refresh, retry behavior, and session continuity
7. Integrations, background jobs, uploads, downloads, webhooks, or payments
8. Responsive, accessibility, localization, timezone, and browser or device differences
9. Security and performance sanity checks

## Testing Tactics

- Use the same tools the app uses in real life: local dev servers, seeded data, logs, network panels, CLI scripts, and database inspection.
- Cross-check UI claims against API responses or stored state when possible.
- Prefer representative, risk-based coverage over exhaustive but shallow clicking.
- Do not invent coverage. Call out what you could not test and why.
- If the user asks for a review, prioritize concrete findings over narrative.

## References

- Read `references/checklist-template.md` when preparing the first-pass checklist.
- Read `references/test-depth-guide.md` when broadening from smoke testing into deeper exploratory and regression coverage.
