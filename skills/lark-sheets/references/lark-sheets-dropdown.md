# Sheets Dropdown

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

这份 reference 汇总下拉列表配置：

- `+set-dropdown`
- `+update-dropdown`
- `+get-dropdown`
- `+delete-dropdown`

> **关键规则：** 使用 `multipleValue` 写入前，必须先设置下拉列表；否则值会被当成纯文本。

<a id="set-dropdown"></a>
## `+set-dropdown`

对应命令：`lark-cli sheets +set-dropdown`

```bash
lark-cli sheets +set-dropdown --url "https://example.larksuite.com/sheets/shtxxxxxxxx" \
  --range "<sheetId>!A2:A100" --condition-values '["选项1", "选项2", "选项3"]'
```

参数：

| 参数 | 必填 | 说明 |
|------|------|------|
| `--url` | 否 | 电子表格 URL（与 `--spreadsheet-token` 二选一） |
| `--spreadsheet-token` | 否 | 表格 token |
| `--range` | 是 | 范围（如 `<sheetId>!A2:A100`） |
| `--condition-values` | 是 | 下拉选项 JSON 数组 |
| `--multiple` | 否 | 是否多选 |
| `--highlight` | 否 | 是否着色 |
| `--colors` | 否 | 颜色 JSON 数组 |
| `--dry-run` | 否 | 仅打印请求，不执行 |

输出：`code`、`msg`

<a id="update-dropdown"></a>
## `+update-dropdown`

对应命令：`lark-cli sheets +update-dropdown`

```bash
lark-cli sheets +update-dropdown --spreadsheet-token "shtxxxxxxxx" \
  --sheet-id "<sheetId>" \
  --ranges '["<sheetId>!A1:A100"]' \
  --condition-values '["选项A", "选项B"]'
```

参数：

| 参数 | 必填 | 说明 |
|------|------|------|
| `--url` | 否 | 电子表格 URL（与 `--spreadsheet-token` 二选一） |
| `--spreadsheet-token` | 否 | 表格 token |
| `--sheet-id` | 是 | 工作表 ID |
| `--ranges` | 是 | 范围 JSON 数组 |
| `--condition-values` | 是 | 选项 JSON 数组 |
| `--multiple` | 否 | 是否多选 |
| `--highlight` | 否 | 是否着色 |
| `--colors` | 否 | 颜色 JSON 数组 |
| `--dry-run` | 否 | 仅打印请求，不执行 |

输出：`spreadsheetToken`、`sheetId`、`dataValidation`

<a id="get-dropdown"></a>
## `+get-dropdown`

对应命令：`lark-cli sheets +get-dropdown`

```bash
lark-cli sheets +get-dropdown --spreadsheet-token "shtxxxxxxxx" \
  --range "<sheetId>!A2:A100"
```

参数：

| 参数 | 必填 | 说明 |
|------|------|------|
| `--url` | 否 | 电子表格 URL（与 `--spreadsheet-token` 二选一） |
| `--spreadsheet-token` | 否 | 表格 token |
| `--range` | 是 | 查询范围 |
| `--dry-run` | 否 | 仅打印请求，不执行 |

输出：

- `dataValidations[].conditionValues`
- `dataValidations[].ranges`
- `dataValidations[].options.multipleValues`
- `dataValidations[].options.highlightValidData`
- `dataValidations[].options.colorValueMap`

<a id="delete-dropdown"></a>
## `+delete-dropdown`

对应命令：`lark-cli sheets +delete-dropdown`

```bash
lark-cli sheets +delete-dropdown --spreadsheet-token "shtxxxxxxxx" \
  --ranges '["<sheetId>!A2:A100", "<sheetId>!C1:C50"]'
```

参数：

| 参数 | 必填 | 说明 |
|------|------|------|
| `--url` | 否 | 电子表格 URL（与 `--spreadsheet-token` 二选一） |
| `--spreadsheet-token` | 否 | 表格 token |
| `--ranges` | 是 | 范围 JSON 数组 |
| `--dry-run` | 否 | 仅打印请求，不执行 |

输出：

- `rangeResults[].range`
- `rangeResults[].success`
- `rangeResults[].updatedCells`

## 典型流程

```bash
# 1. 配置下拉
lark-cli sheets +set-dropdown --url "<url>" \
  --range "<sheetId>!J2:J100" --condition-values '["选项1","选项2"]' --multiple

# 2. 再写入 multipleValue
lark-cli sheets +write --url "<url>" --sheet-id "<sheetId>" --range "J2" \
  --values '[[{"type":"multipleValue","values":["选项1","选项2"]}]]'
```

## 参考

- [cell-data](lark-sheets-cell-data.md#write) — 写入普通单元格数据
