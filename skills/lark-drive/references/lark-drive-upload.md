
# drive +upload

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

上传本地文件到飞书云空间。目标位置可以是 Drive 文件夹，也可以是 wiki 节点。

## 快速决策
- 用户要在 Drive 里上传、创建、读取、覆盖更新**原生 `.md` 文件**（不是导入成 docx），切到 [`lark-markdown`](../../lark-markdown/SKILL.md)。

## 命令

```bash
# 上传到 Drive 文件夹
lark-cli drive +upload --file ./report.pdf --folder-token fldbc_xxx

# 上传到 wiki 节点
lark-cli drive +upload --file ./report.pdf --wiki-token wikcn_xxx

# 不指定目标时，上传到调用者的 Drive 根目录
lark-cli drive +upload --file ./report.pdf

# 自定义上传后的文件名
lark-cli drive +upload --file ./report.pdf --name "季度总结.pdf"

# 覆盖已存在文件（原地覆盖，保留 file_token）
lark-cli drive +upload --file ./report.pdf --file-token boxcn_existing_file

# 原生命令（高级/分片上传）：预上传 + 完成上传
lark-cli drive files upload_prepare --data '{
  "file_name": "report.pdf",
  "parent_type": "explorer",
  "parent_node": "fldbc_xxx",
  "size": 1048576,
  "file_token": "boxcn_existing_file"
}'
lark-cli drive files upload_finish --data '{
  "upload_id": "<UPLOAD_ID>",
  "block_num": 1
}'

# 查看完整参数定义
lark-cli schema drive.files.upload_prepare
```

> [!IMPORTANT]
> 如果文件是**以应用身份（bot）新建上传**的，如 `lark-cli drive +upload --as bot` 在上传成功后，CLI 会**尝试为当前 CLI 用户自动授予该文件的 `full_access`（可管理权限）**。
>
> 如果这次调用传了 `--file-token`，表示是在**覆盖已有文件**，CLI **不会**额外修改该文件权限。
>
> 以应用身份上传时，结果里会额外返回 `permission_grant` 字段，明确说明授权结果：
> - `status = granted`：当前 CLI 用户已获得该文件的可管理权限
> - `status = skipped`：本地没有可用的当前用户 `open_id`，因此不会自动授权；可提示用户先完成 `lark-cli auth login`，再让 AI / agent 继续使用应用身份（bot）授予当前用户权限
> - `status = failed`：文件已上传成功，但自动授权用户失败；会带上失败原因，并提示稍后重试或继续使用 bot 身份处理该文件
>
> `permission_grant.perm = full_access` 表示该资源已授予“可管理权限”。
>
> **不要擅自执行 owner 转移。** 如果用户需要把 owner 转给自己，必须单独确认。

> [!TIP]
> 当底层上传接口返回版本号时，shortcut 会在结果里额外透出 `version`。

## 目标位置选择（关键）

- 上传到 Drive 文件夹：传 `--folder-token <folder_token>`，shortcut 会发送 `parent_type=explorer`
- 上传到 wiki 节点：传 `--wiki-token <wiki_token>`，shortcut 会发送 `parent_type=wiki`
- 上传到 Drive 根目录：`--folder-token` 和 `--wiki-token` 都不传
- 覆盖已有文件：额外传 `--file-token <existing_file_token>`；shortcut 会把它原样透传到底层 `upload_all` / `upload_prepare`，让后端按覆盖语义写入
- bot 模式下，`--file-token` 覆盖只改文件内容；不会额外给当前 CLI 用户补 `full_access`
- 不要传空目标值：`--folder-token ""` / `--wiki-token ""` 会被视为参数错误；如需上传到 Drive 根目录，应直接省略这两个参数
- 不要传空 `--file-token`：如需新建上传，直接省略该参数；显式传空字符串会报错
- `--folder-token` 和 `--wiki-token` 互斥，不要同时传
- `--wiki-token` 传的是 **wiki node token**，不是 `space_id`

Shortcut 参数：

| 参数 | 必填 | 说明 |
|------|------|------|
| `--file` | 是 | 本地文件路径 |
| `--file-token` | 否 | 已存在文件的 token；传入后按“覆盖已有文件”语义上传 |
| `--folder-token` | 否 | 目标文件夹 token；与 `--wiki-token` 互斥；省略时默认为 Drive 根目录；显式传空字符串会报错 |
| `--wiki-token` | 否 | 目标 wiki 节点 token；与 `--folder-token` 互斥；会映射为 `parent_type=wiki`、`parent_node=<wiki_token>`；显式传空字符串会报错 |
| `--name` | 否 | 上传后的文件名；默认使用本地文件名 |

参数（预上传 `--data` JSON body）：

| 字段 | 必填 | 说明 |
|------|------|------|
| `file_name` | 是 | 文件名 |
| `parent_type` | 是 | 父节点类型；上传到文件夹 / 根目录时用 `"explorer"`，上传到 wiki 节点时用 `"wiki"` |
| `parent_node` | 是 | 父节点 token；`explorer` 时传文件夹 token（根目录可为空字符串），`wiki` 时传 wiki node token |
| `size` | 是 | 文件大小（字节） |
| `file_token` | 否 | 已存在文件 token；传入后覆盖该文件内容 |

> [!CAUTION]
> 这是**写入操作** —— 执行前必须确认用户意图。

## 参考

- [lark-drive](../SKILL.md) -- 云空间全部命令
- [lark-shared](../../lark-shared/SKILL.md) -- 认证和全局参数
