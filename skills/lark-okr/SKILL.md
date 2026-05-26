---
name: lark-okr
version: 1.0.0
description: "飞书 OKR：管理目标与关键结果。查看和编辑 OKR 周期、目标（Objective）、关键结果（Key Result）、对齐关系、量化指标和进展记录。当用户需要查看或创建 OKR、管理目标和关键结果、查看对齐关系时使用。"
metadata:
  requires:
    bins: [ "lark-cli" ]
  cliHelp: "lark-cli okr --help"
---

# okr (v2)

**CRITICAL — 开始前 MUST 先用 Read 工具读取 [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md)，其中包含认证、权限处理**

## Shortcuts（推荐优先使用）

Shortcut 是对常用操作的高级封装（`lark-cli okr +<verb> [flags]`）。有 Shortcut 的操作优先使用。

| Shortcut                                                     | 说明                       |
|--------------------------------------------------------------|--------------------------|
| [`+cycle-list`](references/lark-okr-cycle-list.md)           | 获取特定用户的 OKR 周期列表，可以按时间筛选 |
| [`+cycle-detail`](references/lark-okr-cycle-detail.md)       | 获取特定 OKR 中所有目标和关键结果的内容   |
| [`+progress-list`](references/lark-okr-progress-list.md)     | 获取目标或关键结果的所有进展记录列表      |
| [`+progress-get`](references/lark-okr-progress-get.md)       | 根据 ID 获取单条 OKR 进展记录      |
| [`+progress-create`](references/lark-okr-progress-create.md) | 为目标或关键结果创建进展记录           |
| [`+progress-update`](references/lark-okr-progress-update.md) | 更新指定 ID 的进展记录内容          |
| [`+progress-delete`](references/lark-okr-progress-delete.md) | 删除指定 ID 的进展记录（不可恢复）      |
| [`+upload-image`](references/lark-okr-image-upload.md)       | 上传图片用于 OKR 进展记录的富文本内容    |

## 格式说明

- [`OKR 业务实体`](references/lark-okr-entities.md) 获取 OKR 实体结构，定义和关系，帮助你更好的使用 OKR 功能
- [`ContentBlock 富文本格式`](references/lark-okr-contentblock.md) — Objective/KeyResult/Progress 中 Content/Note 字段使用的富文本格式说明
- **强烈建议** 在操作 OKR 前，阅读[`OKR 业务实体`](references/lark-okr-entities.md)以了解基础概念

## API Resources

```bash
lark-cli schema okr.<resource>.<method>   # 调用 API 前必须先查看参数结构
lark-cli okr <resource> <method> [flags] # 调用 API
```

> **重要**：使用原生 API 时，**必须**先运行 `schema` 查看 `--data` / `--params` 参数结构，**不要**猜测字段格式！

### alignments

- `delete` — 删除对齐关系
- `get` — 获取对齐关系

### categories

- `list` — 批量获取分类

### cycles

- `list` — 批量获取用户周期
- `objectives_position` — 更新用户周期下全部目标的位置
    - 请求中必须同时修改对应周期下全部目标的位置，且不允许位置重叠，否则会参数校验失败。
- `objectives_weight` — 更新用户周期下全部目标的权重
    - 请求中必须同时修改对应周期下全部目标的权重，且所有权重值的和必须等于 1 ，否则会参数校验失败。

### cycle.objectives

- `create` — 创建目标
- `list` — 批量获取用户周期下的目标

### indicators

- `patch` — 更新量化指标

### key_results

- `delete` — 删除关键结果
- `get` — 获取关键结果
- `patch` — 更新关键结果

### key_result.indicators

- `list` — 获取关键结果的量化指标

### objectives

- `delete` — 删除目标
- `get` — 获取目标
- `key_results_position` — 更新全部关键结果的位置
    - 请求中必须同时修改对应目标下全部关键结果的位置，且不允许位置重叠，否则会参数校验失败。
- `key_results_weight` — 更新全部关键结果的权重
    - 请求中必须同时修改对应目标下全部关键结果的权重，且所有权重值的和必须等于 1 ，否则会参数校验失败。
- `patch` — 更新目标

### objective.alignments

- `create` — 创建对齐关系
    - 对齐不允许对齐自己的目标，且发起对齐的目标和被对齐的目标所在周期时间上必须有重叠，否则会参数校验失败。
- `list` — 批量获取目标下的对齐关系

### objective.indicators

- `list` — 获取目标的量化指标

### objective.key_results

- `create` — 创建关键结果
- `list` — 批量获取目标下的关键结果

## 权限表

| 方法                                | 所需 scope                    |
|-----------------------------------|-----------------------------|
| `alignments.delete`               | `okr:okr.content:writeonly` |
| `alignments.get`                  | `okr:okr.content:readonly`  |
| `categories.list`                 | `okr:okr.setting:read`      |
| `cycles.list`                     | `okr:okr.period:readonly`   |
| `cycles.objectives_position`      | `okr:okr.content:writeonly` |
| `cycles.objectives_weight`        | `okr:okr.content:writeonly` |
| `cycle.objectives.create`         | `okr:okr.content:writeonly` |
| `cycle.objectives.list`           | `okr:okr.content:readonly`  |
| `indicators.patch`                | `okr:okr.content:writeonly` |
| `key_results.delete`              | `okr:okr.content:writeonly` |
| `key_results.get`                 | `okr:okr.content:readonly`  |
| `key_results.patch`               | `okr:okr.content:writeonly` |
| `key_result.indicators.list`      | `okr:okr.content:readonly`  |
| `objectives.delete`               | `okr:okr.content:writeonly` |
| `objectives.get`                  | `okr:okr.content:readonly`  |
| `objectives.key_results_position` | `okr:okr.content:writeonly` |
| `objectives.key_results_weight`   | `okr:okr.content:writeonly` |
| `objectives.patch`                | `okr:okr.content:writeonly` |
| `objective.alignments.create`     | `okr:okr.content:writeonly` |
| `objective.alignments.list`       | `okr:okr.content:readonly`  |
| `objective.indicators.list`       | `okr:okr.content:readonly`  |
| `objective.key_results.create`    | `okr:okr.content:writeonly` |
| `objective.key_results.list`      | `okr:okr.content:readonly`  |

