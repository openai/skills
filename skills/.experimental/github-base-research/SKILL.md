---
name: github-base-research
description: Conduct in-depth parallel research across GitHub repositories and determine whether one high-quality project or a composable set of projects should be used as the base for building a requested app or tool. Use when users ask to find existing repositories to start from, compare open-source foundations, avoid building from scratch, or combine multiple repos into one implementation plan.
---

# GitHub Base Research

Use this skill to research existing GitHub projects before proposing fresh implementation.

## Follow this workflow

1. Distill the build goal into a capability list.
Define:
- Core capabilities (required)
- Nice-to-have capabilities
- Preferred stack/language
- License constraints
- Deployment/runtime constraints

2. Build a query matrix.
Generate 8-20 targeted search queries that cover:
- Functional keywords
- Domain terms
- Framework/runtime variants
- "awesome" lists and starter kits

Use `references/query-playbook.md` for query patterns.

3. Collect repository data in parallel.
Use the bundled script:

```bash
bash scripts/collect_github_repos.sh \
  --queries-file /tmp/queries.txt \
  --output /tmp/repo-candidates.json \
  --per-query 30 \
  --parallel 4 \
  --min-stars 50 \
  --max-candidates 120
```

This script:
- Executes GitHub search queries in parallel
- Uses retry/backoff on GitHub API rate-limit responses
- Falls back to serial execution if burst parallelism fails
- Deduplicates candidate repos
- Fetches detailed metadata for each repo in parallel
- Filters low-signal results by star threshold and archived/fork status
- Produces one normalized JSON array

If API secondary limits are noisy, rerun with:

```bash
bash scripts/collect_github_repos.sh \
  --queries-file /tmp/queries.txt \
  --output /tmp/repo-candidates.json \
  --safe-mode
```

4. Score and rank candidates.
Use the scoring script:

```bash
python3 scripts/rank_github_bases.py \
  --input /tmp/repo-candidates.json \
  --required-capabilities "auth,rbac,billing,audit-log" \
  --preferred-language "TypeScript" \
  --min-stars 50 \
  --max-inactive-days 730 \
  --top 12 \
  --combo-max 3 \
  --emit-markdown /tmp/base-research-report.md
```

5. Run hard quality gates before final recommendation.
Reject candidates that are:
- Archived, disabled, or unlicensed when license is required
- Inactive for long periods unless intentionally stable
- Mostly abandoned (few recent commits, unresolved issue backlog, poor docs)

Use `references/evaluation-rubric.md` for thresholds and judgment rules.

6. Recommend one base or a composable set.
Prefer a single base repository when it covers required capabilities with acceptable quality.
Recommend a multi-repo composition when:
- No single repo covers required capabilities
- Best candidates specialize in complementary subsystems
- Integration effort remains realistic

7. Deliver a decision-ready output.
Always provide:
- Ranked shortlist with scores and rationale
- Single-base recommendation (or explicit "none")
- Multi-repo composition option (if viable)
- Risks, integration effort, and missing capabilities
- Clear next implementation step

Use `references/report-template.md` to format final output.

## Notes

- Prioritize maintainability and integration fit over star count alone.
- Treat high stars with stale maintenance as medium risk by default.
- Prefer explicit licenses (MIT/Apache-2.0/BSD) for commercial viability unless user says otherwise.
- Scripts are compatible with macOS default Bash 3.2 (no `readarray` dependency).
