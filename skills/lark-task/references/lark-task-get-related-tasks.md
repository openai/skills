# task +get-related-tasks

> **Prerequisites:** Please read `../lark-shared/SKILL.md` to understand authentication, global parameters, and security rules.
>
> **⚠️ Note:** This API must be called with a user identity. **Do NOT use an app identity, otherwise the call will fail.**
>
> **Pagination / Time Cursor Rule:**
> In `+get-related-tasks`, `page_token` is the task `updated_at` cursor in microseconds.
>
> **Execution Priority:**
> 1. If the request contains a start/end time boundary (for example, "今年以来", "最近一个月", "从 3 月 1 日开始"), first convert the **start time** boundary to a microsecond `page_token` and query from that token.
> 2. Continue pagination using returned `page_token` until `has_more=false`, but never exceed 40 total page fetches.
> 3. Do NOT default to `--page-all` for time-bounded queries.
>
> Only use `--page-all` from the beginning when:
> 1. the user explicitly asks for a full scan of all related tasks, or
> 2. no time boundary can be inferred from the request.

List tasks related to the current user.

## Recommended Commands

```bash
# List all related tasks
lark-cli task +get-related-tasks

# List incomplete related tasks starting from a page token
lark-cli task +get-related-tasks --include-complete=false --page-token "1752730590582902"

# Show only tasks created by me
lark-cli task +get-related-tasks --created-by-me
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--include-complete=<bool>` | No | Default behavior includes completed tasks. Set to `false` to keep only incomplete tasks. |
| `--page-all` | No | Automatically paginate through all pages (max 40). |
| `--page-limit <int>` | No | Max page limit (default 20). |
| `--page-token <string>` | No | Start from the specified page token. This token is the task's last update time cursor in microseconds. |
| `--created-by-me` | No | Keep only tasks whose creator is the current user. This is a client-side filter applied after fetching related-task pages. |
| `--followed-by-me` | No | Keep only tasks followed by the current user. This is a client-side filter applied after fetching related-task pages. |

> **Page Token Note:** In `+get-related-tasks`, the `page_token` is a microsecond-level cursor representing the task's last update time. For example, `1752730590582902` should be treated as an updated-at cursor, not a task ID.
>
> **Pagination Note for Client-side Filters:** When `--created-by-me` or `--followed-by-me` is used, filtering happens locally after each upstream related-task page is fetched. The returned `has_more` and `page_token` still describe the upstream cursor, so later pages may contain more matching tasks, or may contain none.

## Workflow

1. Determine whether the user needs all related tasks or a filtered subset.
2. Execute `lark-cli task +get-related-tasks ...`
3. Report the matching tasks and, if present, the next `page_token`.
