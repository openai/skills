---
name: twist-cli
description: Manage Twist workspaces, threads, messages, DMs, reactions, and search using the `tw` CLI; use for reading and responding to Twist conversations from the command line.
---

# Twist CLI (tw)

Access Twist messaging via the `tw` CLI. Use when the user asks about their Twist workspaces, threads, messages, or wants to interact with Twist in any way.

## Setup

```bash
tw auth token <your-api-token>   # Save API token
tw auth status                   # Verify authentication
tw auth logout                   # Remove saved token
tw workspaces                    # List available workspaces
tw workspace use <ref>           # Set current workspace
```

## Inbox

```bash
tw inbox                         # Show inbox threads
tw inbox --unread                # Only unread threads
tw inbox --channel <filter>      # Filter by channel name (fuzzy)
tw inbox --since <date>          # Filter by date (ISO format)
tw inbox --limit <n>             # Max items (default: 50)
```

## Threads

```bash
tw thread view <thread-ref>      # View thread with comments
tw thread view <ref> --unread    # Show only unread comments
tw thread view <ref> --context 3 # Include 3 read comments before unread
tw thread reply <ref> "content"  # Post a comment
tw thread done <ref>             # Archive thread (mark done)
```

## Conversations (DMs/Groups)

```bash
tw msg unread                    # List unread conversations
tw msg view <conversation-ref>   # View conversation messages
tw msg reply <ref> "content"     # Send a message
tw msg done <ref>                # Archive conversation
```

## Search

```bash
tw search "query"                # Search content
tw search "query" --type threads # Filter: threads, messages, or all
tw search "query" --author <ref> # Filter by author
tw search "query" --title-only   # Search thread titles only
tw search "query" --mention-me   # Results mentioning current user
tw search "query" --since <date> # Content from date
tw search "query" --channel <id> # Filter by channel IDs (comma-separated)
```

## Users & Channels

```bash
tw user                          # Show current user info
tw users                         # List workspace users
tw users --search <text>         # Filter by name/email
tw channels                      # List workspace channels
```

## Reactions

```bash
tw react thread <id> 👍          # Add reaction to thread
tw react comment <id> +1         # Add reaction (shortcode)
tw react message <id> heart      # Add reaction to DM message
tw unreact thread <id> 👍        # Remove reaction
```

Supported shortcodes: +1, -1, heart, tada, smile, laughing, thinking, fire, check, x, eyes, pray, clap, rocket, wave

## Output Formats

All list/view commands support:

```bash
--json    # Output as JSON
--ndjson  # Output as newline-delimited JSON (for streaming)
--full    # Include all fields (default shows essential fields only)
```

## Reference System

Commands accept flexible references:
- **Numeric IDs**: `123` or `id:123`
- **Twist URLs**: Full `https://twist.com/...` URLs (parsed automatically)
- **Fuzzy names**: For workspaces/users - `"My Workspace"` or partial matches

## Common Workflows

**Check inbox and respond:**
```bash
tw inbox --unread --json
tw thread view <id> --unread
tw thread reply <id> "Thanks, I'll look into this."
tw thread done <id>
```

**Search and review:**
```bash
tw search "deployment" --type threads --json
tw thread view <thread-id>
```

**Check DMs:**
```bash
tw msg unread --json
tw msg view <conversation-id>
tw msg reply <id> "Got it, thanks!"
```
