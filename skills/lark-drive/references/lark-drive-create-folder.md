# drive +create-folder（创建云空间文件夹）

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

在飞书云空间中创建一个新文件夹。该 shortcut 对原生 `drive files create_folder` 做了一层更适合日常使用的封装：`--folder-token` 可省略，此时会在调用者根目录创建；如果使用 `--as bot`，创建成功后 CLI 会尝试把新文件夹的可管理权限自动授予当前 CLI 用户。

## 命令

```bash
# 在根目录创建文件夹
lark-cli drive +create-folder \
  --name "周报归档"

# 在指定父文件夹下创建子文件夹
lark-cli drive +create-folder \
  --folder-token <PARENT_FOLDER_TOKEN> \
  --name "2026-W16"

# 预览底层调用
lark-cli drive +create-folder \
  --folder-token <PARENT_FOLDER_TOKEN> \
  --name "分析资料" \
  --dry-run
```

## 返回值

成功后会返回一个 JSON 对象，常见字段包括：

- `folder_token`：新建文件夹 token，可直接用于后续 `drive +move`、`drive +upload` 等命令
- `url`：新建文件夹链接（如果接口返回）
- `name`：文件夹名称
- `parent_folder_token`：父文件夹 token；为空字符串表示创建在根目录
- `permission_grant`（可选）：仅 `--as bot` 时返回，说明是否已自动为当前 CLI 用户授予可管理权限

> [!IMPORTANT]
> 如果文件夹是**以应用身份（bot）创建**的，如 `lark-cli drive +create-folder --as bot`，在创建成功后 CLI 会**尝试为当前 CLI 用户自动授予该文件夹的 `full_access`（可管理权限）**。
>
> 以应用身份创建时，结果里会额外返回 `permission_grant` 字段，明确说明授权结果：
> - `status = granted`：当前 CLI 用户已获得该文件夹的可管理权限
> - `status = skipped`：本地没有可用的当前用户 `open_id`，因此不会自动授权；可提示用户先完成 `lark-cli auth login`，再让 AI / agent 继续使用应用身份（bot）授予当前用户权限
> - `status = failed`：文件夹已创建成功，但自动授权用户失败；会带上失败原因，并提示稍后重试或继续使用 bot 身份处理该文件夹
>
> `permission_grant.perm = full_access` 表示该资源已授予“可管理权限”。
>
> **不要擅自执行 owner 转移。** 如果用户需要把 owner 转给自己，必须单独确认。

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--name` | 是 | 文件夹名称，不能为空，最长 256 字节 |
| `--folder-token` | 否 | 父文件夹 token；省略时表示在调用者根目录创建 |

## 行为说明

- **根目录创建**：不传 `--folder-token` 时，shortcut 会向 API 显式传空字符串 `folder_token=""`，让后端按“根目录”语义创建
- **bot 自动授权**：只有在 `--as bot` 时，结果才会额外带上 `permission_grant`
- **原生 API 仍可用**：如果用户明确要求按底层 API 字段调用，仍可继续使用 `lark-cli drive files create_folder`

## 推荐场景

- 用户说“在云空间新建一个文件夹 / 目录”时，优先使用 `drive +create-folder`
- 用户给了父文件夹链接或 token，需要在其下继续分层建目录时，传 `--folder-token`
- 如果后续还要上传文件、移动文件、建子目录，优先复用返回值里的 `folder_token`

> [!CAUTION]
> `drive +create-folder` 是**写入操作**，执行前必须确认用户意图。

## 参考

- [lark-drive](../SKILL.md) -- 云空间全部命令
- [lark-shared](../../lark-shared/SKILL.md) -- 认证和全局参数
