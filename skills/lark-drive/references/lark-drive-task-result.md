
# drive +task_result

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

查询异步任务结果。该 shortcut 聚合了导入、导出、移动/删除文件夹、Wiki 节点 / 文档迁入 Wiki 等多种异步任务的结果查询，统一接口方便调用。

> [!IMPORTANT]
> 对于 `import` 场景，如果使用 `--as bot` 且这次查询**已经拿到最终在线文档目标**（`ready=true` 且返回了最终 `token` / `url`），CLI 会**再次尝试为当前 CLI 用户自动授予该资源的 `full_access`（可管理权限）**。
>
> 此时结果里会额外返回 `permission_grant` 字段，明确说明授权结果：
> - `status = granted`：当前 CLI 用户已获得该导入结果的可管理权限
> - `status = skipped`：本地没有可用的当前用户 `open_id`，或最终结果缺少可授权的在线文档目标，因此不会自动授权；可提示用户先完成 `lark-cli auth login`，再让 AI / agent 继续使用应用身份（bot）授予当前用户权限
> - `status = failed`：导入结果已就绪，但自动授权用户失败；会带上失败原因，并提示稍后重试或继续使用 bot 身份处理该文档
>
> `permission_grant.perm = full_access` 表示该资源已授予“可管理权限”。
>
> **不要擅自执行 owner 转移。** 如果用户需要把 owner 转给自己，必须单独确认。

## 命令

```bash
# 查询导入任务结果
lark-cli drive +task_result \
  --scenario import \
  --ticket <IMPORT_TICKET>

# 查询导出任务结果
lark-cli drive +task_result \
  --scenario export \
  --ticket <EXPORT_TICKET> \
  --file-token <SOURCE_DOC_TOKEN>

# 查询移动/删除文件夹任务状态
lark-cli drive +task_result \
  --scenario task_check \
  --task-id <TASK_ID>

# 查询 Wiki 移动任务结果（wiki +move 异步超时后的续跑）
lark-cli drive +task_result \
  --scenario wiki_move \
  --task-id <TASK_ID>

# 查询 Wiki 删除知识空间任务结果（wiki +delete-space 异步超时后的续跑）
lark-cli drive +task_result \
  --scenario wiki_delete_space \
  --task-id <TASK_ID>
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--scenario` | 是 | 任务场景，可选值：`import` (导入任务)、`export` (导出任务)、`task_check` (移动/删除文件夹任务)、`wiki_move` (Wiki 移动任务)、`wiki_delete_space` (Wiki 删除知识空间任务) |
| `--ticket` | 条件必填 | 异步任务 ticket，**import/export 场景必填** |
| `--task-id` | 条件必填 | 异步任务 ID，**task_check / wiki_move / wiki_delete_space 场景必填** |
| `--file-token` | 条件必填 | 导出任务对应的源文档 token，**export 场景必填** |

## 场景说明

| 场景 | 说明 | 所需参数 |
|------|------|----------|
| `import` | 文档导入任务（如将本地文件导入为云文档） | `--ticket` |
| `export` | 文档导出任务（如云文档导出为 PDF/Word） | `--ticket`、`--file-token` |
| `task_check` | 文件夹移动/删除任务 | `--task-id` |
| `wiki_move` | Wiki 移动任务（`wiki +move` 的 docs-to-wiki 异步流程，超时后续跑用） | `--task-id` |
| `wiki_delete_space` | Wiki 删除知识空间任务（`wiki +delete-space` 的异步流程，超时后续跑用） | `--task-id` |

## 返回结果

### Import 场景返回

```json
{
  "scenario": "import",
  "ticket": "<IMPORT_TICKET>",
  "type": "sheet",
  "ready": true,
  "failed": false,
  "job_status": 0,
  "job_status_label": "success",
  "job_error_msg": "success",
  "token": "<IMPORTED_DOC_TOKEN>",
  "url": "https://example.feishu.cn/sheets/<IMPORTED_DOC_TOKEN>",
  "extra": ["2000"],
  "permission_grant": {
    "status": "granted",
    "perm": "full_access",
    "member_type": "openid",
    "user_open_id": "<CURRENT_USER_OPEN_ID>",
    "message": "Granted the current CLI user full_access (可管理权限) on the new spreadsheet."
  }
}
```

**字段说明：**
- `ready`: 是否已经导入完成，可直接使用 `token` / `url`
- `failed`: 是否已经失败
- `job_status`: 服务端返回的原始状态码
- `job_status_label`: 便于阅读的状态标签，例如 `success` / `processing`
- `token`: 导入后的文档 token
- `url`: 导入后的文档链接
- `permission_grant`: 仅 `--as bot` 且这次查询已经拿到最终在线文档目标时返回，用于说明是否已自动为当前 CLI 用户授予可管理权限；如果当前仍是 `ready=false`，则不会返回这个字段

### Export 场景返回

```json
{
  "scenario": "export",
  "ticket": "<EXPORT_TICKET>",
  "ready": true,
  "failed": false,
  "file_extension": "pdf",
  "type": "doc",
  "file_name": "docName",
  "file_token": "<EXPORTED_FILE_TOKEN>",
  "file_size": 34356,
  "job_error_msg": "success",
  "job_status": 0,
  "job_status_label": "success"
}
```

**字段说明：**
- `ready`: 是否已经完成导出，可直接使用 `file_token`
- `failed`: 是否已经失败
- `job_status`: 服务端返回的原始状态码
- `job_status_label`: 便于阅读的状态标签，例如 `success` / `processing`
- `file_token`: 导出文件的 token，用于下载
- `file_extension`: 导出文件扩展名
- `file_size`: 导出文件大小（字节）

### Task_check 场景返回

```json
{
  "scenario": "task_check",
  "task_id": "<TASK_ID>",
  "status": "success",
  "ready": true,
  "failed": false
}
```

**字段说明：**
- `status`: 任务状态，`success`=成功，`failed`=失败，`pending`=处理中
- `ready`: 是否已经完成
- `failed`: 是否已经失败

### Wiki_move 场景返回

```json
{
  "scenario": "wiki_move",
  "task_id": "<TASK_ID>",
  "ready": true,
  "failed": false,
  "status": 0,
  "status_msg": "success",
  "wiki_token": "wikcnXXX",
  "node_token": "wikcnXXX",
  "space_id": "<TARGET_SPACE_ID>",
  "obj_token": "<OBJ_TOKEN>",
  "obj_type": "docx",
  "parent_node_token": "",
  "node_type": "origin",
  "origin_node_token": "",
  "title": "项目计划",
  "has_child": false,
  "node": {
    "space_id": "<TARGET_SPACE_ID>",
    "node_token": "wikcnXXX",
    "obj_token": "<OBJ_TOKEN>",
    "obj_type": "docx",
    "parent_node_token": "",
    "node_type": "origin",
    "origin_node_token": "",
    "title": "项目计划",
    "has_child": false
  },
  "move_results": [
    {
      "status": 0,
      "status_msg": "success",
      "node": { "...": "同上" }
    }
  ]
}
```

**字段说明：**
- `ready`: 所有 `move_results[].status` 都为 `0` 时为 `true`
- `failed`: 任一 `move_results[].status` 小于 `0` 时为 `true`
- `status` / `status_msg`: 第一个 move_result 的状态码 / 标签（无结果时回退为 `1` / `processing`）
- `wiki_token` / `node_token`: 移入 Wiki 后的目标节点 token（首个结果有 `node.node_token` 时镜像到顶层，便于下游脚本使用）
- `space_id`、`obj_token`、`obj_type`、`title` 等：从首个 `move_results[0].node` 平铺到顶层，方便直接引用
- `move_results`: 保留完整列表（适用于一次任务移动多个文档的场景）

### Wiki_delete_space 场景返回

```json
{
  "scenario": "wiki_delete_space",
  "task_id": "<TASK_ID>",
  "ready": true,
  "failed": false,
  "status": "success",
  "status_msg": "success"
}
```

**字段说明：**
- `ready`: `status=success` 时为 `true`
- `failed`: `status=failure` 或 `failed` 时为 `true`；未知非成功状态（如 `processing`）视为进行中
- `status`: 服务端返回的原始 `delete_space_result.status`
- `status_msg`: 优先使用 `delete_space_result.status_msg`，否则回落到 `status`，再回落到 `processing`

## 使用场景

### 配合 +import 使用

```bash
# 1. 创建导入任务
lark-cli drive +import --file ./data.xlsx --type sheet
# 若任务很快完成：直接返回 token / url
# 若内置轮询超时：返回 ready=false、ticket 和 next_command

# 2. 轮询导入结果
lark-cli drive +task_result --scenario import --ticket <IMPORT_TICKET>
# 如果这里返回 ready=true 且使用 --as bot，结果还会包含 permission_grant
```

### 配合 +move 使用

```bash
# 1. 移动文件夹（异步操作）
lark-cli drive +move --file-token <FOLDER_TOKEN> --type folder --folder-token <TARGET_FOLDER_TOKEN>
# 若轮询窗口内完成：直接返回 ready=true
# 若内置轮询结束仍未完成：返回 ready=false、task_id 和 next_command

# 2. 轮询移动结果
lark-cli drive +task_result --scenario task_check --task-id <TASK_ID>
```

### 配合 wiki +move 使用

```bash
# 1. 把 Drive 文档迁入 Wiki（异步任务可能返回 task_id）
lark-cli wiki +move --obj-type docx --obj-token <DOC_TOKEN> --target-space-id <TARGET_SPACE_ID>
# 若内置轮询窗口内完成：直接返回 ready=true 和 wiki_token
# 若轮询窗口结束仍未完成：返回 ready=false、task_id、timed_out=true 和 next_command

# 2. 续跑查询 Wiki 移动结果（next_command 即下面这条）
lark-cli drive +task_result --scenario wiki_move --task-id <TASK_ID> --as user
```

> **身份保持一致**：续跑命令的 `--as` 必须与原 `wiki +move` 调用一致；`wiki +move` 的 `next_command` 已自动带上正确的 `--as`。

### 配合 wiki +delete-space 使用

```bash
# 1. 删除知识空间（高风险写操作，必须显式带 --yes；接口可能同步返回空 task_id，也可能返回异步 task_id）
lark-cli wiki +delete-space --space-id <SPACE_ID> --yes
# 若同步返回：直接 ready=true
# 若轮询窗口结束仍未完成：返回 ready=false、task_id、timed_out=true 和 next_command

# 2. 续跑查询 Wiki 删除结果（next_command 即下面这条）
lark-cli drive +task_result --scenario wiki_delete_space --task-id <TASK_ID> --as user
```

### 配合 +export 使用

```bash
# 1. 发起导出
lark-cli drive +export --token <SOURCE_DOC_TOKEN> --doc-type docx --file-extension pdf
# 若轮询窗口内完成：直接下载本地文件
# 若内置轮询结束仍未完成：返回 ready=false、ticket 和 next_command

# 2. 继续查询导出结果
lark-cli drive +task_result --scenario export --ticket <EXPORT_TICKET> --file-token <SOURCE_DOC_TOKEN>

# 3. 拿到 file_token 后下载
lark-cli drive +export-download --file-token <EXPORTED_FILE_TOKEN>
```

## 权限要求

| 场景 | 所需 scope |
|------|-----------|
| import | `drive:drive.metadata:readonly` |
| export | `drive:drive.metadata:readonly` |
| task_check | `drive:drive.metadata:readonly` |
| wiki_move | `wiki:space:read` |
| wiki_delete_space | `wiki:space:read` |

> [!NOTE]
> `import` 场景在 `--as bot` 且任务最终就绪时，还可能额外尝试一次协作者授权；如果 `permission_grant.status = failed`，请根据失败信息检查应用是否具备相应的文档协作者授权能力。

## 参考

- [lark-drive](../SKILL.md) -- 云空间全部命令
- [lark-shared](../../lark-shared/SKILL.md) -- 认证和全局参数
