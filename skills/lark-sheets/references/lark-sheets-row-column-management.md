# Sheets Row and Column Management

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

这份 reference 汇总行列结构操作：

- `+add-dimension`
- `+insert-dimension`
- `+update-dimension`
- `+move-dimension`
- `+delete-dimension`

<a id="add-dimension"></a>
## `+add-dimension`

对应命令：`lark-cli sheets +add-dimension`

在工作表末尾追加空行或空列，不影响已有数据。

```bash
lark-cli sheets +add-dimension --spreadsheet-token "shtxxxxxxxx" \
  --sheet-id "<sheetId>" --dimension ROWS --length 10
```

参数：

| 参数 | 必填 | 说明 |
|------|------|------|
| `--url` | 否 | 电子表格 URL（与 `--spreadsheet-token` 二选一） |
| `--spreadsheet-token` | 否 | 表格 token |
| `--sheet-id` | 是 | 工作表 ID |
| `--dimension` | 是 | `ROWS` 或 `COLUMNS` |
| `--length` | 是 | 追加数量（1-5000） |
| `--dry-run` | 否 | 仅打印请求，不执行 |

输出：`addCount`、`majorDimension`

<a id="insert-dimension"></a>
## `+insert-dimension`

对应命令：`lark-cli sheets +insert-dimension`

在指定位置插入空行或空列，已有数据向下或向右移动。

```bash
lark-cli sheets +insert-dimension --spreadsheet-token "shtxxxxxxxx" \
  --sheet-id "<sheetId>" --dimension ROWS --start-index 3 --end-index 7
```

参数：

| 参数 | 必填 | 说明 |
|------|------|------|
| `--url` | 否 | 电子表格 URL（与 `--spreadsheet-token` 二选一） |
| `--spreadsheet-token` | 否 | 表格 token |
| `--sheet-id` | 是 | 工作表 ID |
| `--dimension` | 是 | `ROWS` 或 `COLUMNS` |
| `--start-index` | 是 | 起始位置（0-indexed） |
| `--end-index` | 是 | 结束位置（0-indexed，不含） |
| `--inherit-style` | 否 | `BEFORE` 或 `AFTER` |
| `--dry-run` | 否 | 仅打印请求，不执行 |

输出：成功时 `data` 为空对象 `{}`

<a id="update-dimension"></a>
## `+update-dimension`

对应命令：`lark-cli sheets +update-dimension`

更新指定范围行/列的显隐状态和行高/列宽。

```bash
lark-cli sheets +update-dimension --spreadsheet-token "shtxxxxxxxx" \
  --sheet-id "<sheetId>" --dimension ROWS --start-index 1 --end-index 3 \
  --visible=false
```

参数：

| 参数 | 必填 | 说明 |
|------|------|------|
| `--url` | 否 | 电子表格 URL（与 `--spreadsheet-token` 二选一） |
| `--spreadsheet-token` | 否 | 表格 token |
| `--sheet-id` | 是 | 工作表 ID |
| `--dimension` | 是 | `ROWS` 或 `COLUMNS` |
| `--start-index` | 是 | 起始位置（**1-indexed**，含） |
| `--end-index` | 是 | 结束位置（**1-indexed**，含） |
| `--visible` | 否 | `--visible=true` 或 `--visible=false` |
| `--fixed-size` | 否 | 行高或列宽（像素） |
| `--dry-run` | 否 | 仅打印请求，不执行 |

输出：成功时 `data` 为空对象 `{}`

<a id="move-dimension"></a>
## `+move-dimension`

对应命令：`lark-cli sheets +move-dimension`

将指定范围的行/列移动到目标位置。

```bash
lark-cli sheets +move-dimension --spreadsheet-token "shtxxxxxxxx" \
  --sheet-id "<sheetId>" --dimension ROWS \
  --start-index 0 --end-index 1 --destination-index 4
```

参数：

| 参数 | 必填 | 说明 |
|------|------|------|
| `--url` | 否 | 电子表格 URL（与 `--spreadsheet-token` 二选一） |
| `--spreadsheet-token` | 否 | 表格 token |
| `--sheet-id` | 是 | 工作表 ID |
| `--dimension` | 是 | `ROWS` 或 `COLUMNS` |
| `--start-index` | 是 | 源起始位置（0-indexed） |
| `--end-index` | 是 | 源结束位置（0-indexed，含） |
| `--destination-index` | 是 | 目标位置（0-indexed） |
| `--dry-run` | 否 | 仅打印请求，不执行 |

输出：成功时 `data` 为空对象 `{}`

<a id="delete-dimension"></a>
## `+delete-dimension`

对应命令：`lark-cli sheets +delete-dimension`

删除指定范围的行或列。

```bash
lark-cli sheets +delete-dimension --spreadsheet-token "shtxxxxxxxx" \
  --sheet-id "<sheetId>" --dimension ROWS --start-index 3 --end-index 7
```

参数：

| 参数 | 必填 | 说明 |
|------|------|------|
| `--url` | 否 | 电子表格 URL（与 `--spreadsheet-token` 二选一） |
| `--spreadsheet-token` | 否 | 表格 token |
| `--sheet-id` | 是 | 工作表 ID |
| `--dimension` | 是 | `ROWS` 或 `COLUMNS` |
| `--start-index` | 是 | 起始位置（**1-indexed**，含） |
| `--end-index` | 是 | 结束位置（**1-indexed**，含） |
| `--dry-run` | 否 | 仅打印请求，不执行 |

输出：`delCount`、`majorDimension`

## 参考

- [spreadsheet-management](lark-sheets-spreadsheet-management.md#info) — 查看当前工作表信息
- [cell-style-and-merge](lark-sheets-cell-style-and-merge.md) — 调整样式或合并单元格
