# pipeline

Add and validate CI/CD workflows one bundle at a time.

## Billing Failures

CI failures can be caused by **billing/usage limits** (e.g., exhausted GitHub Actions minutes), not code issues. If CI fails and you suspect a billing issue, **run the equivalent steps locally** to validate. If local runs pass, treat the bundle as validated and proceed. Note in the REPORT that validation was done locally.

## Rules

1. **One bundle per run, one run per phase** - add one workflow, validate all. Bundles accumulate across phases as the project matures.
2. **GitHub Actions first** - GitLab CI noted but limited support
3. **Respect known-issues.md** - skip workflows marked as flaky
4. **Document secrets, never create them** - just document requirements
5. **3-minute timeout** - if CI still running, report and exit
6. **Monorepo aware** - matrix builds or path filters
7. **PR-aware** - check and fix open PRs with failing CI or pending reviews
8. **Address reviews** - apply code changes from review comments when actionable
9. **Questions need humans** - flag review questions for manual response, don't guess

### No Deferral Policy

- NEVER mark a task as "pending", "requires X", or "blocked" if the blocker is something YOU can resolve
- If a dependency needs installing, INSTALL IT
- If a workflow file needs creating, CREATE IT
- If a config needs generating, GENERATE IT
- "The environment isn't set up" is NOT a blocker -- setting it up IS the task
- The ONLY valid blocker is something that requires USER input, credentials/secrets you don't have, or sudo access
- If you skip a task that was executable, that is a **critical failure**

## Master List (5 Bundles)

Industry standard order (fast feedback to comprehensive):

| Priority | Bundle | Contents |
|----------|--------|----------|
| 1 | **Code Quality** | Lint + format check + type check |
| 2 | **Build & Test** | Build + unit tests + coverage reporting |
| 3 | **Security** | Secrets scanning (gitleaks) + SAST/CodeQL + dependency review |
| 4 | **Integration** | E2E tests + integration tests + DB migration dry-run |
| 5 | **Operations** | Failure notifications + Dependabot/Renovate + release tagging + deploy trigger + post-deploy smoke test |

## Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--dry-run` | false | Preview what would happen without changes |
| `--skip-install` | false | Don't create workflow files |
| `--verbose` | true | Show full CI output |
| `--pr <number>` | none | Focus on specific PR (fix CI failures, address reviews) |

## Flow

### Step 1: DETECT

1. Check for `.spec_system/CONVENTIONS.md`
   - If missing: Run initspec yourself to create it. Only ask the user if initspec requires user input you don't have.
   - Read Stack section for languages/runtimes
   - Read CI/CD section for platform and configured workflows
   - Read Workspace Structure table (if present) for package list and stacks

2. Read `.spec_system/state.json` for monorepo context:
   - `monorepo` field: `true` / `false` / `null`
   - `packages` array (when `monorepo: true`): each entry has `name`, `path`, `type`, `stack`

3. Detect CI platform from existing files:
   - `.github/workflows/` = GitHub Actions
   - `.gitlab-ci.yml` = GitLab CI (note: limited support)
   - If none: Default to GitHub Actions

4. Check for open PRs with CI issues:
   ```bash
   gh pr list --state open --json number,title,statusCheckRollup,reviewDecision
   ```
   - Identify PRs with failing checks
   - Identify PRs with requested changes
   - If `--pr <number>` specified, focus on that PR

5. Check for `.spec_system/audit/known-issues.md`
   - Load Skipped Workflows section
   - Note: "Known issues loaded (N workflows skipped)"

6. If `--dry-run`: Skip to Dry Run Output

### Step 1a: Determine Workflow Strategy (Monorepo Only)

**Skip this step if** `monorepo` is not `true` in state.json.

When `monorepo: true`, determine the CI/CD strategy based on workspace structure:

1. **Identify workspace manager**: Check for turbo.json, nx.json, pnpm-workspace.yaml, Cargo.toml workspace, go.work
2. **Determine trigger strategy**:
   - **Path filters**: Workflows trigger only when files in the relevant package change. Use when packages are independent or loosely coupled.
   - **Matrix builds**: A single workflow runs jobs for each package. Use when packages share the same language/toolchain.
   - **Task runner delegation**: Delegate to turbo/nx/cargo which handles caching and dependency ordering. Use when a workspace task runner is present.
3. **Map package dependencies**: If package B depends on package A, changes to A must trigger CI for both A and B

Example workflow strategy:
```
Monorepo CI strategy:
- Task runner: turbo (detected)
- Trigger: path filters per package + shared paths trigger all
- Quality: turbo run lint typecheck (handles per-package)
- Test: turbo run test (handles per-package with caching)
- Shared paths: packages/shared/**, .github/**, package.json
```

### Step 2: COMPARE

Compare CI/CD table in CONVENTIONS.md against 5-bundle master list:
- Check Bundle column for "configured" vs "not configured"
- Scan `.github/workflows/` for existing workflow files
- Build list of missing bundles in priority order

If all bundles configured: "All CI/CD workflows configured. Jumping to Step 5"

### Step 3: SELECT

Pick the highest-priority missing bundle from Step 2.

Output: "Selected: [Bundle Name] - not yet configured"

### Step 4: IMPLEMENT

Generate workflow file(s) for the selected bundle.

**Workflow templates by bundle:**

| Bundle | Workflow File | Triggers |
|--------|---------------|----------|
| Code Quality | `.github/workflows/quality.yml` | push, pull_request |
| Build & Test | `.github/workflows/test.yml` | push, pull_request |
| Security | `.github/workflows/security.yml` | push, pull_request, schedule |
| Integration | `.github/workflows/integration.yml` | pull_request (to main) |
| Operations | `.github/workflows/release.yml` + `deploy.yml` + dependabot.yml | push to main, tags |

**Monorepo workflow generation** (when `monorepo: true`):

- **With task runner (turbo/nx)**: Use the task runner as the build orchestrator. It handles per-package execution, caching, and dependency ordering automatically.
  ```yaml
  # Example: turbo-based quality workflow
  jobs:
    quality:
      steps:
        - run: pnpm install
        - run: pnpm turbo run lint typecheck
  ```
- **Without task runner**: Use path filters per package to trigger targeted jobs, plus a shared trigger for common files.
  ```yaml
  # Example: path-filtered triggers
  on:
    push:
      paths:
        - 'apps/web/**'
        - 'packages/shared/**'    # shared dependency
        - '.github/workflows/**'  # workflow changes
  ```
- **Mixed stacks**: Use matrix strategy to run language-specific jobs per package.
  ```yaml
  # Example: matrix for mixed stacks
  strategy:
    matrix:
      include:
        - package: apps/web
          lang: node
          commands: "biome ci && vitest run"
        - package: apps/api
          lang: python
          commands: "ruff check . && pytest"
  ```
- **Cross-package dependencies**: Changes to shared packages (type: library) must trigger CI for all dependent packages. Map these via workspace config or the `packages` array in state.json.

**Single-repo**: Generate standard single-target workflows.

**Language-specific jobs** (from CONVENTIONS.md Stack):

| Language | Quality | Build & Test | Security |
|----------|---------|--------------|----------|
| Python | ruff check, ruff format --check, mypy | pytest --cov | CodeQL, gitleaks, pip-audit |
| TypeScript | biome ci | vitest run --coverage | CodeQL, gitleaks, npm audit |
| Rust | cargo fmt --check, cargo clippy | cargo test | cargo audit |
| Go | gofmt -d, golangci-lint | go test | govulncheck |

**Database migration testing** (when migration tool detected in CONVENTIONS.md):
- Add DB service to integration workflow (PostgreSQL, MySQL, etc. matching project's DB type)
- Migration validation steps: run all migrations from scratch, run down migrations (verify rollback), run up again (verify idempotency)
- Optionally run seed script to verify seed data loads against fresh schema
- Scope: Add to Integration bundle workflow (`.github/workflows/integration.yml`)

**Deployment workflow** (when Operations bundle is selected):
- Create `.github/workflows/deploy.yml` triggered on push to main (after tests pass)
- If the infra workflow step has configured a deploy target (webhook, Git-based, or platform integration), wire it into the workflow
- Add a post-deploy smoke test step: `curl -f https://[production-url]/health` (or equivalent health endpoint)
- If smoke test fails, the workflow should report failure (rollback is manual unless platform supports automatic rollback)
- If no deploy target is configured yet, generate a placeholder workflow with a `TODO` comment and document in REPORT
- **Monorepo**: Create per-package deploy jobs (triggered by path filters) or a single orchestrated deploy using the task runner

1. Generate workflow YAML with appropriate jobs
2. **Monorepo**: Include path filters, matrix strategy, or task runner delegation as determined in Step 1a
3. Commit and push to current branch
4. If secrets required, document in output (don't create secrets)

### Step 5: VALIDATE

Trigger and monitor CI:

1. Push triggers workflows
2. Poll `gh run list --limit 5` for up to 3 minutes
3. Check status of ALL workflows, not just the new one
4. `gh run view <id> --log` for failures

**If `--pr` specified or open PRs detected:**

1. Check PR CI status:
   ```bash
   gh pr checks <number>
   ```

2. Get PR review comments:
   ```bash
   gh pr view <number> --json reviews,comments
   ```

3. Identify actionable items:
   - Failing CI checks on PR branch
   - Review comments requesting changes
   - Unresolved review threads

**If CI fails due to billing/usage limits** (see Billing Failures above):
- Run the workflow's steps locally (lint, test, build, etc.) to validate
- If local runs pass, treat as validated and continue to Step 7

**If still running after 3 minutes:**
```
CI still running. Validate locally and proceed.
```

### Step 6: FIX

**For CI failures:**

1. Parse error logs from `gh run view --log`
2. Identify failing file and line
3. Attempt fix locally
4. Commit, push, re-poll

**For each category:**
- **Lint/format errors**: Run local tools with fix flag, commit
- **Type errors**: Attempt fix, verify locally first
- **Test failures**: Attempt fix, run locally to verify
- **Security findings**: Evaluate severity, fix or add to known-issues.md

**For PR review comments** (when `--pr` or PRs detected):

1. Fetch review comments:
   ```bash
   gh api repos/{owner}/{repo}/pulls/{number}/comments
   ```

2. For each actionable comment:
   - Parse file path and line number from comment
   - Read the code context
   - Apply the requested change
   - Commit with message: "Address review: <summary>"

3. For review threads:
   - Group related comments by thread
   - Address the root issue
   - Reply to confirm resolution (if possible via API)

**Review comment categories:**
- **Code style**: Apply formatting/naming changes
- **Logic issues**: Fix bugs or improve implementation
- **Missing tests**: Add requested test cases
- **Documentation**: Add/update comments or docs
- **Questions**: If clarification needed, note in report for manual response

**After 3 failed attempts per issue**: Try a completely different approach. Only log for manual review if the fix requires secrets, platform access, or credentials you don't have.

Filter out workflows in known-issues.md Skipped Workflows section.

### Step 7: RECORD

Update `.spec_system/CONVENTIONS.md` CI/CD table:

```markdown
| Bundle | Status | Workflow |
|--------|--------|----------|
| Code Quality | configured | .github/workflows/quality.yml |
| Build & Test | configured | .github/workflows/test.yml |
| Security | not configured | - |
```

**Monorepo only**: If workflows use per-package triggers or matrix builds, note the strategy in the table:

```markdown
| Bundle | Status | Workflow | Strategy |
|--------|--------|----------|----------|
| Code Quality | configured | quality.yml | turbo run lint typecheck |
| Build & Test | configured | test.yml | matrix (per-package) |
```

### Step 8: REPORT

```
REPORT
- Added: Code Quality workflow
- File: .github/workflows/quality.yml
- Jobs: lint (ruff), format (ruff), typecheck (mypy)
- Fixed: 23 lint errors, 8 format issues
- Remaining: 0
- CI Status: All workflows passing

Required setup (if any):
- Add CODECOV_TOKEN to repository secrets for coverage upload
```

**For PRs** (when `--pr` or PRs addressed):
```
REPORT
- PR #42: "Add user authentication"
- CI Status: All checks passing (was: 3 failing)
- Fixed: 2 type errors, 1 test failure
- Reviews addressed: 4 comments resolved
- Remaining reviews: 1 (question - needs manual response)
- Review status: Changes requested -> Ready for re-review
```

**For monorepos:**
```
[apps/web] Quality: passing | Test: 2 failures
[apps/api] Quality: passing | Test: passing
```

### Step 9: RECOMMEND

- **CI failures remain**: List required actions, validate locally and fix within this run
- **PR has unresolved items**: Report status, note what needs manual response
- **PR is ready**: Confirm all checks passing and reviews addressed, recommend merge
- **Bundles remain**: Note which bundle comes next (it will be added in a future phase's pipeline run)
- **All 5 bundles configured and passing**: Recommend infra

## Dry Run Output

```
PIPELINE PREVIEW (DRY RUN)

Repository: monorepo (Turborepo)
Platform: GitHub Actions
Stack: Python 3.12, TypeScript

Configured: Code Quality, Build & Test
Missing: Security, Integration, Operations

Would add: Security
Would create: .github/workflows/security.yml
Would include: gitleaks, CodeQL (python, typescript), dependency review

Open PRs with issues:
- #42 "Add auth" - 2 failing checks, 3 review comments
- #38 "Fix bug" - 1 failing check

Required secrets:
- None for this bundle

Run without --dry-run to apply.
```

**With `--pr 42`:**
```
PIPELINE PREVIEW (DRY RUN) - PR #42

PR: #42 "Add user authentication"
Branch: feature/auth -> main
CI Status: 2 failing (quality, test)
Reviews: 3 comments (2 actionable, 1 question)

Would fix:
- src/auth.ts:23 - type error (missing null check)
- src/auth.ts:45 - lint error (unused import)
- tests/auth.test.ts - failing assertion

Would address reviews:
- src/auth.ts:30 - "Add error handling" (actionable)
- src/auth.ts:52 - "Rename variable" (actionable)
- src/auth.ts:67 - "Why this approach?" (question - manual response needed)

Run without --dry-run to apply.
```

## Secrets Handling

When a workflow requires secrets:

1. Generate workflow file with secret references
2. Document required secrets in REPORT
3. Workflow will fail until secrets configured

```
Required setup:
1. Add CODECOV_TOKEN to repository secrets
2. Add SLACK_WEBHOOK_URL for failure notifications

Workflows will fail until secrets are configured.
```

Do NOT attempt to create or manage secrets.
