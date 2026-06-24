# task +tasklist-search

> **Prerequisites:** Please read `../lark-shared/SKILL.md` to understand authentication, global parameters, and security rules.
>
> **⚠️ Note:** This shortcut uses tasklist search followed by tasklist detail queries to render the final output.

Search tasklists by keyword and optional filters.

## Recommended Commands

```bash
# Search by keyword
lark-cli task +tasklist-search --query "测试"

# Search tasklists created by specific users
lark-cli task +tasklist-search --creator "ou_xxx,ou_yyy"

# Search by creation time range
lark-cli task +tasklist-search --query "Q2" --create-time "-30d,+0d"
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--query <string>` | No | Search keyword. If omitted, at least one filter must be provided. |
| `--creator <ids>` | No | Creator open_ids, comma-separated. |
| `--create-time <range>` | No | Creation time range in `start,end` form. Each side supports ISO/date/relative/ms input. |
| `--page-token <string>` | No | Page token for pagination. |
| `--page-all` | No | Automatically paginate through all pages (max 40). |
| `--page-limit <int>` | No | Max page limit (default 20). |

## Workflow

1. Build the search keyword and filters from the user's request.
2. Execute `lark-cli task +tasklist-search ...`
3. Report the matched tasklists and the next `page_token` if more results exist.

