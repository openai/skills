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

## Example query file

```text
feature flag platform starter kit typescript
feature flag management api react nextjs
open source feature management service go
policy engine authorization rbac service
audit log sdk typescript node
```

## Collection sequence

1. Collect candidates in parallel:

```bash
bash scripts/collect_github_repos.sh \
  --queries-file /tmp/queries.txt \
  --output /tmp/repo-candidates.json \
  --per-query 40 \
  --parallel 8 \
  --max-candidates 120
```

2. Rank and propose base repo strategy:

```bash
python3 scripts/rank_github_bases.py \
  --input /tmp/repo-candidates.json \
  --required-capabilities "auth,authorization,audit-log" \
  --preferred-language "TypeScript" \
  --top 12 \
  --combo-max 3 \
  --emit-markdown /tmp/base-research-report.md
```

## Coverage guidance

- Include at least 2 framework variants when stack is unspecified.
- Include at least 2 architecture shapes (library + full app) when possible.
- Include at least 1 query focused on integrations (payments, queue, search, auth provider).
- Avoid narrowing too early with very specific adjectives.
