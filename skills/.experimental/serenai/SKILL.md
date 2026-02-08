---
name: serenai
description: Query databases and APIs via SerenAI gateway. Pay-per-query access to SQL databases, web scraping, search APIs, and MCP tools with micropayments.
metadata:
  short-description: Pay-per-query databases and APIs
---

# SerenAI

Query databases and call APIs through SerenAI's micropayment gateway. Access SQL databases, web scrapers, search engines, and AI tools—pay only for what you use.

## Overview

SerenAI provides a unified gateway for accessing paid APIs and databases. Instead of managing multiple API keys and subscriptions, register once and access any publisher in the marketplace with prepaid credits (SerenBucks) or crypto payments (x402 protocol).

Use cases:
- Query SQL databases without provisioning infrastructure
- Scrape websites with Firecrawl (returns LLM-ready markdown)
- Search the web with Exa (neural AI search)
- Call any MCP tool exposed by publishers

## Prerequisites

1. **Register as an agent** (no authentication required):

```bash
curl -X POST https://api.serendb.com/auth/agent \
  -H "Content-Type: application/json" \
  -d '{"name": "Codex Agent"}'
```

2. **Save credentials** from response:
   - `api_key`: Use for all authenticated requests (shown once)
   - `recovery_code`: Store securely for account recovery

3. **Set environment variable**:

```bash
export SEREN_API_KEY="seren_xxxx"
```

## Quick Decision Tree

```
What do you need?
├─ Query a database → Database Query workflow
├─ Scrape a website → Use Firecrawl publisher
├─ Search the web → Use Exa publisher
├─ Call a REST API → API Proxy workflow
├─ Use an MCP tool → MCP Tool workflow
├─ Check costs first → Estimate workflow
└─ Manage wallet → Wallet workflow
```

## Workflows

### Database Query

Query any database publisher with SQL:

```bash
curl -X POST "https://api.serendb.com/publishers/{publisher-slug}/query" \
  -H "Authorization: Bearer $SEREN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT * FROM users LIMIT 10"}'
```

Tips:
- Always use `LIMIT` to control costs
- Use `/estimate` endpoint to check cost before expensive queries

### API Proxy

Call REST APIs through publishers:

```bash
curl -X POST "https://api.serendb.com/publishers/{publisher-slug}/proxy" \
  -H "Authorization: Bearer $SEREN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "method": "POST",
    "path": "/v1/scrape",
    "body": {"url": "https://example.com"}
  }'
```

### MCP Tool

Call MCP tools exposed by publishers:

```bash
curl -X POST "https://api.serendb.com/publishers/{publisher-slug}/{tool-name}" \
  -H "Authorization: Bearer $SEREN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "latest AI news"}'
```

### Estimate Cost

Check cost before executing:

```bash
curl -X POST "https://api.serendb.com/publishers/{slug}/estimate" \
  -H "Authorization: Bearer $SEREN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT * FROM large_table"}'
```

### Wallet Management

```bash
# Check balance
curl https://api.serendb.com/wallet/balance \
  -H "Authorization: Bearer $SEREN_API_KEY"

# Claim free daily credits
curl -X POST https://api.serendb.com/wallet/free-credits/claim \
  -H "Authorization: Bearer $SEREN_API_KEY"

# View transaction history
curl "https://api.serendb.com/wallet/transactions?limit=20" \
  -H "Authorization: Bearer $SEREN_API_KEY"

# Deposit funds (returns Stripe checkout URL)
curl -X POST https://api.serendb.com/wallet/deposit \
  -H "Authorization: Bearer $SEREN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"amount_usd": 10}'
```

## Popular Publishers

| Publisher | Type | Use Case |
|-----------|------|----------|
| `exa` | Search | Neural AI search with embeddings |
| `firecrawl` | Scraping | Web pages to LLM-ready markdown |
| `email-search` | Search | Find email addresses by domain |

Browse all publishers:

```bash
curl "https://api.serendb.com/publishers"
```

## Pricing

- **Database queries**: ~$0.001–0.01 per query
- **API calls**: $0.001–0.10 per call (set by publisher)
- **Free tier**: Daily free credits available

## Account Recovery

If you lose your API key:

```bash
curl -X POST https://api.serendb.com/auth/recover \
  -H "Content-Type: application/json" \
  -d '{"recovery_code": "REC-XXXX-XXXX"}'
```

This issues a new API key and revokes all previous credentials.

## Troubleshooting

### Authentication Errors
- Verify `SEREN_API_KEY` is set correctly
- Check the key starts with `seren_`
- Use recovery code if key was lost

### Insufficient Balance
- Check balance with `/wallet/balance`
- Claim free daily credits
- Deposit via Stripe (minimum $5)

### Query Errors
- Verify publisher slug exists
- Check SQL syntax for database publishers
- Use `/estimate` to validate queries

### Rate Limits
- Batch operations where possible
- Cache frequent queries
- Contact publisher for higher limits

## Resources

- Docs: https://docs.serendb.com
- Publishers: https://serendb.com/publishers
- Support: hello@serendb.com
