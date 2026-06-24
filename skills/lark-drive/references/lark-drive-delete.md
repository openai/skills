
# drive +delete

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

删除云空间内的文件或文件夹。删除后资源会进入回收站。

> [!CAUTION]
> 这是**高风险写操作**。CLI 层要求显式传 `--yes`；如果用户已经明确要求删除且目标明确，直接执行并带上 `--yes`。

## 命令

```bash
# 删除普通文件
lark-cli drive +delete \
  --file-token <FILE_TOKEN> \
  --type file \
  --yes

# 删除在线文档
lark-cli drive +delete \
  --file-token <DOCX_TOKEN> \
  --type docx \
  --yes

# 删除文件夹（异步操作，会自动有限轮询任务状态）
lark-cli drive +delete \
  --file-token <FOLDER_TOKEN> \
  --type folder \
  --yes
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--file-token` | 是 | 需要删除的文件或文件夹 token |
| `--type` | 是 | 文件类型，可选值：`file`、`docx`、`bitable`、`doc`、`sheet`、`mindnote`、`folder`、`shortcut`、`slides` |
| `--yes` | 是 | 确认执行高风险删除操作 |

## 行为说明

- **普通文件删除**：同步操作，成功时直接返回 `deleted=true`
- **文件夹删除**：异步操作，接口返回 `task_id`，shortcut 会先做有限轮询；如果在轮询窗口内完成，则直接返回成功结果
- **轮询超时不是失败**：文件夹删除内置最多轮询 30 次、每次间隔 2 秒；如果轮询结束任务仍未完成，会返回 `task_id`、`status`、`ready=false`、`timed_out=true` 和 `next_command`
- **继续查询**：当看到 `next_command` 时，改用 `lark-cli drive +task_result --scenario task_check --task-id <TASK_ID>` 继续查询
- **状态值**：`task_check` 的服务端状态通常是 `success`、`fail`、`process`

## 推荐续跑方式

```bash
# 第一步：先直接删除文件夹
lark-cli drive +delete \
  --file-token <FOLDER_TOKEN> \
  --type folder \
  --yes

# 如果返回 ready=false / timed_out=true，再继续查
lark-cli drive +task_result \
  --scenario task_check \
  --task-id <TASK_ID>
```

## 限制

- 该 shortcut 仅支持云空间文件或文件夹，不支持 wiki 文档
- 该接口不支持并发调用
- 调用频率上限为 5 QPS 且 10000 次/天

## 权限要求

- 删除文件时，调用身份需要满足以下其一：
- 是文件所有者，并且拥有该文件所在父文件夹的编辑权限
- 不是文件所有者，但拥有该父文件夹的 owner 或 full access 权限

## 参考

- [lark-drive](../SKILL.md) -- 云空间全部命令
- [lark-shared](../../lark-shared/SKILL.md) -- 认证和全局参数
