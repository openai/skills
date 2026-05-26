# Sheets Cell Images

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

这份 reference 汇总单元格图片写入能力：

- `+write-image`

<a id="write-image"></a>
## `+write-image`

对应命令：`lark-cli sheets +write-image`

特性：

- 将本地图片文件写入到指定单元格
- 支持格式：PNG、JPEG、JPG、GIF、BMP、JFIF、EXIF、TIFF、BPG、HEIC
- `--range` 必须表示单个单元格，如 `A1` 或 `<sheetId>!B2:B2`
- `--name` 默认取 `--image` 的文件名

```bash
# 写入图片到指定单元格
lark-cli sheets +write-image --spreadsheet-token "shtxxxxxxxx" \
  --range "<sheetId>!B2:B2" \
  --image "./logo.png"

# 使用 URL + sheet-id，指定单个单元格
lark-cli sheets +write-image --url "https://example.larksuite.com/sheets/shtxxxxxxxx" \
  --sheet-id "<sheetId>" --range "C3" \
  --image "./chart.jpg"

# 自定义图片名称
lark-cli sheets +write-image --spreadsheet-token "shtxxxxxxxx" \
  --range "<sheetId>!A1:A1" \
  --image "./output.png" --name "revenue_chart.png"
```

参数：

| 参数 | 必填 | 说明 |
|------|------|------|
| `--url` | 否 | 电子表格 URL（与 `--spreadsheet-token` 二选一） |
| `--spreadsheet-token` | 否 | 表格 token |
| `--range` | 是 | 目标单元格：`<sheetId>!A1:A1` 或相对单元格 |
| `--sheet-id` | 否 | 工作表 ID |
| `--image` | 是 | 本地图片文件的相对路径 |
| `--name` | 否 | 图片文件名（默认取 `--image` 的文件名） |
| `--dry-run` | 否 | 仅打印请求，不执行 |

输出：

- `spreadsheetToken`
- `updateRange`
- `revision`

## 参考

- [cell-data](lark-sheets-cell-data.md#write) — 写入普通单元格数据
- [float-images](lark-sheets-float-images.md) — 管理浮动图片
