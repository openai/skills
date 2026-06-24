# Base data analysis SOP

Base 数据查询与分析任务的执行契约。覆盖记录读取、筛选、排序、Top/Bottom N、聚合统计、分组聚合、多表关联、临时分析和查询后写入前的目标定位。

具体命令参数不要在本文猜；需要时跳到对应 reference：

- `+data-query`: [lark-base-data-query.md](lark-base-data-query.md)
- 视图筛选/排序/投影: [lark-base-view-set-filter.md](lark-base-view-set-filter.md), [lark-base-view-set-sort.md](lark-base-view-set-sort.md), [lark-base-view-set-visible-fields.md](lark-base-view-set-visible-fields.md)
- 记录读取: [lark-base-record.md](lark-base-record.md)

## 0. Hard Rules

- 全局问题不能用默认 `+record-list --limit N` 片面地回答。
- `jq` / shell / 本地代码是在个人电脑或当前运行环境中处理已返回数据，只适合小范围结果；超过 200 行默认不推荐本地统计、排序或求极值，应改用 Base 云端查询服务的 filter/sort/aggregate。
- “最高、最低、最新、最早、Top、Bottom、总数、全部、异常、最大、最小、最多、最少、优先级最高”等全局语义，必须在 Base 云端查询服务中完成筛选、排序或聚合。
- `+record-search` 用于关键词检索字段的展示文本；可搜多类字段，但匹配的是文本表示（如人员命中 name），不要用它替代金额、状态、日期、空值等结构化条件。
- 不要依赖已有视图，除非用户明确指定该视图，或你已读取并验证其 filter/sort/projection 符合当前问题。
- 交付输出必须使用用户可读的真实字段值；内部 ID、`record_id`、关联记录 ID、open_id、编码字段只可作为连接键或定位键，不能替代最终输出，除非用户明确要求输出这些键值。
- 每次读取必须做最小投影，并包含后续解释、回查或写入需要的业务 key。

## 1. Intent -> Tool Path

| 用户意图 | 首选路径 | 关键规则 |
| --- | --- | --- |
| 看几条、预览、示例 | `+record-list --limit N` | 保持局部语义；不要推广为全局结论 |
| 已知 `record_id` | `+record-get` | 直接读取；不要 search/list 反查 |
| 明确关键词 | `+record-search` | 按字段展示文本命中；使用 `search_fields` 限定匹配范围、`select_fields` 投影降低返回内容 token 量；不要把文本检索当作结构化关联解析 |
| 按条件找明细记录 | 先创建临时视图设置筛选和可见字段，再用 `+record-list --view-id` 读取 | 条件字段来自 `+field-list`；不要先读全表再本地过滤 |
| 排序 / TopN 原始记录 | 临时视图 filter/sort/projection -> `+record-list --view-id --limit N` | 最高/最新降序，最低/最早升序 |
| 聚合 / 分组 / 分组排序 | `+data-query` | 使用 filters/dimensions/measures/sort/limit |
| 聚合后输出实体字段 | `+data-query` 得到业务 key -> record 路径回查明细 | `+data-query` 不返回原始记录或 link 明细；聚合结果中的 key 需要再解析成用户要求字段 |
| 多表 / 多跳关联 | 以候选数最小的事实表为驱动表，沿业务 key 或 link `record_id` 逐跳回查 | 读出 link 单元格里的关联 `record_id` 后，到被关联表批量 `+record-get` 展示字段，并在回答用结果中合并展示 |
| 查询后写入 / 视图化 | 先用本 SOP 得到可复核的目标记录 id 集合 | 再进入记录写入或视图配置；高价值可复用查询优先沉淀为持久视图 |

## 2. Execution Patterns

### 2.1 结构化明细与 TopN

使用视图路径：

1. `+field-list` 确认筛选字段、排序字段、展示字段、业务 key。
2. `+view-create` 创建 grid 视图。
3. 设置 filter/sort/visible fields。
4. `+record-list --view-id <view_id> --limit <N>` 读取结果。

不要从未筛选、未排序的全表输出中手动挑选。一次性查询可用临时视图；如果这个筛选/排序结果对用户后续查看有价值，应保留为持久视图，不要删除，并告知用户视图名称和用途。视图参数细节见 view-set references。

### 2.2 聚合分析与 TopN

使用 `+data-query`：

- 让 Base 云端查询服务完成 filters、dimensions、measures、sort、pagination.limit。
- `pagination.limit` 是 Base 云端查询服务中的聚合结果限制，不是本地分页扫描。
- 需要输出明细或用户可读字段时，先拿业务 key，再用 record 路径精确回查。
- 字段类型、日期 value、DSL shape 以 [lark-base-data-query.md](lark-base-data-query.md) 为准。

### 2.3 关系查询与回查

- link 单元格通常是关联表 `record_id` 数组，不是用户可读内容，只是连接键。
- 先用 `+field-list` 确认 link 字段的 `link_table`、业务唯一键和展示字段。
- 从驱动表拿到候选记录后，用关联 `record_id` 到关联表 `+record-get` 批量读取记录内容。
- 多跳关系逐跳建立 `record_id/key -> 用户可读字段` 映射；最终用户可读的信息。

禁止：

- 把 link `record_id` 当最终输出。
- 用 `+record-search` 搜 link `record_id`。
- 基于 ID、自增编号、link 值做语义猜测；禁止依赖字段先验、样本记忆补全交付输出。

## 3. Range & Pagination Contract

- `+record-list` 默认页、固定 `--limit`、本地 `jq`、shell 管道、手工浏览输出，都只覆盖已读取范围；超过 200 行不要把本地处理当作推荐路径。
- `has_more=true`、存在下一页 offset/page token、或返回行数等于 page size，都表示可能还有未读取数据。
- 对全局问题，只有 Base 云端查询服务已经通过 filter/sort/aggregate 收敛目标范围，或 `data-query` 已在云端完成聚合、排序和限制时，才可以用有限返回形成结论。
- 必须全量导出时，按 CLI 分页语义串行翻页；不要并发调用 `+record-list`。

## 4. Final Answer Check

形成交付输出前必须能确认：

- 问题范围是局部样例、单点定位、全局明细、聚合分析、多表关联，还是查询后写入。
- 筛选、排序、聚合是否发生在 Base 云端查询服务中，而不是本地 `jq` / shell 中。
- 如果使用 `jq` / shell，本地输入是否是 200 行以内的小范围结果；超过 200 行是否已改用 Base 云端查询服务查询。
- 如果使用 `+record-list`，是否处理了 `has_more`，且投影包含业务 key 和解释字段。
- 如果涉及关系查询，是否按 `record_id` 或业务 key 精确回查，交付输出是否来自关联表真实字段。
- 交付输出能追溯到表、字段、筛选条件、排序/聚合条件和连接键。

任一项无法确认时，继续查询或明确说明只能得到局部结论。
