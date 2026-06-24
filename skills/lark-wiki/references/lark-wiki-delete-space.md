# wiki +delete-space

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

删除一个飞书知识空间（知识库）。OpenAPI 对应 `DELETE /open-apis/wiki/v2/spaces/:space_id`。

- **不可逆**：该操作会将知识空间连同其下所有节点彻底删除，执行前必须反复确认
- **同步 / 异步两种返回**：
  - 如果接口直接返回空 `task_id`，说明删除同步完成，shortcut 立即返回 `ready=true`
  - 如果接口返回非空 `task_id`，shortcut 会先对任务做有限轮询；轮询窗口内仍未完成会输出 `next_command`，引导调用方使用 `lark-cli drive +task_result --scenario wiki_delete_space --task-id <TASK_ID>` 继续查

## 命令

```bash
# 同步或异步删除一个知识空间（必须显式加 --yes 确认）
lark-cli wiki +delete-space \
  --space-id <SPACE_ID> \
  --yes

# 预览底层调用链（不会真的删除）
lark-cli wiki +delete-space \
  --space-id <SPACE_ID> \
  --dry-run
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--space-id` | 是 | 要删除的知识空间 ID |
| `--yes` | 是（真删时） | 高风险写操作确认。不传则 CLI 直接返回 `unsafe_operation_blocked` 错误 |

## 行为说明

- **请求**：对 `/open-apis/wiki/v2/spaces/{space_id}` 发送 `DELETE`
- **同步返回**：响应 `data.task_id` 为空字符串时直接返回 `ready=true`、`failed=false`、`status_msg="success"`
- **异步返回**：响应 `data.task_id` 非空时进入有限轮询
- **任务轮询**：调用 `GET /open-apis/wiki/v2/tasks/{task_id}?task_type=delete_space`，读取 `data.task.delete_space_result.status`
  - `status=success` → `ready=true`
  - `status=failure` / `status=failed` → 返回错误（`wiki delete-space task failed: <status_msg 或 status>`）
  - 其他值（如 `processing`、`running`）→ 视为进行中，继续轮询
- **有限轮询窗口**：固定最多轮询 `30` 次，每次间隔 `2` 秒
- **轮询超时不是失败**：如果窗口结束任务仍在处理中，会返回 `task_id`、`status`、`status_msg`、`ready=false`、`timed_out=true`、`next_command`
- **继续查询**：看到 `next_command` 后，改用 `lark-cli drive +task_result --scenario wiki_delete_space --task-id <TASK_ID>` 继续查
- **轮询请求全部失败时直接报错**：如果任务已创建，但后续每一次状态查询都失败，shortcut 会返回带 hint 的错误，并给出继续查询命令

## 返回结果

### 同步删除

```json
{
  "space_id": "7629741305993170448",
  "ready": true,
  "failed": false,
  "status": "success",
  "status_msg": "success"
}
```

### 异步删除完成

```json
{
  "space_id": "7629741305993170448",
  "task_id": "7631425120875056669-965458aec67417f5982250806c97950697ccb82f",
  "ready": true,
  "failed": false,
  "status": "success",
  "status_msg": "success"
}
```

### 异步轮询超时

```json
{
  "space_id": "7629741305993170448",
  "task_id": "7631425120875056669-965458aec67417f5982250806c97950697ccb82f",
  "ready": false,
  "failed": false,
  "status": "processing",
  "status_msg": "processing",
  "timed_out": true,
  "next_command": "lark-cli drive +task_result --scenario wiki_delete_space --task-id 7631425120875056669-965458aec67417f5982250806c97950697ccb82f --as user"
}
```

**输出字段说明：**

- `space_id`：入参的知识空间 ID
- `ready`：任务是否已经完成
- `failed`：任务是否已失败（显式返回 `failure` / `failed` 时为 `true`）
- `task_id`：异步任务 ID，仅异步场景返回
- `status` / `status_msg`：异步任务的原始状态和可读标签
- `timed_out`、`next_command`：轮询窗口内未完成时返回

## dry-run 编排

dry-run 会展示两步调用链：

1. `DELETE /open-apis/wiki/v2/spaces/{space_id}`
2. `GET /open-apis/wiki/v2/tasks/{task_id}?task_type=delete_space`（仅异步时真实发生）

## 权限说明

当前 shortcut 声明的权限为 `wiki:space:write_only` 和 `wiki:space:read`。前者用于发起删除请求，后者用于轮询同一命令内的异步任务状态；如果本地 token 缺失任一权限，CLI 会直接提示重新执行 `lark-cli auth login --scope "wiki:space:write_only wiki:space:read"`。

异步超时后的 `lark-cli drive +task_result --scenario wiki_delete_space --task-id <TASK_ID>` 只需 `wiki:space:read`（纯读任务状态）。

## 空间解析：如何拿到 `space_id`

`wiki +delete-space` 只接受 `--space-id` 作为目标。用户在对话里常常只说知识库的**名称**或贴一条**知识库 URL**，这时**不能**把名称 / URL 原样当成 `space_id` 传进去，必须先解析。三种输入路径：

### 1. 已经有 `space_id`
直接用，无需解析。

### 2. 只有知识库 URL（`.../wiki/<token>`）

```bash
lark-cli wiki spaces get_node \
  --params '{"token":"<wiki_token>"}' \
  --format json
```

读取 `data.node.space_id`。

### 3. 只有知识库名称

调用 `wiki spaces list`：

```bash
# 第一页
lark-cli wiki spaces list --format json

# 如果需要继续翻页（看下方停止条件），带上 page_token
lark-cli wiki spaces list --params '{"page_token":"<上一页返回的 page_token>"}' --format json
```

#### 翻页与匹配策略

**边翻边匹配**：每拿一页就在已累计的 items 上对 `name` 做精确匹配（区分大小写、保留空格），满足任一条件即停止翻页：

- (A) **累计精确匹配 ≥ 1 条** → 停止翻页，已找到目标
- (B) **`has_more=false`**（已翻完所有页）→ 停止翻页

结束后：

1. 如果累计精确匹配 ≥ 1：把**所有**精确匹配作为候选列给用户
2. 如果精确匹配 = 0（此时必然已走到 `has_more=false`，已收集全量 items）：在全量 items 上做**宽松匹配**（`name` trim 空格 + 大小写不敏感 + 子串包含），作为候选
3. 宽松匹配也 0 条：停下来问用户是不是名字拼错、或者调用方没权限看到这个空间；**不要**自己改名字重试

> 不做更激进的归一化（比如去括号、去版本号尾缀），那些容易把 "客户台账（归档）" 误命中到 "客户台账"。

#### 早停的小边界

早停（条件 A）意味着**可能漏掉**位于更后面页的同名空间。这种重名 corner case 由下面的"用户确认"兜底：LLM 展示候选时应照抄 `name + space_id`，用户如果觉得不是自己想删的那一个，可以要求继续翻页。

#### 确认流程（硬约束）

**无论精确还是模糊，无论命中 1 条还是多条，发起删除前都必须先把候选列给用户**，由用户明确回选一个 `space_id`。不要因为"只命中一条"就跳过确认直接删。

列候选时至少包含以下字段，方便用户分辨：

- `name`（原始值，不做归一化）
- `space_id`
- `space_type`（`team` / `person` 等）
- `description`（若有）
- `visibility`（若有）

示例话术：

```text
根据 "客户台账" 找到以下候选：
  1) name="客户台账", space_id=7629...0448, space_type=team, description="销售部"
  2) name="客户台账（归档）", space_id=7629...0449, space_type=team, description="2023 以前"
请回复序号或 space_id 确认要删除的那一个；如果都不是请说明。
```

命中 0 条：停下来问用户是名称拼错了、还是调用方无权限看到这个空间；**不要**自动尝试改名字再查一次。

#### 执行删除

用户明确选定 `space_id` 后：

```bash
lark-cli wiki +delete-space --space-id <RESOLVED_SPACE_ID> --yes
```

> [!IMPORTANT]
> 删库不可逆。关键不变量：**发给服务端的 `--space-id` 必须是用户在上一轮对话里明确指认过的那一个**，不是 LLM 单方面"从匹配结果自动选"。

## 风险等级

- Risk：**`high-risk-write`**
- 框架会强制要求 `--yes` 确认；不传 `--yes` 时命令会直接返回 `unsafe_operation_blocked` 错误，不会真的发请求

> [!CAUTION]
> `wiki +delete-space` 是**不可逆的写入操作**。执行前务必与用户再次确认 `--space-id`，并清楚该空间下的所有节点都会一并被删除。

## 参考

- [lark-wiki](../SKILL.md) -- 知识库全部命令
- [lark-shared](../../lark-shared/SKILL.md) -- 认证和全局参数
- [drive +task_result](../../lark-drive/references/lark-drive-task-result.md) -- 异步任务的续跑查询命令
