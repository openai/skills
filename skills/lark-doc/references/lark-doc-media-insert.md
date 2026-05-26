
# docs +media-insert（文档末尾插入图片/文件）

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

把"创建空 block → 上传文件 → 设置 token"三步合并成一个命令，在**文档末尾**插入本地图片或文件。

## 来源选择（Agent 必读）

> **最高优先级：用户明确指定了来源，就严格按用户的来。** 下面的启发式只在用户没表态时生效。
>
> - 用户说"把这张截图插进去"、"用剪切板里的图"、"我刚复制的" → 无条件走 `--from-clipboard`。
> - 用户说"用 `~/Downloads/foo.png`"、"插本地这个文件"、给了具体路径 → 无条件走 `--file`。
> - 用户两者都没说清 → 按下表的启发式推断。
>
> 即使推断看起来更"优"（比如用户说了路径但你觉得走剪切板更省事），也**不要自作主张**换来源。要换，先问。

按下列顺序判断，**不要反向做**：

| 用户的图片来源 | 命令 | 禁止做法 |
|----------------|------|----------|
| 图片已经在剪切板里（截图快捷键、从飞书/浏览器复制、从设计稿复制） | `--from-clipboard` | ❌ 不要先把剪切板存到本地文件再用 `--file`。多一步文件 I/O，还得清理临时文件。 |
| 图片是磁盘上的真实文件 | `--file <path>` | — |
| 图片是 URL | 先下载到本地 → `--file`；或用 `drive` 相关命令 | — |

`--from-clipboard` 走进程内存直传，不产生临时文件；macOS / Windows 内置支持，Linux 需要 `xclip` 或 `wl-paste` 或 `xsel` 任一。

### 剪切板为空时的 fallback

`--from-clipboard` 失败（剪切板里不是图片 / 没有图片 / Linux 上三个工具都没装）时，命令会返回 `clipboard contains no image data`（或类似的平台错误）。**这不是错误退出理由，而是 fallback 信号。**

**Agent 的标准处置顺序**（每一步失败再进下一步，不要并行）：

1. 先用 `--from-clipboard` 试一次。
2. 如果返回"no image data"类错误，**向用户明确说明剪切板里没有可识别的图片**，请用户提供本地文件路径或重新复制一张图。
3. 拿到本地路径后，用 `--file <path>` 重试**同一条插入命令**（其他参数如 `--doc` / `--align` / `--caption` 保持不变）。

**禁止做法**：
- ❌ 不要悄悄把空剪切板当"成功但没插入"处理。必须提示用户。
- ❌ 不要在剪切板失败后自行瞎猜某个本地文件路径（比如最近修改的 png）。必须让用户给路径。
- ❌ 不要用"先让用户保存剪切板到磁盘再 `--file`"的建议绕过 `--from-clipboard`，当且仅当剪切板确实没图片时才退回本地路径。

## 命令

```bash
# 🟢 推荐：从剪切板直接插入（无需先存盘）
lark-cli docs +media-insert --doc doxcnXXX --from-clipboard

# 从本地文件插入
# 除了上传本地文件，还可以在 `docs +update` 时直接通过网络 URL 插入图片，无需先下载到本地：
lark-cli docs +update --api-version v2 --doc "<doc_id>" --command block_insert_after \
  --block-id "目标 block_id" \
  --content '<img href="https://example.com/photo.png"/>'

# 插入图片（默认）
lark-cli docs +media-insert --doc doxcnXXX --file ./image.png

# doc 支持直接传 docx URL（自动提取 document_id）
lark-cli docs +media-insert --doc "https://xxx.feishu.cn/docx/doxcnXXX" --from-clipboard

# 如果上一步是 create-doc，优先传返回值里的 doc_id
# 不要把 /wiki/... 形式的 doc_url 直接传给 docs +media-insert
lark-cli docs +media-insert --doc doxcnReturnedByCreateDoc --file ./image.png

# 插入文件（非图片）
lark-cli docs +media-insert --doc doxcnXXX --file ./spec.pdf --type file

# 图片对齐与描述（caption）
lark-cli docs +media-insert --doc doxcnXXX --from-clipboard --align center --caption "架构图"
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--doc <id>` | 是 | 文档 ID 或 docx URL（仅支持 `/docx/<document_id>` 形式自动提取；**不支持 `/wiki/...` URL 自动提取**） |
| `--from-clipboard` | 二选一 | 从系统剪切板读取图片（与 `--file` 互斥）。macOS/Windows 内置支持，Linux 需要 `xclip` / `wl-paste` / `xsel` 之一。 |
| `--file <path>` | 二选一 | 本地文件路径（文件大于 20MB 时自动切换分片上传） |
| `--type <type>` | 否 | `image`（默认）或 `file`。`--from-clipboard` 目前只产出 image。 |
| `--align <align>` | 否 | 仅图片：`left` / `center`（默认）/ `right` |
| `--caption <text>` | 否 | 仅图片：图片描述 |

> [!IMPORTANT]
> 如果上一步是 [`lark-doc-create`](lark-doc-create.md)，并且它在知识库/知识空间场景下返回的是 `/wiki/...` 形式的 `doc_url`，后续调用 `docs +media-insert` 时应优先传 `doc_id`，不要直接传这个 `doc_url`。

## 平台注意（仅 `--from-clipboard`）

| 平台 | 依赖 | 典型错误 |
|------|------|---------|
| macOS | osascript（内置） | 剪切板为空 / 不是图片 → "clipboard contains no image data" |
| Windows | PowerShell + System.Windows.Forms（内置） | 同上 |
| Linux | `xclip` 或 `wl-paste` 或 `xsel` 任一 | 都没安装 → 报错会提示用发行版包管理器安装 |

命令不支持读取 TIFF 等非 PNG/JPEG/GIF/WebP/BMP 的冷门格式；遇到这类剪切板会返回 "contains no image data"，此时才考虑先用系统工具转成文件再 `--file`。

## 输出

命令成功后会输出 JSON，包含：`document_id`、`block_id`、`file_token`、`file_name`（剪切板路径下为 `clipboard.png`）、`type`。

> [!CAUTION]
> 这是**写入操作**（会修改文档内容）—— 执行前必须确认用户意图。

## 参考

- [lark-doc-fetch](lark-doc-fetch.md) — 获取文档内容（可用于确认插入后的结果、以及提取媒体 token）
- [lark-shared](../../lark-shared/SKILL.md) — 认证和全局参数
