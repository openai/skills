# base +view-set-timebar

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

更新时间轴配置。

## 1. 顶层规则

- `--json` 必须是 JSON 对象。
- 顶层固定写 `start_time`、`end_time`、`title` 三个字段，三者都必填。
- `start_time` / `end_time` 必须是当前时间轴支持的日期字段。
- `title` 必须是当前表中已存在的字段。
- 仅 `calendar` / `gantt` 视图支持。

## 2. 推荐命令

```bash
lark-cli base +view-set-timebar \
  --base-token <base_token> \
  --table-id <table_id> \
  --view-id <view_id> \
  --json '{"start_time":"fld_start","end_time":"fld_end","title":"fld_title"}'
```

## 3. JSON 写法

```json
{
  "start_time": "fld_start",
  "end_time": "fld_end",
  "title": "fld_title"
}
```

## 4. 使用建议

- 优先传字段 id，不要依赖字段名。
- `start_time` / `end_time` 稳定做法优先使用日期时间字段。
- `title` 通常传主字段或文本标题字段。
- 建议先用 [lark-base-view-get-timebar.md](lark-base-view-get-timebar.md) 读取现状。

## 5. 易错点

- 不要把普通文本、选项、链接字段写到 `start_time` / `end_time`。
- 不要漏传 `title`。
- 不要在 `grid` / `gallery` / `kanban` 视图上调用。

## 6. 参考

- [lark-base-view.md](lark-base-view.md)
- [lark-base-view-get-timebar.md](lark-base-view-get-timebar.md)
