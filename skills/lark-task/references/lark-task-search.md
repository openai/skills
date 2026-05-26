# task +search

> **Prerequisites:** Please read `../lark-shared/SKILL.md` to understand authentication, global parameters, and security rules.
>
> **⚠️ Note:** This API must be called with a user identity. **Do NOT use an app identity, otherwise the call will fail.**

Search tasks by keyword and optional filters.

## Recommended Commands

```bash
# Search by keyword
lark-cli task +search --query "test"

# Search incomplete tasks assigned to specific users
lark-cli task +search --assignee "ou_xxx,ou_yyy" --completed=false

# Search by due time range
lark-cli task +search --query "release" --due "-1d,+7d"
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--query <string>` | No | Search keyword. If omitted, at least one filter must be provided. |
| `--creator <ids>` | No | Creator open_ids, comma-separated. |
| `--assignee <ids>` | No | Assignee open_ids, comma-separated. |
| `--follower <ids>` | No | Follower open_ids, comma-separated. |
| `--completed=<bool>` | No | Filter by completion state. |
| `--due <range>` | No | Due time range in `start,end` form. Each side supports ISO/date/relative/ms input. |
| `--page-token <string>` | No | Page token for pagination. |
| `--page-all` | No | Automatically paginate through all pages (max 40). |
| `--page-limit <int>` | No | Max page limit (default 20). |

## Workflow

1. Build the keyword and filters from the user's request.
2. Execute `lark-cli task +search ...`
3. Report the matched tasks and include the next `page_token` if more results exist.

