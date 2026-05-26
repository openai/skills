# base +view-set-visible-fields

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

更新视图可见字段列表（同时控制视图中的字段顺序）。

## 1. 顶层规则

- `--json` 必须是 JSON 对象。
- 顶层固定写法：`{"visible_fields":[...]}`
- `visible_fields` 每项可传字段 id 或字段名。
- 仅 `grid` / `kanban` / `gallery` / `calendar` / `gantt` 视图支持。

## 2. 推荐命令

```bash
lark-cli base +view-set-visible-fields \
  --base-token <base_token> \
  --table-id <table_id> \
  --view-id <view_id> \
  --json '{"visible_fields":["标题","fld_status"]}'
```

## 3. JSON 写法

```json
{
  "visible_fields": ["标题", "fld_status"]
}
```

## 4. 使用建议

- 优先传字段 id，不要依赖字段名。
- 数组顺序用于控制视图字段顺序。
- 如果未包含主字段 `primaryField`，结果中会自动补到第一位。

## 5. 易错点

- 不要传裸数组：`["fld_a","fld_b"]`；必须包成 `{"visible_fields":[...]}`
- 如果传字段名，必须与当前表真实字段名精确匹配。
- 最终返回顺序可能与传入顺序不同，因为主字段会被强制置顶。

## 参考

- [lark-base-view.md](lark-base-view.md) — view 索引页
