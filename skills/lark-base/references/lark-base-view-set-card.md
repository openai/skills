# base +view-set-card

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

更新卡片封面配置。

## 1. 顶层规则

- `--json` 必须是 JSON 对象。
- 仅 `gallery` / `kanban` 视图支持。
- `cover_field` 必填；可传 `attachment` 类型的字段 id、字段名，或 `null`。

## 2. 推荐命令

设置封面：

```bash
lark-cli base +view-set-card \
  --base-token <base_token> \
  --table-id <table_id> \
  --view-id <view_id> \
  --json '{"cover_field":"fld_cover"}'
```


## 3. JSON 写法

```json
{
  "cover_field": "fld_cover"
}
```

```json
{
  "cover_field": null
}
```

## 4. 使用建议

- 建议先用 [lark-base-view-get-card.md](lark-base-view-get-card.md) 读取现状，再改。
- 优先传字段 id，不要依赖字段名。
- 普通文本、数字、选择字段不能作为封面字段。

## 5. 易错点

- 不要传空字符串；清空时传 `null`。
- 不要在 `grid` / `calendar` / `gantt` 视图上调用。
- 不要假设任意字段都能做封面；稳定做法是先找 `attachment` 字段。

## 6. 参考

- [lark-base-view.md](lark-base-view.md)
- [lark-base-view-get-card.md](lark-base-view-get-card.md)
