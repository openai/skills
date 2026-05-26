
# base +data-query

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

对多维表格数据进行聚合查询（分组、过滤、排序、聚合计算），基于以下语法的 JSON DSL：

查询类任务还必须先遵守 [`lark-base-data-analysis-sop.md`](lark-base-data-analysis-sop.md)。`+data-query` 适合让筛选、分组、聚合、排序和 TopN 在 Base 云端查询服务中执行；不要用默认分页的 `+record-list` 或本地 `jq` 替代聚合查询。

## 限制

- **权限要求**（按文档类型分流）：
  - **普通多维表格**：调用者拥有文档的**阅读权限**即可
  - **高级权限多维表格**：调用者必须是文档管理员，拥有 **FA（Full Access / 完全访问权限）**

  权限不足时返回权限错误。

## 推荐命令

```bash
# 按字段分组计数
lark-cli base +data-query \
  --base-token MAGObxxxxx \
  --dsl '{
    "datasource": {"type": "table", "table": {"tableId": "tblxxxxxxxx"}},
    "dimensions": [{"field_name": "城市", "alias": "dim_city"}],
    "measures": [{"field_name": "城市", "aggregation": "count", "alias": "count"}],
    "shaper": {"format": "flat"}
  }'

# 带过滤条件 + 排序 + 限制条数
lark-cli base +data-query \
  --base-token MAGObxxxxx \
  --dsl '{
    "datasource": {"type": "table", "table": {"tableId": "tblxxxxxxxx"}},
    "dimensions": [{"field_name": "城市", "alias": "dim_city"}],
    "measures": [{"field_name": "金额", "aggregation": "sum", "alias": "total_amount"}],
    "filters": {
      "type": 1,
      "conjunction": "and",
      "conditions": [{"field_name": "城市", "operator": "isNot", "value": [""]}]
    },
    "sort": [{"field_name": "total_amount", "order": "desc"}],
    "pagination": {"limit": 100},
    "shaper": {"format": "flat"}
  }'

# 使用 tableName（表名）代替 tableId
lark-cli base +data-query \
  --base-token MAGObxxxxx \
  --dsl '{
    "datasource": {"type": "table", "table": {"tableName": "销售数据"}},
    "measures": [{"field_name": "金额", "aggregation": "sum", "alias": "total"}],
    "shaper": {"format": "flat"}
  }'

# 聚合后如需读取明细，先让 data-query 返回可回查的业务 key
lark-cli base +data-query \
  --base-token MAGObxxxxx \
  --dsl '{
    "datasource": {"type": "table", "table": {"tableId": "tblxxxxxxxx"}},
    "dimensions": [{"field_name": "业务编号", "alias": "biz_key"}],
    "measures": [{"field_name": "指标值", "aggregation": "max", "alias": "max_value"}],
    "filters": {
      "type": 1,
      "conjunction": "and",
      "conditions": [{"field_name": "状态", "operator": "is", "value": ["有效"]}]
    },
    "sort": [{"field_name": "max_value", "order": "desc"}],
    "pagination": {"limit": 10},
    "shaper": {"format": "flat"}
  }'
```

## 参数

| 参数                     | 必填 | 说明 |
|------------------------|------|------|
| `--base-token <token>` | 是 | Base Token（base_token） |
| `--dsl <json>`         | 是 | LiteQuery Protocol JSON DSL 查询语句 |

## 如何从链接中提取参数

用户通常会提供如下 URL：

```
https://example.feishu.cn/base/<base_token>?table=<table_id>
```

- `--base-token`：取 `/base/` 后面的字符串
- DSL 中的 `tableId`：取 `table=` 后面的值

## API 入参详情

**HTTP 方法和路径：**

```
POST /open-apis/base/v3/bases/:base_token/data/query
```

**Path 参数：**

| 参数 | 必填 | 说明 |
|------|------|------|
| `base_token` | 是 | Base Token |

**Request Body — DSL 结构：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `datasource` | object | 是 | 数据源，包含 `type`（固定 `"table"`）和 `table` 对象 |
| `datasource.table.tableId` | string | 二选一 | 目标数据表 ID |
| `datasource.table.tableName` | string | 二选一 | 目标数据表名称 |
| `dimensions` | Dimension[] | 否* | 分组维度字段（GROUP BY） |
| `measures` | Measure[] | 否* | 聚合度量字段 |
| `filters` | FilterGroup | 否 | 过滤条件（WHERE） |
| `sort` | Sort[] | 否 | 排序规则 |
| `pagination` | object | 否 | 限制返回行数，`{limit: N}`，最大 5000 |
| `shaper` | object | 否 | 结果格式，固定 `{format: "flat"}` |

> \* `dimensions` 和 `measures` 至少填写一个。

**Dimension 字段：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `field_name` | string | 是 | 字段名称 |
| `alias` | string | 否 | 输出列别名，需全局唯一 |

**Measure 字段：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `field_name` | string | 是 | 字段名称 |
| `aggregation` | string | 是 | 聚合函数：`sum`、`avg`、`min`、`max`、`count`、`count_all`、`distinct_count` |
| `alias` | string | 否 | 输出列别名，需全局唯一 |

**聚合函数适用字段类型：**

| 聚合函数 | 适用字段类型 |
|----------|-------------|
| `sum` / `avg` | `number` |
| `min` / `max` | `number`、`datetime` |
| `count` | 全字段适用，计数非空值 |
| `count_all` | 全字段适用，计数所有行 |
| `distinct_count` | 全字段适用 |

> `number` 包含 `style.type` 为 `progress` / `currency` / `rating` 等所有子类型。

**FilterGroup：**

```json
{
  "filters": {
    "type": 1,
    "conjunction": "and",
    "conditions": [
      {"field_name": "城市", "operator": "is", "value": ["北京"]}
    ]
  }
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `type` | int | 是 | 固定填 `1` |
| `conjunction` | string | 否 | 条件组合逻辑：`"and"` 或 `"or"`，默认 `"and"` |
| `conditions` | Condition[] | 否 | 条件列表 |

**Condition：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `field_name` | string | 是 | 字段名称（必须与表中字段名精确匹配） |
| `operator` | string | 是 | 运算符（见下方运算符表） |
| `value` | string[] | 是 | 条件值数组；`isEmpty`/`isNotEmpty` 时**必须**传空数组 `[]` |

**运算符：**

| 运算符 | 说明 |
|--------|------|
| `is` | 等于 |
| `isNot` | 不等于 |
| `contains` | 包含 |
| `doesNotContain` | 不包含 |
| `isEmpty` | 为空 |
| `isNotEmpty` | 不为空 |
| `isGreater` | 大于 |
| `isGreaterEqual` | 大于等于 |
| `isLess` | 小于 |
| `isLessEqual` | 小于等于 |

> 各运算符的适用字段类型见下方「按各字段类型筛选时 value 格式详解」。

**按各字段类型筛选时 value 格式详解：**

*`text`*

| 运算符 | value 格式 | 元素个数 | 示例 |
|--------|-----------|---------|------|
| `is` / `isNot` / `contains` / `doesNotContain` | `["文本内容"]` | 仅 1 个 | `["Hello"]` |
| `isEmpty` / `isNotEmpty` | `[]` | 0 个 | `[]` |

> **不支持** `isGreater` / `isGreaterEqual` / `isLess` / `isLessEqual`：文本无自然顺序，比较运算无意义。
> `text` 也覆盖电话、超链接、邮箱、条码字段；通过 `style.type` 区分（`plain`（默认）/ `phone` / `url` / `email` / `barcode`），运算符集合一致。
> 当 `style.type=url` 时，value 筛选的是链接显示名称，而不是 URL 本身。

*`number`*

| 运算符 | value 格式 | 元素个数 | 示例 |
|--------|-----------|---------|------|
| `is` / `isNot` / `isGreater` / `isGreaterEqual` / `isLess` / `isLessEqual` | `["数字字符串"]` | 仅 1 个 | `["23.4"]`、`["-100"]` |
| `isEmpty` / `isNotEmpty` | `[]` | 0 个 | `[]` |

> value 必须为合法数字的字符串形式。
> `number` 也覆盖货币、进度、评分字段；通过 `style.type` 区分（`plain`（默认）/ `currency` / `progress` / `rating`），运算符集合一致，仅 value 解释不同：
> - 当 `style.type=progress` 时，34% 对应 0.34 而不是 34。
> - 当 `style.type=rating` 时，必须输入整数，代表评分。

*`auto_number`*

| 运算符 | value 格式 | 元素个数 | 示例 |
|--------|-----------|---------|------|
| `is` / `isNot` / `contains` / `doesNotContain` | `["编号字符串"]` | 仅 1 个 | `["00001"]` |
| `isGreater` / `isGreaterEqual` / `isLess` / `isLessEqual` | `["编号字符串"]` | 仅 1 个 | `["00010"]` |
| `isEmpty` / `isNotEmpty` | `[]` | 0 个 | `[]` |

*`select`*

| 运算符 | value 格式 | 元素个数 | 示例 |
|--------|-----------|---------|------|
| `is` / `isNot` | `["选项名"]` | **仅 1 个** | `["选项A"]` |
| `contains` / `doesNotContain` | `["选项A", "选项B"]` | 可多个 | `["选项A", "选项B"]` |
| `isEmpty` / `isNotEmpty` | `[]` | 0 个 | `[]` |

> **不支持** `isGreater` / `isGreaterEqual` / `isLess` / `isLessEqual`：选项为枚举值，无自然顺序。
> 通过 `multiple` 区分单选（`multiple=false`，默认）/ 多选（`multiple=true`）。

*`user` / `created_by` / `updated_by`*

| 运算符 | value 格式 | 元素个数 | 示例                     |
|--------|-----------|---------|------------------------|
| `is` / `isNot` | `["用户ID1", "用户ID2"]` | **可多个** | `["ou_aaa", "ou_bbb"]` |
| `contains` / `doesNotContain` | `["用户ID1", "用户ID2"]` | 可多个 | `["ou_aaa", "ou_bbb"]` |
| `isEmpty` / `isNotEmpty` | `[]` | 0 个 | `[]`                   |

> **不支持** `isGreater` / `isGreaterEqual` / `isLess` / `isLessEqual`：人员无法比大小。
> 用户 ID 使用 `open_id`（`ou_` 前缀），接口层会自动做 ID 转换。

*`group_chat`*

| 运算符 | value 格式 | 元素个数 | 示例 |
|--------|-----------|---------|------|
| `is` / `isNot` | `["群组ID1", "群组ID2"]` | 可多个 | `["oc_aaa", "oc_bbb"]` |
| `contains` / `doesNotContain` | `["群组ID1", "群组ID2"]` | 可多个 | `["oc_aaa", "oc_bbb"]` |
| `isEmpty` / `isNotEmpty` | `[]` | 0 个 | `[]` |

> **不支持** `isGreater` / `isGreaterEqual` / `isLess` / `isLessEqual`：群组无法比大小。

*`link`*

| 运算符 | value 格式 | 元素个数 | 示例 |
|--------|-----------|---------|------|
| `is` / `isNot` | `["recId1", "recId2"]` | 可多个 | `["recAAA", "recBBB"]` |
| `contains` / `doesNotContain` | `["recId1", "recId2"]` | 可多个 | `["recAAA", "recBBB"]` |
| `isEmpty` / `isNotEmpty` | `[]` | 0 个 | `[]` |

> **不支持** `isGreater` / `isGreaterEqual` / `isLess` / `isLessEqual`：关联记录无法比大小。
> value 传关联表记录的 `record_id`。
> 双向关联（创建时设 `bidirectional=true`）也属于 `link` 类型，运算符与单向关联一致。

*`location`*

| 运算符 | value 格式 | 元素个数 | 示例 |
|--------|-----------|---------|------|
| `is` / `isNot` / `contains` / `doesNotContain` | `["地址文本"]` | 仅 1 个 | `["北京市朝阳区..."]` |
| `isEmpty` / `isNotEmpty` | `[]` | 0 个 | `[]` |

> **不支持** `isGreater` / `isGreaterEqual` / `isLess` / `isLessEqual`：地理位置无自然顺序。

*`checkbox`*

| 运算符 | value 格式 | 元素个数 | 示例 |
|--------|-----------|---------|------|
| `is` | `["true"]` 或 `["false"]` | 仅 1 个 | `["true"]` |

> 仅支持 `is` 运算符，不支持其他运算符。

*`datetime` / `created_at` / `updated_at`*

日期字段仅支持 `is`、`isEmpty`、`isNotEmpty`、`isGreater`、`isLess` 五种运算符。

value 使用预定义关键字机制，第一个元素为字符串常量名称：

| 关键字 | 说明 | value 格式 | 支持的运算符 |
|--------|------|-----------|-------------|
| `ExactDate` | 精确日期 | `["ExactDate", "1773187200000"]`（毫秒时间戳） | `is`、`isGreater`、`isLess` |
| `Today` | 今天 | `["Today"]` | `is`、`isGreater`、`isLess` |
| `Tomorrow` | 明天 | `["Tomorrow"]` | `is`、`isGreater`、`isLess` |
| `Yesterday` | 昨天 | `["Yesterday"]` | `is`、`isGreater`、`isLess` |
| `CurrentWeek` | 本周 | `["CurrentWeek"]` | 仅 `is` |
| `LastWeek` | 上周 | `["LastWeek"]` | 仅 `is` |
| `CurrentMonth` | 本月 | `["CurrentMonth"]` | 仅 `is` |
| `LastMonth` | 上月 | `["LastMonth"]` | 仅 `is` |
| `TheLastWeek` | 过去七天 | `["TheLastWeek"]` | 仅 `is` |
| `TheNextWeek` | 未来七天 | `["TheNextWeek"]` | 仅 `is` |
| `TheLastMonth` | 过去三十天 | `["TheLastMonth"]` | 仅 `is` |
| `TheNextMonth` | 未来三十天 | `["TheNextMonth"]` | 仅 `is` |

> - **ExactDate 时区行为**：毫秒时间戳在实际筛选时会被转为**文档时区当天零点**，跨时区场景需注意日期可能偏移一天。
> - **范围型关键字**（`CurrentWeek`、`LastWeek`、`CurrentMonth`、`LastMonth`、`TheLastWeek`、`TheNextWeek`、`TheLastMonth`、`TheNextMonth`）仅支持 `is` 运算符。
> - **关键字大小写敏感**：`ExactDate`、`Today`、`CurrentWeek` 等首字母大写，写错大小写会导致校验失败。

*`attachment`*

| 运算符 | value 格式 | 元素个数 | 示例 |
|--------|-----------|---------|------|
| `isEmpty` / `isNotEmpty` | `[]` | 0 个 | `[]` |

> 附件字段仅支持 `isEmpty` 和 `isNotEmpty`，不支持其他运算符。

*`formula` / `lookup`*

公式和查找引用字段的运算符和 value 格式 **取决于其结果数据类型**，按结果类型参照上方对应字段类型的规则。例如：

- 公式结果为数字 → 按 `number` 规则
- 公式结果为日期 → 按 `datetime` 规则
- 公式结果为单选 → 按 `select` 规则

**Sort 字段：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `field_name` | string | 是 | 字段名称或 alias |
| `order` | string | 否 | `"asc"`（默认）或 `"desc"` |

**Pagination 字段：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `limit` | int | 否 | 返回记录数上限，必须为正整数，最大 5000；不填时使用系统默认值。不支持 offset |

**Shaper 字段：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `format` | string | 是 | 固定为 `"flat"`，表示返回扁平化的对象数组 |

## API 出参详情

**成功时：**

```json
{"code": 0, "data": {"main_data": [{"dim_city": {"value": "北京"}, "total_amount": {"value": 12345.00}}, ...]}, "msg": ""}
```

**失败时：**

```json
{"code": 800004006, "data": {"error": {"code": 800004006, ...}}, "msg": "DSL validation failed"}
```

**Response 字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `code` | int | 状态码，0 为成功 |
| `msg` | string | 错误信息 |
| `data.main_data` | []object | 查询结果数组，每个元素为一行数据 |
| `data.error` | object | 失败时的错误详情 |

每行数据的字段值封装在 CellValue 中：

```json
{
  "dim_city": {
    "value": "北京"
  },
  "total_amount": {
    "value": 12345.00
  }
}
```

- `value`：展示值（人员名称、选项名称、格式化日期等）

## 返回值

命令成功后输出 `data` 字段的内容：

```json
{
  "main_data": [
    {
      "dim_city": {"value": "直营"},
      "measure_count": {"value": 1}
    },
    {
      "dim_city": {"value": "加盟"},
      "measure_count": {"value": 2}
    }
  ]
}
```

## 工作流

1. 确认 base-token 和 table-id
2. **先查表结构**：执行 `lark-cli base +field-list --base-token <base_token> --table-id <table_id>`
3. 从返回的字段列表中获取 field_name（DSL 中使用的字段名称）
4. 根据字段信息构造 DSL JSON
5. 执行 +data-query
6. 解读返回结果：
   - 结果在 `data.main_data` 数组中，每个元素代表一行
   - 每行对象的 key 为 DSL 中指定的 `alias`；未指定 alias 时，key 为自动生成的列名
   - 每个 value 是 CellValue 对象，实际值在 `value` 字段中，如 `{"value": "北京"}` 或 `{"value": 12345.00}`
   - 失败时结果在 `data.error` 中，包含具体错误码和信息

## 与记录读取组合

`+data-query` 不返回原始记录或 link 字段明细。需要输出聚合结果对应的原始记录字段、展示值或关联表字段时，按以下方式组合：

1. 用 `+data-query` 在 Base 云端查询服务中完成全局筛选、分组、聚合、排序和 TopN，得到业务 key、分组值或候选范围。
2. 如果已经拿到候选记录的 `record_id`，用 `+record-get` 读取明细字段。
3. 如果拿到的是结构化业务 key（例如编号、状态、日期、金额等），优先创建临时视图做精确过滤后再 `+record-list --view-id` 读取；不要用 `+record-search` 代替结构化条件。
4. 只有候选条件本身是文本展示值关键词时，才使用 `+record-search`，并用 `search_fields` 限定范围、`select_fields` 做投影。
5. 若候选记录包含 link 字段，提取关联 `record_id` 后到关联表用 `+record-get` 批量读取展示字段。
6. 最终回答业务字段，不要把内部 `record_id` 当作用户可读答案。

不要把 `data-query pagination.limit` 理解为分页扫描；它只限制 Base 云端查询服务返回的聚合结果行数，不支持 offset。需要全量明细导出时回到 data analysis SOP 的 record 分页规则。

## 坑点

- ⚠️ **必须先查表结构**：DSL 的 `field_name` 必须与表中字段名称精确匹配（区分大小写），不能凭猜测构造。先用 `lark-cli base +field-list --base-token <base_token> --table-id <table_id>` 获取真实字段名
- ⚠️ **权限要求按文档类型分流**：普通多维表格只需文档**阅读权限**；高级权限多维表格必须是文档管理员（**FA / Full Access**），否则返回权限错误
- ⚠️ **alias 不支持中文**：dimensions 和 measures 的 alias 必须使用英文（如 `dim_city`、`total_amount`），中文 alias 会导致错误
- ⚠️ **API 路径是 `base/v3`**：本接口路径为 `/open-apis/base/v3/bases/:base_token/data/query`，不是 `bitable/v1`。两者完全不同，用错版本号会返回 `[2200] Internal Error`
- ⚠️ **`dimensions` 和 `measures` 至少填一个**：两个都不填会返回 DSL 校验错误
- ⚠️ **`shaper` 必须为 `{"format": "flat"}`**：不填或填其他值会导致结果格式不可预期，建议始终显式指定
- ⚠️ **数据表标识 `tableId` vs `tableName`**：datasource 中可以用 `tableId`（如 `tblXXX`）或 `tableName`（数据表的用户自定义显示名称），二选一，不要混用
- ⚠️ **`pagination.limit` 最大 5000**：超过会报错，且不支持 offset，只支持 limit
- ⚠️ **所有 alias 必须全局唯一**：dimensions 和 measures 之间的 alias 也不能重名
- ⚠️ **不要用本地分页结果替代 data-query**：凡是全局计数、分组、聚合、排序 TopN，优先让 `+data-query` 在 Base 云端查询服务中执行；默认页 `+record-list` 后本地统计只能得到已读取范围内的结果

## 参考

- [lark-base](../SKILL.md) — 多维表格全部命令
- [lark-shared](../../lark-shared/SKILL.md) — 认证和全局参数
- [lark-base-data-analysis-sop.md](lark-base-data-analysis-sop.md) — 查询范围、选路、下推、分页、record 明细回查和关系查询 SOP
- [lark-base-cell-value.md](lark-base-cell-value.md) — CellValue 格式规范
- [lark-base-shortcut-field-properties.md](lark-base-shortcut-field-properties.md) — shortcut 字段类型与 JSON 结构
