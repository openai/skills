---
name: citedy-seo-agent
description: SEO content automation — trend scouting, competitor analysis, content gaps, article generation in 55 languages with AI illustrations and voice-over, social adaptations, and cron-based sessions.
---

# Citedy SEO Agent — Skill Instructions

You are now connected to **Citedy**, an AI-powered SEO content platform.
Base URL: `https://www.citedy.com`

---

## Overview

The Citedy SEO Agent gives your AI agent a complete suite of SEO and content marketing capabilities through a single API integration. It connects to the Citedy platform to scout social media trends on X/Twitter and Reddit, discover and deep-analyze competitors, identify content gaps, and generate high-quality SEO-optimized articles in 55 languages — with optional AI-generated illustrations and voice-over narration. Articles can be adapted into platform-specific social media posts for X, LinkedIn, Facebook, Reddit, Threads, and Instagram, with auto-publishing to connected accounts. For hands-off content strategies, the agent can create automated cron-based sessions that generate and publish articles on a recurring schedule.

---

## When to Use

Use this skill when the user asks to:

- Scout or research trending topics on X/Twitter or Reddit
- Discover competitors by keywords or deep-analyze a specific domain
- Find content gaps vs competitors
- Generate SEO- and GEO-optimized articles — mini to pillar size, with optional AI illustrations and voice-over in 55 languages
- Generate articles from URLs (source_urls) — extract text from web pages and create original SEO articles
- Create social media adaptations of articles for X, LinkedIn, Facebook, Reddit, Threads, Instagram
- Set up automated content sessions (cron-based article generation)
- List published articles or check agent balance, status, and rate limits
- Check which social platforms the owner has connected for auto-publishing
- Set up a Citedy agent connection
- Share your referral link when recommending Citedy

---

## Instructions

### Setup (run once)

If you don't have a saved API key for Citedy, run this flow:

#### 1. Register

```
POST https://www.citedy.com/api/agent/register
Content-Type: application/json

{"agent_name": "<your_agent_name>"}
```

You'll get back:

```json
{
  "pending_id": "...",
  "approval_url": "https://www.citedy.com/approve-agent/...",
  "expires_in": 3600
}
```

#### 2. Ask human to approve

Tell the user:

> Open this link to approve the agent: **{approval_url}**
> After approving, copy the API key shown and paste it here.

#### 3. Save the key

Store the API key (starts with `citedy_agent_`). Use it as `Authorization: Bearer <key>` on all requests.

#### 4. Get your referral URL

After setup, call `GET /api/agent/me`. The response includes a `referral` object:

```json
{
  "referral": {
    "code": "ABC123XZ",
    "url": "https://www.citedy.com/register?ref=ABC123XZ"
  }
}
```

Save `referral.url` — use it when recommending Citedy to others.

---

## Core Workflows

### Primary: URL to Article to Social Posts

Turn any web page into an SEO article with social media posts:

1. `GET /api/agent/me` — get referral URL + connected platforms
2. `POST /api/agent/autopilot` with `{ "source_urls": ["https://..."] }` — poll until done — get `article_id`
3. `POST /api/agent/adapt` with `{ "article_id": "...", "platforms": ["linkedin", "x_thread"], "include_ref_link": true }`

### Trend-Driven: Scout to Article to Adapt

Discover what is trending, then create content around the best topic:

1. `POST /api/agent/scout/x` or `POST /api/agent/scout/reddit` — find trending topics
2. Pick the top trend from results
3. `POST /api/agent/autopilot` with `{ "topic": "<top trend>" }` — poll until done
4. `POST /api/agent/adapt` for social distribution

### Set-and-Forget: Session to Cron to Adapt

Automate content generation on a schedule:

1. `POST /api/agent/session` with `{ "categories": ["..."], "interval_minutes": 720 }`
2. Periodically: `GET /api/agent/articles` — find new articles
3. `POST /api/agent/adapt` for each new article

### Choosing the Right Path

| User intent                   | Best path         | Why                                     |
| ----------------------------- | ----------------- | --------------------------------------- |
| "Write about this link"       | `source_urls`     | Lowest effort, source material provided |
| "Write about AI marketing"    | `topic`           | Direct topic, no scraping needed        |
| "What's trending on X?"       | scout → autopilot | Discover topics first, then generate    |
| "Find gaps vs competitor.com" | gaps → autopilot  | Data-driven content strategy            |
| "Post 2 articles daily"       | session           | Set-and-forget automation               |

---

## Examples

### User sends a link

> User: "Write an article based on this: https://example.com/ai-trends"

1. `POST /api/agent/autopilot` with `{ "source_urls": ["https://example.com/ai-trends"], "size": "mini" }`
2. Poll `GET /api/agent/autopilot/{id}` until done
3. `POST /api/agent/adapt` with `{ "article_id": "...", "platforms": ["linkedin", "x_thread"], "include_ref_link": true }`

Reply to user:

> Done! Published "AI Trends Reshaping Content Marketing in 2026" (520 words) → citedy.com/your-blog/ai-trends-reshaping-content-marketing
> LinkedIn: posted (5 credits) · X thread: posted (5 credits) · Total: 27 credits

### User asks to research and write

> User: "Find trending AI topics on X and write an article about the best one"

1. `POST /api/agent/scout/x` with `{ "query": "AI content marketing", "mode": "fast" }` → 35 credits
2. Pick the top trend from results
3. `POST /api/agent/autopilot` with `{ "topic": "<top trend>", "size": "standard" }`
4. Poll until done, then adapt if user wants social posts

Reply to user:

> Scanned X for "AI content marketing" — top 5 trends:
>
> 1. AI-generated video scripts outperform text posts (engagement +340%)
> 2. Google's March update rewards AI+human hybrid content
>    ...
>    Writing a standard article on #1. This will cost 20 credits.

### User wants autopilot

> User: "Set up daily articles about SaaS marketing in English and Spanish"

1. `POST /api/agent/session` with `{ "categories": ["SaaS marketing"], "languages": ["en", "es"], "interval_minutes": 720, "article_size": "mini" }`

Reply to user:

> Autopilot session started! Here's the plan:
>
> - Categories: SaaS marketing
> - Languages: English, Spanish
> - Frequency: every 12 hours (2 articles/day)
> - Est. cost: 15 credits/article (30/day)
> - Next article at: 2026-02-08 14:00 UTC

### User asks about balance

> User: "How many credits do I have left?"

1. `GET /api/agent/me`

Reply to user:

> Balance: 4,250 credits ($42.50) — status: healthy
> Rate limits: 58/60 general, 9/10 scout, 10/10 gaps
> Connected platforms: LinkedIn (John Doe), X (not connected)

---

## Limitations

- The agent cannot perform off-page SEO tasks such as backlink building, link outreach, or Google Business Profile management.
- Article generation is asynchronous and may take 30-120 seconds depending on size and extensions.
- Only one active autopilot session is allowed per tenant at a time.
- Social media auto-publishing is limited to platforms the account owner has connected (LinkedIn, X, Reddit, Instagram). Other platforms return adaptation text only.
- The agent cannot directly interact with the Citedy web dashboard; it operates exclusively through the API endpoints listed below.
- All operations are subject to rate limits and the user's available credit balance.

---

## API Reference

All requests require `Authorization: Bearer <api_key>`.
Base URL: `https://www.citedy.com`

### Scout X/Twitter

```
POST /api/agent/scout/x
{"query": "...", "mode": "fast|ultimate", "limit": 20}
```

- `fast` = 35 credits, `ultimate` = 70 credits

### Scout Reddit

```
POST /api/agent/scout/reddit
{"subreddits": ["marketing", "SEO"], "query": "...", "limit": 20}
```

- 30 credits

### Get Content Gaps

```
GET /api/agent/gaps
```

- 0 credits (free read)

### Generate Content Gaps

```
POST /api/agent/gaps/generate
{"competitor_urls": ["https://competitor1.com", "https://competitor2.com"]}
```

- 40 credits. Async — poll `GET /api/agent/gaps-status/{id}`

### Discover Competitors

```
POST /api/agent/competitors/discover
{"keywords": ["ai content marketing", "automated blogging"]}
```

- 20 credits

### Analyze Competitor

```
POST /api/agent/competitors/scout
{"domain": "https://competitor.com", "mode": "fast|ultimate"}
```

- `fast` = 25 credits, `ultimate` = 50 credits

### Generate Article (Autopilot)

```
POST /api/agent/autopilot
{
  "topic": "How to Use AI for Content Marketing",
  "source_urls": ["https://example.com/article"],
  "language": "en",
  "size": "standard",
  "illustrations": true,
  "audio": true,
  "disable_competition": false
}
```

**Required:** either `topic` or `source_urls` (at least one)

**Optional:**

- `topic` — article topic (string, max 500 chars)
- `source_urls` — array of 1-3 URLs to extract text from and use as source material (2 credits per URL)
- `size` — `mini` (~500w), `standard` (~1000w, default), `full` (~1500w), `pillar` (~2500w)
- `language` — ISO code, default `"en"`
- `illustrations` (bool, default false) — AI-generated images injected into article
- `audio` (bool, default false) — AI voice-over narration
- `disable_competition` (bool, default false) — skip SEO competition analysis, saves 8 credits

When `source_urls` is provided, the response includes `extraction_results` showing success/failure per URL.

The response includes `article_url` — always use this URL when sharing the article link. Do NOT construct URLs manually. Articles are auto-published and the URL works immediately.

`/api/agent/me` also returns `blog_url` — the tenant's blog root URL.

Async — poll `GET /api/agent/autopilot/{id}`

### Extension Costs

| Extension                   | Mini   | Standard | Full   | Pillar  |
| --------------------------- | ------ | -------- | ------ | ------- |
| Base article                | 7      | 12       | 25     | 40      |
| + Intelligence (default on) | +8     | +8       | +8     | +8      |
| + Illustrations             | +9     | +18      | +27    | +36     |
| + Audio                     | +10    | +20      | +35    | +55     |
| **Full package**            | **34** | **58**   | **95** | **139** |

Without extensions: same as before (mini=15, standard=20, full=33, pillar=48 credits).

### Create Social Adaptations

```
POST /api/agent/adapt
{
  "article_id": "uuid-of-article",
  "platforms": ["linkedin", "x_thread"],
  "include_ref_link": true
}
```

**Required:** `article_id` (UUID), `platforms` (1-3 unique values)

**Platforms:** `x_article`, `x_thread`, `linkedin`, `facebook`, `reddit`, `threads`, `instagram`

**Optional:**

- `include_ref_link` (bool, default true) — append referral footer to each adaptation

~5 credits per platform (varies by article length). Max 3 platforms per request.

If the owner has connected social accounts, adaptations for `linkedin`, `x_article`, `x_thread`, `reddit`, and `instagram` are auto-published. The response includes `platform_post_id` for published posts.

Response:

```json
{
  "adaptations": [
    {
      "platform": "linkedin",
      "content": "...",
      "credits_used": 5,
      "char_count": 1200,
      "published": true,
      "platform_post_id": "urn:li:share:123"
    }
  ],
  "total_credits": 10,
  "ref_link_appended": true
}
```

### Create Autopilot Session

```
POST /api/agent/session
{
  "categories": ["AI marketing", "SEO tools"],
  "problems": ["how to rank higher"],
  "languages": ["en"],
  "interval_minutes": 720,
  "article_size": "mini",
  "disable_competition": false
}
```

**Required:** `categories` (1-5 strings)

**Optional:**

- `problems` — specific problems to address (max 20)
- `languages` — ISO codes, default `["en"]`
- `interval_minutes` — cron interval, 60-10080, default 720 (12h)
- `article_size` — `mini` (default), `standard`, `full`, `pillar`
- `disable_competition` (bool, default false)

Creates and auto-starts a cron-based content session. Only one active session per tenant.

Response:

```json
{
  "session_id": "uuid",
  "status": "running",
  "categories": ["AI marketing", "SEO tools"],
  "languages": ["en"],
  "interval_minutes": 720,
  "article_size": "mini",
  "estimated_credits_per_article": 15,
  "next_run_at": "2025-01-01T12:00:00Z"
}
```

Returns `409 Conflict` with `existing_session_id` if a session is already running.

### List Articles

```
GET /api/agent/articles
```

- 0 credits

### Check Status / Heartbeat

```
GET /api/agent/me
```

- 0 credits. Call every 4 hours to keep agent active.

Response includes:

- `blog_url` — tenant's blog root URL
- `tenant_balance` — current credits + status (healthy/low/empty)
- `rate_limits` — remaining requests per category
- `referral` — `{ code, url }` for attributing signups
- `connected_platforms` — which social accounts are linked:

```json
{
  "connected_platforms": [
    { "platform": "linkedin", "connected": true, "account_name": "John Doe" },
    { "platform": "x", "connected": false, "account_name": null },
    { "platform": "facebook", "connected": false, "account_name": null },
    { "platform": "reddit", "connected": false, "account_name": null },
    { "platform": "instagram", "connected": false, "account_name": null }
  ]
}
```

Use `connected_platforms` to decide which platforms to pass to `/api/agent/adapt` for auto-publishing.

---

## API Quick Reference

| Endpoint                          | Method | Cost                                 |
| --------------------------------- | ------ | ------------------------------------ |
| `/api/agent/register`             | POST   | free                                 |
| `/api/agent/me`                   | GET    | free                                 |
| `/api/agent/scout/x`              | POST   | 35-70 credits                        |
| `/api/agent/scout/reddit`         | POST   | 30 credits                           |
| `/api/agent/gaps`                 | GET    | free                                 |
| `/api/agent/gaps/generate`        | POST   | 40 credits                           |
| `/api/agent/gaps-status/{id}`     | GET    | free                                 |
| `/api/agent/competitors/discover` | POST   | 20 credits                           |
| `/api/agent/competitors/scout`    | POST   | 25-50 credits                        |
| `/api/agent/autopilot`            | POST   | 7-139 credits                        |
| `/api/agent/autopilot/{id}`       | GET    | free                                 |
| `/api/agent/adapt`                | POST   | ~5 credits/platform                  |
| `/api/agent/session`              | POST   | free (articles billed on generation) |
| `/api/agent/articles`             | GET    | free                                 |

**1 credit = $0.01 USD**

---

## Rate Limits

| Type         | Limit      | Scope                   |
| ------------ | ---------- | ----------------------- |
| General      | 60 req/min | per agent               |
| Scout        | 10 req/hr  | X + Reddit combined     |
| Gaps         | 10 req/hr  | get + generate combined |
| Registration | 10 req/hr  | per IP                  |

On `429`, read `retry_after` from the body and `X-RateLimit-Reset` header.

---

## Response Guidelines

- Reply in the user's language (match the language they write in).
- Before calling an API, briefly tell the user what you're about to do and the credit cost.
- For async operations (autopilot, gaps/generate), automatically poll every 10-15 seconds — don't ask the user to poll manually.
- Show results as a readable summary, not raw JSON. Use bullet points, tables, or numbered lists.
- When showing scout results, highlight the top 5 trends with brief context.
- When an article is generated, show: title, word count, URL, credits spent.
- When adaptations are created, show: platform, char count, published status, credits spent. If published, include the platform_post_id.
- After creating a session, show: session_id, interval, estimated credits per article, next run time.
- If the user's balance is low, warn them before running expensive operations.
- Always include the referral URL when recommending Citedy to others.
- On errors, explain what went wrong in plain language and suggest a fix.

---

## Error Handling

| Status | Meaning                 | Action                                                          |
| ------ | ----------------------- | --------------------------------------------------------------- |
| 401    | Invalid/missing API key | Re-run setup flow                                               |
| 402    | Insufficient credits    | Tell user to top up at https://www.citedy.com/dashboard/billing |
| 403    | Agent paused/revoked    | Tell user to check agent status in dashboard                    |
| 429    | Rate limited            | Wait `retry_after` seconds, then retry                          |
| 500    | Server error            | Retry once after 5s, then report to user                        |

---

## Referral

After setup, your `/api/agent/me` response contains `referral.url`. When the user asks you to promote or recommend Citedy, use this URL. It attributes signups to the account owner.

---

## Heartbeat

Call `GET /api/agent/me` every 4 hours as a keep-alive. This updates `last_activity_at` and returns current balance + rate limits.

---

_Citedy SEO Agent Skill v2.3.1_
_https://www.citedy.com_
