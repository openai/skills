# base record shortcuts

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

record 相关命令索引。

## 命令导航

| 文档 | 命令 | 说明 |
|------|------|------|
| [lark-base-data-analysis-sop.md](lark-base-data-analysis-sop.md) | `+record-get` / `+record-search` / `+record-list` / `+data-query` / 视图筛选排序 | 数据查询与分析统一选路、筛选排序投影、聚合后回查明细 SOP |
| [lark-base-record-upsert.md](lark-base-record-upsert.md) | `+record-upsert` | 创建或更新记录 |
| [lark-base-record-batch-create.md](lark-base-record-batch-create.md) | `+record-batch-create` | 按 `fields/rows` 批量创建记录 |
| [lark-base-record-batch-update.md](lark-base-record-batch-update.md) | `+record-batch-update` | 批量更新记录 |
| [lark-base-record-upload-attachment.md](lark-base-record-upload-attachment.md) | `+record-upload-attachment` | 上传本地文件到附件字段并更新记录 |
| [`../../lark-doc/references/lark-doc-media-download.md`](../../lark-doc/references/lark-doc-media-download.md) | `lark-cli docs +media-download` | 下载 Base 附件到本地（附件的 `file_token` 来自 `+record-get` 的附件字段） |
| [lark-base-record-delete.md](lark-base-record-delete.md) | `+record-delete` | 删除一条或多条记录 |
| [lark-base-record-share-link-create.md](lark-base-record-share-link-create.md) | `+record-share-link-create` | 生成记录分享链接（支持单条或批量，最多 100 条）|

## 说明

- 读取记录前优先阅读 [lark-base-data-analysis-sop.md](lark-base-data-analysis-sop.md)，它合并了 `record / view / data-query` 的选路、分页、投影、聚合后回查明细和 link 关联读取。
- 聚合页只保留目录职责；写入、删除、历史等命令的详细说明请进入对应单命令文档。
- 所有 `+xxx-list` 调用都必须串行执行；若要批量跑多个 list 请求，只能串行执行。
- `+record-list` 支持重复传参 `--field-id` 做字段筛选。
- `+record-get` 支持重复 `--record-id` 或 `--json '{"record_id_list":[...]}'` 批量读取；也支持重复传参 `--field-id` 裁剪返回字段，避免返回全字段。
- 写记录 JSON 前优先阅读 [lark-base-cell-value.md](lark-base-cell-value.md)。
- 本地文件写入附件字段时，必须使用 `+record-upload-attachment`。
- 从附件字段下载文件时，用 `lark-cli docs +media-download --token <file_token> --output <path>`，用法见 [`../../lark-doc/references/lark-doc-media-download.md`](../../lark-doc/references/lark-doc-media-download.md)。
