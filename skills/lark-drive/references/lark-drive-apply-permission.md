
# drive +apply-permission（申请文档权限）

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

本 skill 对应 shortcut：`lark-cli drive +apply-permission`。

向云文档 **Owner** 发起 `view` 或 `edit` 权限申请。申请会以卡片形式推送给 Owner，由 Owner 决定是否通过。

> [!CAUTION]
> 这是**写入操作** —— 会给 Owner 发推送通知，不要批量或自动化调用。可以先用 `--dry-run` 预览。

## 身份要求

- **仅支持 `user` 身份**（使用 `user_access_token`），不支持 `bot` / `tenant_access_token`；shortcut 已在 `AuthTypes` 中强制限定为 `user`，使用 bot 会被拒。
- 所需 scope：`docs:permission.member:apply`（若用户缺权限会走统一的 permission 错误路径）。

## 命令

```bash
# 通过 URL 申请（type 自动从 URL 推断）
lark-cli drive +apply-permission \
  --token "https://example.larksuite.com/docx/doxcnxxxxxxxxx" \
  --perm view \
  --remark "安全评估：需查看需求文档内容" --as user

# 通过 bare token + 显式 --type
lark-cli drive +apply-permission \
  --token "doxcnxxxxxxxxx" --type docx \
  --perm edit --as user
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--token` | 是 | 目标文档 token 或完整 URL（`/docx/`、`/sheets/`、`/base/`、`/bitable/`、`/file/`、`/wiki/`、`/doc/`、`/mindnote/`、`/slides/` 路径里的 token 会被自动提取） |
| `--type` | 否 | 目标类型，可选值 `doc` / `sheet` / `file` / `wiki` / `bitable` / `docx` / `mindnote` / `slides`。传 URL 时可由 shortcut 自动推断；bare token 必须显式传 |
| `--perm` | 是 | 申请的权限，仅支持 `view` 或 `edit`（**不支持 `full_access`**，CLI 侧会直接拒绝） |
| `--remark` | 否 | 备注，会显示在权限申请卡片上 |
| `--dry-run` | 否 | 仅打印请求内容，不实际发送 |

## 输出

API 成功时返回空 `data`（仅 `code: 0, msg: "success"`），对应 CLI 输出：

```json
{
  "ok": true,
  "identity": "user",
  "data": {}
}
```

## 频率限制

- **应用级**：每应用每租户每分钟最多 10 次。
- **用户级**：同一用户对**同一篇文档**一天不超过 5 次。

## 常见错误

| 错误码 | 含义 | CLI 处理 |
|---|---|---|
| `1063006` | 申请次数已达上限（5 次/日） | CLI 自动加 hint：`permission-apply quota reached: each user may request access on the same document at most 5 times per day` |
| `1063007` | 当前文档无法申请（如：文档禁用外部申请、申请者已拥有对应权限、目标类型不支持 apply） | CLI 自动加 hint：`this document does not accept a permission-apply request ... contact the owner directly` |
| `1063002` | 无操作权限（如该租户关闭了外部申请） | 由统一 permission 错误路径处理 |
| `1063004` | 用户所在组织无分享权限 | 由统一 permission 错误路径处理 |
| `1063005` | 资源已删除 | 需要确认目标文档/节点是否仍存在 |
| `1066001/1066002` | 服务端异常 / 并发冲突 | 稍后重试 |

## 与 wiki URL 的关系

传入 `/wiki/<node_token>` 时，shortcut 会直接用 `node_token` 作为路径参数并以 `type=wiki` 调用接口。如果需要先把 wiki 节点解析成 `obj_token`（例如想显式对底层 docx 申请），自行先调 `wiki spaces get_node` 拿 `obj_token + obj_type`，再用 bare token + `--type docx` 调本命令。

## 参考

- OpenAPI 端点：`POST /open-apis/drive/v1/permissions/:token/members/apply`
