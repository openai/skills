# base +record-batch-create

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

批量创建记录。

## 适用场景（重点）

- 适合导入 CSV / Excel、外部系统一次性写入新数据。
- 先把输入数据映射到合适的字段类型，再组装 `fields + rows`。

## 推荐命令

```bash
lark-cli base +record-batch-create --base-token <base_token> --table-id <table_id> \
  --json '{"fields":["标题","状态"],"rows":[["任务 A","Open"],["任务 B","Done"]]}'

lark-cli base +record-batch-create --base-token <base_token> --table-id <table_id> --json @batch-create.json
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--base-token <token>` | 是 | Base Token |
| `--table-id <id_or_name>` | 是 | 表 ID 或表名 |
| `--json <body>` | 是 | 批量创建请求体，必须是 JSON 对象。支持直接传 JSON 字符串，或 `@<file_path>` 从文件读取 |

## API

`POST /open-apis/base/v3/bases/:base_token/tables/:table_id/records/batch_create`

## `--json` 结构

本节只说明 `+record-batch-create` 的外层 JSON 形状；CellValue 统一看 [lark-base-cell-value.md](lark-base-cell-value.md)。

对象形态：`{"fields":[...],"rows":[...]}`。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `fields` | `string[]` | 是 | 字段 ID 或字段名数组 |
| `rows` | `CellValue[][]` | 是 | 二维数组，每一行按 `fields` 同序给 cell；单次最多 200 行 |

## 返回重点

返回 `fields`、`field_id_list`、`record_id_list`、`data`，其中 `data` 与 `fields` 列顺序对齐。

## 坑点

- `fields` 与每行 `rows` 的列顺序必须一一对应。
- 空单元格必须显式用 `null` 填充。
- 单次最多 200 行，超出需分批写入。
- select 写入未知选项时平台可能自动新增选项；如果不是要新增选项，先确认真实选项名。

## 参考

- [lark-base-record.md](lark-base-record.md) — record 索引页
- [lark-base-cell-value.md](lark-base-cell-value.md) — CellValue 格式规范
