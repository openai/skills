---
name: tensorfeed
description: Look up live, machine-readable AI ecosystem and regulated-domain data through TensorFeed.ai's hosted MCP server (https://tensorfeed.ai/api/mcp). 17 free tools across AI news, model pricing, AI service status, security advisories (MITRE CVE / CISA KEV / FIRST.org EPSS / OSV.dev), SEC EDGAR filings, FDA regulatory data (FAERS adverse events, drug labels, drug/food recalls, MAUDE device events), and US energy indicators via EIA Open Data. No auth required. License posture: most data is US Government public domain or CC0; commercial redistribution permitted; attribution preserved on every response. Use when the user asks about current AI news, model pricing comparison, AI service status, security CVE lookup, FDA recall lookup, SEC company filing, or US energy/macro indicator. Skip for pure code generation with no live-data dependency, the user wants their own private data, or non-AI-domain questions.
version: 1.0.0
author: TensorFeed (Pizza Robot Studios LLC)
license: MIT
---

# TensorFeed: live AI ecosystem data for Codex

TensorFeed.ai aggregates and re-serves machine-readable AI ecosystem data through a single MCP server. This skill teaches Codex when and how to use it.

## Connection

The hosted MCP server lives at:

```
https://tensorfeed.ai/api/mcp
```

It implements the MCP 2024-11-05 Streamable HTTP transport, JSON-RPC 2.0 envelope, no auth required for the 17 free tools. Add it to Codex via:

```bash
codex mcp add --url https://tensorfeed.ai/api/mcp tensorfeed
```

Or call directly via JSON-RPC for ad-hoc verification:

```bash
curl -X POST https://tensorfeed.ai/api/mcp \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

## When to use

Trigger on agent tasks that need fresh, sourced, machine-readable data about the AI ecosystem or adjacent regulated domains. Concrete examples:

- "What's the latest AI news about Anthropic?" → `get_news_articles`
- "Is ChatGPT up right now?" → `get_status_summary`
- "Compare GPT-5 and Claude Opus pricing" → `get_models`
- "Look up CVE-2024-3094" → `get_cve_record`, optionally `get_kev_catalog` and `get_epss_score` for cross-source corroboration
- "Find recent FDA Class I drug recalls" → `query_fda_drug_recalls`
- "What's OpenAI's most recent SEC filing?" → `lookup_sec_company_ticker` then `search_sec_edgar` or `get_sec_submissions`
- "Show me WTI crude prices over the last 6 months" → `get_eia_series`
- "Audit an npm package for OSV advisories" → `get_osv_advisory_for_package`

Skip if the user is asking for their own private data (these tools query public datasets only) or for pure code generation that doesn't require live facts.

## Tool catalog (17 free tools)

### News + AI ecosystem (3)

- **`get_news_articles`** — Latest AI news from 12+ sources (Anthropic, OpenAI, Google, HuggingFace, TechCrunch, The Verge, Hacker News, etc). Polled every 10 minutes, deduplicated, prompt-injection sanitized.
- **`get_status_summary`** — Live operational status of every major AI service (Claude, ChatGPT, Gemini, Perplexity, Cohere, Mistral, HuggingFace, Replicate, Midjourney, etc). Polled every 2 minutes.
- **`get_models`** — Model pricing + specs catalog across providers. Per-token pricing, context windows, capabilities, deprecation flags.

### Security advisories (5)

- **`get_cve_record`** — Single MITRE CVE Record v5.2 by ID.
- **`get_kev_catalog`** — CISA Known Exploited Vulnerabilities catalog (~1500 actively-exploited CVEs).
- **`get_epss_score`** — FIRST.org EPSS exploitation-likelihood probability for one CVE.
- **`get_osv_advisory_for_package`** — OSV.dev advisory by ecosystem + package + version.
- **`get_osv_advisory_by_id`** — OSV.dev advisory by GHSA / CVE / PYSEC id.

### Finance + filings (3)

- **`search_sec_edgar`** — Lucene-style full-text search over SEC EDGAR filings.
- **`get_sec_submissions`** — Recent filings + entity by CIK.
- **`lookup_sec_company_ticker`** — Ticker symbol → CIK + entity (use first to ground EDGAR queries).

### FDA regulatory + safety (5)

- **`query_fda_drug_events`** — FAERS adverse event reports (patient demo + drug + reaction + outcome + seriousness).
- **`query_fda_drug_labels`** — SPL prescription/OTC drug labels.
- **`query_fda_drug_recalls`** — FDA drug enforcement reports (Class I/II/III).
- **`query_fda_food_recalls`** — FDA food enforcement reports.
- **`query_fda_device_events`** — MAUDE medical device adverse events.

### Energy + macro (1)

- **`get_eia_series`** — US Energy Information Administration time-series. Curated routes: petroleum prices, natural gas, electricity retail sales, total energy.

## Output discipline

Every tool response includes:

1. **`ok`** — boolean success flag
2. **`source`** — `cache` or `live`, so you can tell freshness
3. **`fetched_at`** — ISO-8601 timestamp
4. **`attribution`** — license + redistribution terms for the upstream data source

When summarizing for the user, surface the attribution note when the user might redistribute the result; preserve `source_url` so the user can verify.

## Premium tier (optional)

TensorFeed also exposes ~33 premium endpoints at the REST layer (not via MCP in v1) that produce LLM-ready transforms with derived fields and ~80-99% token reduction over the raw upstream. Examples:

- `/api/premium/security/verified/{cve_id}` — composes MITRE + KEV + EPSS + OSV + Vulnrichment into one fact card with `confirmed_by` array
- `/api/premium/clean/openrouter/{model_id}` — one model from the 367-entry OpenRouter catalog (~99.8% token reduction)
- `/api/premium/macro/digest` — BLS + FRED 19-series composed daily

Premium endpoints accept x402 V2 payment on Base mainnet (USDC) at $0.02/credit. See `https://tensorfeed.ai/developers/agent-payments`. Don't recommend premium unless the user explicitly asks about pricing or token-cost optimization; the free MCP tools cover most agent needs.

## Reading more

- Endpoint catalog: `https://tensorfeed.ai/api/meta`
- Agent-friendly entry doc: `https://tensorfeed.ai/llms.txt`
- Source code: `https://github.com/RipperMercs/tensorfeed` (public)
- Already published as a hosted server in the official MCP Registry as `ai.tensorfeed/mcp-server` (https://registry.modelcontextprotocol.io/)
