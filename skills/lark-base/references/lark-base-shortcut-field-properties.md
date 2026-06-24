# base shortcut field JSON 规范（lark-base-shortcut-field-properties）

> 适用命令：`lark-cli base +field-create`、`lark-cli base +field-update`

本文件定义 **shortcut 写字段** 时 `--json` 的推荐格式，是字段类型与字段 JSON 结构的 source of truth。目标不是复刻完整 schema，而是让 agent 稳定产出正确 payload。

## 1. 顶层规则（必须遵守）

- `--json` 必须是 JSON 对象。
- 顶层统一使用：`type` + `name` + 类型特有字段。
- 所有字段类型都支持可选 `description`；支持纯文本，也支持 Markdown 链接。
- 不要使用旧结构：`field_name`、`property`、`ui_type`、数字枚举 `type`。
- `+field-update` 使用同样的字段 JSON 结构，但语义是 `PUT`；建议先 `+field-get` 再按目标状态全量提交。
- `type=formula` 或 `type=lookup` 创建/更新前，必须先读对应 guide。

推荐示例：

```json
{
  "type": "text",
  "name": "需求背景",
  "description": "记录需求背景与已知约束"
}
```

## 2. 字段速查

| 类型 | 最小必填字段 | 常见补充字段 |
|------|--------------|-------------|
| `text` | `type` `name` | `style.type` |
| `number` | `type` `name` | `style` |
| `select` | `type` `name` | `multiple` + `options`，或 `multiple` + `dynamic_options_source` |
| `datetime` | `type` `name` | `style.format` |
| `created_at` / `updated_at` | `type` `name` | `style.format` |
| `user` / `group_chat` | `type` `name` | `multiple` |
| `created_by` / `updated_by` | `type` `name` | 无 |
| `link` | `type` `name` `link_table` | `bidirectional` `bidirectional_link_field_name` |
| `formula` | `type` `name` `expression` | 无 |
| `lookup` | `type` `name` `from` `select` `where` | `aggregate` |
| `auto_number` | `type` `name` | `style.rules` |
| `attachment` / `location` / `checkbox` | `type` `name` | 无 |

所有类型都可额外传 `description`；上表的“常见补充字段”只列类型特有配置。

## 3. 各类型写法

### 3.1 text

文本字段；电话、超链接、邮箱、条码也都属于 `text`，通过 `style.type` 区分。

最小写法（默认 `style.type` 为 `plain`）：

```json
{
  "type": "text",
  "name": "标题"
}
```

常用写法：

```json
{
  "type": "text",
  "name": "标题",
  "description": "主标题字段"
}
```

```json
{
  "type": "text",
  "name": "联系电话",
  "style": { "type": "phone" }
}
```

```json
{
  "type": "text",
  "name": "官网",
  "style": { "type": "url" }
}
```

常用 `style.type`：`plain`（默认）、`phone`、`url`、`email`、`barcode`。

### 3.2 number

数字字段；货币、进度、评分都属于 `number`，通过 `style.type` 区分。

最小写法（默认 `style.type` 为 `plain`）：

```json
{
  "type": "number",
  "name": "工时"
}
```

`style` 是按 `type` 区分的对象；不同 `style.type` 的内部字段不一样，不要混传。

#### `plain`

支持字段：`precision`、`percentage`、`thousands_separator`

默认值 / 约束：
- `precision` 取值 `0..4`，默认 `2`
- `percentage` 默认 `false`
- `thousands_separator` 默认 `false`

```json
{
  "type": "number",
  "name": "工时",
  "style": {
    "type": "plain",
    "precision": 2,
    "percentage": false,
    "thousands_separator": true
  }
}
```

#### `currency`

支持字段：`precision`、`currency_code`

默认值 / 约束：
- `precision` 取值 `0..4`，默认 `2`
- `currency_code` 必填，如 `CNY`、`USD`、`EUR`

```json
{
  "type": "number",
  "name": "预算",
  "style": { "type": "currency", "precision": 2, "currency_code": "CNY" }
}
```

#### `progress`

支持字段：`percentage`、`color`

默认值 / 约束：
- `percentage` 默认 `true`
- `color` 必填
- `color` 可用：`Blue`、`Purple`、`DarkGreen`、`Green`、`Cyan`、`Orange`、`Red`、`Gray`、`WhiteToBlueGradient`、`WhiteToPurpleGradient`、`WhiteToOrangeGradient`、`GreenToRedGradient`、`RedToGreenGradient`、`BlueToPinkGradient`、`PinkToBlueGradient`、`SpectralGradient`

```json
{
  "type": "number",
  "name": "完成度",
  "style": { "type": "progress", "percentage": true, "color": "Blue" }
}
```

#### `rating`

支持字段：`icon`、`min`、`max`

默认值 / 约束：
- `icon` 默认 `star`
- `icon` 可用：`star`、`heart`、`thumbsup`、`fire`、`smile`、`lightning`、`flower`、`number`
- `min` 取值 `0..1`，默认 `1`
- `max` 取值 `1..10`，默认 `5`

```json
{
  "type": "number",
  "name": "评分",
  "style": { "type": "rating", "icon": "star", "min": 1, "max": 5 }
}
```

### 3.3 select

单选和多选都使用 `select`；用 `multiple` 区分。`multiple` 默认 `false`。静态选项用 `options`，动态选项用 `dynamic_options_source`；两者不要同时传。

#### 静态选项

支持字段：`multiple`、`options`

默认值 / 约束：
- `multiple` 默认 `false`
- `options` 最多 `10000` 项
- `options[]` 结构是 `{name, hue?, lightness?}`
- `options[].name` 必填
- `options[].hue` 可用：`Red`、`Orange`、`Yellow`、`Lime`、`Green`、`Turquoise`、`Wathet`、`Blue`、`Carmine`、`Purple`、`Gray` 缺省值为 `Blue`
- `options[].lightness` 可用：`Lighter`、`Light`、`Standard`、`Dark`、`Darker` 缺省值为 `Lighter`
- 选项里没有 `id`，只有 `name`。

```json
{
  "type": "select",
  "name": "状态",
  "multiple": false,
  "options": [
    { "name": "Todo", "hue": "Blue", "lightness": "Lighter" },
    { "name": "Done", "hue": "Green", "lightness": "Light" }
  ]
}
```

#### 动态选项

支持字段：`multiple`、`dynamic_options_source`

默认值 / 约束：
- `multiple` 默认 `false`
- `dynamic_options_source` 结构是 `{table_id, field_id}`
- `dynamic_options_source.table_id` 填来源表 id 或表名
- `dynamic_options_source.field_id` 填来源字段 id 或字段名
- `dynamic_options_source` 仅创建支持；更新已有字段时不要传

```json
{
  "type": "select",
  "name": "动态状态",
  "multiple": false,
  "dynamic_options_source": {
    "table_id": "选项表",
    "field_id": "候选状态"
  }
}
```

### 3.4 datetime

手动填写的日期/时间字段。系统时间用 `created_at` / `updated_at`。

最小写法：

```json
{
  "type": "datetime",
  "name": "截止时间"
}
```

支持字段：`style.format`

默认值 / 约束：
- `style.format` 默认 `yyyy/MM/dd` 可用格式：`yyyy/MM/dd`、`yyyy/MM/dd HH:mm`、`yyyy/MM/dd HH:mm Z`、`yyyy-MM-dd`、`yyyy-MM-dd HH:mm`、`yyyy-MM-dd HH:mm Z`、`MM-dd`、`MM/dd/yyyy`、`dd/MM/yyyy`

常用写法：

```json
{
  "type": "datetime",
  "name": "截止时间",
  "style": { "format": "yyyy-MM-dd HH:mm" }
}
```

### 3.5 created_at / updated_at

系统创建时间 / 系统更新时间字段；可配显示格式，但记录写入时应视为只读。

支持字段：`style.format`

默认值 / 约束：
- `style.format` 默认 `yyyy/MM/dd`
- 可用格式：`yyyy/MM/dd`、`yyyy/MM/dd HH:mm`、`yyyy/MM/dd HH:mm Z`、`yyyy-MM-dd`、`yyyy-MM-dd HH:mm`、`yyyy-MM-dd HH:mm Z`、`MM-dd`、`MM/dd/yyyy`、`dd/MM/yyyy`

```json
{ "type": "created_at", "name": "创建时间" }
```

```json
{ "type": "updated_at", "name": "更新时间", "style": { "format": "yyyy/MM/dd HH:mm" } }
```

### 3.6 user / group_chat

人员字段和群字段都支持 `multiple`。

默认值 / 约束：
- `multiple` 默认 `true`

```json
{ "type": "user", "name": "负责人", "multiple": true }
```

```json
{ "type": "group_chat", "name": "负责群", "multiple": true }
```

### 3.7 created_by / updated_by

系统创建人 / 系统修改人字段；记录写入时应视为只读。

```json
{ "type": "created_by", "name": "创建人" }
```

```json
{ "type": "updated_by", "name": "更新人" }
```

### 3.8 link

关联字段；`link_table` 必填。

支持字段：`link_table`、`bidirectional`、`bidirectional_link_field_name`

默认值 / 约束：
- `link_table` 必填
- `link` 字段的单元格表示“当前记录关联到的对侧表记录集合”
- `bidirectional` 默认 `false`
- `bidirectional=true` 时，会在被关联表自动创建一个反向关联字段。任一侧记录的关联关系发生变更时，另一侧对应记录会自动同步更新
- `bidirectional_link_field_name` 仅在 `bidirectional=true` 时使用

```json
{
  "type": "link",
  "name": "关联任务",
  "link_table": "任务表"
}
```

双向关联：

```json
{
  "type": "link",
  "name": "关联任务",
  "link_table": "任务表",
  "bidirectional": true,
  "bidirectional_link_field_name": "反向关联"
}
```

更新时注意：
- `link` 不允许转换为其他类型，其他类型也不能转换为 `link`。
- 现有 `link` 字段的 `bidirectional` 不能改。

### 3.9 formula

公式字段；`expression` 必填。创建/更新前先读 [formula-field-guide.md](formula-field-guide.md) 学习公式语法。

```json
{
  "type": "formula",
  "name": "合计",
  "expression": "1+1"
}
```

### 3.10 lookup

查找引用字段；`from`、`select`、`where` 必填，`aggregate` 可选。创建/更新前先读 [lookup-field-guide.md](lookup-field-guide.md)。

支持字段：`from`、`select`、`where`、`aggregate`

默认值 / 约束：
- `from`、`select`、`where` 必填
- `aggregate` 默认 `raw_value` 代表不进行聚合，直接返回 select 回的原始值
- `aggregate` 可用：`raw_value`、`sum`、`average`、`counta`、`unique_counta`、`max`、`min`、`unique`
- `where.logic` 默认 `and`，仅支持 `and` / `or`
- `where.conditions` 至少 1 条
- `conditions` 每项是三元组 `[field, op, value?]`

```json
{
  "type": "lookup",
  "name": "状态汇总",
  "from": "任务表",
  "select": "状态",
  "where": {
    "logic": "and",
    "conditions": [
      ["负责人", "==", { "type": "field_ref", "field": "当前负责人" }],
      ["状态", "non_empty", null]
    ]
  },
  "aggregate": "raw_value"
}
```

### 3.11 auto_number

自动编号字段；不写 `style.rules` 时使用默认规则：`NO.001`。

最小写法：

```json
{
  "type": "auto_number",
  "name": "编号"
}
```

支持字段：`style.rules`

默认值 / 约束：
- `style.rules` 是规则数组，数量 `1..9`
- 默认规则：

```json
{
  "style": {
    "rules": [
      { "type": "text", "text": "NO." },
      { "type": "incremental_number", "length": 3 }
    ]
  }
}
```

#### `text`

支持字段：`text`

```json
{ "type": "text", "text": "TASK-" }
```

#### `incremental_number`

支持字段：`length`

默认值 / 约束：
- `length` 取值 `1..9`

```json
{ "type": "incremental_number", "length": 4 }
```

#### `created_time`

支持字段：`date_format`

默认值 / 约束：
- `date_format` 可用：`yyyyMMdd`、`yyyyMM`、`yyMM`、`MMdd`、`yyyy`、`MM`、`dd`

```json
{ "type": "created_time", "date_format": "yyyyMMdd" }
```

自定义规则：

```json
{
  "type": "auto_number",
  "name": "编号",
  "style": {
    "rules": [
      { "type": "text", "text": "TASK-" },
      { "type": "created_time", "date_format": "yyyyMMdd" },
      { "type": "incremental_number", "length": 4 }
    ]
  }
}
```

### 3.12 attachment / location / checkbox

```json
{ "type": "attachment", "name": "附件" }
```

```json
{ "type": "location", "name": "位置" }
```

```json
{ "type": "checkbox", "name": "完成" }
```

## 4. 创建与更新

- `+field-create`：按目标字段配置直接构造 `--json`。
- `+field-update`：使用同样的 JSON 结构，但语义是 `PUT`；建议先 `+field-get`，再按目标完整状态提交。

## 5. 易错点

- `select` 只有一个类型；不要写 `single_select` / `multi_select`，用 `multiple` 控制是否多选。
- `number` 的精度、货币、进度、评分配置都放在 `style` 下，不要写顶层 `precision`。
- `datetime` 是手动日期字段；系统时间请改用 `created_at` / `updated_at`。
- `formula` / `lookup` 没读 guide 前不要直接写。
