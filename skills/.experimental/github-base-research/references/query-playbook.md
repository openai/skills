# Query Playbook

## Objective

Generate broad but relevant repository candidates, then narrow to high-quality foundations.

## Query matrix

Create 8-20 lines in a query file by combining:

1. Problem intent terms
- `workflow automation`
- `crm integration`
- `vector search`
- `feature flag`

2. Build shape terms
- `starter kit`
- `boilerplate`
- `template`
- `reference implementation`

3. Stack/runtime terms
- `typescript`
- `go`
- `python`
- `nextjs`
- `fastapi`
- `electron`

4. Quality hints
- `production`
- `maintained`
- `monorepo`
- `cli`

5. GitHub qualifiers for signal control
- `stars:>50`
- `archived:false`
- `fork:false`
- `pushed:>=2024-01-01`

## Example query file

```text
feature flag platform starter kit typescript stars:>80 archived:false fork:false
feature flag management api react nextjs stars:>50 pushed:>=2024-01-01
open source feature management service go stars:>80 archived:false
policy engine authorization rbac service stars:>100 archived:false
audit log sdk typescript node stars:>50 fork:false
```

## Collection sequence

1. Collect candidates in parallel:

```bash
bash scripts/collect_github_repos.sh \
  --queries-file /tmp/queries.txt \
  --output /tmp/repo-candidates.json \
  --per-query 30 \
  --parallel 4 \
  --min-stars 50 \
  --max-candidates 120
```

If secondary rate limits occur, rerun safely:

```bash
bash scripts/collect_github_repos.sh \
  --queries-file /tmp/queries.txt \
  --output /tmp/repo-candidates.json \
  --safe-mode \
  --max-candidates 90
```

2. Rank and propose base repo strategy:

```bash
python3 scripts/rank_github_bases.py \
  --input /tmp/repo-candidates.json \
  --required-capabilities "auth,authorization,audit-log" \
  --preferred-language "TypeScript" \
  --min-stars 50 \
  --max-inactive-days 730 \
  --top 12 \
  --combo-max 3 \
  --emit-markdown /tmp/base-research-report.md
```

## Coverage guidance

- Include at least 2 framework variants when stack is unspecified.
- Include at least 2 architecture shapes (library + full app) when possible.
- Include at least 1 query focused on integrations (payments, queue, search, auth provider).
- Avoid narrowing too early with very specific adjectives.
