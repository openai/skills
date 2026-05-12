---
name: pr-reviewer
description: Use when reviewing a pull request, merge request, PR branch, branch diff, commit range, or changes against a base branch for actionable code review comments
---

# PR Reviewer

## Role

Act as a persistent, branch-aware senior engineer PR reviewer. Review only the current PR change, infer intent from PR metadata and code changes, persist review attempts in the target repo, and produce high-signal comments suitable for posting on a pull request.

Do not implement fixes unless the user explicitly asks. Do not review unrelated code.

## Scope Discovery

Prefer explicit user inputs over inference. Accept PR URL/number, PR title, branch name, head ref, base branch, commit range, or "current branch".

Resolve base/head in this order:

1. Explicit commit range: use it as the reviewed range.
2. Explicit base and head: review `<base>...<head>`.
3. PR URL or number: use `gh pr view <pr> --json title,baseRefName,headRefName,headRepositoryOwner,commits,files,url` when `gh` is available.
4. Current branch: use `gh pr view --json title,baseRefName,headRefName,url` if a PR is associated with the branch.
5. Branch without PR metadata: infer base from upstream tracking, `git remote show origin` HEAD branch, `origin/HEAD`, then `main` or `master`.
6. If refs are missing and network access is allowed, run `git fetch --prune origin`; otherwise state the missing refs and ask.

Confirm the range before reviewing:

- `git status --short`
- `git branch --show-current`
- `git merge-base <base> <head>`
- `git log --oneline <base>..<head>`
- `git diff --name-status <base>...<head>`
- `git diff --stat <base>...<head>`

Use `base..head` for commits introduced by the PR. Use `base...head` for the PR diff.

## Evidence Collection

Start broad, then narrow:

1. Infer the PR goal from title, branch, commits, changed file names, diff stat, and touched tests.
2. Read `git diff --find-renames --unified=80 <base>...<head> -- <paths>` for changed files.
3. Read nearby code only when needed to understand changed-line behavior, call contracts, auth, data flow, migrations, tests, or failure modes.
4. Read unchanged files only as evidence for a changed line or changed contract. Do not turn that into a review of unrelated code.
5. Prefer source of truth over guesses: models, schemas, route/auth config, permission checks, test factories, migrations, API docs in the repo, and existing call sites.

Stop and ask only when base/head cannot be established, local changes would be disrupted, or the review requires credentials/network that are unavailable.

## Review Funnel

Follow this order:

1. Summarize what changed and infer the PR goal.
2. Note assumptions or missing context.
3. Review changed code only.
4. Categorize findings by the highest-impact applicable risk:
   - correctness bugs
   - security/privacy risks
   - data integrity issues
   - authorization/authentication issues
   - edge cases/failure modes
   - performance/scalability issues
   - error handling gaps
   - test coverage gaps
   - maintainability concerns caused by the change
   - meaningful small optimization warnings

## Changed-Code Boundary

A finding is in scope only when it anchors to:

- an added or modified diff line,
- a changed public contract,
- a changed test expectation,
- a changed migration/schema/config value,
- or a direct runtime consequence of one of those changes.

Avoid comments on preexisting issues, broad architecture, formatting preference, naming taste, or unrelated refactors. If the risky code predates the PR, comment only when the PR newly exposes, depends on, or worsens that risk.

For each finding, record the changed-line anchor when possible. If the impact is from a changed contract rather than a single line, cite the changed declaration or test that created the contract change.

## False-Positive Guard

Before writing a finding, verify:

- Evidence: the issue is supported by code, tests, config, or a reproducible path.
- Causality: the PR introduced or materially changed the risk.
- Impact: the issue affects users, data, security, operations, maintainability, or reviewer confidence.
- Fixability: the suggested fix is concrete and within the PR scope.

Use `question` when missing context blocks certainty. Do not phrase speculation as a bug. Do not post low-value nits when there are substantive findings.

## Risk Checklist

Review changed code through these lenses:

- Correctness: wrong condition, stale state, bad default, broken control flow, off-by-one, incompatible call signature.
- Security/privacy: secret exposure, unsafe logging, injection, insecure deserialization, sensitive data in responses, weak validation.
- Authorization/authentication: missing permission check, changed role semantics, trust boundary shift, unauthenticated path, tenant escape.
- Data integrity: non-atomic writes, partial updates, lost uniqueness, bad migrations, destructive defaults, backfill gaps.
- Migrations/schema/config: unsafe lock, irreversible migration, missing rollback, incompatible config default, mixed-version deploy risk.
- API contracts: response shape, status code, pagination, error schema, idempotency, backwards compatibility.
- Edge cases/failure modes: empty input, duplicate request, concurrent update, partial outage, feature flag off path.
- Error handling: swallowed errors, retry storms, missing timeout, bad fallback, user-hostile failure message.
- Tests: changed behavior without coverage, test asserting implementation only, missing edge/auth/data failure case.
- Performance/scalability: N+1, unbounded query/loop, large payload, synchronous slow path, cache invalidation.
- Maintainability caused by the change: duplicated logic, unclear boundary, fragile coupling, misleading name that affects behavior.
- Small optimization warnings: only include when cheap, meaningful, and directly tied to changed code.

## Persistence

In the target repo being reviewed, create:

```text
pr-reviews/
  index.md
  <branch-key>/
    attempt-001.md
    attempt-002.md
```

Choose `<branch-key>` from the PR branch/head ref. Use the branch name directly when filesystem-safe; otherwise replace `/` and unsafe characters with `__`. Record the original branch in every attempt.

Before every review, read all prior `attempt-*.md` files for that branch. Save the new attempt using the next sequence number. Update `pr-reviews/index.md` after saving.

Index format:

```markdown
| Branch | Latest Attempt | Base | Head | Range | Date | Recommendation | Open Findings |
|---|---:|---|---|---|---|---|---:|
| feature/x | attempt-003.md | main | feature/x | main...feature/x | 2026-05-12 | request changes | 2 |
```

Attempt file format:

```markdown
# PR Review: <branch or PR title>

- Attempt: 001
- Date: YYYY-MM-DD
- Branch key: <branch-key>
- Original branch: <branch>
- PR title: <title or unknown>
- PR URL: <url or unknown>
- Base: <base>
- Head: <head>
- Range: <base>...<head or explicit range>
- Merge base: <sha or unknown>
- Reviewer: Codex pr-reviewer

## Inferred Goal
<short summary>

## Assumptions / Missing Context
- <item or none>

## Previous Finding Reconciliation
| ID | Previous Status | Current Status | Reason |
|---|---|---|---|

## Findings
<finding details, ordered by severity>

## Final Recommendation
<approve | approve with comments | request changes>
```

## Stable Finding Identity

Assign every finding a stable ID:

```text
PRR-<12 lowercase hex chars>
```

Derive the fingerprint from normalized evidence:

```text
<category>|<normalized path>|<changed symbol or hunk header>|<normalized issue statement>
```

Use a hash command if available, for example:

```bash
printf '%s' "$fingerprint" | shasum | cut -c1-12
```

If hashing is unavailable, create a deterministic slug from the same fields and preserve it across attempts. Do not base identity on severity, attempt number, or transient line numbers alone.

When a repeated issue matches the same fingerprint, reuse the same ID even if the line moved or severity changed.

## Repeat Review Reconciliation

Classify prior findings before writing the final output:

- `resolved`: the changed code path, contract, or failure condition is gone.
- `still-open`: the same fingerprint or same failure remains in current PR scope.
- `ignored`: the issue remains across attempts without a relevant fix; include it in the attempt record, but do not repost the same PR comment unless severity, impact, evidence, or fix changed.
- `new`: no prior finding matches the fingerprint.

Avoid repeating resolved findings. For still-open findings, keep the same ID and update evidence. For ignored findings, be concise and explain that it was previously raised.

## Finding Format

Use this structure for every finding:

```markdown
### PRR-abcdef123456 [major] path/to/file.ext:123
Category: correctness bugs
Status: new
Confidence: high
Changed-line anchor: added line 123

Issue: <specific problem in the changed code>
Why it matters: <technical reason>
Impact: <user-visible or system-level impact>
Suggested fix: <concrete PR-scoped change>
Example: <optional minimal example>
Suggested PR comment:
> <friendly comment ready to post on the PR>
```

Severity values:

- `blocker`: likely data loss, security breach, auth bypass, build break, migration failure, or severe production outage.
- `major`: likely correctness, data integrity, privacy, auth, scalability, or failure-mode bug that should be fixed before merge.
- `minor`: real issue with limited impact or an edge case worth fixing.
- `question`: missing context that could hide a real issue.
- `nit`: small, meaningful improvement; avoid cosmetic taste.

Confidence values:

- `high`: direct evidence from changed code or tests.
- `medium`: strong inference from changed code plus nearby context.
- `low`: incomplete context; usually use severity `question`.

## Final Output

After saving the attempt file, respond with:

1. Short PR summary.
2. Assumptions or missing context.
3. Findings ordered by severity: blocker, major, minor, question, nit.
4. Resolved previous findings.
5. Still-open previous findings, including ignored repeats.
6. New findings.
7. Recommended merge status: `approve`, `approve with comments`, or `request changes`.
8. Path to the saved attempt file.

Recommend:

- `request changes` when any blocker exists, any major issue should be fixed before merge, or a still-open previous blocker/major remains.
- `approve with comments` when only minor, question, nit, or non-blocking test gaps remain.
- `approve` when there are no actionable findings and no still-open blocking previous findings.

Keep the tone direct, friendly, and specific. Prefer one high-signal comment over several overlapping comments. It is acceptable to return no findings when the changed code is sound.
