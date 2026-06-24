# base +view-set-filter

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

更新视图筛选配置。

## 1. 顶层规则

- `--json` 必须是 JSON 对象。
- 顶层结构是 `{logic?, conditions?}`。
- `logic` 默认 `and`；推荐只用 canonical 值 `and` / `or`。
- `conditions` 默认空数组。
- 每条条件写成 tuple：`[field, operator, value?]`。
- `empty` / `non_empty` 可写成 2 项：`[field, "empty"]`、`[field, "non_empty"]`。
- 支持 `filter` 的视图类型：`grid`、`kanban`、`gallery`、`calendar`、`gantt`。

## 2. operator

可用 operator：
- `==`
- `!=`
- `>`
- `>=`
- `<`
- `<=`
- `intersects`
- `disjoint`
- `empty`
- `non_empty`

## 3. value 写法

### `text` / `location`

用字符串：

```json
["标题", "intersects", "发布"]
```

### `number` / `auto_number`

用数字：

```json
["工时", ">=", 3.5]
```

### `select`

用选项名数组：

```json
["状态", "intersects", ["Doing", "Blocked"]]
```

### `user` / `created_by` / `updated_by`

用对象数组：

> **人员筛选：不要猜 ID。** 不知道 `open_id` 时，先用 `lark-contact` 查 id：`lark-cli contact +search-user --query "<姓名/邮箱/手机号>" --as user`。

```json
["负责人", "intersects", [{ "id": "ou_xxx" }]]
```

### `group_chat`

用对象数组：

> **群组筛选：不要猜 ID。** 不知道 `chat_id` 时，先用 `lark-im` 搜群：`lark-cli im +chat-search --query "<群名关键词>" --as user`；取结果里的 `oc_xxx`。

```json
["负责群", "intersects", [{ "id": "oc_xxx" }]]
```

### `link`

用记录 id 对象数组：

```json
["关联任务", "intersects", [{ "id": "rec_xxx" }]]
```

### `checkbox`

用布尔值：

```json
["完成", "==", true]
```

### `datetime` / `created_at` / `updated_at`

用相对时间关键字或 `ExactDate(...)`：

```json
["截止时间", "==", "ExactDate(2026-01-01)"]
```

```json
["截止时间", "==", "ExactDate(2026-01-01 11:30)"]
```

```json
["截止时间", "==", "Today"]
```

可用关键字：
- `Today`
- `Yesterday`
- `Tomorrow`

### `formula` / `lookup`

- 筛选值类型由字段计算结果类型动态决定。
- 拿不准时，先把 `value` 当作单个字符串填入做一次尝试。
- 如果报错，再按错误提示把 `value` 改成对应类型。

字符串示例：

```json
["风险说明", "intersects", "高风险"]
```

数字示例：

```json
["汇总分", ">=", 80]
```

## 4. 推荐命令

```bash
lark-cli base +view-set-filter \
  --base-token <base_token> \
  --table-id <table_id> \
  --view-id <view_id> \
  --json '{"logic":"and","conditions":[["状态","intersects",["Doing"]],["负责人","intersects",[{"id":"ou_xxx"}]],["截止时间","empty"]]}'
```

## 5. JSON 写法

```json
{
  "logic": "and",
  "conditions": [
    ["状态", "intersects", ["Doing"]],
    ["负责人", "intersects", [{ "id": "ou_xxx" }]],
    ["截止时间", "empty"]
  ]
}
```

清空写法：

```json
{
  "conditions": []
}
```

## 6. 使用建议

- 建议先用 [lark-base-view-get-filter.md](lark-base-view-get-filter.md) 读取现状，再改。
- 优先传字段 id，不要依赖字段名。
- 需要清空全部筛选时，直接传 `{"conditions":[]}`。

## 7. 易错点

- 不要再写旧对象风格：`{"field_name":...,"operator":...}`。
- `user` / `group_chat` / `link` 不要写成单个标量。
- `empty` / `non_empty` 不要硬塞无意义的 value。
- 日期条件稳定写法用 `ExactDate(...)` 或 `Today` / `Yesterday` / `Tomorrow`。
- `formula` / `lookup` 的 value 形状不固定；拿不准时先读当前 filter 或字段定义，或根据错误提示修正类型。

## 8. 参考

- [lark-base-view.md](lark-base-view.md)
- [lark-base-view-get-filter.md](lark-base-view-get-filter.md)
- [lookup-field-guide.md](lookup-field-guide.md)
