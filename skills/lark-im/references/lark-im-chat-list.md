# im +chat-list

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) first to understand authentication, global parameters, and safety rules.

List groups the current user (or bot, with `--as bot`) is a member of. Useful for enumerating "my chats" without a search keyword, or for bulk operations against the caller's chats. Supports pagination, sort order, and (user identity only) muted-chat filtering.

This skill maps to the shortcut: `lark-cli im +chat-list` (internally calls `GET /open-apis/im/v1/chats`).

## Commands

```bash
# List the user's chats (default sort: ByCreateTimeAsc)
lark-cli im +chat-list

# Sort by recent activity (most recently active first)
lark-cli im +chat-list --sort-type ByActiveTimeDesc

# Limit page size
lark-cli im +chat-list --page-size 50

# Pagination
lark-cli im +chat-list --page-token "xxx"

# Drop muted chats (user identity only)
lark-cli im +chat-list --exclude-muted

# JSON output
lark-cli im +chat-list --format json

# Preview the request without executing it
lark-cli im +chat-list --dry-run
```

## Parameters

| Parameter | Required | Limits | Description |
|------|------|------|------|
| `--user-id-type <type>` | No | `open_id` (default), `union_id`, `user_id` | ID type used for `owner_id` in the response |
| `--sort-type <type>` | No | `ByCreateTimeAsc` (default), `ByActiveTimeDesc` | Result ordering |
| `--page-size <n>` | No | 1-100, default 20 | Number of results per page |
| `--page-token <token>` | No | - | Pagination token from the previous response |
| `--exclude-muted` | No | User identity only | Drop chats the current user has muted (do-not-disturb). Under `--as bot`, the flag is silently inactive; see "Filtering muted chats" below |
| `--format json` | No | - | Output as JSON |
| `--dry-run` | No | - | Preview the request without executing it |

> **Note:** Supports both `--as user` (default) and `--as bot`. When using bot identity, the app must have bot capability enabled.

## Output Fields

| Field | Description |
|------|------|
| `chat_id` | Chat ID (`oc_xxx` format) |
| `name` | Chat name |
| `description` | Chat description |
| `owner_id` | Owner ID (type controlled by `--user-id-type`) |
| `external` | Whether the chat is external |
| `chat_status` | Chat status (`normal` / `dissolved` / `dissolved_save`) |

## Filtering muted chats

`--exclude-muted` (user identity only) drops chats the current user has set to do-not-disturb. After the list call, the CLI batches the page's chat_ids through `POST /open-apis/im/v1/chat_user_setting/batch_get_mute_status` and filters client-side. Under `--as bot`, the mute API is UAT-only and the filter is silently skipped.

When the flag is set, the JSON envelope gains a `filter` sub-object (absent otherwise, so existing consumers are unaffected); `fetched_count == returned_count + filtered_count` always holds:

```json
{
  "chats": [...],
  "filter": {
    "applied": "exclude_muted",
    "fetched_count": 20,
    "returned_count": 17,
    "filtered_count": 3,
    "hint": "Filtered out 3 muted chat(s) on this page (17 remaining); use --page-token to fetch more."
  }
}
```

## Usage Scenarios

### Scenario 1: List my recent chats

```bash
lark-cli im +chat-list --sort-type ByActiveTimeDesc --page-size 10
```

### Scenario 2: List my non-muted chats sorted by activity

```bash
lark-cli im +chat-list --sort-type ByActiveTimeDesc --exclude-muted
```

### Scenario 3: Iterate all my chats programmatically

```bash
TOKEN=""
while :; do
  RESP=$(lark-cli im +chat-list --page-size 100 --page-token "$TOKEN" --format json)
  echo "$RESP" | jq -r '.data.chats[].chat_id'
  HAS_MORE=$(echo "$RESP" | jq -r '.data.has_more')
  [ "$HAS_MORE" = "true" ] || break
  TOKEN=$(echo "$RESP" | jq -r '.data.page_token')
done
```

## Common Errors and Troubleshooting

| Symptom | Root Cause | Solution |
|---------|---------|---------|
| `--page-size must be an integer between 1 and 100` | page-size is out of range or not an integer | Use an integer between 1 and 100 |
| Permission denied (99991672) | The bot app does not have `im:chat:read` TAT permission enabled | Enable the permission for the app in the Open Platform console |
| Permission denied (99991679) with `--as user` | UAT is not authorized for `im:chat:read` | Run `lark-cli auth login --scope "im:chat:read"` |
| `Bot ability is not activated` (232025) | The app does not have bot capability enabled | Enable bot capability in the Open Platform console |
| `--exclude-muted` returns all chats unfiltered and `hint` says "no effect under bot identity" | Running under `--as bot` (mute API is UAT-only) | Switch to `--as user` for mute filtering |
