---
name: nine-gate-spec
description: Per-gate purpose, deliverable, audit script, and tooling for the 9-gate delivery regime.
type: reference
---

# Nine-Gate Specification

Each gate is a unit of work whose closure is conditioned on a programmatic audit returning zero HIGH/CRITICAL findings. A gate that is "manually approved" without an audit is not closed; it is wished closed. The audits live in `scripts/` and are wired into CI by Gate 9.

## Gate 1 -- Discovery Constitution

**Purpose.** Convert a one-line idea into a constitution the team can be held to. The output is the contract every later gate refers back to.

**Deliverables.**
- `PRODUCT.md` with frontmatter, one-sentence Golden Path, persona+pain, outcome metric, riskiest assumption, four-risk ledger, golden_path_step 1-7, prod_url placeholder.
- `SPEC.md` with scope and acceptance criteria.
- `PLAN.md` with appetite, kill criteria, deferred list (>=3 items, >=3 from the banned list).
- `TASKS.md` initial backlog.
- `COMPETITIVE_BENCHMARK.md` with at least one numeric comparison vs v0/Bolt/Lovable/Railway.

**Audit.** `audit_constitution.py`. Checks file presence, frontmatter, required sections, single-sentence Golden Path (regex on terminators), and the 14 mandatory questions.

**Tools.** `python-frontmatter`, `pyyaml`, regex.

## Gate 2 -- Statement of Work

**Purpose.** Freeze scope. The SoW is the appetite and the kill criteria, not a spec.

**Deliverables.**
- Numeric appetite in PLAN.md (e.g. "4 weeks" or "$15k" or "1 sprint").
- At least one falsifiable kill criterion.
- Deferred list with >=3 of: RBAC, compliance, marketplace, multi-region, observability, integrations.
- TASKS.md must not contain any banned-list term in MVP scope.

**Audit.** `audit_sow.py`.

**Tools.** Regex against PLAN.md/TASKS.md.

## Gate 3 -- Design

**Purpose.** Every screen the user touches is mapped to a `golden_path_step`. Off-step screens are killed before pixels are pushed.

**Deliverables.** A `design/` directory with one file per screen, each carrying a `golden_path_step: N` frontmatter field and a one-line user goal. Wireframes/mockups checked in or linked. No screen exists without a step.

**Audit.** Manual review (programmatic audit deferred to v1.1). The orchestrator's `gate 3` command currently prints a manual-review notice. The skill remains red on Gate 3 until a designer signs off in `design/SIGNOFF.md`.

**Tools.** Figma, Excalidraw, or plain markdown wireframes; whatever leaves a versioned artefact.

## Gate 4 -- Build

**Purpose.** Every commit traces to an AC; debt is named, not hidden; new TODO/FIXME without a DEBT.md row is a hygiene failure.

**Deliverables.**
- Every commit on the branch contains a ticket id (`[A-Z]+-\d+`).
- Every new TODO/FIXME/XXX/HACK has a DEBT.md row referencing `<file>:<line>`.
- No new `.skip`, `.only`, `it.todo`, or `xfail` in test files.
- No mock/stub/localhost references in non-test source (`audit_real_wiring.py`).

**Audit.** `audit_build.py`, `audit_real_wiring.py`.

**Tools.** `git diff origin/main...HEAD`, `git log --oneline`, ripgrep.

## Gate 5 -- QA

**Purpose.** The product works for a real user against real infrastructure. Tests are not theatre.

**Deliverables.**
- Unit tests pass with zero skips (`audit_unit.py`).
- Integration tests do not mock HTTP/DB layers (`audit_integration.py`).
- E2E tests run against a non-localhost preview URL with at least one `@golden-path` test green (`audit_e2e.py`).
- API contract: oasdiff/graphql-inspector against origin/main shows no breaking change OR a DEBT.md entry (`audit_contract.py`).
- Diff coverage >= 80% (`audit_coverage.py`).
- Mutation score >= 60% if Stryker/mutmut configured (`audit_mutation.py`).
- Static analysis (eslint/tsc/ruff/mypy) clean with strict flags (`audit_static.py`).
- Console error/warning count = 0 on golden path (`audit_console_clean.py`).

**Tools.** vitest/jest/pytest, Playwright, oasdiff, graphql-inspector, diff-cover, Stryker/mutmut, eslint/tsc/ruff/mypy.

## Gate 6 -- UAT

**Purpose.** A human walks the product on the live URL and signs off in writing.

**Deliverables.**
- `e2e/uat/` with at least one `*.uat.spec.{ts,js,py}`.
- `UAT_REPORT.md` with `sha256:` of the artefact under test and `Signed-off-by:` line.
- Git tag matching `uat-v*`.

**Audit.** `audit_uat.py`.

**Tools.** Playwright (UAT scripts), `git tag`, sha256.

## Gate 7 -- Deploy

**Purpose.** Production is real, monitored, and rollback-tested.

**Deliverables.**
- `prod_url` in PRODUCT.md frontmatter resolves with HTTP 200 and non-empty `<title>`.
- A workflow file under `.github/workflows/*.yml` references `smoke`.
- Either a git tag `rollback-drill-YYYY-MM-DD` within 14 days OR `runbooks/rollback-drills.md` modified within 14 days.

**Audit.** `audit_deploy.py`, `audit_demo_url.py`.

**Tools.** `requests`, GitHub Actions, `git tag`.

## Gate 8 -- Handoff

**Purpose.** The user receives source, runbook, credentials path, walkthrough, and a debt ledger.

**Deliverables.**
- `README.md`, `runbooks/runbook.md`, `DEBT.md`, `HANDOFF.md` exist and are non-empty.
- `HANDOFF.md` has filled sections: Credentials Vault Link, Admin Walkthrough Video, Knowledge Transfer Date.

**Audit.** `audit_handoff.py`.

**Tools.** Filesystem checks, regex.

## Gate 9 -- Warranty

**Purpose.** The audit regime travels with the code. Future contributors cannot ship around it.

**Deliverables.**
- `.github/workflows/*.yml` references `audit_constitution`, `audit_build`, `audit_qa` (or the full set).
- Branch protection on main includes those audit jobs as required checks.

**Audit.** `audit_warranty.py`.

**Tools.** YAML parsing (`pyyaml`), `gh api repos/:owner/:repo/branches/main/protection`.

## Tooling stack quick reference

| Tool | Purpose | Where used |
| --- | --- | --- |
| ripgrep | fast grep for debt markers, mock patterns | Gate 4, cross-cutting |
| diff-cover | diff-only line coverage threshold | Gate 5 |
| Stryker (Node) / mutmut (Py) | mutation testing | Gate 5 |
| Playwright | E2E + UAT against real preview URL | Gate 5, 6 |
| oasdiff | OpenAPI breaking-change detection | Gate 5 |
| graphql-inspector | GraphQL breaking-change detection | Gate 5 |
| eslint, tsc, ruff, mypy | static analysis (strict) | Gate 5 |
| `gh` CLI | branch protection inspection | Gate 9 |
| markdownlint, vale | doc hygiene | Gate 1, 8 |
| repolinter | repo structural conformance | Gate 9 |

The tools must exist on `$PATH` for the audit to run. If a tool is missing, the audit emits an `INFO` finding with the install hint and continues. Missing tools are not pass-by-default at Gate 9; the warranty audit checks that CI itself has them installed.
