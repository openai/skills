# base +view-create

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

创建一个视图。

## 1. 顶层规则

- --json 结构是 `{name, type?}`。
- `name` 必填；同表内应唯一。
- `type` 可省略；省略时默认 `grid`。
- 视图类型取值范围：`grid`、`kanban`、`gallery`、`calendar`、`gantt`。
- `+view-create` 不负责排序、分组、筛选、时间轴、卡片封面、可见字段顺序；这些配置需要创建后再调用对应命令。
- 表单视图不走 `+view-create`；使用表单相关命令。

## 2. 推荐命令

```bash
lark-cli base +view-create \
  --base-token <base_token> \
  --table-id <table_id> \
  --json '{"name":"进行中","type":"grid"}'
```

## 3. JSON 写法

```json
{ "name": "进行中", "type": "grid" }
```

最小写法：

```json
{ "name": "默认视图" }
```

## 4. 使用建议

- 需要设置可见字段顺序时，创建后继续调用 [lark-base-view-set-visible-fields.md](lark-base-view-set-visible-fields.md)。
- 需要设置筛选、分组、排序、时间轴、卡片封面时，创建后继续调用对应 `+view-set-*` 命令。

## 5. 易错点

- 不要把 `form` 当成 `type` 传进来。
- 不要指望 `+view-create` 一次完成视图布局与属性配置。

## 6. 参考

- [lark-base-view.md](lark-base-view.md)
- [lark-base-view-set-visible-fields.md](lark-base-view-set-visible-fields.md)
