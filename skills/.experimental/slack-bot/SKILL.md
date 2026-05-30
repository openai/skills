---
name: "slack-bot"
description: "Use when the user needs to post Slack messages as a bot or user using environment tokens, choose a bot by name, resolve channels/mentions (users and user groups) to IDs, and send rich-text messages with entities and links via Slack Web API calls (curl/PowerShell) without a bundled script."
---

# Slack Bot Posting (API-Only)

## Workflow

Use direct Slack Web API calls (`curl` on macOS/Linux, `curl.exe` or `Invoke-RestMethod` on Windows). Do not rely on bundled scripts.

1. Select token from environment using actor + optional bot name.
2. Resolve channel name to channel ID (unless input is already `C...`/`G...`/`D...`).
3. Resolve mentions and inline entities (`@user`, `@usergroup`, `#channel`, broadcast tags, explicit Slack IDs).
4. Convert links and formatting into rich-text elements.
5. Build rich-text blocks with resolved entities.
6. Call `chat.postMessage`.

## Inputs

- `actor`: `bot` or `user`
- `bot_name`: optional; valid only for `actor=bot`
- `channel`: `#name`, `name`, or channel ID
- `message`: text content that may include mentions

## Token selection rules

- Never ask users to paste raw tokens in chat. Ask them to set env vars locally.
- For `actor=bot` with `bot_name`, normalize bot name to env suffix: uppercase + non-alnum to `_`.
  - Example: `release-bot` -> `SLACK_BOT_TOKEN_RELEASE_BOT`
- Resolution order:
  - Bot + bot*name: `SLACK_BOT_TOKEN*<NORMALIZED_NAME>`->`SLACK_BOT_TOKEN`->`SLACK_TOKEN`
  - Bot without bot_name: `SLACK_BOT_TOKEN` -> `SLACK_TOKEN`
  - User: `SLACK_USER_TOKEN` -> `SLACK_TOKEN`
- If `bot_name` is provided and named token is missing but fallback token exists, ask for confirmation before fallback.
- If fallback is not approved, stop and ask the user to set the named token.

## Required API scopes

- `chat:write`
- `users:read`
- `usergroups:read` (for `@usergroup` / subteam mentions)
- `channels:read` for public channels
- `groups:read` for private channels

## API calls

### 1) Resolve channel

If channel input is not an ID, call `conversations.list` with pagination and match by name (case-insensitive):

```bash
curl -sS -H "Authorization: Bearer $SLACK_TOKEN_IN_USE" \
  "https://slack.com/api/conversations.list?exclude_archived=true&limit=1000&types=public_channel,private_channel,mpim,im"
```

Use `response_metadata.next_cursor` until found or exhausted.

### 2) Resolve mentions and inline entities

Parse mentions/entities in this order so explicit Slack IDs win over fuzzy text matching:

- Existing `<@U...>`: keep as explicit user mention.
- Existing `<!subteam^S...|...>`: keep as explicit user group mention.
- Existing `<#C...|...>` / `<#G...|...>`: keep as explicit channel mention.
- Existing `<!here>`, `<!channel>`, `<!everyone>`: keep as broadcast mention.
- Plain `@alias`: resolve through `users.list` (with pagination), matching alias against:
  - `name`
  - `profile.display_name`
  - `profile.display_name_normalized`
  - `profile.real_name`
  - `profile.real_name_normalized`
- Plain `@group-handle` (or any unmatched `@token`): attempt `usergroups.list` match against:
  - `handle`
  - `name`
- Plain `#channel-name`: resolve by channel name through `conversations.list` (same method as channel input resolution).
- If alias maps to multiple users, treat as ambiguous and ask user to disambiguate.
- If group handle maps to multiple user groups, treat as ambiguous and ask user to disambiguate.
- If any mention/entity cannot be resolved, ask user to provide explicit Slack form (`<@U...>`, `<!subteam^S...|...>`, `<#C...|...>`).

Get users:

```bash
curl -sS -H "Authorization: Bearer $SLACK_TOKEN_IN_USE" \
  "https://slack.com/api/users.list?limit=1000"
```

Get user groups:

```bash
curl -sS -H "Authorization: Bearer $SLACK_TOKEN_IN_USE" \
  "https://slack.com/api/usergroups.list?include_disabled=false&include_count=false"
```

### 3) Resolve links and formatting into rich text

Build normalized segments before composing the final Slack block payload:

- Existing Slack links `<https://example.com|label>`: preserve as links.
- Plain URLs (`https://...`): convert to link elements.
- Existing channel/user/usergroup/broadcast references: keep as typed entities, not raw text.
- Preserve plain text around entities in separate text elements.
- Optional formatting tokens if present in user message:
  - `*bold*` -> text element with `"style":{"bold":true}`
  - `_italic_` -> text element with `"style":{"italic":true}`
  - `~strike~` -> text element with `"style":{"strike":true}`
  - `` `code` `` -> text element with `"style":{"code":true}`
- If formatting parse is uncertain or would alter meaning, keep raw text unchanged.

### 4) Post rich text

Construct `blocks` with `rich_text` and `rich_text_section` elements.

- User mention element: `{"type":"user","user_id":"U123..."}`
- User group mention element: `{"type":"usergroup","usergroup_id":"S123..."}`
- Broadcast element: `{"type":"broadcast","range":"here|channel|everyone"}`
- Channel mention element: `{"type":"channel","channel_id":"C123..."}`
- Link element: `{"type":"link","url":"https://example.com","text":"optional label"}`
- Text element: `{"type":"text","text":"..."}`

Then post:

```bash
curl -sS -X POST "https://slack.com/api/chat.postMessage" \
  -H "Authorization: Bearer $SLACK_TOKEN_IN_USE" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d @payload.json
```

`payload.json` must include:

- `channel`: resolved channel ID
- `text`: fallback plain-text string with explicit Slack refs where available (`<@U...>`, `<!subteam^S...|...>`, `<#C...|...>`, `<!here>`)
- `blocks`: rich text blocks

## Windows note

On Windows, prefer `curl.exe` (not PowerShell alias) or `Invoke-RestMethod` with equivalent headers/body.

## Output expectations

- Show final API result with `ok`, `channel`, and `ts`.
- Also report which token env key was used (for example `SLACK_BOT_TOKEN_RELEASE_BOT`).
- If any mention/entity resolution fails or is ambiguous, do not post until the user confirms/disambiguates.
