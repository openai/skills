# OKR ContentBlock 富文本格式

OKR 的 Objective、KeyResult 中的 content/notes 字段使用 `ContentBlock` 富文本格式。本文档描述其结构和使用方式。

## ContentBlock 结构概览

```json
{
  "blocks": [
    {
      "block_element_type": "paragraph",
      "paragraph": {
        "style": {
          "list": {
            "list_type": "bullet",
            "indent_level": 0,
            "number": 1
          }
        },
        "elements": [
          {
            "paragraph_element_type": "textRun",
            "text_run": {
              "text": "Hello World",
              "style": {
                "bold": true,
                "strike_through": false,
                "back_color": {
                  "red": 255,
                  "green": 0,
                  "blue": 0,
                  "alpha": 1
                },
                "text_color": {
                  "red": 0,
                  "green": 255,
                  "blue": 0,
                  "alpha": 1
                },
                "link": {
                  "url": "https://example.com"
                }
              }
            }
          },
          {
            "paragraph_element_type": "docsLink",
            "docs_link": {
              "url": "https://larkoffice.com/docx/xxx",
              "title": "Lark Document"
            }
          },
          {
            "paragraph_element_type": "mention",
            "mention": {
              "user_id": "ou_xxx"
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
            "file_token": "file_xxx",
            "src": "https://...",
            "width": 800,
            "height": 600
          }
        ]
      }
    }
  ]
}
```

## 类型定义

### ContentBlock

根级别内容块。

| 字段       | 类型                      | 说明      |
|----------|-------------------------|---------|
| `blocks` | `ContentBlockElement[]` | 内容块元素数组 |

### ContentBlockElement

内容块元素，支持段落或图库。

| 字段                   | 类型                 | 说明                                         |
|----------------------|--------------------|--------------------------------------------|
| `block_element_type` | `BlockElementType` | 块类型：`paragraph` \| `gallery`               |
| `paragraph`          | `ContentParagraph` | 段落内容（当 `block_element_type="paragraph"` 时） |
| `gallery`            | `ContentGallery`   | 图库内容（当 `block_element_type="gallery"` 时）   |

### ContentParagraph

段落内容。

| 字段         | 类型                          | 说明          |
|------------|-----------------------------|-------------|
| `style`    | `ContentParagraphStyle`     | 段落样式（列表类型等） |
| `elements` | `ContentParagraphElement[]` | 段落内元素数组     |

### ContentParagraphElement

段落内元素，支持文本、文档链接、提及。

| 字段                       | 类型                     | 说明                                        |
|--------------------------|------------------------|-------------------------------------------|
| `paragraph_element_type` | `ParagraphElementType` | 元素类型：`textRun` \| `docsLink` \| `mention` |
| `text_run`               | `ContentTextRun`       | 文本内容                                      |
| `docs_link`              | `ContentDocsLink`      | 飞书文档链接                                    |
| `mention`                | `ContentMention`       | 用户提及                                      |

### ContentTextRun

文本块。

| 字段      | 类型                 | 说明   |
|---------|--------------------|------|
| `text`  | `string`           | 文本内容 |
| `style` | `ContentTextStyle` | 文本样式 |

### ContentTextStyle

文本样式。

| 字段               | 类型             | 说明    |
|------------------|----------------|-------|
| `bold`           | `boolean`      | 是否粗体  |
| `strike_through` | `boolean`      | 是否删除线 |
| `back_color`     | `ContentColor` | 背景颜色  |
| `text_color`     | `ContentColor` | 文字颜色  |
| `link`           | `ContentLink`  | 链接    |

### ContentColor

颜色。

| 字段      | 类型        | 说明           |
|---------|-----------|--------------|
| `red`   | `int32`   | 红色通道 (0-255) |
| `green` | `int32`   | 绿色通道 (0-255) |
| `blue`  | `int32`   | 蓝色通道 (0-255) |
| `alpha` | `float64` | 透明度 (0-1)    |

### ContentParagraphStyle

段落样式。

| 字段     | 类型            | 说明   |
|--------|---------------|------|
| `list` | `ContentList` | 列表样式 |

### ContentList

列表样式。

| 字段             | 类型         | 说明                                                                  |
|----------------|------------|---------------------------------------------------------------------|
| `list_type`    | `ListType` | 列表类型：`bullet` \| `number` \| `checkBox` \| `checkedBox` \| `indent` |
| `indent_level` | `int32`    | 缩进层级                                                                |
| `number`       | `int32`    | 序号（当 `list_type="number"` 时）                                        |

### ContentGallery

图片块。目前仅有进展记录中的富文本支持展示图片。

由于 OKR 应用中进展页面的布局排版限制，一个 ContentGallery 元素中**仅可放置一个图片元素**，需要插入多张图片时需使用多个 ContentGallery 元素
(同一个 ContentGallery 中添加多个 image 会导致这些图片在狭窄的横向排版空间中互相挤占，效果很差)

| 字段       | 类型                   | 说明    |
|----------|----------------------|-------|
| `images` | `ContentImageItem[]` | 图片项数组 |

### ContentImageItem

图片项。

| 字段           | 类型        | 说明       |
|--------------|-----------|----------|
| `file_token` | `string`  | 文件 token |
| `src`        | `string`  | 图片 URL   |
| `width`      | `float64` | 宽度       |
| `height`     | `float64` | 高度       |

> **如何获取 `file_token`？** 使用 [`+upload-image`](lark-okr-image-upload.md) 命令上传本地图片，返回的 `file_token` 可用于构建 `ContentGallery` 图片块。

### ContentDocsLink

飞书文档链接。

| 字段      | 类型       | 说明     |
|---------|----------|--------|
| `url`   | `string` | 链接 URL |
| `title` | `string` | 链接标题   |

### ContentMention

提及。

| 字段        | 类型       | 说明    |
|-----------|----------|-------|
| `user_id` | `string` | 用户 ID |

### ContentLink

链接。

| 字段    | 类型       | 说明     |
|-------|----------|--------|
| `url` | `string` | 链接 URL |

## 使用示例

### 示例 1：简单文本段落

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
              "text": "提升用户满意度"
            }
          }
        ]
      }
    }
  ]
}
```

### 示例 2：带格式的文本段落

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
              "text": "Q2 目标",
              "style": {
                "bold": true
              }
            }
          },
          {
            "paragraph_element_type": "textRun",
            "text_run": {
              "text": " - 提升产品质量"
            }
          }
        ]
      }
    }
  ]
}
```

### 示例 3：带列表的段落

```json
{
  "blocks": [
    {
      "block_element_type": "paragraph",
      "paragraph": {
        "style": {
          "list": {
            "list_type": "bullet",
            "indent_level": 0
          }
        },
        "elements": [
          {
            "paragraph_element_type": "textRun",
            "text_run": {
              "text": "完成功能开发"
            }
          }
        ]
      }
    },
    {
      "block_element_type": "paragraph",
      "paragraph": {
        "style": {
          "list": {
            "list_type": "bullet",
            "indent_level": 0
          }
        },
        "elements": [
          {
            "paragraph_element_type": "textRun",
            "text_run": {
              "text": "进行用户测试"
            }
          }
        ]
      }
    }
  ]
}
```

### 示例 4：带用户提及和图片（仅进展记录支持）的段落

```json
{
  "blocks": [
    {
      "block_element_type": "paragraph",
      "paragraph": {
        "elements": [
          {
            "paragraph_element_type": "mention",
            "mention": {
              "user_id": "ou_example_user"
            }
          },
          {
            "paragraph_element_type": "textRun",
            "text_run": {
              "text": " 请关注此进度并查看以下图片"
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
            "file_token": "img_example_token",
            "src": "https://example.com/image.png",
            "width": 800,
            "height": 600
          }
        ]
      }
    }
  ]
}
```
