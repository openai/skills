---
name: jira-epic-skeleton
description: Six outcome-epics (not capability-epics) for the agentic delivery workflow, each mapped to a golden_path_step.
type: template
---

# Jira Epic Skeleton -- Outcome Epics

The single most damaging organisational anti-pattern in this skill's lineage is the **capability epic**: epics named "Auth Epic", "Generation Epic", "Deploy Epic". Capability epics close green while the user-facing outcome remains broken. This skeleton replaces them with six **outcome epics**, one per Golden Path step where a user observable state changes. Each epic only closes when the named outcome holds for a real user on the live URL.

> Rule of thumb: an outcome-epic name reads as a complete sentence in the past tense from the user's point of view. "Idea Captured" works. "Auth Epic" does not.

---

## Epic 1 -- Idea Captured

**Outcome statement.** "I, the user, told the system my idea, my persona, and my pain. The system has stored it in a way I can re-read tomorrow."

**Sample stories.**
- US-1.1 As a solo founder I can paste a one-line idea and a 3-bullet persona+pain into the intake form.
- US-1.2 As a returning user I can re-open my intake and edit it.
- US-1.3 As a stakeholder I can read the intake as a markdown file in the repo.

**AC pattern.**
- Given an authenticated user, when they submit the intake form, then a `PRODUCT.md` is created/updated in the project repo with frontmatter `golden_path_step: 1` and the Golden Path one-sentence is present.
- Given an existing intake, when the user re-opens it, then the form is pre-filled.
- Given the intake submitted, when `audit_constitution.py` runs, then it reports zero CRITICAL findings.

**golden_path_step:** 1.

---

## Epic 2 -- Spec Approved

**Outcome statement.** "The system gave me back a specification I recognise as my idea. I edited it, approved it, and the approval is recorded."

**Sample stories.**
- US-2.1 As a user I see an AI-generated SPEC.md derived from my intake.
- US-2.2 As a user I edit SPEC.md inline and save.
- US-2.3 As a user I click Approve and a PR is opened on my behalf to merge SPEC.md.

**AC pattern.**
- Given an intake exists, when the spec generation completes, then SPEC.md exists with frontmatter `golden_path_step: 2`, scope, and acceptance criteria.
- Given the user approves, when the approval workflow runs, then a git commit `docs(spec): approve <idea>` lands on the project default branch.
- Given the approval, when `audit_sow.py` runs, then it reports zero HIGH/CRITICAL findings.

**golden_path_step:** 2.

---

## Epic 3 -- Code Generated

**Outcome statement.** "The system wrote the code that implements the approved spec. The code compiles, lints, types pass, and lives in version control."

**Sample stories.**
- US-3.1 As a user I see code generation begin within 5 seconds of approving the spec.
- US-3.2 As a user I receive a link to the PR with the generated code.
- US-3.3 As a user I can request changes; the system updates the PR.

**AC pattern.**
- Given an approved spec, when generation completes, then a PR exists with non-empty diff, eslint/tsc/ruff/mypy clean (per `audit_static.py`), and no mocks/localhost in non-test source (per `audit_real_wiring.py`).
- Given the PR, when commits are inspected, then every commit message contains a ticket id matching `[A-Z]+-\d+` (per `audit_build.py`).
- Given the PR, when `audit_build.py` runs, then there are no new TODO/FIXME without DEBT.md rows.

**golden_path_step:** 3.

---

## Epic 4 -- Tests Passed

**Outcome statement.** "Tests run and pass on real infrastructure. The user can read a green test report. Mutation, contract, and console-clean checks are green too."

**Sample stories.**
- US-4.1 As a user I see a test results page with unit, integration, and E2E sections.
- US-4.2 As a user I see at least one `@golden-path` test green against a non-localhost preview URL.
- US-4.3 As a user I see zero console errors and zero skipped tests.

**AC pattern.**
- Given the generated code, when CI runs, then `audit_unit.py`, `audit_integration.py`, `audit_e2e.py`, `audit_contract.py`, `audit_coverage.py`, `audit_mutation.py`, `audit_static.py`, `audit_console_clean.py` all return exit code 0.
- Given a Playwright run, when the JSON report is parsed, then `@golden-path` test count >= 1 and all are passing.
- Given the integration suite, when scanned, then no test mocks `requests/axios/fetch/prisma/psycopg`.

**golden_path_step:** 4.

---

## Epic 5 -- Preview Deployed

**Outcome statement.** "The product is reachable on a real URL. A user can hit it from a different machine. The page renders and has a non-empty title."

**Sample stories.**
- US-5.1 As a user I receive a preview URL within 60 seconds of tests passing.
- US-5.2 As a user I open the URL in a fresh browser and the golden path completes end-to-end.
- US-5.3 As a user I see structured logs in a viewer (cloud provider's free tier suffices).

**AC pattern.**
- Given tests are green, when deploy runs, then the prod_url in PRODUCT.md frontmatter responds HTTP 200 (per `audit_demo_url.py` and `audit_deploy.py`).
- Given the URL, when curled, then body length > 500 bytes and `<title>` is non-empty.
- Given the deploy, when `.github/workflows/*.yml` is inspected, then a smoke job exists.

**golden_path_step:** 5.

---

## Epic 6 -- User Accepted

**Outcome statement.** "A real human walked the live URL, recognised it as their product, and signed off in writing. We have the artefact tagged in git."

**Sample stories.**
- US-6.1 As a user I receive a UAT script and walk it on the live URL.
- US-6.2 As a user I sign UAT_REPORT.md with my name and the date.
- US-6.3 As a delivery lead I tag the accepted commit `uat-v1.0.0`.

**AC pattern.**
- Given a deployed preview, when the user completes the UAT script, then `UAT_REPORT.md` exists with `sha256:` and `Signed-off-by:` lines (per `audit_uat.py`).
- Given the sign-off, when `git tag --list 'uat-v*'` runs, then a tag exists.
- Given handoff, when `audit_handoff.py` runs, then README.md, runbooks/runbook.md, DEBT.md, HANDOFF.md exist and HANDOFF.md sections "Credentials Vault Link", "Admin Walkthrough Video", "Knowledge Transfer Date" are filled.

**golden_path_step:** 6 (continues into 7 for warranty).

---

## Mapping summary

| Epic | golden_path_step | Closing audit script(s) |
| --- | --- | --- |
| 1 Idea Captured | 1 | audit_constitution.py |
| 2 Spec Approved | 2 | audit_sow.py |
| 3 Code Generated | 3 | audit_build.py, audit_real_wiring.py, audit_static.py |
| 4 Tests Passed | 4 | audit_unit.py, audit_integration.py, audit_e2e.py, audit_contract.py, audit_coverage.py, audit_mutation.py, audit_console_clean.py |
| 5 Preview Deployed | 5 | audit_deploy.py, audit_demo_url.py |
| 6 User Accepted | 6 (+ 7) | audit_uat.py, audit_handoff.py, audit_warranty.py |

## Why six and not nine

The 9-gate regime has nine gates. The Jira board has six epics. The mismatch is intentional: the six outcome-epics are user-facing milestones; the nine gates are internal quality bars. Multiple gates support a single outcome-epic; no outcome-epic is owned by a single gate. The user does not care about Gate 5 vs. Gate 7; the user cares about "did I get a working URL". Organise visible work around the user; organise invisible quality work around the gates.

## What this skeleton replaces

Capability-style epics ("Auth", "Generation", "Deploy") are deleted from the backlog at Gate 1. If a piece of work cannot be filed under one of the six outcome-epics, it does not belong in MVP. It goes to PLAN.md's deferred list with a one-line justification. This is the operational form of the Golden Path Doctrine.
