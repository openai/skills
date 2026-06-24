# base +record-share-link-create

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

为一条或多条记录生成分享链接（单次调用最多传入 100 条，内部调用批量接口）。

## 推荐命令

```bash
# 单条记录
lark-cli base +record-share-link-create \
  --base-token <base_token> \
  --table-id <table_id> \
  --record-ids <record_id>

# 多条记录（使用 "," 分隔）
lark-cli base +record-share-link-create \
  --base-token <base_token> \
  --table-id <table_id> \
  --record-ids rec001,rec002,rec003
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--base-token <token>` | 是 | Base Token |
| `--table-id <id>` | 是 | 表 ID |
| `--record-ids <ids...>` | 是 | 记录 ID 列表，逗号分隔或重复使用该标志，最多 100 条 |

## API 入参详情

**HTTP 方法和路径：**

```http
POST /open-apis/base/v3/bases/:base_token/tables/:table_id/records/share_links/batch
```

**请求体：**

```json
{
  "record_ids": ["rec001", "rec002", "rec003"]
}
```

> CLI 会自动对 `--record-ids` 去重后再调用接口。

## 返回重点

- 成功时直接返回接口 `data` 字段内容，包含 `record_share_links` 映射（key 为 record_id，value 为分享链接）。结构如下：

```json
{
  "record_share_links": {
    "rec001": "https://example.feishu.cn/record/TW2wrdbkoeoYXYcwvyIczJ2ZnFb"
  }
}
```

- 若部分记录 ID 无权限/不存在，则 `record_share_links` 中只会包含有效记录对应的分享链接
- 若全部记录 ID 都无权限/不存在，则会返回错误信息 `records do not exist or no read permission`

## 坑点

- ⚠️ 单次最多 100 条记录，超出会被 CLI 校验拦截。
- ⚠️ 重复的 record_id 会在调用前自动去重。
- ⚠️ `--record-ids` 为空时会被校验拦截。

## 参考

- [lark-base-record.md](lark-base-record.md) — record 索引页
