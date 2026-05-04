---
name: tooling-stack
description: Exact installation commands, invocation patterns, and exit-code semantics for every tool the audit suite calls.
type: reference
---

# Tooling Stack

Every tool the audit suite calls is documented here with: **install**, **invocation**, **exit-code semantics**. If a tool is missing, `lib/tool_runner.py` returns exit code 127 and the calling audit emits an `INFO` finding with the install hint.

## Doc and prose hygiene

### markdownlint
- **Install.** `npm i -g markdownlint-cli` (Node) or `markdownlint-cli2`.
- **Invocation.** `markdownlint "**/*.md" --ignore node_modules`
- **Exit codes.** `0` clean; `1` lint failures; `2` config error.
- **Used at.** Gate 1 (PRODUCT.md, SPEC.md, etc.), Gate 8 (HANDOFF.md, README.md).

### vale
- **Install.** `brew install vale` or download from https://vale.sh.
- **Invocation.** `vale --output=line .`
- **Exit codes.** `0` clean; `1` issues found.
- **Used at.** Gate 1 / 8 prose review (optional).

### gitlint
- **Install.** `pipx install gitlint`.
- **Invocation.** `gitlint --commits origin/main..HEAD`
- **Exit codes.** `0` clean; `1` violation.
- **Used at.** Gate 4 (commit message hygiene; complementary to `audit_build.py` ticket-id check).

## Search and static analysis

### ripgrep (rg)
- **Install.** `brew install ripgrep`.
- **Invocation.** `rg -n 'TODO|FIXME|XXX|HACK' --type py --type ts`
- **Exit codes.** `0` matches found; `1` no matches; `2` error.
- **Used at.** Gate 4 debt-marker scan, Gate 4 real-wiring scan. Audits use Python `re` directly so ripgrep is optional.

### eslint
- **Install.** project-local `npm i -D eslint`.
- **Invocation.** `npx eslint . --max-warnings 0`
- **Exit codes.** `0` clean; `1` lint errors; `2` config error.
- **Used at.** `audit_static.py`. Strict flag is `--max-warnings 0`.

### tsc
- **Install.** project-local `npm i -D typescript`.
- **Invocation.** `npx tsc --noEmit`
- **Exit codes.** `0` clean; non-zero on type errors.
- **Used at.** `audit_static.py`.

### ruff
- **Install.** `pipx install ruff` or `uv pip install ruff`.
- **Invocation.** `ruff check .`
- **Exit codes.** `0` clean; `1` lint findings; `2` config.
- **Used at.** `audit_static.py`.

### mypy
- **Install.** `pipx install mypy`.
- **Invocation.** `mypy --strict .`
- **Exit codes.** `0` clean; `1` type errors; `2` usage.
- **Used at.** `audit_static.py`.

### ts-prune / vulture
- **ts-prune install.** `npm i -D ts-prune`. Detects unused TypeScript exports.
- **vulture install.** `pipx install vulture`. Detects unused Python code.
- **Invocation.** `npx ts-prune` / `vulture src/`.
- **Exit codes.** Both: non-zero on findings.
- **Used at.** Optional Gate 4 dead-code check; not yet wired but recommended.

## Test and coverage

### vitest
- **Install.** `npm i -D vitest`.
- **Invocation.** `npx vitest run --reporter=json`.
- **Exit codes.** `0` all pass; `1` failures.
- **Used at.** `audit_unit.py`.

### jest
- **Install.** `npm i -D jest`.
- **Invocation.** `npx jest --json --ci`.
- **Exit codes.** `0` pass; `1` failures.
- **Used at.** `audit_unit.py`.

### pytest
- **Install.** `pipx install pytest pytest-json-report`.
- **Invocation.** `pytest --tb=no -q --json-report --json-report-file=-`.
- **Exit codes.** `0` pass; `1` failures; `2` interrupted; `5` no tests.
- **Used at.** `audit_unit.py`.

### diff-cover
- **Install.** `pipx install diff-cover`.
- **Invocation.** `diff-cover coverage.xml --compare-branch=origin/main --fail-under=80 --json-report diff-cover.json`.
- **Exit codes.** `0` met threshold; `1` below.
- **Used at.** `audit_coverage.py`. Falls back to coverage.xml line-rate or `coverage-final.json` if diff-cover is missing.

### Stryker (Node mutation testing)
- **Install.** `npm i -D @stryker-mutator/core @stryker-mutator/vitest-runner`.
- **Invocation.** `npx stryker run`.
- **Output.** `reports/mutation/mutation-report.json` with `mutationScore`.
- **Used at.** `audit_mutation.py`. Threshold: 60%.

### mutmut (Python mutation testing)
- **Install.** `pipx install mutmut`.
- **Invocation.** `mutmut run` then `mutmut results`.
- **Used at.** `audit_mutation.py`. Threshold: 60%.

## E2E and contract

### Playwright
- **Install.** `npm i -D @playwright/test && npx playwright install`.
- **Invocation.** `npx playwright test --reporter=json`.
- **Exit codes.** `0` pass; `1` failures.
- **Used at.** `audit_e2e.py`. Requires baseURL to be a real preview URL (not localhost). Tests must include at least one `@golden-path` tag.

### oasdiff
- **Install.** `go install github.com/tufin/oasdiff@latest` or `brew install oasdiff`.
- **Invocation.** `oasdiff breaking <old.yaml> <new.yaml>`.
- **Exit codes.** `0` no breaking changes; non-zero with output on breaking.
- **Used at.** `audit_contract.py`. The audit stashes `origin/main:openapi.yaml` to a temp file for comparison.

### graphql-inspector
- **Install.** `npm i -g @graphql-inspector/cli`.
- **Invocation.** `graphql-inspector diff <old.graphql> <new.graphql>`.
- **Used at.** `audit_contract.py`.

## Deploy and operations

### Vercel CLI
- **Install.** `npm i -g vercel`.
- **Invocation.** `vercel --prod`, `vercel inspect <url>`.
- **Used at.** Gate 7 deploy (manual or scripted).

### Netlify CLI
- **Install.** `npm i -g netlify-cli`.
- **Invocation.** `netlify deploy --prod`.
- **Used at.** Gate 7.

### Argo CD / Argo Rollouts
- **Install.** Cluster-side; `kubectl argo rollouts` plugin.
- **Used at.** Gate 7 (canary rollouts and rollback drills) for k8s shops.

### gh CLI
- **Install.** `brew install gh && gh auth login`.
- **Invocation.** `gh api repos/:owner/:repo/branches/main/protection`.
- **Exit codes.** `0` ok; non-zero on auth/permission.
- **Used at.** `audit_warranty.py` to verify branch protection required checks.

## Repo conformance

### repolinter
- **Install.** `npm i -g repolinter`.
- **Invocation.** `repolinter lint .`.
- **Exit codes.** `0` clean; `1` violations.
- **Used at.** Optional Gate 9 enforcement; verifies that LICENSE, README, etc. are present and conformant.

## Tool-runner contract

`scripts/lib/tool_runner.py::run(cmd, cwd=None, timeout=120)` returns a `ToolResult(exit_code, stdout, stderr)`. On `FileNotFoundError`, exit code is `127` with stderr `binary not found: <name>`. On timeout, exit code is `124`. Audits MUST treat 127 as `INFO` (tool optional/missing), not as `CRITICAL`. The exception is `audit_warranty.py`, which expects CI to have the tools and treats their absence as a HIGH finding because Gate 9 is the warranty.

## Why exit codes matter

Audits compose. The orchestrator's `audit` subcommand merges every script's `Report` into a single aggregate. Exit code 0 means no HIGH/CRITICAL findings; anything else fails the gate. Tools that exit 127 because they are not installed locally would otherwise close gates by default; the `INFO` mapping prevents that. CI should fail fast on missing tools by adding an explicit "preflight" job that runs `command -v <tool>` for each tool the audit suite expects.
