# im +flag-cancel

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for authentication, global parameters, and security rules.

This skill maps to shortcut: `lark-cli im +flag-cancel`. Underlying API: `POST /open-apis/im/v1/flags/cancel`.

## Double-Cancel Behavior (Important)

A message can have flags on both layers simultaneously:
- Message layer: `(default, message)`
- Feed layer: `(thread, feed)` or `(msg_thread, feed)` depending on chat type

**When no `--flag-type` is specified, the shortcut performs double-cancel**: removes both message layer and feed layer flags. The server handles cancel requests for non-existent flags idempotently, so this is safe.

**Feed layer item_type is determined by chat_mode**:
- Topic-style chat (`chat_mode=topic`) → `item_type=thread`
- Regular chat (`chat_mode=group`) → `item_type=msg_thread`

## Commands

```bash
# Double-cancel both layers (recommended default)
lark-cli im +flag-cancel --as user --message-id om_xxx

# Only cancel message layer
lark-cli im +flag-cancel --as user --message-id om_xxx --flag-type message

# Only cancel feed layer (need to specify item-type)
lark-cli im +flag-cancel --as user --message-id om_xxx --item-type thread --flag-type feed

# Preview request
lark-cli im +flag-cancel --as user --message-id om_xxx --dry-run
```

## Parameters

| Parameter | Required | Description |
|------|------|------|
| `--message-id <om_xxx>` | Required | Message ID |
| `--flag-type <name>` | No | `message` or `feed`; **when omitted, double-cancels both layers** |
| `--item-type <name>` | No | `default\|thread\|msg_thread`; required when `--flag-type feed` |
| `--as user` | Required | Currently only supports user identity |

## Idempotency

The server doesn't return an error for cancel requests when the flag doesn't exist, so repeated `+cancel` calls are idempotent.

## Permissions

- Required scopes: `im:feed.flag:write`, `im:message.group_msg:get_as_user`, `im:message.p2p_msg:get_as_user`, `im:chat:read`
- The message/chat read scopes are used by the default double-cancel path to auto-detect the feed-layer item type.

## Note

- **Do not call +flag-list for verification**: If the cancel API returns success, the flag is removed. Calling +flag-list to verify is expensive (requires full pagination) and unnecessary.

## Finding Message ID Efficiently

If you have message content but not the message ID:

1. **Use `+messages-search`** to find the message by content, then extract `message_id` from the result
2. **Do NOT use `+flag-list`** to find the message — it requires full pagination and is very inefficient

```bash
# Search by message content to find message_id
lark-cli im +messages-search --as user --query "message content here" -q '.data.items[0].message_id'
```
