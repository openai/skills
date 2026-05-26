# task +upload-attachment

> **Prerequisites:** Please read `../lark-shared/SKILL.md` to understand authentication, global parameters, and security rules.

Upload a single local file as an attachment to a task (or any resource type accepted by the Task attachment endpoint). Max file size per upload is **50 MB**. For task agents, use `--resource-type=task_delivery`.

## Recommended Commands

```bash
# Upload a local file as a task attachment (relative path required)
lark-cli task +upload-attachment \
  --resource-id "<task_guid>" \
  --file "./report.pdf"

# Pass a Feishu task applink instead of a raw guid — the guid is extracted automatically
lark-cli task +upload-attachment \
  --resource-id "https://applink.feishu.cn/client/todo/task?guid=<task_guid>" \
  --file "./note.md"

# Explicit resource type / user id type
lark-cli task +upload-attachment \
  --resource-id "<task_guid>" \
  --resource-type task \
  --user-id-type open_id \
  --file "./design.png"

# Upload a local file to a task agent
lark-cli task +upload-attachment \
  --resource-id "4b113c53-a68b-419f-8bd0-c9c532a3285a" \
  --file "./飞书.zip" \
  --resource-type task_delivery
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--resource-id <guid_or_applink>` | Yes | Target resource GUID. Accepts a raw task GUID or a Feishu task applink URL (`.../client/todo/task?guid=...`); the `guid` query parameter is extracted automatically. Do not use `suite_entity_num` / display IDs like `t104121`. |
| `--file <path>` | Yes | Local file path to upload. Must be a relative path within the current working directory; absolute paths and paths escaping the cwd are rejected. Single file only, ≤ 50 MB. |
| `--resource-type <type>` | No | Owning resource type. Defaults to `task`. Use `task_delivery` when uploading to task agents. |
| `--user-id-type <type>` | No | User ID type for the request. Defaults to `open_id`. |

## Workflow

1. Confirm the target task GUID (or applink) and the local file path with the user.
2. Ensure the file is within the current working directory and its size is ≤ 50 MB; otherwise ask the user to move/split the file.
3. Determine if this is a task agent: if yes, add `--resource-type task_delivery`.
4. Execute `lark-cli task +upload-attachment --resource-id "..." --file "..."`.
5. Report the returned attachment record. The output exposes all fields returned by the API (e.g. `guid`, `name`, `size`, `url`, `uploader`, ...); always surface the attachment `guid` and, if present, the `url` so the user can jump to the attachment directly.

## Output

The command returns the single created attachment record as a flat JSON object — every field returned by the API (`guid`, `name`, `size`, `url`, `resource_type`, `resource_id`, `uploader`, ...) is preserved verbatim. Pretty mode also prints a human-readable summary with the resource, file name, size, and attachment GUID.

> [!CAUTION]
> This is a **Write Operation** -- You must confirm the user's intent before executing.

> [!NOTE]
> The Task attachment upload endpoint accepts exactly one file per call. To upload multiple files, invoke the shortcut once per file.
