# base +view-set-sort

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

更新视图排序配置。

## 1. 顶层规则

- `--json` 必须是 JSON 对象。
- 顶层写法固定为 `{"sort_config":[...]}`。
- `sort_config` 最多 10 项。
- 每项写 `{ "field": "<field_id_or_name>", "desc": false }`。
- `desc` 可省略；省略时等价于 `false`。
- 仅 `grid` / `kanban` / `gallery` / `gantt` 视图支持。

## 2. 推荐命令

设置排序：

```bash
lark-cli base +view-set-sort \
  --base-token <base_token> \
  --table-id <table_id> \
  --view-id <view_id> \
  --json '{"sort_config":[{"field":"fld_priority","desc":true},{"field":"fld_created_at","desc":false}]}'
```

清空排序：

```bash
lark-cli base +view-set-sort \
  --base-token <base_token> \
  --table-id <table_id> \
  --view-id <view_id> \
  --json '{"sort_config":[]}'
```

## 3. JSON 写法

```json
{
  "sort_config": [
    { "field": "fld_priority", "desc": true }
  ]
}
```

## 4. 使用建议

- 优先传字段 id，不要依赖字段名。
- 如需覆盖已有排序，建议先用 [lark-base-view-get-sort.md](lark-base-view-get-sort.md) 读取现状。
- 只传对象；不要传 `[]` 或 `[{"field":"..."}]` 这类裸数组。

## 5. 易错点

- 不要把 `sort_config` 写成对象。
- 不要超过 10 项。
- 不要在 `calendar` 这类不支持排序配置的视图上调用。

## 6. 参考

- [lark-base-view.md](lark-base-view.md)
- [lark-base-view-get-sort.md](lark-base-view-get-sort.md)
