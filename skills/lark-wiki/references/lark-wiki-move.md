# wiki +move

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

在飞书知识库中移动已有 Wiki 节点，或将 Drive 文档迁入 Wiki。这个 shortcut 统一封装了两类流程：

- `node` 模式：移动已有 Wiki 节点，可同空间移动，也可跨空间移动
- `docs_to_wiki` 模式：把 Drive 文档迁入目标知识空间；必要时可提交移动申请，并在异步任务场景下自动有限轮询

当 `docs_to_wiki` 返回 `task_id` 时，shortcut 会先轮询一小段时间；如果轮询窗口内仍未完成，会返回 `next_command`，让调用方继续执行 `lark-cli drive +task_result --scenario wiki_move --task-id <TASK_ID>`。

## 与 `drive +move` 的区别

- `wiki +move` 的目标是 **知识空间或 Wiki 父节点**，使用 `--target-space-id` / `--target-parent-token`
- `drive +move` 的目标是 **Drive 文件夹**，使用 `--folder-token`
- 如果源对象已经是 Wiki 节点，必须使用 `wiki +move`，而不是 `drive +move`
- 如果源对象还是 Drive 文档，但用户要“迁入知识库”“挂到某个 Wiki 页面下”，也应使用 `wiki +move`
- 如果用户只是想整理云空间文件夹，把文件/文件夹挪到另一个 Drive 文件夹，应使用 `drive +move`

## 口语目标识别

- 当用户说“移动到某个知识库”“挂到某个页面下”“迁入 Wiki”时，按 **Wiki 目标** 处理，优先使用 `wiki +move`
- 当用户说“移动到某个文件夹”“移动到云空间根目录”时，按 **Drive 文件夹目标** 处理，优先使用 `drive +move`
- 当用户说“移动到我的文档库”“移动到我的知识库”“放到个人知识库”时，应先按 **Wiki 个人知识库目标** 理解，而不是直接退化成 `drive +move`
- 遇到“我的文档库”这类表述时，可以把它理解成：先用 `my_library` 去查询用户个人知识库，再拿到真实 `space_id`
- 推荐做法是先执行 `lark-cli wiki spaces get --params '{"space_id":"my_library"}'`，取回真实知识库 `space_id`，再把这个 `space_id` 用到 `wiki +move`
- 当前 `wiki +move` 文档的主示例仍以显式 `--target-space-id` / `--target-parent-token` 为主；如果调用方只有自然语言目标，不要因为目标暂时不明确就改走 `drive +move`

## 命令

```bash
# 将已有 wiki 节点移动到另一个父节点下
lark-cli wiki +move \
  --node-token <NODE_TOKEN> \
  --target-parent-token <TARGET_PARENT_TOKEN>

# 将已有 wiki 节点移动到另一个知识空间根目录
lark-cli wiki +move \
  --node-token <NODE_TOKEN> \
  --target-space-id <TARGET_SPACE_ID>

# 将 Drive 文档迁入某个知识空间根目录
lark-cli wiki +move \
  --obj-type docx \
  --obj-token <DOC_TOKEN> \
  --target-space-id <TARGET_SPACE_ID>

# 将 Drive 文档迁入某个父节点下；如果当前没有直接移动权限，则提交申请
lark-cli wiki +move \
  --obj-type sheet \
  --obj-token <SHEET_TOKEN> \
  --target-space-id <TARGET_SPACE_ID> \
  --target-parent-token <TARGET_PARENT_TOKEN> \
  --apply

# 预览底层调用链
lark-cli wiki +move \
  --obj-type docx \
  --obj-token <DOC_TOKEN> \
  --target-space-id <TARGET_SPACE_ID> \
  --dry-run
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--node-token` | 条件必填 | 要移动的 Wiki 节点 token。传入后命令进入 `node` 模式 |
| `--source-space-id` | 否 | 源知识空间 ID，仅 `node` 模式可用；不传时会根据 `--node-token` 自动解析 |
| `--target-space-id` | 条件必填 | 目标知识空间 ID。`docs_to_wiki` 模式必填；`node` 模式下如果不传，则必须传 `--target-parent-token` |
| `--target-parent-token` | 否 | 目标父节点 token。`docs_to_wiki` 不传时表示迁入目标知识空间根目录 |
| `--obj-type` | 条件必填 | Drive 文档类型，仅 `docs_to_wiki` 模式可用。可选值：`doc`、`sheet`、`bitable`、`mindnote`、`docx`、`file`、`slides` |
| `--obj-token` | 条件必填 | Drive 文档 token，仅 `docs_to_wiki` 模式可用 |
| `--apply` | 否 | 仅 `docs_to_wiki` 模式可用；当当前调用方不能直接移动文档时，提交一个 move request |

## 模式选择与校验规则

- **`node` 模式**：只要传了 `--node-token`，就会按“移动已有 Wiki 节点”执行
- **`docs_to_wiki` 模式**：未传 `--node-token` 时，按“把 Drive 文档迁入 Wiki”执行
- `node` 模式下，`--node-token` 不能与 `--obj-type`、`--obj-token`、`--apply` 同时使用
- `node` 模式下，`--target-parent-token` 和 `--target-space-id` 不能同时为空
- `docs_to_wiki` 模式下，必须同时提供 `--obj-type`、`--obj-token`、`--target-space-id`
- `docs_to_wiki` 模式下，`--source-space-id` 非法，只能用于 `node` 模式

## 空间解析与一致性校验

### `node` 模式

- **源空间解析**：如果未传 `--source-space-id`，shortcut 会先调用 `GET /open-apis/wiki/v2/spaces/get_node` 查询 `--node-token`，再读取其 `space_id`
- **目标父节点解析**：如果传了 `--target-parent-token`，shortcut 会先解析该父节点所属的 `space_id`
- **一致性校验**：如果同时传了 `--target-space-id` 和 `--target-parent-token`，shortcut 会校验两者是否属于同一个知识空间；不一致时直接返回验证错误
- **移动到空间根目录**：如果只传 `--target-space-id`，则表示移动到该知识空间根目录

### `docs_to_wiki` 模式

- `--target-space-id` 始终必填
- `--target-parent-token` 可选；不传时表示移动到目标知识空间根目录
- 请求体会自动映射成 `obj_type`、`obj_token`、`parent_wiki_token`、`apply`

## 行为说明

- **`node` 模式是同步操作**：请求成功后直接返回移动后的节点信息
- **`docs_to_wiki` 可能是同步，也可能是异步**：
  - 如果接口直接返回 `wiki_token`，shortcut 会立刻返回 `ready=true`
  - 如果接口返回 `applied=true`，shortcut 会返回 `ready=false`、`failed=false`、`applied=true` 和 `status_msg="move request submitted for approval"`
  - 如果接口返回 `task_id`，shortcut 会先进入有限轮询
- **有限轮询窗口**：固定最多轮询 `30` 次，每次间隔 `2` 秒
- **轮询超时不是失败**：如果轮询窗口结束任务仍在处理中，会返回 `task_id`、`status`、`status_msg`、`ready=false`、`timed_out=true` 和 `next_command`
- **继续查询**：看到 `next_command` 后，改用 `lark-cli drive +task_result --scenario wiki_move --task-id <TASK_ID>` 继续查
- **任务失败直接报错**：如果轮询期间任务进入失败态，shortcut 会直接返回错误，不会再输出 `ready=false` 结果
- **轮询请求全部失败时也直接报错**：如果任务已创建，但后续每一次状态查询都失败，shortcut 会返回带 hint 的错误，并给出继续查询命令

## 返回结果

### `node` 模式典型返回

```json
{
  "mode": "node",
  "source_space_id": "space_src",
  "target_space_id": "space_dst",
  "space_id": "space_dst",
  "node_token": "wikcnode_xxx",
  "obj_token": "doccn_xxx",
  "obj_type": "docx",
  "parent_node_token": "wikcparent_xxx",
  "node_type": "origin",
  "origin_node_token": "",
  "title": "项目计划",
  "has_child": false
}
```

### `docs_to_wiki` 异步超时返回

```json
{
  "mode": "docs_to_wiki",
  "obj_type": "docx",
  "obj_token": "doccn_xxx",
  "target_space_id": "space_xxx",
  "target_parent_token": "wikcparent_xxx",
  "task_id": "7500000000000000001",
  "ready": false,
  "failed": false,
  "status": 1,
  "status_msg": "processing",
  "timed_out": true,
  "next_command": "lark-cli drive +task_result --scenario wiki_move --task-id 7500000000000000001"
}
```

**输出字段说明：**

- `mode`：当前执行模式，值为 `node` 或 `docs_to_wiki`
- `ready`：任务是否已经完成并可直接继续使用结果
- `failed`：任务是否已失败
- `task_id`：异步任务 ID，仅异步场景返回
- `status` / `status_msg`：异步任务的主状态码和可读状态
- `wiki_token`：docs-to-wiki 成功后返回的 Wiki 节点 token；同时也会镜像到 `node_token`
- `space_id`、`node_token`、`obj_token`、`obj_type`、`parent_node_token`、`title` 等：成功拿到节点信息时返回，方便下游继续调用

## dry-run 编排

- `node` 模式下，dry-run 会根据是否需要解析源节点 / 目标父节点，展示 1 到 3 步的调用链
- `docs_to_wiki` 模式下，dry-run 会展示两步：
  1. `POST /open-apis/wiki/v2/spaces/{target_space_id}/nodes/move_docs_to_wiki`
  2. `GET /open-apis/wiki/v2/tasks/{task_id}?task_type=move`

## 权限说明

CLI 会在执行前做本地 scope 预检查；当前 shortcut 声明的权限为 `wiki:node:move`、`wiki:node:read`、`wiki:space:read`（分别覆盖 move 写操作、节点解析读操作、以及异步任务轮询读操作）。如果本地 token 已记录 scopes 且缺失任一权限，命令会直接提示重新执行 `lark-cli auth login --scope ...`。

当异步任务超时后，后续 `lark-cli drive +task_result --scenario wiki_move --task-id <TASK_ID>` 只需要 `wiki:space:read` 权限。

> [!CAUTION]
> `wiki +move` 是**写入操作**。执行前必须确认用户意图，以及目标节点 / 目标知识空间是否明确。

## 参考

- [lark-wiki](../SKILL.md) -- 知识库全部命令
- [lark-shared](../../lark-shared/SKILL.md) -- 认证和全局参数
- [drive +task_result](../../lark-drive/references/lark-drive-task-result.md) -- docs-to-wiki 异步任务的续跑查询命令
