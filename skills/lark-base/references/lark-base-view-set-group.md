# base +view-set-group

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

更新视图分组配置。

## 1. 顶层规则

- `--json` 必须是 JSON 对象。
- 顶层写法固定为 `{"group_config":[...]}`。
- 每项写 `{ "field": "<field_id_or_name>", "desc": false }`。
- `desc` 可省略；省略时等价于 `false`。
- 仅 `grid` / `kanban` / `gantt` 视图支持。
- `group_config` 传空数组 `[]` 表示清空分组。
- 分组字段必须是当前视图可分组的字段；字段存在也不代表一定可分组。

## 2. 推荐命令

设置分组：

```bash
lark-cli base +view-set-group \
  --base-token <base_token> \
  --table-id <table_id> \
  --view-id <view_id> \
  --json '{"group_config":[{"field":"fld_status","desc":false}]}'
```

清空分组：

```bash
lark-cli base +view-set-group \
  --base-token <base_token> \
  --table-id <table_id> \
  --view-id <view_id> \
  --json '{"group_config":[]}'
```

## 3. JSON 写法

```json
{
  "group_config": [
    { "field": "fld_status", "desc": false }
  ]
}
```

## 4. 使用建议

- 优先传字段 id，不要依赖字段名。
- 建议先用 [lark-base-view-get-group.md](lark-base-view-get-group.md) 读取现状。
- 只传对象；不要传 `[]` 或 `[{"field":"..."}]` 这类裸数组。
- 提交项数不要超过 3；如果当前视图实际允许更少，以错误提示为准收敛。

## 5. 易错点

- 不要把 `group_config` 写成对象。
- 不要拿当前视图不支持分组的字段去分组。
- 不要在 `gallery` / `calendar` 视图上调用。

## 6. 参考

- [lark-base-view.md](lark-base-view.md)
- [lark-base-view-get-group.md](lark-base-view-get-group.md)
