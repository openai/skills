---
name: x-twitter-skills
description: Research live discourse on X/Twitter for product, developer, market, and cultural topics. Use when you need current sentiment, expert takes, launch reactions, issue reports, or linked resources from X posts. Trigger when users ask things like "search X", "what are people saying on Twitter", "check X for", "X research", or when recent X conversation would materially improve an answer.
---

# X/Twitter Skills

Run fast, sourced research over X/Twitter from Codex.

For API/search operator details, read `references/x-api.md`.

## Quick Start

Run from this skill directory:

```bash
cd ~/.codex/skills/x-twitter-skills
npm install
```

Set your X API token:

```bash
export X_BEARER_TOKEN="your-token"
```

Or place it in `~/.config/env/global.env`:

```bash
X_BEARER_TOKEN=your-token
```

## CLI Commands

```bash
npm run x -- search "<query>" [options]
npm run x -- plan "<research question>" [options]
npm run x -- brief "<research question>" [options]
npm run x -- profile <username> [--count N] [--replies] [--json]
npm run x -- thread <tweet_id> [--pages N] [--archive]
npm run x -- tweet <tweet_id> [--json]
npm run x -- watchlist
npm run x -- watchlist add <user> [note]
npm run x -- watchlist remove <user>
npm run x -- watchlist check
npm run x -- cache clear
```

Search options:

- `--sort likes|impressions|retweets|recent|signal` (default: `likes`)
- `--min-score N` (applies to `--sort signal`; minimum signal threshold)
- `--since 1h|3h|12h|1d|7d|<ISO-time>`
- `--archive` use full-archive endpoint (all-time)
- `--min-likes N`
- `--min-impressions N`
- `--pages N` (1-5)
- `--limit N`
- `--quick` (1 page, max 10 results, stricter noise filter)
- `--from <username>`
- `--quality` (post-filter min 10 likes)
- `--no-replies`
- `--save` (writes markdown report to `data/drafts/`)
- `--json`
- `--markdown`

Plan options:

- `--max-queries N` (2-10)
- `--json`

Brief options:

- `--since 1h|3h|12h|1d|7d|<ISO-time>`
- `--archive`
- `--pages N` (1-5 per planned query)
- `--max-queries N` (2-10)
- `--cache-min N` (cache TTL in minutes)
- `--min-score N` (minimum signal score to include in brief synthesis)
- `--max-cost USD` (abort if worst-case reads exceed budget)
- `--compare-last` (show deltas vs last brief on same question)
- `--dry-run` (print planned queries and estimated cost without API calls)
- `--save`
- `--json`

Examples:

```bash
npm run x -- search "OpenAI Agents SDK" --quick
npm run x -- search "rust web framework" --sort likes --pages 2
npm run x -- search "ai coding agent" --archive --since 30d --limit 20
npm run x -- search "from:karpathy eval" --markdown --save
npm run x -- plan "what are devs saying about model context protocol"
npm run x -- brief "openai agents sdk adoption risks and wins" --since 3d --save
npm run x -- brief "openai agents sdk adoption risks and wins" --since 3d --max-cost 2.00
npm run x -- brief "openai agents sdk adoption risks and wins" --max-queries 4 --dry-run
npm run x -- brief "openai agents sdk adoption risks and wins" --since 3d --compare-last
npm run x -- profile levelsio --count 15
```

## Agentic Research Loop

1. Break the user question into 3-5 targeted queries.
2. Run initial searches and identify high-signal accounts/posts.
3. Follow key threads with `thread <tweet_id>`.
4. Pull linked pages/repos/docs from tweet URLs for deeper verification.
5. Use `brief` to auto-synthesize themes, voices, domains, and polarity.

## Heuristics

- Too noisy: add `-is:reply`, narrow keywords, use `--sort likes`.
- Too sparse: widen with `OR`, reduce filters, remove `--quality`.
- Expert-first: use `from:` and `--min-likes`.
- Technical depth: add `has:links` and inspect linked docs/repos.

## Guardrails

- Use this skill for read-only research and synthesis.
- Do not post, like, retweet, or perform account actions.
- Be explicit about time windows (`--since` / `--archive`) in summaries.
- Preserve source links so findings are auditable.

## Files

```text
x-twitter-skills/
├── SKILL.md
├── LICENSE.txt
├── agents/openai.yaml
├── assets/
│   ├── x-twitter-skills-small.svg
│   └── x-twitter-skills.svg
├── package.json
├── scripts/
│   ├── x-search.ts
│   ├── lib/
│   │   ├── api.ts
│   │   ├── brief.ts
│   │   ├── brief-history.ts
│   │   ├── cache.ts
│   │   ├── format.ts
│   │   ├── planner.ts
│   │   └── watchlist.ts
│   └── tests/
│       ├── api.test.ts
│       ├── brief-history.test.ts
│       ├── brief.test.ts
│       └── planner.test.ts
├── data/
│   ├── watchlist.json
│   ├── watchlist.example.json
│   └── drafts/
└── references/
    └── x-api.md
```

## Validation

```bash
npm test
```
