
# drive +search（云空间搜索：扁平 flag，面向自然语言场景）

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

基于 Search v2 接口 `POST /open-apis/search/v2/doc_wiki/search`，以**用户身份**统一搜索云空间对象。

和老的 `docs +search` 相比：

- 把常用过滤条件全部**扁平化为独立 flag**（`--edited-since`、`--mine`、`--doc-types`、`--folder-tokens` 等），不再要求用户或 AI 手写嵌套 `--filter` JSON
- 额外暴露了 4 个"我"维度：`my_edit_time`（我编辑过）、`my_comment_time`（我评论过）、`open_time`（我打开过）、`create_time`（文档创建时间）——直接对应用户自然语言里的"最近我编辑过的"、"我评论过的"等表达
- 自动处理 `my_edit_time` / `my_comment_time` 的小时级聚合（服务端存储粒度）：亚小时输入会向整点 snap，并在 stderr 打出提示
- `--mine` 一键从当前登录用户的 open_id 填 `creator_ids`，不必再先去查 contact

> **资源发现入口统一**：`drive +search` 同样返回 `SHEET` / `Base` / `FOLDER` 等全部云空间对象，不只是文档 / Wiki。用户说"找一个表格"、"找报表"、"最近打开的表格"时，也从这里开始；定位后再切到对应业务 skill（如 `lark-sheets`）做对象内部操作。

## 命令

> **关键约束：搜索关键词必须通过 `--query` 传递。**
> 正确：`lark-cli drive +search --query "方案"`
> 错误：`lark-cli drive +search 方案`
> `+search` 不接受位置参数；空 `--query` 或省略 `--query` 表示纯靠 filter 浏览（合法）。

### 自然语言 → 命令映射速查

| 用户说 | 命令 |
|---|---|
| 最近一个月我编辑过的文档 | `lark-cli drive +search --query "" --edited-since 1m` |
| 最近一个月我编辑过 且 我评论过的 | `lark-cli drive +search --query "" --edited-since 1m --commented-since 1m` |
| 最近一周我打开过的表格 | `lark-cli drive +search --query "" --opened-since 7d --doc-types sheet` |
| 我创建的所有文档 | `lark-cli drive +search --query "" --mine` |
| 我 30-60 天前创建的文档（粗略"上个月"，按 30 天滑窗算） | `lark-cli drive +search --query "" --mine --created-since 2m --created-until 1m` |
| 我 2026 年 3 月创建的文档（精确日历月） | `lark-cli drive +search --query "" --mine --created-since 2026-03-01 --created-until 2026-04-01` |
| 关键词"预算"，最近一周我打开过，按编辑时间降序 | `lark-cli drive +search --query 预算 --opened-since 7d --sort edit_time` |
| 某个 wiki space 下、我 30-60 天前创建的 | `lark-cli drive +search --query "" --mine --space-ids space_xxx --created-since 2m --created-until 1m` |
| 张三创建的文档 | `lark-cli drive +search --query "" --creator-ids ou_zhangsan` |
| 我最近 3 个月评论过的 docx | `lark-cli drive +search --query "" --commented-since 3m --doc-types docx` |

### 更多示例

```bash
# 纯关键词搜索
lark-cli drive +search --query "季度总结"

# 使用服务端 query 高级语法（和 docs +search 一致）
lark-cli drive +search --query 'intitle:方案'
lark-cli drive +search --query '"季度 总结"'
lark-cli drive +search --query '方案 OR 草稿'
lark-cli drive +search --query '方案 -草稿'

# 只搜某个文件夹下的文档
lark-cli drive +search --query 方案 --folder-tokens fld_123456

# 只搜某个知识空间下的 Wiki
lark-cli drive +search --query 研发规范 --space-ids space_1234567890fedcba

# 指定群内分享过的文档
lark-cli drive +search --query 方案 --chat-ids oc_1234567890abcdef

# 只搜标题 / 只搜评论
lark-cli drive +search --query 周报 --only-title
lark-cli drive +search --query 延期原因 --only-comment

# 人类可读格式
lark-cli drive +search --query OKR --format pretty

# 翻页（--format json 先拿 page_token）
lark-cli drive +search --query 方案 --format json
lark-cli drive +search --query 方案 --page-token '<PAGE_TOKEN>'
```

## 参数

### 核心

| 参数 | 必填 | 说明 |
|---|---|---|
| `--query <text>` | 否 | 搜索关键词；支持服务端高级语法（`intitle:`、`""`、`OR`、`-`）。空字符串或省略表示纯 filter 浏览 |
| `--page-size <n>` | 否 | 每页数量，默认 15，最大 20。超过 20 自动 clamp；非正数（≤0）回落 15；**非数字值直接返回 validation 错误** |
| `--page-token <token>` | 否 | 上一次响应里的 `page_token`，用于翻页 |
| `--format` | 否 | `json`（默认）/ `pretty` |

### 身份（creator 维度）

| 参数 | 映射 | 说明 |
|---|---|---|
| `--mine` | `creator_ids = [当前用户 open_id]` | bool。一键"我创建的"；从当前登录用户身份（`runtime.UserOpenId()`）解析 open_id，取不到直接报错（提示运行 `lark-cli auth login`） |
| `--creator-ids ou_x,ou_y` | `creator_ids = [...]` | 显式 open_id 列表，逗号分隔；**与 `--mine` 互斥** |

### 时间维度（每个维度一对 since/until）

| 参数 | 映射 API 字段 | 是否小时 snap |
|---|---|---|
| `--edited-since` / `--edited-until` | `my_edit_time.start` / `.end` | ✅ start 向下取整，end 向上取整 |
| `--commented-since` / `--commented-until` | `my_comment_time.start` / `.end` | ✅ 同上 |
| `--opened-since` / `--opened-until` | `open_time.start` / `.end` | ❌ 原样透传 |
| `--created-since` / `--created-until` | `create_time.start` / `.end` | ❌ 原样透传（文档创建时间，非"我"语义）|

### 作用域

| 参数 | 映射 | 说明 |
|---|---|---|
| `--doc-types docx,sheet` | `doc_types` | 逗号分隔。允许值：`doc,sheet,bitable,mindnote,file,wiki,docx,folder,catalog,slides,shortcut` |
| `--folder-tokens fld_a,fld_b` | `folder_tokens`（仅 doc_filter） | 存在时只发 `doc_filter`；**与 `--space-ids` 互斥** |
| `--space-ids sp_x` | `space_ids`（仅 wiki_filter） | 存在时只发 `wiki_filter`；**与 `--folder-tokens` 互斥** |
| `--chat-ids oc_x` | `chat_ids` | 逗号分隔 |
| `--sharer-ids ou_x` | `sharer_ids` | 逗号分隔，open_id |

### 其他

| 参数 | 映射 | 说明 |
|---|---|---|
| `--only-title` | `only_title: true` | bool |
| `--only-comment` | `only_comment: true` | bool |
| `--sort <value>` | `sort_type`（转大写枚举） | 允许值：`default, edit_time, edit_time_asc, open_time, create_time` |

> `--sort`：CLI 只暴露服务端**正式支持**的 5 个值。服务端 enum 里 `CREATE_TIME_ASC` 协议标注"暂不支持"，`ENTITY_CREATE_TIME_ASC` / `ENTITY_CREATE_TIME_DESC` 已废弃，CLI 直接不放出来，传了会被 cobra enum 校验拒掉。

## 时间值格式

所有 `--*-since` / `--*-until` 共用：

| 输入 | 含义 |
|---|---|
| `7d` / `30d` | N 天前的当前时刻 |
| `1m` | 30 天前（固定 30 天，**不是**日历月）|
| `3m` / `6m` | 90 / 180 天前 |
| `1y` | 365 天前 |
| `2026-04-01` | 本地时区 00:00:00 |
| `2026-04-01 10:00:00` / `2026-04-01T10:00:00` | 本地时区具体时刻 |
| `2026-04-01T10:00:00+08:00` | RFC3339 带时区 |
| `1743523200`（≥ 10 位纯数字）| Unix 秒直接透传 |

> `m` 绑定 month（30 天），不支持 minute——因为 `my_edit_time` / `my_comment_time` 在服务端是小时聚合，分钟粒度没意义。

## 小时聚合（my_edit_time / my_comment_time）

服务端对这两个字段按整点聚合，亚小时输入会被 CLI 向整点对齐：

```text
start: floor 到整点   16:23:45 → 16:00:00
end:   ceil  到整点   16:23:45 → 17:00:00
```

发生对齐时，stderr 会打印一条 notice，例如：

```text
notice: my_edit_time has hour-level granularity server-side;
        start 2026-04-22 16:23:00 → 2026-04-22 16:00:00
        end   2026-04-22 16:28:00 → 2026-04-22 17:00:00
```

stdout 的 JSON 输出不受影响。`open_time` / `create_time` 不做 snap。

## 输出

- `--format json`（默认）：`{ total, has_more, page_token, results: [...] }`；所有 `*_time` 字段递归补 `*_time_iso`
- `--format pretty`：4 列 table —— `type | title | edit_time | url`
- `title_highlighted` / `summary_highlighted` 可能包含 `<h>` / `<hb>` 高亮标签，客户端对比前需先剥离

> **注意**：返回体里的 `total` 字段不够准确（官方确认，仅供参考）。需要精确统计的场景，按实际 `results` 做去重和累加，不要把 `total` 当结果数承诺。

## 决策规则

- **和 `docs +search` 的选择**：优先使用 `drive +search`（本指令），不要再用 `docs +search`。`docs +search` 进入维护期、后续会下线。
- **身份快捷方式**：只要用户说"我创建的"，直接 `--mine` 即可，不需要先查 contact 拿 open_id。
- **时间维度选择**：
  - "我编辑的"、"我修改的" → `--edited-since` / `--edited-until`
  - "我评论的"、"我回复过的" → `--commented-since` / `--commented-until`
  - "我看过的"、"我打开过的"、"最近看过的" → `--opened-since` / `--opened-until`
  - "创建于"、"新建的"（文档整体维度，与"我"无关）→ `--created-since` / `--created-until`
- **作用域选择**：
  - "某个文件夹下" → `--folder-tokens`（doc-only）
  - "某个 wiki 空间下" → `--space-ids`（wiki-only）
  - 两者不能同时使用，混用会报错
- **身份 flag 互斥**：`--mine` 和 `--creator-ids` 不要同时传，会直接报错。"我和张三创建的" 用 `--creator-ids ou_me,ou_zhangsan`（需要先拿到自己 open_id，但这种场景少见）。
- **实体补全**：
  - 用户说"某个群里"，先用 `lark-im` 查 `chat_id`
  - 用户说"某人创建/分享的"（非自己），先用 `lark-contact` 查 open_id，再填 `--creator-ids` / `--sharer-ids`
- **查询语义下推**：`--query` 支持的服务端高级语法（`intitle:`、`""`、`OR`、`-`）优先使用，不要先模糊搜再在客户端二次过滤。
- **时间表达**：
  - 模糊相对时间（"最近半年"、"过去 30 天"、"最近一周"）→ `--*-since 6m` / `--*-since 30d` / `--*-since 7d`，不展开成 ISO 时间
  - **日历表达**（"上个月"、"上周"、"本月"、"前年"、"今年 3 月"等明确日历单位）→ **必须算出绝对 `YYYY-MM-DD` 边界**（如"上个月" = 上一个日历月的 1 号 → 当月 1 号），**不要近似成 `1m`/`2m`**：CLI 里 `m` 是固定 30 天、`y` 固定 365 天，跟日历差 0-3 天，月末月初尤其容易偏出去
  - 绝对日期 → 直接 `YYYY-MM-DD` 或 RFC3339
- **分页策略**：默认只返回第一页，并说明 `has_more` 和下一页命令。只有用户明确要"全部 / 全量 / 继续翻"才继续。单轮翻页上限 5 页。
- **原始返回**：用户要求"原始数据"、"接口返回"时用 `--format json`，不做客户端精确过滤或摘要重写。

## 权限

| 操作 | 所需 scope |
|---|---|
| 搜索云空间对象（文档 / Wiki / 表格等资源发现） | `search:docs:read` |

## 常见错误

| code | 含义 | 处理 |
|---|---|---|
| `99992351` | `--creator-ids` / `--sharer-ids` 里有 open_id 超出**应用的通讯录可见范围**，服务端拒绝识别 | 让管理员在开发者后台把这些用户加进应用的"通讯录可见性"授权里；或把超出范围的 open_id 从参数里去掉。这和 `search:docs:read` scope 不是一回事 —— 是"应用能看见哪些人"而不是"应用能调用哪个接口" |

## 时间范围自动裁剪（`--opened-*` 专有）

服务端对 `open_time` 过滤**每次请求最多支持 3 个月**（90 天）窗口。其他三个时间维度（`--edited-*` / `--commented-*` / `--created-*`）**不受影响**。

CLI 在发请求前会检查 `--opened-since` 到有效 `--opened-until`（没传则取 `now`）的跨度：

| 跨度 | 行为 |
|---|---|
| ≤ 90 天 | 原样透传 |
| 91 ~ 365 天 | **自动裁剪**到"最近一个 90 天 slice"，stderr 打一条 notice 列出所有剩余 slice 的 `--opened-since` / `--opened-until` 参数值 |
| > 365 天 | 直接报 validation 错，要求缩小范围或自行拆分多次查询 |

Notice 示例（用户原本要求"过去 8 个月"，会被拆成 3 个 slice）：

```text
notice: --opened-* window spans 240 days (~8 months), exceeds the server-side 3-month (90-day) limit.
        this query was narrowed to the most recent slice; 3 slices total:
          [slice 1/3 current] --opened-since 2026-01-24T21:54:02+08:00 --opened-until 2026-04-24T21:54:02+08:00
          [slice 2/3]         --opened-since 2025-10-26T21:54:02+08:00 --opened-until 2026-01-24T21:54:02+08:00
          [slice 3/3]         --opened-since 2025-08-27T21:54:02+08:00 --opened-until 2025-10-26T21:54:02+08:00
        pagination: paginate within a slice via --page-token using that slice's --opened-since / --opened-until values verbatim (NOT the original relative time like '1y' / '8m' — relative times re-resolve against time.Now() and would mismatch the page_token); switch to the next slice's --opened-* flags only after has_more=false, and do not carry --page-token across slices.
```

### Agent 看到 notice 时的处理

**标准流程（分页 × slice 的先后顺序）：**

1. **跑 slice 1**（本次请求已自动裁剪到这个窗口），把结果呈现给用户
2. **先在当前 slice 内翻页**：返回的 `has_more = true` 且用户想看更多时，把 `--opened-since` / `--opened-until` 改成 notice 里 `[slice 1/N current]` 行给出的**具体时间值**（**不要继续用原始的 `--opened-since 1y` 这种相对值**——CLI 每次调用都按 `time.Now()` 重算窗口，相对值 + `--page-token` 一起跑会让 page_token 绑到一个漂移的窗口上、结果静默失真），加 `--page-token` 继续翻，直到 `has_more = false`
3. **再切换到下一个 slice**：当前 slice 翻完后，如果用户还要"更老的"，用 notice 里列的 slice 2 的 `--opened-since` / `--opened-until` 值，**其他 flag（`--query`、`--doc-types`、`--page-size`、`--sort`……）保持原样，`--page-token` 不带**，重新发请求
4. **依次递推**：slice 2 翻完后切 slice 3，以此类推
5. 用户只对最近一段感兴趣时，跳过第 3 步及以后 —— 避免无意义的 API 调用

> `--page-token` 只在单 slice 上下文内有效；切 slice 时不要把上一个 slice 的 `page_token` 带过去。

### 注意事项

- `--sort` 在**单 slice 内部**是正确的。跨 slice 的全局 sort（例如"过去一年我打开过的，按 edit_time desc 排"）不被 CLI 保证，需要 agent 自行拉完多个 slice 后在客户端 re-sort 再呈现
- 裁剪只改 request 发出去的 `open_time` 范围，`--query` / 其他 filter 不动
- 最后一个（最老的）slice 常常不足 90 天，这是正常的截断
