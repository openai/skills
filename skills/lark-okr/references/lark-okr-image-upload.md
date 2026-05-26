# okr +upload-image

> **前置条件：** 先阅读 [`lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

上传本地图片，用于 OKR 进展记录的富文本内容。

## 推荐命令

```bash
# 上传图片用于目标的进展记录
lark-cli okr +upload-image \
  --file ./progress_screenshot.png \
  --target-id 1234567890123456789 \
  --target-type objective

# 上传图片用于关键结果的进展记录
lark-cli okr +upload-image \
  --file ./chart.jpg \
  --target-id 9876543210987654321 \
  --target-type key_result
```

## 参数

| 参数              | 必填 | 默认值 | 说明                                    |
|-----------------|----|-----|---------------------------------------|
| `--file`        | 是  | —   | 本地图片路径。**必须使用相对路径**（如 `./photo.png`）。 |
| `--target-id`   | 是  | —   | 目标 ID 或关键结果 ID（int64 类型，正整数）          |
| `--target-type` | 是  | —   | 目标类型：`objective` \| `key_result`      |
| `--dry-run`     | 否  | —   | 预览 API 调用而不实际执行。                      |

## 工作流程

1. 使用 `+cycle-list` 和 `+cycle-detail` 获取目标或关键结果的 ID。
2. 准备本地图片文件，确保格式受支持。
3. 执行 `lark-cli okr +upload-image --file ./image.png --target-id "..." --target-type objective`。
4. 获取返回的 `file_token`，用于构建 ContentBlock 中的图片内容。

## 输出

返回 JSON：

```json
{
  "file_token": "example-file-token",
  "url": "https://example.larksuite.com/download?file_token=example-file-token",
  "file_name": "screenshot.png",
  "size": 102400
}
```

其中：

- `file_token` — 用于在 ContentBlock 的 `ContentGallery` 中引用图片
- `url` — 图片的访问 URL
- `file_name` — 上传的文件名
- `size` — 文件大小（字节）

## 在进展记录中使用上传的图片

上传图片后，将返回的 `file_token` 用于构建 ContentBlock 的图库块：

```json
{
  "blocks": [
    {
      "block_element_type": "paragraph",
      "paragraph": {
        "elements": [
          {
            "paragraph_element_type": "textRun",
            "text_run": {
              "text": "本周进展截图："
            }
          }
        ]
      }
    },
    {
      "block_element_type": "gallery",
      "gallery": {
        "images": [
          {
            "file_token": "example-file-token",
            "width": 800,
            "height": 600
          }
        ]
      }
    }
  ]
}
```

然后在创建或更新进展记录时使用此 ContentBlock：

```bash
lark-cli okr +progress-create \
  --content @content_with_image.json \
  --target-id 1234567890123456789 \
  --target-type objective
```

## 安全限制

- `--file` 参数**必须使用相对路径**（如 `./photo.png` 或 `images/photo.png`），不支持绝对路径
- 图片文件必须存在于当前工作目录或其子目录中
- 不支持符号链接指向目录外的文件

## 参考

- [lark-okr](../SKILL.md) -- 所有 OKR 命令(shortcut 和 API 接口)
- [ContentBlock 格式](lark-okr-contentblock.md) -- 进展内容使用的富文本格式，包含图片块的使用说明
- [lark-okr-progress-create](lark-okr-progress-create.md) -- 创建进展记录
- [lark-okr-progress-update](lark-okr-progress-update.md) -- 更新进展记录
- [lark-shared](../../lark-shared/SKILL.md) -- 认证和全局参数
