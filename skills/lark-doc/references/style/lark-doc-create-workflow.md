# 从零创作工作流

用户提供主题、需求或简要说明，需要生成一份新的飞书文档时，遵循本工作流。

## 核心方法论 — Code-Act Loop

通过自适应的 **Code-Act Loop** 驱动文档创作，而非固定模板式的工作流。每次任务都循环执行：

1. **Plan（规划）** — 根据用户目标和文档当前状态，评估下一步该做什么
2. **Execute（执行）** — 运行相应的 `lark-cli docs` 命令，或 **spawn** Agent 子任务并行推进
3. **Observe（观察）** — 检查命令输出，验证正确性，核查样式是否达标
4. **Iterate（迭代）** — 如需调整，回到 Plan 继续循环

循环在文档达到质量标准且满足用户需求时结束。不要试图一次性产出完美内容——迭代打磨效果更好。根据用户实际需求灵活决定文档结构和版块，而不是套用固定模板。


## 典型 Code-Act Loop 流程

### 第一波 — 规划与骨架（串行）

1. 分析用户需求：受众、目的、范围
2. 设计大纲——每个 h1/h2 章节至少规划 1 个非文本 block
3. `docs +create --api-version v2` **只建骨架**：标题 + 开头 `<callout>` + 各级标题 + 每节一句占位摘要
   - ⚠️ **不要**一次性把完整章节内容塞进 `--content`。超长 `--content` 容易触发字符/参数限制。
   - 完整内容留到第二波，由各 Agent 用 `docs +update --command append` 或 `block_insert_after` 分段写入。

### 第二波 — 内容撰写（并行 Agent）

4. Spawn Agent 并行撰写各章节。每个 Agent 需收到：
   - 文档 token、负责的章节范围、期望的 block 类型
   - `lark-doc-xml.md` 和 `lark-doc-style.md` 的完整路径（Agent 须先读取）
   - 使用 `docs +update --command append` 或 `block_insert_after` 写入

### 第三波 — 整合审查 + 画板意图识别（串行）

5. `docs +fetch --api-version v2 --detail with-ids` 获取文档，审查整体效果
6. 评估样式达标（富 block 密度、元素多样性、连续 `<p>` 数量）
7. **画板意图识别**：逐章节扫描，按 `lark-doc-style.md`「画板意图识别」表判断是否有段落适合用图表达。记录需要插图的章节及推荐的画板类型

### 第四波 — 润色与图表（并行 Agent）
8. Spawn Agent 定向改进：（结合 `lark-doc-style.md` 润色）
   - **优先处理第三波识别出的画板需求**：简单图直接 `<whiteboard type="mermaid|plantuml">`，复杂图 spawn Agent 使用 **lark-whiteboard** skill
   - 文字密集章节转为 `<table>`/`<grid>`/`<callout>`
   - 主要章节间补充 `<hr/>`
   - 本地图片使用 `docs +media-insert` 插入


## Agent 子任务要求

Spawn Agent 时必须提供：文档 token、章节范围（标题/block ID）、`lark-doc-xml.md` 和 `lark-doc-style.md` 路径、具体的 `docs +update` command 和 `--block-id`。
