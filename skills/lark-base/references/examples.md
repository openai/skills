# 飞书多维表格使用场景完整示例（base）

本文档提供基于 `lark-cli base +...` shortcut 的完整示例。

> **返回**: [SKILL.md](../SKILL.md) | **参考**: [shortcut 字段 JSON 规范](lark-base-shortcut-field-properties.md) · [CellValue 规范](lark-base-cell-value.md)

---

## 场景 1：用 unified Shortcut 快速建表

适合已经明确字段结构、希望一次性完成建表的场景。

```bash
lark-cli base +table-create \
  --base-token bascnXXXXXXXX \
  --name "客户管理表" \
  --fields '[
    {"name":"客户名称","type":"text","description":"主标题字段"},
    {"name":"负责人","type":"user","multiple":false,"description":"用于标记客户跟进的直接负责人"},
    {"name":"签约日期","type":"datetime"},
    {"name":"状态","type":"select","multiple":false,"options":[{"name":"进行中"},{"name":"已完成"}]}
  ]'
```

---

## 场景 2：创建数据表并查看字段

适合需要先建表、再确认字段结构的场景。

### 步骤 1：在已有 Base 中创建数据表

```bash
lark-cli base +table-create \
  --base-token bascnXXXXXXXX \
  --name "客户管理表"
```

### 步骤 2：列出字段

```bash
lark-cli base +field-list \
  --base-token bascnXXXXXXXX \
  --table-id tblXXXXXXXX \
  --limit 100
```

> 提示：Base token 统一通过 `--base-token` 传入；表 ID 统一通过 `--table-id` 传入。

---

## 场景 3：创建、读取、更新单条记录

### 新增记录

```bash
lark-cli base +record-upsert \
  --base-token bascnXXXXXXXX \
  --table-id tblXXXXXXXX \
  --json '{
    "客户名称":"字节跳动",
    "负责人":[{"id":"ou_xxx"}],
    "状态":"进行中"
  }'
```

### 列出记录

```bash
lark-cli base +record-list \
  --base-token bascnXXXXXXXX \
  --table-id tblXXXXXXXX \
  --limit 100
```

### 更新记录

```bash
lark-cli base +record-upsert \
  --base-token bascnXXXXXXXX \
  --table-id tblXXXXXXXX \
  --record-id recXXXXXXXX \
  --json '{
    "状态":"已完成"
  }'
```

### 删除记录

```bash
lark-cli base +record-delete \
  --base-token bascnXXXXXXXX \
  --table-id tblXXXXXXXX \
  --record-id recXXXXXXXX \
  --yes
```

---

## 场景 4：配置视图筛选后按视图读取记录

需要筛选查询时，推荐先写视图筛选，再通过 `view_id` 读取记录。

### 更新视图筛选条件

```bash
lark-cli base +view-set-filter \
  --base-token bascnXXXXXXXX \
  --table-id tblXXXXXXXX \
  --view-id vewXXXXXXXX \
  --json '{
    "logic":"and",
    "conditions":[
      {
        "field_name":"状态",
        "operator":"is",
        "value":["进行中"]
      }
    ]
  }'
```

### 按视图读取记录

```bash
lark-cli base +record-list \
  --base-token bascnXXXXXXXX \
  --table-id tblXXXXXXXX \
  --view-id vewXXXXXXXX \
  --limit 100
```

---

## 场景 5：什么时候优先用 Shortcut

- 需要一次性建表并附带字段、视图时，优先 `lark-cli base +table-create`
- 需要按业务字段名做 upsert 时，优先 `lark-cli base +record-upsert`
- 需要配置筛选视图时，优先 `lark-cli base +view-set-filter`
- 需要记录历史时，优先 `lark-cli base +record-history-list`
