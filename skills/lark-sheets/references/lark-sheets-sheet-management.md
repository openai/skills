# Sheets Sheet Management

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

这份 reference 汇总工作表级操作：

- `+create-sheet`
- `+copy-sheet`
- `+delete-sheet`
- `+update-sheet`

其中 `+create-sheet` / `+copy-sheet` / `+delete-sheet` 底层封装官方“操作工作表（operate-sheets）”接口；`+update-sheet` 封装“更新工作表属性”接口。

<a id="create-sheet"></a>
## `+create-sheet`

对应命令：`lark-cli sheets +create-sheet`

```bash
# 在表格末尾或服务端默认位置创建工作表
lark-cli sheets +create-sheet --spreadsheet-token "shtxxxxxxxx" \
  --title "明细"

# 指定插入位置（0-based）
lark-cli sheets +create-sheet --url "https://example.larksuite.com/sheets/shtxxxxxxxx" \
  --title "汇总" --index 0
```

参数：

| 参数 | 必填 | 说明 |
|------|------|------|
| `--url` | 否 | 电子表格 URL（与 `--spreadsheet-token` 二选一） |
| `--spreadsheet-token` | 否 | 表格 token |
| `--title` | 否 | 工作表标题，最长 100 字符，不能包含 `/ \ ? * [ ] :` |
| `--index` | 否 | 工作表位置（从 0 开始） |
| `--dry-run` | 否 | 仅打印请求，不执行 |

输出：

- `spreadsheet_token`
- `sheet.sheet_id`
- `sheet.title`
- `sheet.index`

<a id="copy-sheet"></a>
## `+copy-sheet`

对应命令：`lark-cli sheets +copy-sheet`

```bash
# 按默认位置复制
lark-cli sheets +copy-sheet --spreadsheet-token "shtxxxxxxxx" \
  --sheet-id "<sheetId>"

# 指定副本名称和位置
lark-cli sheets +copy-sheet --url "https://example.larksuite.com/sheets/shtxxxxxxxx" \
  --sheet-id "<sheetId>" --title "销售副本" --index 2
```

参数：

| 参数 | 必填 | 说明 |
|------|------|------|
| `--url` | 否 | 电子表格 URL（与 `--spreadsheet-token` 二选一） |
| `--spreadsheet-token` | 否 | 表格 token |
| `--sheet-id` | 是 | 源工作表 ID |
| `--title` | 否 | 新工作表标题，最长 100 字符，不能包含 `/ \ ? * [ ] :` |
| `--index` | 否 | 新工作表位置（从 0 开始） |
| `--dry-run` | 否 | 仅打印请求，不执行 |

说明：

- 传 `--index` 时，CLI 会先复制，再追加一次位置更新，把副本移动到目标索引

输出：

- `spreadsheet_token`
- `sheet.sheet_id`
- `sheet.title`
- `sheet.index`

<a id="delete-sheet"></a>
## `+delete-sheet`

对应命令：`lark-cli sheets +delete-sheet`

> [!CAUTION]
> 这是**高风险删除操作**。CLI 会要求显式确认；可以先用 `--dry-run` 预览。

```bash
lark-cli sheets +delete-sheet --spreadsheet-token "shtxxxxxxxx" \
  --sheet-id "<sheetId>"
```

参数：

| 参数 | 必填 | 说明 |
|------|------|------|
| `--url` | 否 | 电子表格 URL（与 `--spreadsheet-token` 二选一） |
| `--spreadsheet-token` | 否 | 表格 token |
| `--sheet-id` | 是 | 要删除的工作表 ID |
| `--dry-run` | 否 | 仅打印请求，不执行 |

输出：

- `deleted`
- `spreadsheet_token`
- `sheet_id`

<a id="update-sheet"></a>
## `+update-sheet`

对应命令：`lark-cli sheets +update-sheet`

用于更新工作表标题、位置、隐藏状态、冻结行列和保护设置。

```bash
# 改名 + 调整冻结
lark-cli sheets +update-sheet --spreadsheet-token "shtxxxxxxxx" \
  --sheet-id "<sheetId>" --title "汇总表" --frozen-row-count 2 --frozen-col-count 1

# 隐藏工作表
lark-cli sheets +update-sheet --url "https://example.larksuite.com/sheets/shtxxxxxxxx" \
  --sheet-id "<sheetId>" --hidden=true

# 开启保护并授权额外编辑人
lark-cli sheets +update-sheet --spreadsheet-token "shtxxxxxxxx" \
  --sheet-id "<sheetId>" --lock LOCK --lock-info "仅财务维护" \
  --user-id-type open_id --user-ids '["ou_xxx","ou_yyy"]'
```

参数：

| 参数 | 必填 | 说明 |
|------|------|------|
| `--url` | 否 | 电子表格 URL（与 `--spreadsheet-token` 二选一） |
| `--spreadsheet-token` | 否 | 表格 token |
| `--sheet-id` | 是 | 要更新的工作表 ID |
| `--title` | 否 | 新标题，最长 100 字符，不能包含 `/ \ ? * [ ] :` |
| `--index` | 否 | 新位置（从 0 开始） |
| `--hidden` | 否 | `--hidden=true` 隐藏，`--hidden=false` 取消隐藏 |
| `--frozen-row-count` | 否 | 冻结行数，`0` 表示取消冻结 |
| `--frozen-col-count` | 否 | 冻结列数，`0` 表示取消冻结 |
| `--lock` | 否 | 保护模式：`LOCK` / `UNLOCK` |
| `--lock-info` | 否 | 保护备注；要求 `--lock LOCK` |
| `--user-id-type` | 否 | `--user-ids` 的 ID 类型：`open_id` / `union_id` / `lark_id` / `user_id` |
| `--user-ids` | 否 | 额外可编辑用户 ID 的 JSON 数组；要求 `--lock LOCK` |
| `--dry-run` | 否 | 仅打印请求，不执行 |

输出：

- `spreadsheet_token`
- `sheet.sheet_id`
- `sheet.title`
- `sheet.hidden`
- `sheet.grid_properties.frozen_row_count`
- `sheet.grid_properties.frozen_column_count`
- `sheet.protect`

## 参考

- [spreadsheet-management](lark-sheets-spreadsheet-management.md#info) — 先获取 `sheet_id`
- [row-column-management](lark-sheets-row-column-management.md) — 需要改行列结构时用这组命令
