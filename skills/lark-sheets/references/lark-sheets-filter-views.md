# Sheets Filter Views

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

这份 reference 汇总筛选视图和筛选条件：

- `+create-filter-view`
- `+update-filter-view`
- `+list-filter-views`
- `+get-filter-view`
- `+delete-filter-view`
- `+create-filter-view-condition`
- `+update-filter-view-condition`
- `+list-filter-view-conditions`
- `+get-filter-view-condition`
- `+delete-filter-view-condition`

<a id="create-filter-view"></a>
## `+create-filter-view`

对应命令：`lark-cli sheets +create-filter-view`

在工作表中创建筛选视图，每个工作表最多 150 个。

```bash
lark-cli sheets +create-filter-view --spreadsheet-token "shtxxxxxxxx" \
  --sheet-id "<sheetId>" --range "<sheetId>!A1:H14"

lark-cli sheets +create-filter-view --spreadsheet-token "shtxxxxxxxx" \
  --sheet-id "<sheetId>" --range "<sheetId>!A1:H14" --filter-view-name "我的筛选"
```

参数：

| 参数 | 必填 | 说明 |
|------|------|------|
| `--url` | 否 | 电子表格 URL（与 `--spreadsheet-token` 二选一） |
| `--spreadsheet-token` | 否 | 表格 token |
| `--sheet-id` | 是 | 工作表 ID |
| `--range` | 是 | 筛选范围 |
| `--filter-view-name` | 否 | 显示名称 |
| `--filter-view-id` | 否 | 自定义 10 位字母数字 ID |

输出：`filter_view`

<a id="update-filter-view"></a>
## `+update-filter-view`

对应命令：`lark-cli sheets +update-filter-view`

```bash
lark-cli sheets +update-filter-view --spreadsheet-token "shtxxxxxxxx" \
  --sheet-id "<sheetId>" --filter-view-id "<fvId>" --range "<sheetId>!A1:J20"
```

参数：

| 参数 | 必填 | 说明 |
|------|------|------|
| `--url` | 否 | 电子表格 URL |
| `--spreadsheet-token` | 否 | 表格 token |
| `--sheet-id` | 是 | 工作表 ID |
| `--filter-view-id` | 是 | 筛选视图 ID |
| `--range` | 否 | 新范围 |
| `--filter-view-name` | 否 | 新显示名称 |

<a id="list-filter-views"></a>
## `+list-filter-views`

对应命令：`lark-cli sheets +list-filter-views`

```bash
lark-cli sheets +list-filter-views --spreadsheet-token "shtxxxxxxxx" --sheet-id "<sheetId>"
```

输出：`items[]`（`filter_view_id`、`filter_view_name`、`range`）

<a id="get-filter-view"></a>
## `+get-filter-view`

对应命令：`lark-cli sheets +get-filter-view`

```bash
lark-cli sheets +get-filter-view --spreadsheet-token "shtxxxxxxxx" \
  --sheet-id "<sheetId>" --filter-view-id "<fvId>"
```

输出：`filter_view`

<a id="delete-filter-view"></a>
## `+delete-filter-view`

对应命令：`lark-cli sheets +delete-filter-view`

```bash
lark-cli sheets +delete-filter-view --spreadsheet-token "shtxxxxxxxx" \
  --sheet-id "<sheetId>" --filter-view-id "<fvId>"
```

参数：

| 参数 | 必填 | 说明 |
|------|------|------|
| `--url` | 否 | 电子表格 URL |
| `--spreadsheet-token` | 否 | 表格 token |
| `--sheet-id` | 是 | 工作表 ID |
| `--filter-view-id` | 是 | 筛选视图 ID |

<a id="create-filter-view-condition"></a>
## `+create-filter-view-condition`

对应命令：`lark-cli sheets +create-filter-view-condition`

为筛选视图的指定列创建筛选条件。

```bash
# 数值筛选：E 列 < 6
lark-cli sheets +create-filter-view-condition --spreadsheet-token "shtxxxxxxxx" \
  --sheet-id "<sheetId>" --filter-view-id "<fvId>" \
  --condition-id "E" --filter-type "number" --compare-type "less" --expected '["6"]'

# 文本筛选：G 列以 a 开头
lark-cli sheets +create-filter-view-condition --spreadsheet-token "shtxxxxxxxx" \
  --sheet-id "<sheetId>" --filter-view-id "<fvId>" \
  --condition-id "G" --filter-type "text" --compare-type "beginsWith" --expected '["a"]'
```

参数：

| 参数 | 必填 | 说明 |
|------|------|------|
| `--url` | 否 | 电子表格 URL |
| `--spreadsheet-token` | 否 | 表格 token |
| `--sheet-id` | 是 | 工作表 ID |
| `--filter-view-id` | 是 | 筛选视图 ID |
| `--condition-id` | 是 | 列字母，如 `E` |
| `--filter-type` | 是 | `hiddenValue` / `number` / `text` / `color` |
| `--compare-type` | 否 | 比较运算符 |
| `--expected` | 是 | 筛选值 JSON 数组 |

输出：`condition`

<a id="update-filter-view-condition"></a>
## `+update-filter-view-condition`

对应命令：`lark-cli sheets +update-filter-view-condition`

```bash
lark-cli sheets +update-filter-view-condition --spreadsheet-token "shtxxxxxxxx" \
  --sheet-id "<sheetId>" --filter-view-id "<fvId>" --condition-id "E" \
  --filter-type "number" --compare-type "between" --expected '["2","10"]'
```

参数与创建条件相同，但 `filter-type` / `compare-type` / `expected` 可按需部分更新。

<a id="list-filter-view-conditions"></a>
## `+list-filter-view-conditions`

对应命令：`lark-cli sheets +list-filter-view-conditions`

```bash
lark-cli sheets +list-filter-view-conditions --spreadsheet-token "shtxxxxxxxx" \
  --sheet-id "<sheetId>" --filter-view-id "<fvId>"
```

输出：`items[]`

<a id="get-filter-view-condition"></a>
## `+get-filter-view-condition`

对应命令：`lark-cli sheets +get-filter-view-condition`

```bash
lark-cli sheets +get-filter-view-condition --spreadsheet-token "shtxxxxxxxx" \
  --sheet-id "<sheetId>" --filter-view-id "<fvId>" --condition-id "E"
```

输出：`condition`

<a id="delete-filter-view-condition"></a>
## `+delete-filter-view-condition`

对应命令：`lark-cli sheets +delete-filter-view-condition`

```bash
lark-cli sheets +delete-filter-view-condition --spreadsheet-token "shtxxxxxxxx" \
  --sheet-id "<sheetId>" --filter-view-id "<fvId>" --condition-id "E"
```

## 参考

- [dropdown](lark-sheets-dropdown.md) — 需要下拉值配合筛选时
- [cell-data](lark-sheets-cell-data.md#find) — 只查数据时用 `+find`
