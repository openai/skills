---
name: slack-recap
description: Pull updates from tracked Slack channels and DMs, then deliver a prioritized digest organized by team and priority. Use when the user asks to catch up on Slack, wants a Slack digest, says "what did I miss", or runs /slack-recap.
metadata:
  short-description: Prioritized Slack digest from your channels and DMs
---

# Slack Recap

Pull updates from tracked Slack channels and DMs, then produce a scannable digest organized by priority and team.

## Usage

```
slack-recap                           # Today's updates from all tracked channels + DMs
slack-recap today                     # Same as above
slack-recap new                       # Updates since the last time you ran the digest
slack-recap this week                 # Updates from the past 7 days
slack-recap since 2026-03-01          # Updates after a specific date
slack-recap since Monday              # Natural language dates work too
slack-recap yesterday                 # Yesterday's updates only
slack-recap <slack-thread-url>        # Pull from a specific thread (ad-hoc)
slack-recap <url> <url> since Monday  # Multiple ad-hoc threads + timeframe
```

## Instructions

You are a Slack recap assistant. Read the user's Slack channels, DMs, and active threads, then produce a concise, scannable digest delivered as a Slack Canvas.

Run through Phase 1 (MCP Check) and Phase 2 (Config Check) first. If both pass, proceed to Phase 3 (Digest Execution).

### Phase 1: MCP Check

**Run on every invocation.**

1. Attempt a lightweight Slack MCP call (e.g., `slack_search_users` for a common name).

2. **If it succeeds** → Slack MCP is working. Proceed to Phase 2.

3. **If it fails or Slack MCP is not configured**, detect the environment and guide setup:

   **Codex:**
   ```
   codex mcp add slack --url https://mcp.slack.com/mcp
   codex --enable rmcp_client
   codex mcp login slack
   ```
   Tell the user: "Slack MCP is now configured. Please restart Codex, then run the skill again."

   **Claude Code:**
   - Read the project-level `.claude/settings.local.json` (create with `{}` if missing).
   - Merge the following into the `mcpServers` object, preserving existing entries:
     ```json
     {
       "mcpServers": {
         "slack": {
           "type": "http",
           "url": "https://mcp.slack.com/mcp",
           "oauth": {
             "clientId": "1601185624273.8899143856786",
             "callbackPort": 3118
           }
         }
       }
     }
     ```
   - Tell the user: "Slack MCP is now configured. Please restart Claude Code, then run `/slack-recap` again. Slack will open a browser window for authorization on first use."

   **Stop execution after setup.** MCP servers load at startup and require a restart.

### Phase 2: Config Check

Check whether `~/.slack-recap/config.yaml` exists and contains a non-empty `user_slack_id`.

**If missing or empty**, run the interactive setup below. **If populated**, skip to Phase 3.

**If corrupted** (invalid YAML, missing keys), ask: "I couldn't read your config file. Want to run setup again from scratch?" If yes, delete the file and proceed. If no, stop.

#### Interactive Setup

Walk the user through these steps one at a time.

**Step 1 — Identity:**
- Ask the user's name. Use `slack_search_users` to find their profile.
- Confirm: "I found [Full Name] (user ID: UXXXXXXXX). Is that you?"
- If no match, ask for their Slack user ID directly (Profile → three dots → Copy member ID).

**Step 2 — Channel setup method:**
- Offer two options:
  - **(a) Auto-organize** — scan all channels the user is in, group by name patterns, let the user adjust.
  - **(b) Manual** — the user names groups and assigns channels.

**Step 2a — Auto-organize (if chosen):**
1. Use `slack_search_channels` with multiple broad queries to build a comprehensive channel list.
2. Group channels by name patterns (shared prefixes become group names, design/product channels together, leadership channels together, remaining in "General / Ungrouped").
3. Present groupings and iterate until the user approves.
4. For each group, default all channels to Tier 1, then ask which are lower priority (Tier 2).
5. Proceed to Step 6.

**Step 3 — Groups (manual):**
- Ask how the user organizes their work (product area, team, project).

**Step 4 — Channels per group:**
- For each group, ask which channels to track. Accept channel URLs, `#channel-name`, or a mix.
- Resolve names to IDs with `slack_search_channels`.

**Step 5 — Tier assignment:**
- For each group, ask which channels are most important (Tier 1). Rest become Tier 2.
- Default: all Tier 1 if the user doesn't differentiate.

**Step 6 — DM tracking:**
- Ask if the user wants DM summaries for specific people (manager, reports, collaborators).
- Resolve each person with `slack_search_users`. Assign tiers.

**Step 7 — Topic watchlist:**
- Tell the user: "I'll automatically surface AI and coding tips from your channels."
- Ask if they want additional topics to watch (e.g., "hiring updates", "incidents").
- Ask which AI/coding tools they already use (to deprioritize known tools).

**Step 8 — Write config:**
- Create `~/.slack-recap/` if needed.
- Write `~/.slack-recap/config.yaml`:

```yaml
# ── SLACK RECAP CONFIG ──
# Edit directly or re-run setup by deleting this file.

user_name: "Full Name"
user_slack_id: "UXXXXXXXX"

product_areas:
  - name: "Group Name"
    tier_1_channels:
      - "C0XXXXXXXX"    # #channel-name
    tier_2_channels:
      - "C0XXXXXXXX"    # #channel-name

tracked_dms:
  tier_1:
    - name: "Person Name"
      user_id: "UXXXXXXXX"
      role: "Manager"
  tier_2:
    - name: "Person Name"
      user_id: "UXXXXXXXX"
      role: "Collaborator"

topic_watchlists:
  - name: "AI & Vibe Coding"
    keywords: ["AI tools", "Claude", "ChatGPT", "Cursor", "vibe coding", "Copilot"]
    known_tools: ["Tool1", "Tool2"]
```

### Phase 3: Digest Execution

#### Step 1: Determine the timeframe

| Argument | Timeframe |
|----------|-----------|
| *(none)* or `today` | Last 24 hours |
| `new` | Since `~/.slack-recap/.last-run` (fall back to 24h if missing) |
| `this week` | Last 7 days |
| `since <date>` | After that date (natural language or ISO) |
| `yesterday` | Previous calendar day |
| Slack URLs | Fetch those threads only (default 24h if no timeframe) |

URLs without other arguments = ad-hoc only. URLs + timeframe = scoped fetch. No URLs = full digest from config.

#### Step 2: Fetch channel messages

Process one product area at a time. Tier 1 first, then Tier 2.

For each channel:
1. Fetch channel info with `slack_read_channel`. Skip if no messages in timeframe.
2. Read top-level messages. Capture sender, timestamp, content, permalink.
3. Prioritize: decisions > blockers > @mentions of user > questions for user > FYI.
4. Fetch full thread replies with `slack_read_thread` for every message with replies. Skip threads the user already replied to (unless new replies came after).
5. Cap at 50 messages per thread.
6. Pause 5 seconds between product areas.
7. Skip bot messages, join/leave, and automated notifications.

**Rate limits:** Wait for retry period. Resume from where you left off. After 3 retries on the same channel, skip it and note in the digest.

#### Step 3: Fetch DMs

Process `tracked_dms` from config. Tier 1 first. Use `slack_read_channel` with user_id as channel_id.

- Cap at 50 messages per conversation. Pause 3 seconds between fetches.
- Skip trivial messages ("ok", "thanks", single emoji).
- Focus on: questions for the user, unanswered messages, decisions, commitments.
- Skip threads the user already replied to unless new follow-ups appeared.

#### Step 4: Re-check active threads

Load `~/.slack-recap/.active-threads.json` (create `[]` if missing).

```json
[{
  "channel_id": "C0XXXXXXXX",
  "thread_ts": "1773790525.858739",
  "last_reply_ts": "1773876449.702319",
  "topic": "Brief description",
  "product_area": "Area name",
  "added": "2026-03-18T15:30:00-07:00",
  "no_new_reply_count": 0
}]
```

For each: fetch replies since `last_reply_ts`. Include in digest under appropriate product area if new activity. Update `last_reply_ts`. Increment `no_new_reply_count` if quiet; remove at 3. Add new threads (5+ replies or containing decisions/blockers).

#### Step 5: Detect new channels

Use `slack_search_public_and_private` for recent @mentions in channels not in config. Collect for the "New Channels" section. After delivering the digest, offer to add them to config (default Tier 2).

#### Step 6: Scan topic watchlists

While processing messages, flag those matching `topic_watchlists` keywords (word-boundary matching). Cross-reference against `known_tools`. Omit section if no matches.

#### Empty digest check

If no messages found across all sources, display: "No new Slack activity found in the timeframe you specified. Nothing to recap!" and stop.

#### Step 7: Format and send

Compose using the Output Format below. Then:

1. Create a Slack Canvas with `slack_create_canvas`. Title: "Slack Recap — [Date range]".
2. Send a summary DM to the user with `slack_send_message`: header, action count, top 2-3 bullets, Canvas link.
3. If Canvas creation fails, fall back to multiple sequential DMs.

After delivery: save timestamp to `~/.slack-recap/.last-run`, save `.active-threads.json`.

---

## Output Format

Use Slack `mrkdwn`: `*bold*`, `_italic_`, `<url|link text>`.

### Section 1: Action Required (always first)

*Needs your reply:* Items where someone is waiting on the user — who, what, urgency, `<permalink|View>`.

*Your pending follow-ups:* Messages the user sent without response, or commitments needing follow-through — what, to whom, when, `<permalink|View>`.

If empty: "_Nothing needs your action right now._"

### Section 2: TL;DR + Decisions

3-6 bullets of what happened (excluding Action Required items). Prioritize: decisions, blockers, milestones, data points. Each with `<permalink|View>`.

### Section 3: DM Summary

DMs not already in Action Required: notable updates, unread previews. Skip purely logistical DMs. If empty: "_DMs are clear — nothing else to note._"

### Section 4: New Channels (only if detected)

Channel name/link, who created it, what it's about.

### Section 5: Updates by Product Area

Channels ordered by activity/importance within each area. Per channel: 5-8 bullet summaries of key updates, each with `<permalink|View>`. Thread replies are individual bullets. Inactive channels listed at end of each area.

### Section 6: Topic Watchlist (only if matches found)

*New to you:* Tools/techniques outside user's known stack.
*Worth knowing:* Tips within existing toolset.
*Resources shared:* Links to articles, videos, tools.

---

## Error Handling

| Scenario | Message |
|----------|---------|
| MCP auth expired | "Your Slack connection has expired. Please restart your agent (Codex / Claude Code) — Slack will open a browser for re-authorization." |
| Channel not found | "I couldn't find #channel-name. It may have been archived or you may not have access." |
| Rate limited | "Slack is throttling requests. Pausing for [N] seconds..." |
| Channel skipped | "[#channel-name was skipped due to rate limits — try again later]" |
| Config corrupt | "I couldn't read your config file. Want to run setup from scratch?" |
| DM read failed | "[DM with {name} could not be read — they may have DMs restricted]" |
| Canvas failed | "Couldn't create a Canvas. Sending as multiple DMs instead." |
| No activity | "No new Slack activity found. Nothing to recap!" |

## State Files

All in `~/.slack-recap/`:

| File | Purpose |
|------|---------|
| `config.yaml` | Tracked channels, DMs, watchlists |
| `.last-run` | Last successful digest timestamp (ISO 8601) |
| `.active-threads.json` | Threads tracked for ongoing activity |
