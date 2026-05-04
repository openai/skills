---
name: anti-patterns
description: Fifteen ways "done" lies; per pattern the symptom, root cause, programmatic detection, and counter-clamp.
type: reference
---

# Fifteen Anti-Patterns

Each anti-pattern is documented as: **symptom** (what you see), **root cause** (why it happens), **programmatic detection** (which audit script catches it), **counter-clamp** (the practice that prevents it).

## 1. AI-Plan-Bloat

**Symptom.** The AI produces a beautiful 40-step plan. Demo of the plan goes well. Nothing is built.

**Root cause.** The plan is treated as evidence of progress. Plans are cheap; real outputs are expensive. The team rewards the cheap thing.

**Detection.** `audit_build.py` -- if commits are sparse but TASKS.md is bursting, plan-bloat is in play. `audit_demo_url.py` -- prod URL is missing, returning <500 bytes, or has no `<title>`.

**Counter-clamp.** Gate 5/Gate 7. No gate closes on a plan; only on a working live URL.

## 2. Platform-vs-Product Drift

**Symptom.** The team ships "platform features" (queue, observability, multi-backend abstraction) instead of product features (user can complete the Golden Path).

**Root cause.** Platform work feels infinite, low-risk, internally legible. Product work is high-risk and externally judged. The team retreats to platform.

**Detection.** `filter_task.py` -- platform tasks score below 0.3 against the seven golden_path_steps and return DEFER.

**Counter-clamp.** Run `filter_task.py` on every ticket before sprinting. Anything that DEFERs goes to PLAN.md deferred list.

## 3. Capability Epic Trap

**Symptom.** Jira epics are organised by capability ("Auth Epic", "Generation Epic", "Deploy Epic") rather than by user outcome ("Idea Captured", "Spec Approved", "Preview Deployed").

**Root cause.** Capability epics map cleanly to engineering teams; outcome epics force cross-team work and accountability. Capability is the easy default.

**Detection.** Manual inspection. The orchestrator's `gate 3` review and `templates/jira-epic-skeleton.md` define the six outcome-epics.

**Counter-clamp.** Re-organise epics around the six outcome-epics in `templates/jira-epic-skeleton.md`. If an epic does not map to a user outcome, it is deferred or merged.

## 4. Vanity Done

**Symptom.** Tickets are closed at high rate. Sprint completion looks healthy. The product still does not work end-to-end.

**Root cause.** "Done" is defined per-component, not per-outcome. A ticket that closes "the auth flow is implemented" passes even when no user can authenticate against the deployed system.

**Detection.** `audit_e2e.py` -- the `@golden-path` test is failing or absent even though tickets are closed.

**Counter-clamp.** Per-outcome AC tied to a passing E2E test against the real preview URL. No ticket is "done" until the E2E assertion that proves it is green.

## 5. Test Theatre

**Symptom.** Test coverage is high. Mutation score is low. CI is green. Real bugs ship.

**Root cause.** Tests assert on irrelevant outputs (return values from mocks; HTTP status codes that the test fixture forces). The tests prove the test, not the code.

**Detection.** `audit_mutation.py` -- mutation score < 60% on changed code. `audit_integration.py` -- HTTP/DB layers are mocked.

**Counter-clamp.** Mutation testing in CI. Integration tests hit real services in a docker-compose or hosted preview environment.

## 6. Wired-But-Broken Frontend

**Symptom.** The frontend renders. Buttons exist. Clicking them does nothing useful, or fails silently, or shows a fake success message.

**Root cause.** Frontend is built against a mocked API client. The mock is never replaced. Or the API exists but the response shape drifts and nobody notices because no end-to-end test runs.

**Detection.** `audit_real_wiring.py` -- `import.*mock|fakeApi|stubApi|MockAdapter` in non-test source. `audit_e2e.py` -- no `@golden-path` test or it fails.

**Counter-clamp.** Frontend integration tests against the real backend in CI; ban mock clients in `src/`.

## 7. Mock-Only Path

**Symptom.** The integration test suite is large and green; production fails on the first real request.

**Root cause.** Integration tests import the production HTTP/DB clients but stub them. The tests verify behaviour against the stub, not against the wire.

**Detection.** `audit_integration.py` -- `vi.mock|jest.mock|@patch|MagicMock` near `requests|axios|prisma|psycopg` import lines.

**Counter-clamp.** Integration tests are reserved for tests that hit real services. Anything that mocks the wire is a unit test (and named accordingly). At least one E2E test (`@golden-path`) hits the deployed preview URL.

## 8. Local-Works-Prod-Doesn't

**Symptom.** "Works on my machine" is the standing joke. Production keeps failing in ways the dev environment cannot reproduce.

**Root cause.** Configuration drift between local and prod (env vars, feature flags, API base URLs, secrets). Local uses fixtures; prod uses real services with different latency, auth, rate limits.

**Detection.** `audit_real_wiring.py` -- `localhost|127.0.0.1` in non-test source. `audit_e2e.py` -- `baseURL` in `playwright.config.*` contains `localhost`.

**Counter-clamp.** Preview URLs per branch (Vercel/Netlify); E2E tests run against preview, never localhost; environment differences captured in a single `infra/env.md`.

## 9. Console Pollution

**Symptom.** The browser console is full of warnings and errors during normal use. Users see them; engineers learned to ignore them.

**Root cause.** The team treats console errors as cosmetic. They are not -- they are usually misconfigured imports, deprecated APIs, missing keys, or unhandled promise rejections that mask real bugs.

**Detection.** `audit_console_clean.py` -- counts `type: console` events with level `error` or `warning` in Playwright trace JSON.

**Counter-clamp.** Console error count = 0 on the golden path is a CI gate. Each existing error is named in DEBT.md or fixed.

## 10. Schema Drift FE/BE

**Symptom.** The frontend expects field `userName`. The backend returns `user_name`. The frontend renders `undefined`. No test catches it.

**Root cause.** No contract pinned between FE and BE. TypeScript types and Pydantic schemas drift independently.

**Detection.** `audit_contract.py` -- oasdiff/graphql-inspector flags breaking changes against `origin/main`.

**Counter-clamp.** Single source of truth (OpenAPI YAML or GraphQL schema or proto). FE and BE generate types from it. Breaking changes require a DEBT.md row and version bump.

## 11. Skipped Tests Graveyard

**Symptom.** The test suite has dozens of `.skip`, `.only`, `it.todo`, or `xfail`. Each was added with the intent to fix; none ever was.

**Root cause.** "Just unblock CI for now" is the default response to a flaky test. The fix never returns to the top of the priority list.

**Detection.** `audit_build.py` -- new `\.skip|\.only|it\.todo|xfail|@pytest\.mark\.skip` in test files in the diff. `audit_unit.py` -- skipped count > 0.

**Counter-clamp.** Skipped tests block Gate 5. Either fix or delete; do not commit a skip.

## 12. TODO/FIXME Accretion

**Symptom.** `rg TODO` returns hundreds of hits. None of them have owners or dates.

**Root cause.** TODOs are cheap to add and have no enforcement. They become a passive-aggressive backlog.

**Detection.** `audit_build.py` -- new TODO/FIXME/XXX/HACK in the diff that is not referenced in DEBT.md.

**Counter-clamp.** Every TODO must have a DEBT.md row referencing `<file>:<line>`. The DEBT.md row has owner + date + acceptance condition.

## 13. No-Real-User-Walked-It

**Symptom.** The team demos to itself. The demo passes. No external user has used the product.

**Root cause.** Internal demos are easy to schedule; external user sessions require recruiting and confront the team with reality.

**Detection.** `audit_uat.py` -- `UAT_REPORT.md` missing or unsigned; no `uat-v*` git tag.

**Counter-clamp.** Gate 6 requires a signed UAT report from a real user against the live URL. Internal sign-off does not count.

## 14. Demo URL Rot

**Symptom.** PRODUCT.md says the prod URL is X. Hitting X returns 503, or 404, or a 200 with an empty body, or a 200 with an old version.

**Root cause.** Deploys are intermittent; the URL is never monitored; rot accumulates between demos.

**Detection.** `audit_demo_url.py` -- HTTP 200 + body length > 500 bytes + non-empty `<title>`. `audit_deploy.py` -- prod_url HEAD fails or no `<title>`.

**Counter-clamp.** Smoke job in CI hits prod_url after every deploy. Gate 7 audit runs on a schedule (daily) to detect rot between deploys.

## 15. BC Theatre (Backward-Compat Theatre)

**Symptom.** API breaking changes ship with a soothing changelog ("we improved the response shape"). Customers' integrations break silently.

**Root cause.** "Backward-compat" is asserted in prose but not enforced. The schema diff is hand-eyeballed.

**Detection.** `audit_contract.py` -- oasdiff flags breaking change without a DEBT.md row documenting the breakage and migration plan.

**Counter-clamp.** Breaking changes require a versioned endpoint or a feature flag, plus a DEBT.md row, plus a customer-comms plan in HANDOFF.md.

## How to use this list

These fifteen are not exhaustive; they are the ones with the highest signal in the failure mode this skill was built to prevent. Print them. Tape them above the standup board. When a gate goes green-but-suspicious, walk the list before declaring victory. Each pattern's counter-clamp is enforced by an audit script; the audits exist because human discipline alone fails on tired Friday afternoons in week six of a six-week cycle.
