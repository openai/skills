---
name: adspirer-ads
description: Manage ad campaigns across Google Ads, Meta Ads, LinkedIn Ads, and TikTok Ads. Use when the user wants to analyze campaign performance, research keywords, create campaigns, optimize budgets, or manage ad accounts via the Adspirer MCP server.
metadata:
  short-description: Manage ad campaigns across Google, Meta, LinkedIn & TikTok
---

# Adspirer Ads

## Overview

This skill provides cross-platform advertising campaign management via the Adspirer MCP server. It enables campaign creation, keyword research, performance analysis, and budget optimization across Google Ads, Meta Ads, LinkedIn Ads, and TikTok Ads — 91 tools total.

## Prerequisites

- Adspirer MCP server must be connected and accessible via OAuth
- Confirm access to at least one connected ad platform

## Required Workflow

**Follow these steps in order. Do not skip steps.**

### Step 0: Set up Adspirer MCP (if not already configured)

If any MCP call fails because the Adspirer MCP is not connected, pause and set it up:

1. Add the Adspirer MCP:
   - `codex mcp add adspirer --url https://mcp.adspirer.com/mcp`
2. Enable remote MCP client:
   - Set `[features] rmcp_client = true` in `config.toml` **or** run `codex --enable rmcp_client`
3. Log in with OAuth:
   - `codex mcp login adspirer`

After successful login, the user will have to restart Codex. Finish your answer and tell them so — when they try again they can continue with Step 1.

If no ad platforms are connected after login, direct the user to https://www.adspirer.com to connect their Google Ads, Meta Ads, LinkedIn Ads, or TikTok Ads accounts.

### Step 1: Check Connected Platforms

Always start here before any ad operation:

- Call `get_connections_status`
- Shows connected platforms, primary/secondary accounts, account IDs
- If the target platform isn't connected, inform the user before attempting platform-specific tools

### Step 2: Identify the Task

Select the appropriate workflow based on the user's goal:

| Goal | Workflow |
|------|----------|
| View campaign metrics | Performance Analysis |
| Find keywords for Google Ads | Keyword Research |
| Create a new campaign | Campaign Creation |
| Reduce wasted ad spend | Budget Optimization |
| Switch ad accounts | Account Management |
| Compare platforms | Cross-Platform Analysis |

### Step 3: Execute Tools

Execute MCP tool calls following the workflow patterns below. Read first (performance, status), then act (create, optimize).

### Step 4: Summarize and Recommend

Present results in tables with key metrics. Highlight top/underperforming items. Propose actionable next steps.

## Practical Workflows

### Performance Analysis

Analyze campaign performance for any connected platform:

- **Google Ads:** `get_campaign_performance` — params: `lookback_days` (7/30/60/90, default 30), optional `customer_id`
- **Meta Ads:** `get_meta_campaign_performance` — params: `lookback_days`, optional `ad_account_id`
- **LinkedIn Ads:** `get_linkedin_campaign_performance` — params: `lookback_days`
- **TikTok Ads:** `get_tiktok_campaign_performance` — params: `lookback_days`

Present results with: impressions, clicks, CTR, spend, conversions, cost/conversion, ROAS. Default to 30-day lookback and primary account.

For cross-platform analysis, call each platform's performance tool and present a side-by-side comparison table.

### Keyword Research (Google Ads)

Always run before creating Search campaigns — never use generic SEO keywords.

- Tool: `research_keywords`
- Params: `business_description` or `seed_keywords`, optional `website_url`, `target_location`
- Present results grouped by intent (high/medium/low), showing search volume, CPC ranges, competition level
- Recommend keywords based on intent alignment and budget

### Campaign Creation

**Google Ads Search (follow this exact order):**
1. `research_keywords` — research keywords first (mandatory, never skip)
2. `discover_existing_assets` — check for existing ad assets before uploading new ones
3. `validate_and_prepare_assets` — validate before creation
4. `create_search_campaign` — create the campaign

**Google Ads Performance Max:**
1. `discover_existing_assets` — check existing assets first
2. `validate_and_prepare_assets` — validate all creative assets
3. `create_pmax_campaign` — create the campaign

**Meta Ads:**
1. `get_connections_status` — verify Meta account is connected
2. `search_meta_targeting` or `browse_meta_targeting` — find audiences
3. Create campaign — created in PAUSED status for user review

**LinkedIn Ads:**
1. `get_linkedin_organizations` — get linked company pages
2. `discover_linkedin_assets` — check existing creative assets
3. `validate_and_prepare_linkedin_assets` — validate assets
4. `create_linkedin_image_campaign` — create the campaign

### Budget Optimization (Google Ads)

- `optimize_budget_allocation` — suggest budget reallocations across campaigns
- `analyze_wasted_spend` — identify underperforming keywords and ad groups
- `analyze_search_terms` — review search term reports for negative keyword opportunities

### Account Management

- `switch_primary_account` — switch between connected ad accounts for a platform
- `get_connections_status` — view all connections and active account

## Safety Rules (Critical)

These tools create REAL campaigns that spend REAL money. Follow these rules strictly:

1. **Always confirm with the user** before creating any campaign or making changes that affect spend
2. **Never retry campaign creation automatically** on error — report the error to the user instead
3. **Never modify live budgets** without explicit user approval
4. All campaigns are created in **PAUSED status** when possible for user review
5. Avoid policy-violating keywords: health conditions, financial hardship, political topics, adult content
6. When in doubt about any spend-affecting action, **ask the user first**

## Platform-Specific Guidance

### Budget Minimums

| Platform | Minimum Daily | Recommended Daily |
|----------|--------------|-------------------|
| Google Ads Search | $10 | $50+ for meaningful data |
| Google Ads PMax | $10 | $50+ for meaningful data |
| Meta Ads | $5/ad set | $20+ for optimization |
| LinkedIn Ads | $10 | $50+ (higher CPCs) |
| TikTok Ads | $20/campaign | $50+ |

### When to Use Each Platform

- **Google Ads** — high-intent search traffic (people actively searching)
- **Meta Ads** — awareness and retargeting (visual, interest-based)
- **LinkedIn Ads** — B2B targeting (job titles, industries, company sizes)
- **TikTok Ads** — younger demographics and brand awareness (video-first)

## Available Tools (91 total)

| Platform | Count | Key Tools |
|----------|-------|-----------|
| Google Ads | 39 | `get_campaign_performance`, `research_keywords`, `create_search_campaign`, `create_pmax_campaign`, `optimize_budget_allocation`, `analyze_wasted_spend`, `analyze_search_terms`, `list_campaigns`, `get_campaign_structure` |
| LinkedIn Ads | 28 | `get_linkedin_campaign_performance`, `create_linkedin_image_campaign`, `get_linkedin_organizations`, `analyze_linkedin_creative_performance` |
| Meta Ads | 20 | `get_meta_campaign_performance`, `search_meta_targeting`, `browse_meta_targeting`, `discover_meta_assets` |
| TikTok Ads | 4 | `get_tiktok_campaign_performance` |
| Account | 2 | `get_connections_status`, `switch_primary_account` |

## Output Formatting Rules

- **Performance reports:** Table with impressions, clicks, CTR, spend, conversions, CPC, ROAS. Order by spend descending.
- **Keyword research:** Group by intent (high/medium/low), show search volume and CPC ranges in a table.
- **Campaign creation:** Confirm all settings with user before execution, show campaign ID after creation.
- **Cross-platform:** Side-by-side comparison table with normalized metrics.
- **Errors:** Report the full error message to the user. Never retry creation tools automatically.

## Troubleshooting

- **Authentication:** If MCP calls fail with 401, re-run `codex mcp login adspirer`. Clear any cached tokens and retry.
- **No platform data:** Verify the ad platform is connected at https://www.adspirer.com. Try a longer lookback period (60 or 90 days).
- **Account mismatch:** Use `switch_primary_account` to change which ad account is active.
- **Rate limits:** Adspirer enforces tool call quotas by subscription tier (Free: 10/month, Plus: 50, Pro: 100, Enterprise: unlimited). If quota exceeded, inform the user about upgrading.
