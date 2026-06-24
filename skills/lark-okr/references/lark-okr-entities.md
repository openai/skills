# OKR 实体定义

本文档描述飞书 OKR API (`/open-apis/okr/v2`) 中涉及的核心实体及其字段定义。

## 实体关系概览

```
Cycle (用户周期)
  └── Objective (目标)
        ├── KeyResult (关键结果)
        │     └── Indicator (指标)
        │     └── list<Progress> (进展记录列表)
        └── Indicator (指标)
        └── list<Progress> (进展记录列表)

Alignment (对齐关系): Objective ↔ Objective
Category (分类): Objective 的分组标签
```

---

## Owner (所有者)

所有者标识 OKR 实体的归属，目前仅支持用户类型。

| 字段           | 类型       | 必填 | 说明                                            |
|--------------|----------|----|-----------------------------------------------|
| `owner_type` | `string` | 是  | 所有者类型，通常为 `"user"`。                           |
| `user_id`    | `string` | 否  | 员工 ID，类型由请求参数 `user_id_type` 决定（默认 `open_id`） |

---

## Cycle (用户周期)

用户周期是 OKR 的顶层容器，代表一个时间段内的所有目标与关键结果。

| 字段                | 类型        | 必填 | 说明                                         |
|-------------------|-----------|----|--------------------------------------------|
| `id`              | `string`  | 是  | 用户周期 ID                                    |
| `create_time`     | `string`  | 是  | 创建时间                                       |
| `update_time`     | `string`  | 是  | 更新时间                                       |
| `tenant_cycle_id` | `string`  | 是  | 租户周期 ID（同一周期在不同用户下有不同的用户周期 ID，但租户周期 ID 相同） |
| `owner`           | `Owner`   | 是  | 所有者                                        |
| `start_time`      | `string`  | 是  | 周期开始时间。总是从某月1日开始                           |
| `end_time`        | `string`  | 是  | 周期结束时间。到某月最后一日结束                           |
| `cycle_status`    | `integer` | 否  | 周期状态，见下表                                   |
| `score`           | `number`  | 否  | 周期分数，范围 [0, 1]，支持一位小数                      |

### 常用术语

- **当前周期**: 指周期的 start_time/end_time
  指周期的 start_time / end_time 所在的时间段与当前时间重叠的周期（即： start_time <= 当前时间 且 end_time >= 当前时间）。 注意：时间重叠是判断当前周期的首要且必须的硬性条件，绝对不能仅仅根据 cycle_status == 1 去判断。 如果有多个符合时间重叠标准的周期，再在这些包含当前时间的周期中过滤，保留周期状态为 default (0) 或 normal (1) 的周期。如果仍然有多个，则选择其中较新的一个。当用户提及“上一个周期”，“下一个周期”一类的表述时，通常是以当前周期为准计算。
- **所有者**: 绝大多数所有者都是用户，少部分租户启用了“团队OKR”功能，所有者可能是部门。用户身份下，只能编辑所有者为当前用户的
  OKR。

### 周期状态 (cycle_status)

| 值 | 常量名       | 说明          |
|---|-----------|-------------|
| 0 | `default` | 默认状态        |
| 1 | `normal`  | 生效中         |
| 2 | `invalid` | 已失效（通常仍可填写） |
| 3 | `hidden`  | 已隐藏（不可见）    |

> **SHORTCUT：** `okr +cycle-list` [lark-okr-cycle-list.md](lark-okr-cycle-list.md) 获取用户的周期列表，可按时间筛选
>
> **API：** `cycles.list`

---

## Objective (目标)

目标是 OKR 中的 "O"，属于某个用户周期，可包含多个关键结果。

| 字段            | 类型             | 必填 | 说明                                                      |
|---------------|----------------|----|---------------------------------------------------------|
| `id`          | `string`       | 是  | 目标 ID                                                   |
| `create_time` | `string`       | 是  | 创建时间，毫秒时间戳，shortcut 会将其解析为日期时间                          |
| `update_time` | `string`       | 是  | 更新时间，毫秒时间戳，shortcut 会将其解析为日期时间                          |
| `owner`       | `Owner`        | 是  | 所有者                                                     |
| `cycle_id`    | `string`       | 是  | 所属用户周期 ID                                               |
| `position`    | `integer`      | 是  | 排序序号，从 1 开始，范围 [1, 100]                                 |
| `content`     | `ContentBlock` | 否  | 目标内容（富文本），见 [ContentBlock 定义](lark-okr-contentblock.md) |
| `score`       | `number`       | 否  | 目标分数，范围 [0, 1]，支持一位小数                                   |
| `notes`       | `ContentBlock` | 否  | 目标备注（富文本），见 [ContentBlock 定义](lark-okr-contentblock.md) |
| `weight`      | `number`       | 否  | 目标权重，范围 [0, 1]，支持三位小数                                   |
| `deadline`    | `string`       | 否  | 截止时间，毫秒时间戳，shortcut 会将其解析为日期时间                          |
| `category_id` | `string`       | 否  | 所属分类 ID                                                 |

> **SHORTCUT：**
> - `okr +cycle-detail` [lark-okr-cycle-detail.md](lark-okr-cycle-detail.md) 获取某个用户周期下的全部目标和关键结果。时间相关的字段会以日期时间格式解析
>
> **API：**
> - `cycle.objectives.list` — 获取周期下的目标列表
> - `objectives.get` — 获取单个目标
> - `cycle.objectives.create` — 创建目标
> - `objectives.delete` — 删除目标
> - `cycles.objectives_position` — 更新周期下的目标排序
> - `cycles.objectives_weight` — 更新周期下的目标权重

---

## KeyResult (关键结果)

关键结果是 OKR 中的 "KR"，属于某个目标，描述目标的可衡量成果。

| 字段             | 类型             | 必填 | 说明                                                        |
|----------------|----------------|----|-----------------------------------------------------------|
| `id`           | `string`       | 是  | 关键结果 ID                                                   |
| `create_time`  | `string`       | 是  | 创建时间，毫秒时间戳                                                |
| `update_time`  | `string`       | 是  | 修改时间，毫秒时间戳                                                |
| `owner`        | `Owner`        | 是  | 所有者                                                       |
| `objective_id` | `string`       | 是  | 所属目标 ID                                                   |
| `position`     | `integer`      | 是  | 排序序号，从 1 开始，范围 [1, 100]                                   |
| `content`      | `ContentBlock` | 否  | 关键结果内容（富文本），见 [ContentBlock 定义](lark-okr-contentblock.md) |
| `score`        | `number`       | 否  | 关键结果分数，范围 [0, 1]，支持一位小数                                   |
| `weight`       | `number`       | 否  | 权重，范围 [0, 1]，支持三位小数                                       |
| `deadline`     | `string`       | 否  | 截止时间，毫秒时间戳                                                |

> **API：**
> - `objective.key_results.list` — 获取目标下的关键结果列表
> - `key_results.get` — 获取单个关键结果
> - `key_results.patch` — 更新关键结果
> - `key_results.delete` — 删除关键结果
> - `objectives.key_results_position` — 更新目标下的关键结果排序
> - `objectives.key_results_weight` — 更新目标下的关键结果权重

---

## Progress (进展记录)

进展记录挂载在目标（Objective）或关键结果（Key Result）上，用于记录阶段性进展内容与进度百分比。每条进展记录包含富文本内容和可选的进度率。

| 字段              | 类型             | 必填 | 说明                                                      |
|-----------------|----------------|----|---------------------------------------------------------|
| `progress_id`   | `string`       | 是  | 进展记录 ID（int64，正整数）                                      |
| `modify_time`   | `string`       | 是  | 最后修改时间，毫秒时间戳，shortcut 会将其解析为日期时间                        |
| `content`       | `ContentBlock` | 否  | 进展内容（富文本），见 [ContentBlock 定义](lark-okr-contentblock.md) |
| `progress_rate` | `ProgressRate` | 否  | 进度率，包含百分比和状态                                            |

### ProgressRate (进度率)

| 字段        | 类型       | 必填 | 说明                                                                                                                           |
|-----------|----------|----|------------------------------------------------------------------------------------------------------------------------------|
| `percent` | `number` | 否  | 进度百分比，范围 [-99999999999, 99999999999]。百分比的取值通常在 0-100，但允许超过此范围，以表示超额完成或负增长等情况。挂载的目标或关键结果的量化指标不使用百分比单位时，以这个字段更新当前值。系统内最多保留两位小数 |
| `status`  | `string` | 否  | 进度状态，shortcut 返回可读字符串，见下表                                                                                                    |

### 进度状态 (progress_rate.status)

| 值         | 常量名 | 说明    |
|-----------|-----|-------|
| `normal`  | 正常  | 进展正常  |
| `overdue` | 逾期  | 进展逾期  |
| `done`    | 已完成 | 进展已完成 |

### 创建进展记录时的参数

创建进展记录时，除了 `content` 外，还需要指定这条进展记录挂载的对应目标或关键结果：

| 字段              | 类型             | 必填 | 说明                                                      |
|-----------------|----------------|----|---------------------------------------------------------|
| `content`       | `ContentBlock` | 是  | 进展内容（富文本），见 [ContentBlock 定义](lark-okr-contentblock.md) |
| `target_id`     | `string`       | 是  | 目标 ID 或关键结果 ID                                          |
| `target_type`   | `integer`      | 是  | 目标类型：`2`=目标（Objective），`3`=关键结果（KeyResult）              |
| `progress_rate` | `ProgressRate` | 否  | 进度率，可设置 `percent` 和 `status`                            |
| `source_title`  | `string`       | 否  | 来源标题，用于在 OKR 界面中显示进展来源                                  |
| `source_url`    | `string`       | 否  | 来源 URL，用于在 OKR 界面中显示进展来源链接                              |

> **SHORTCUT：**
> - `okr +progress-get` [lark-okr-progress-get.md](lark-okr-progress-get.md) 获取单条进展记录
> - `okr +progress-create` [lark-okr-progress-create.md](lark-okr-progress-create.md) 为目标或关键结果创建进展记录
> - `okr +progress-update` [lark-okr-progress-update.md](lark-okr-progress-update.md) 更新进展记录内容
> - `okr +progress-delete` [lark-okr-progress-delete.md](lark-okr-progress-delete.md) 删除进展记录
> - `okr +progress-list` [lark-okr-progress-list.md](lark-okr-progress-list.md) 获取目标/关键结果下的进展记录
---

## Indicator (指标)

指标是目标和关键结果的量化度量，可独立挂载在 Objective 或 KeyResult 上。

| 字段                             | 类型              | 必填 | 说明                                 |
|--------------------------------|-----------------|----|------------------------------------|
| `id`                           | `string`        | 是  | 指标 ID                              |
| `create_time`                  | `string`        | 是  | 创建时间，毫秒时间戳                         |
| `update_time`                  | `string`        | 是  | 更新时间，毫秒时间戳                         |
| `owner`                        | `Owner`         | 是  | 所有者                                |
| `entity_type`                  | `integer`       | 是  | 所属实体类型：`2`=目标，`3`=关键结果             |
| `entity_id`                    | `string`        | 是  | 所属实体 ID                            |
| `indicator_status`             | `integer`       | 是  | 指标状态，见下表                           |
| `status_calculate_type`        | `integer`       | 是  | 状态计算方式，见下表                         |
| `start_value`                  | `number`        | 否  | 起始值，范围 [-99999999999, 99999999999] |
| `target_value`                 | `number`        | 否  | 目标值，范围 [-99999999999, 99999999999] |
| `current_value`                | `number`        | 否  | 当前值，范围 [-99999999999, 99999999999] |
| `current_value_calculate_type` | `integer`       | 否  | 当前值计算方式，见下表                        |
| `unit`                         | `IndicatorUnit` | 否  | 指标单位                               |

### 修改指南

- **进度值**: 一般指 `current_value`，单位未提及时通常用百分制计算。
- 当用户要求量化的更新 OKR 进度时，一般指的就是修改对应 OKR 的 Indicator。
- OKR 在未设置量化指标时，Indicator 的内容为空。如果用户未做特别说明，更新进度时可以默认将进度以百分制设置（初始值0，目标值100，unit
  参见下文设置为 0/PERCENT）

### 指标状态 (indicator_status)

| 值  | 说明  |
|----|-----|
| -1 | 未定义 |
| 0  | 正常  |
| 1  | 有风险 |
| 2  | 已延期 |

### 状态计算方式 (status_calculate_type)

| 值 | 说明              | 适用范围    |
|---|-----------------|---------|
| 0 | 手动更新            | 目标、关键结果 |
| 1 | 基于进度和当前时间自动更新   | 目标、关键结果 |
| 2 | 基于风险最高的关键结果状态更新 | 仅目标     |

### 当前值计算方式 (current_value_calculate_type)

| 值 | 说明            | 适用范围    |
|---|---------------|---------|
| 0 | 手动更新          | 目标、关键结果 |
| 1 | 基于关键结果进度自动更新  | 仅目标     |
| 2 | 基于拆解的关键结果进度更新 | 仅关键结果   |

### IndicatorUnit (指标单位)

| 字段           | 类型        | 必填 | 说明                                                                          |
|--------------|-----------|----|-----------------------------------------------------------------------------|
| `unit_type`  | `integer` | 是  | 单位类型：`0`=公共，`1`=自定义                                                         |
| `unit_value` | `string`  | 是  | 单位值。公共类型可选：`PERCENT`(百分比)、`NONE`(无单位)、`YUAN`(元)、`DOLLAR`(美元)；自定义类型字符长度不超过 5 |

> **API：**
> - `key_result.indicators.list` — 获取关键结果的指标
> - `objective.indicators.list` — 获取目标的指标
> - `indicators.patch` — 更新指标

---

## Alignment (对齐关系)

对齐关系描述两个目标之间的上下对齐。

| 字段                 | 类型        | 必填 | 说明                    |
|--------------------|-----------|----|-----------------------|
| `id`               | `string`  | 是  | 对齐 ID                 |
| `create_time`      | `string`  | 是  | 创建时间，毫秒时间戳            |
| `update_time`      | `string`  | 是  | 更新时间，毫秒时间戳            |
| `from_owner`       | `Owner`   | 是  | 发起对齐的所有者              |
| `to_owner`         | `Owner`   | 是  | 被对齐的所有者               |
| `from_entity_type` | `integer` | 是  | 发起对齐的实体类型，固定为 `2`（目标） |
| `from_entity_id`   | `string`  | 是  | 发起对齐的实体 ID            |
| `to_entity_type`   | `integer` | 是  | 被对齐的实体类型，固定为 `2`（目标）  |
| `to_entity_id`     | `string`  | 是  | 被对齐的实体 ID             |

> **API：**
> - `alignments.get` — 获取对齐关系
> - `alignments.delete` — 删除对齐关系
> - `objective.alignments.list` — 批量获取目标下的对齐关系
> - `objective.alignments.create` — 创建对齐关系

---

## Category (分类)

分类用于对目标进行分组标记（如"个人 OKR"、"团队 OKR"、"承诺 OKR"）等。具体的分类根据租户设置而定。

| 字段              | 类型             | 必填 | 说明                                                          |
|-----------------|----------------|----|-------------------------------------------------------------|
| `id`            | `string`       | 是  | 分类 ID                                                       |
| `create_time`   | `string`       | 是  | 创建时间，毫秒时间戳                                                  |
| `update_time`   | `string`       | 是  | 更新时间，毫秒时间戳                                                  |
| `category_type` | `string`       | 是  | 分类类型：`"person"`=个人，`"team"`=团队                              |
| `enabled`       | `boolean`      | 是  | 是否启用                                                        |
| `color`         | `string`       | 是  | 颜色标识：`blue`、`purple`、`wathet`、`turquoise`、`indigo`、`orange` |
| `name`          | `CategoryName` | 是  | 多语言名称                                                       |

### CategoryName (分类名称)

| 字段   | 类型       | 必填 | 说明  |
|------|----------|----|-----|
| `zh` | `string` | 否  | 中文名 |
| `en` | `string` | 否  | 英文名 |
| `ja` | `string` | 否  | 日文名 |

> **API：** `categories.list` — 批量获取租户设置的分类列表

---

## 通用请求参数

以下参数在多数 OKR API 中通用：

| 参数                   | 位置      | 必填 | 默认值                    | 说明                                               |
|----------------------|---------|----|------------------------|--------------------------------------------------|
| `user_id_type`       | `query` | 否  | `"open_id"`            | 用户 ID 类型：`open_id` \| `union_id` \| `user_id`    |
| `department_id_type` | `query` | 否  | `"open_department_id"` | 部门 ID 类型：`open_department_id` \| `department_id` |
| `page_size`          | `query` | 否  | `10`                   | 分页大小，最大 100                                      |
| `page_token`         | `query` | 否  | `""`                   | 分页键，首页传空串                                        |

---

## 权限 Scope 说明

| Scope                          | 权限类型 | 说明           |
|--------------------------------|------|--------------|
| `okr:okr.content:readonly`     | 读    | 读取 OKR 内容    |
| `okr:okr.content:writeonly`    | 写    | 写入/删除 OKR 内容 |
| `okr:okr.period:readonly`      | 读    | 读取 OKR 周期    |
| `okr:okr.progress:readonly`    | 读    | 读取进展记录       |
| `okr:okr.progress:writeonly`   | 写    | 创建/更新进展记录    |
| `okr:okr.progress:delete`      | 写    | 删除进展记录       |
| `okr:okr.progress.file:upload` | 写    | 上传进展记录图片附件   |
| `okr:okr.setting:read`         | 读    | 读取 OKR 设置    |

所有 OKR API 均支持 `user` 和 `tenant`（应用）两种 access token 类型。

## 参考

- [OKR ContentBlock 富文本格式](lark-okr-contentblock.md) — content/notes 字段的富文本结构定义
- [okr +cycle-list](lark-okr-cycle-list.md) — 列出用户 OKR 周期
- [okr +cycle-detail](lark-okr-cycle-detail.md) — 获取周期下的目标与关键结果
- [okr +progress-get](lark-okr-progress-get.md) — 获取进展记录
- [okr +progress-create](lark-okr-progress-create.md) — 创建进展记录
- [okr +progress-update](lark-okr-progress-update.md) — 更新进展记录
- [okr +progress-delete](lark-okr-progress-delete.md) — 删除进展记录
