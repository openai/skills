# base +base-copy

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

复制一个已有 Base；可选只复制结构，不复制内容。

## 推荐命令

```bash
lark-cli base +base-copy \
  --base-token app_xxx \
  --name "Copied Base"

lark-cli base +base-copy \
  --base-token app_xxx \
  --name "Copied Base" \
  --folder-token fld_xxx \
  --time-zone Asia/Shanghai \
  --without-content
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--base-token <token>` | 是 | 源 Base Token |
| `--name <name>` | 否 | 新 Base 名称 |
| `--folder-token <token>` | 否 | 目标文件夹 token |
| `--time-zone <tz>` | 否 | 时区，如 `Asia/Shanghai` |
| `--without-content` | 否 | 只复制结构，不复制内容 |

## API 入参详情

**HTTP 方法和路径：**

```
POST /open-apis/base/v3/bases/:base_token/copy
```

## 返回重点

- 返回 `base`。
- CLI 会额外标记 `copied: true`。
- 回复结果时，必须主动返回新 Base 的可访问链接：
  - 优先使用返回结果中的 `base.url`
  - 同时返回新 Base 的 token
  - 如果本次返回没有 `url`，至少返回新 Base 的名称和 token

> [!IMPORTANT]
> 如果 Base 是**以应用身份（bot）复制**出来的，shortcut 会在复制成功后自动尝试为当前 CLI 用户添加该 Base 的 `full_access`（管理员）权限，并在输出中附带 `permission_grant` 字段。
>
> `permission_grant.status` 语义如下：
> - `granted`：当前 CLI 用户已获得该 Base 的管理员权限
> - `skipped`：Base 已复制成功，但没有可授权的当前 CLI 用户，或复制结果缺少可授权 token
> - `failed`：Base 已复制成功，但自动授权失败；结果中会包含失败原因，用户可稍后重试授权，或继续使用应用身份（bot）处理该 Base
>
> 回复复制结果时，除 `base token` 和可访问链接外，还必须明确告知用户 `permission_grant` 的结果。
>
> **仍然不要擅自执行 owner 转移。** 如果用户需要把 owner 转给自己，必须单独确认。

## 工作流

> [!CAUTION]
> 这是**写入操作** — 执行前必须向用户确认。

1. 先确认源 Base Token。
2. `--name`、`--folder-token`、`--time-zone` 都是可选项；用户没要求时不要为这些可选参数额外追问。
3. 只要结构时，显式传 `--without-content`。
4. 复制成功后，整理并返回：新 Base 名称、token，以及响应中已有的可访问链接。

## 参考

- [lark-base-workspace.md](lark-base-workspace.md) — base / workspace 索引页
- [lark-base-base-create.md](lark-base-base-create.md) — 创建全新 Base
