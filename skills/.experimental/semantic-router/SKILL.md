---
name: semantic-router
description: 让 AI 代理根据对话内容自动选择最合适的模型。四层识别（系统过滤→关键词→指示词→语义相似度），四池架构（高速/智能/人文/代理），五分支路由，全自动 Fallback 回路。支持 trigger_groups_all 非连续词组命中。
version: 7.9.4
author: halfmoon82
tags: [semantic, routing, model-pools, task-classification, fallback, system-passthrough, production]
requires_approval: true
---

> 🔒 **安全声明**：本技能需要修改 OpenClaw 配置以实现模型路由功能。所有配置变更前会自动备份，支持一键回滚。建议在测试环境验证后再部署到生产环境。

# 🔷 Semantic Router v7.9.3 — 生产级会话路由系统 🔷

**ClawHub**: https://clawhub.ai/halfmoon82/semantic-router  
**版本**: 7.6.3 (生产环境)  
**作者**: halfmoon82
**状态**: ✅ ROM 级固化，完全测试通过

## 🎯 这个技能解决什么问题？

### 核心问题（v7.2 新解决）

你是否遇到过：
- **Cron Job 导致会话频繁重置** — 后台定时任务打断用户交互
- **Discord/Telegram 渠道会话突然清空** — 长任务无法延续
- **AGENTS.md 被截断注入** — 大文件超过 20KB 限制
- **模型自动切换被全局配置覆盖** — 切换不生效

### 解决方案

**会话隔离架构**：
```
用户直连渠道（稳定）
    ├─ 主代理会话 → semantic-router（精准路由）
    └─ Cron Job 隔离会话（独立环境）
        ├─ cloudflared-watchdog
        ├─ Fallback 回切检查
        └─ 自定义后台任务
```

**完整配置引导**：
- 零冲突的智能合并配置
- 预检脚本防止覆盖现有设置
- 自动回滚失败的配置修改

---

## 🔒 安全与权限说明

### 为什么需要这些权限？

| 权限 | 用途 | 安全措施 |
|------|------|----------|
| 读取 `openclaw.json` | 检测现有模型配置 | 只读，不修改 |
| 修改 `openclaw.json` | 添加模型池配置 | **自动备份** + **一键回滚** |
| 执行本地脚本 | 运行配置向导和验证 | 开源脚本，可审计 |
| 重启 Gateway | 应用新配置 | 失败自动回滚 |

### 配置保护机制

1. **前置备份**：任何修改前自动创建带时间戳的备份
2. **语法验证**：JSON 修改后自动验证语法
3. **健康检查**：Gateway 重启后验证服务可用性
4. **自动回滚**：任何步骤失败立即恢复原配置

```bash
# 手动回滚命令
python3 ~/.openclaw/workspace/.lib/config-rollback-guard.py rollback
```

### 代码审计

- 所有脚本开源，位于 `scripts/` 目录
- 核心逻辑 `semantic_check.py` 62KB，完全可审计
- 无网络请求，无数据上报，纯本地运行

---

## 🚀 快速安装

### 第一步：安装技能

```bash
# 从 ClawHub 安装
clawhub install https://clawhub.ai/halfmoon82/semantic-router

# 或手动复制到本地
cp -r ~/.openclaw/workspace/skills/semantic-router ~/my-projects/
```

### 第二步：运行配置引导

```bash
# 启动交互式配置向导
python3 ~/.openclaw/workspace/skills/semantic-router/scripts/setup_wizard.py

# 向导将：
# 1. 检测你的已有配置
# 2. 扫描可用模型
# 3. 推荐三池配置
# 4. 生成 pools.json 和 tasks.json
```

### 第三步：隔离现有 Cron Job（重要！）

```bash
# 列出你的所有 Cron Job
cron list | jq '.jobs[] | {id, name, sessionKey}'

# 对每个使用了渠道会话（telegram/discord/whatsapp）的 Job，执行隔离
cron update {job_id} \
  --patch '{"sessionKey": null, "sessionTarget": "isolated"}'

# 示例（cloudflared-watchdog）
cron update ba28e228-473a-4963-8413-c228762bf2d1 \
  --patch '{"sessionKey": null, "sessionTarget": "isolated"}'
```

### 第四步：验证安装

```bash
# 测试语义检查
python3 ~/.openclaw/workspace/skills/semantic-router/scripts/semantic_check.py \
  "帮我写个Python爬虫" "Highspeed"

# 预期输出
# {
#   "branch": "C",
#   "task": "development",
#   "target_pool": "Intelligence",
#   "primary_model": "claude-opus-4.6",
#   "declaration": "【语义检查 by DeepEye@halfmoon82】P1-任务切换..."
# }
```

---

## 🎓 核心概念

### 四池模型架构

| 池名 | 用途 | 模型示例 | 特点 |
|------|------|---------|------|
| **Highspeed** | 查询、检索、信息搜索 | gemini-2.5-flash | 快速、成本低 |
| **Intelligence** | 开发、编程、复杂任务 | claude-sonnet-4.6 | 精准、能力强 |
| **Humanities** | 内容生成、翻译、写作 | gemini-2.5-pro | 平衡、流畅 |
| **Agentic** | 长上下文代理、Computer Use、专业知识工作 | gpt-5.4 | 1M上下文、工具调用、多步骤 |

### 两步判断法

**Step 1: 关键词 + 指示词检测**
```
"帮我写个爬虫" → 关键词 "写" + "爬虫" → 开发任务 → Intelligence
"继续刚才的" → 指示词 "继续" → 延续当前池 → B 分支
"查一下天气" → 关键词 "查" + "天气" → 查询任务 → Highspeed
"帮我整理这些材料做成PPT" → trigger_groups_all 规则命中 → 代理任务 → Agentic
```

**trigger_groups_all 非连续词组命中（v7.7 新增）**

支持在 tasks.json 中定义分组规则，每条规则内所有分组取 AND，分组内词取 OR，多条规则取 OR：
```json
"trigger_groups_all": [
  [["帮我","自动","用AI"], ["操作","填写","截图"]],
  [["处理","生成","制作"], ["报告","表格","文档","PPT"]]
]
```
说"帮我自动操作浏览器"→ 规则①命中 → Agentic 池。无需精确关键词，口语自然表达即可触发。

**Step 2: 上下文关联度评分**（当 Step 1 无结果时）
```
相似度 ≥ 0.15 → 延续当前会话（B 分支）
相似度 0.08~0.15 → 延续但警告（B+ 分支）
相似度 < 0.08 → 新话题，重置会话（C-auto 分支）
```

### 五分支路由决策

| 分支 | 触发条件 | 动作 | 会话行为 |
|------|--------|------|--------|
| **A** | 关键词完全匹配 | 直接切到目标池 | 切换模型，不重置 |
| **B** | 指示词（延续） | 保持当前 | 无动作 |
| **B+** | 中等关联度（0.08~0.15） | 保持 + 警告 | 输出漂移警告 |
| **C** | 新任务关键词 | 切到目标池 | 切换模型，不重置 |
| **C-auto** | 低关联度（<0.08） | 重置 + 切池 | `/new` + 切换模型 |

---

## ⚙️ 完整配置指南（无冲突）

### 问题：为什么配置容易冲突？

你的 OpenClaw 配置可能已经存在：
- 已配置的模型提供商（OpenAI、Claude、本地 LLM 等）
- 已配置的模型池（可能与语义路由的池名冲突）
- 已定义的任务类型（可能与 tasks.json 冲突）

直接覆盖会导致：❌ 原有配置丢失  
❌ 某些模型无法使用  
❌ Cron Job 执行失败

### 解决方案：智能合并流程

#### **Step 1: 环境检测**

```bash
# 检查现有配置
cat ~/.openclaw/openclaw.json | jq '.models | keys'
# 输出: ["anthropic", "openai", "google-ai", "minimax-cn"]

cat ~/.openclaw/openclaw.json | jq '.agents[0].model'
# 输出: "custom-llmapi-lovbrowser-com/anthropic/claude-haiku-4.5"
```

#### **Step 2: 冲突预检**

```bash
# 备份当前配置
cp ~/.openclaw/openclaw.json \
   ~/.openclaw/backup/openclaw.json.backup-$(date +%s)

# 运行预检脚本
python3 ~/.openclaw/workspace/.lib/config-rollback-guard.py check

# 查看冲突报告
cat ~/.openclaw/logs/config-modification.log
```

#### **Step 3: 智能合并（推荐）**

```bash
# 选项 A: 使用自动合并脚本
python3 ~/.openclaw/workspace/.lib/merge-config.py \
  --existing ~/.openclaw/openclaw.json \
  --new ~/.openclaw/workspace/skills/semantic-router/config/pools.json \
  --output ~/.openclaw/openclaw.json.merged \
  --mode append  # 仅追加，不覆盖

# 选项 B: 手动合并（更安全）
# 编辑 ~/.openclaw/openclaw.json，按以下步骤：
# 1. 检查 .models 字段，仅追加缺失的提供商
# 2. 检查 .agents[].model，如果已有则不修改
# 3. 检查 .env，仅追加缺失的环境变量（如 LOVBROWSER_API_KEY）
```

#### **Step 4: 验证 & 激活**

```bash
# 验证 JSON 语法
python3 -c "import json; json.load(open('~/.openclaw/openclaw.json'))" && echo "✅ JSON 有效"

# 备份原配置
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak

# 应用新配置
cp ~/.openclaw/openclaw.json.merged ~/.openclaw/openclaw.json

# 重启 Gateway（失败时自动回滚）
openclaw gateway restart

# 如果启动失败，自动回滚
python3 ~/.openclaw/workspace/.lib/config-rollback-guard.py rollback
```

---

## 🔧 Cron Job 隔离最佳实践

### ❌ 错误做法（会导致会话重置）

```bash
cron add \
  --name "my-background-task" \
  --sessionKey "agent:main:telegram:direct:123456" \
  --sessionTarget "main" \
  --payload '{"kind": "agentTurn", "message": "执行任务..."}'
```

**为什么错？**
- sessionKey 使用了 Telegram 渠道的直连会话
- 任务消息可能无法匹配 tasks.json 中的关键词
- semantic-router 触发 C-auto 分支 → 会话被强制重置
- 用户的长任务被打断 ❌

### ✅ 正确做法 A：隔离会话（推荐）

```bash
cron add \
  --name "my-background-task" \
  --sessionTarget "isolated" \
  --payload '{
    "kind": "agentTurn",
    "message": "运维任务：执行后台清理。检查磁盘空间...",
    "timeoutSeconds": 60
  }'

# 关键字段：
# - sessionKey: null （让 Gateway 自动分配隔离会话）
# - sessionTarget: "isolated" （完全隔离，语义路由只在这个会话内生效）
```

**优点：**
- ✅ 后台任务不影响用户会话
- ✅ 完全隔离，无须担心关键词匹配
- ✅ 自动过期清理（24h）

### ✅ 正确做法 B：包含显式关键词（如果需要直连会话）

```bash
cron add \
  --name "my-background-task" \
  --sessionKey "agent:main:cron:manual" \
  --payload '{
    "kind": "agentTurn",
    "message": "【运维检查】执行磁盘空间检查。关键词: 检查、运维、系统。"
  }'

# 消息中必须包含 tasks.json 中的关键词
# （检查、运维、系统）→ 可以匹配到 "query" 或 "operations" 任务类型
```

---

## 📊 监控与故障排除

### 检查隔离状态

```bash
# 验证 Cron Job 已隔离
cron list | jq '.jobs[] | select(.name == "cloudflared-watchdog") | {id, name, sessionKey, sessionTarget}'

# 期望输出
# {
#   "id": "ba28e228-473a-4963-8413-c228762bf2d1",
#   "name": "cloudflared-watchdog",
#   "sessionKey": null,              ✅ 已隔离
#   "sessionTarget": "isolated"      ✅ 隔离会话
# }
```

### 查看语义路由日志

```bash
# 实时监控路由决策
tail -f ~/.openclaw/logs/gateway.log | grep "semantic-router"

# 查看特定消息的路由结果
cat ~/.openclaw/workspace/.lib/semantic_check.log | jq '.[] | select(.input | contains("爬虫"))'
```

### 故障排除表

| 症状 | 根因 | 解决方案 |
|------|------|--------|
| "Cron Job 执行失败，超时 30s" | 消息文本不在 tasks.json 中，semantic-router 无法识别 | 方案 A: 改用隔离会话 / 方案 B: 添加关键词 |
| "Discord 会话仍在被重置" | sessionKey 未清空，仍使用渠道会话 | `cron update {id} --patch '{"sessionKey": null}'` |
| "模型没有切换到目标池" | 全局 default_model 覆盖了切换结果 | 改用隔离会话避免全局影响 |
| "配置修改后 Gateway 启动失败" | JSON 语法错误 或 模型不可用 | 运行 `config-rollback-guard.py rollback` 回滚 |

---

## 📋 语义检查声明格式

semantic-router 自动生成的声明格式规范：

### 声明示例
```
【语义检查 by DeepEye@halfmoon82】P2-延续｜模型池:【智能池】｜实际模型:claude-opus-4.6
【语义检查 by DeepEye@halfmoon82】P1-执行开发任务｜新会话→智能池｜实际模型:claude-opus-4.6
```

### 字段说明
| 字段 | 说明 |
|------|------|
| `PX` | P1=开发/自动化, P2=信息检索, P3=内容生成 |
| `模型池:【XXX池】` | 当前所属模型池中文名 |
| `实际模型:` | 当前调用的模型 ID |
| `新会话→` | C分支专用，表示触发 session reset |

完整规范见：[references/declaration-format.md](references/declaration-format.md)

## ⚡ 架构变更说明（2026-03-06）

### M1 机制更新（FIX-0 第一轮）

**原实现**：`prependContext` 包含声明字符串（`declarationPrepend`），用于让 LLM 在回复首行输出声明。

**问题根因**：声明字符串含 `ctx_score`（每消息均不同的浮点相似度）等易变字段，导致：
- 每条用户消息前缀不同 → LLM provider 前缀缓存（prefix cache）每轮全部 miss
- 20 轮对话的历史 input tokens 每轮都重新计费

**新实现**：
- `declarationPrepend` 从 `prependContext` 数组中移除（声明改由 `semantic_check.log` 记录）
- `extractDeclKey` → `extractSkillKey`：缓存键只关心 skill/retry/degrade 激活状态
- 普通消息（无技能激活）`prependContext = undefined` → 用户消息完全干净 → 对话历史 100% cache 命中
- 技能激活时：`prependContext = skillPrepend`（技能指令相对稳定）→ 高缓存命中率

**节省估算**：单活跃会话每日约节省 6-10M tokens（对话历史从 input 变为 cache_read，约 1/10 价格）

### Option C 路由标签（FIX-0 第二轮，2026-03-06 续）

**背景**：用户需要在 Discord/Telegram 回复中看到语义路由声明（当前使用的模型池+模型）。
由于 OpenClaw 主网关的 `message_sending` hook 从未被触发（架构限制：`deliver-DCtqEVTU.js` 的 `globalHookRunner` 在主网关上下文中从不初始化），无法在发送前修改消息内容。
选择 Option C：通过 `prependContext` 注入路由标签指令，由 LLM 自行在首行输出。

**新增函数**：`extractStableRoutingParts(declarationText, fallbackModel)`
- 从 `declarationText` 提取：`pool`、`model`、`sessionType`
- `sessionType: "延续" | "新对话"` — 通过解析 `P\d+-XXX` 分支标签判断：`延续` → 延续，其他 → 新对话

**路由标签格式**：
```
【语义检查·路由】高速池｜gemini-2.5-flash｜延续
【语义检查·路由】智能池｜claude-sonnet-4.6｜新对话
```

**注入逻辑**（`before_agent_start`）：
```typescript
const isChannelSession = isMainAgentSession
  && !sessionKey.includes(":cron:")
  && !sessionKey.includes(":subagent:");   // subagent 不注入

const routingInstruction = routingTag
  ? `请在你回复的第一行，原样输出以下路由标签（不要修改）：${routingTag}`
  : undefined;

// M1 stability: combinedKey = skillKey + routingTagKey
// routingTagKey = "rt:{pool}:{model}:{sessionType}"
// 相同池+模型+会话类型 → 相同 prependContext → LLM prefix cache 命中
```

**缓存稳定性分析**：
| 场景 | routingTagKey | 结果 |
|------|---------------|------|
| 连续对话（同池同模型） | `rt:高速池:gemini-2.5-flash:延续` 不变 | M1 命中，cache hit ✅ |
| 首条新话题消息 | `rt:xxx:yyy:新对话` | cache miss（pool 切换本来就 miss）✅ |
| Gateway 重启后首条 | 任意 key | cache miss（M1 state 清空），第二条起命中 ✅ |

**subagent 排除**：`isChannelSession` 新增 `!sessionKey.includes(":subagent:")` 条件。
原因：subagent session 如 `agent:main:subagent:xxx` 满足 `startsWith("agent:main:")`，若不排除会注入两份 routingInstruction，导致 Discord 回复中路由标签重复出现。

### FIX-4（lockModel 毒化修复）

`modelOverride`/`providerOverride` 已从 `before_agent_start` 返回值中移除。路由仅通过 `sessions.patch` 实现。原 lockModel 时返回 override 会毒化所有 fallback（kimi-coding/zai/minimax 等非 lovbrowser 渠道），导致 All models failed。

## 📚 完整文档

| 文档 | 内容 | 位置 |
|------|------|------|
| **SKILL.md** | 技能说明（本文件） | `/skills/semantic-router/` |
| **README_v3_PRODUCTION.md** | 完整部署指南（英文） | `/skills/semantic-router/` |
| **README_v7.2_生产部署指南_中文.docx** | 完整部署指南（中文 DOCX） | `/skills/semantic-router/` |
| **declaration-format.md** | 声明格式规范（已内置） | `/skills/semantic-router/references/` |
| **完整架构指南** | 五分支、评分算法、Fallback 回路 | `docs/INTELLIGENT_ROUTING_SYSTEM.md` |
| **部署清单** | 7 步完整部署流程 | `docs/ROUTING_DEPLOYMENT_CHECKLIST.md` |

---

## 💡 常见问题

**Q: 我应该选择哪种隔离方案？**
A: 99% 的情况下，选择方案 A（隔离会话）。只有在特殊需求下（需要在用户可见的会话中执行）才选方案 B。

**Q: 隔离会话会占用额外资源吗？**
A: 不会。隔离会话是临时的，自动过期（24h），不会额外占用内存。

**Q: 如何自定义三池模型？**
A: 编辑 `~/.openclaw/workspace/.lib/pools.json`，或运行 `setup_wizard.py` 交互式配置。

**Q: 我的原有配置会被覆盖吗？**
A: 不会。使用智能合并流程（Step 3），仅追加缺失配置，保留原有设置。

---

## 🎓 学习路径

1. **快速体验（5 分钟）**
   - 运行 `setup_wizard.py`
   - 隔离现有 Cron Job
   - 测试语义检查

2. **深入理解（30 分钟）**
   - 阅读本文档
   - 自定义 tasks.json 关键词
   - 配置三池模型

3. **生产部署（1 小时）**
   - 完整配置指南
   - 智能合并配置
   - 故障排除与监控

---

## 📊 版本对比

| 特性 | v7.0 | v7.1 | v7.2 |
|------|------|------|------|
| 关键词匹配 | ✅ | ✅ | ✅ |
| 上下文评分 | ✅ | ✅ | ✅ |
| 三池架构 | ✅ | ✅ | ✅ |
| **会话隔离规则** | ❌ | ❌ | **✅ 新增** |
| **无冲突配置** | ❌ | ❌ | **✅ 新增** |
| **完整故障排除** | ❌ | ❌ | **✅ 新增** |

---

## 📝 许可与支持

- **许可证**: MIT
- **ClawHub**: https://clawhub.ai/halfmoon82/semantic-router
- **反馈**: 在 ClawHub 提交 issue 或改进建议

---

**最后更新**: 2026-03-06 GMT+8
**维护者**: halfmoon82  
**稳定性**: ⭐⭐⭐⭐⭐ (生产级)

---

## ⚖️ 知识产权与归属声明 (Intellectual Property & Attribution)

**Powered by halfmoon82** 🔷

本技能（Semantic Router）由 **halfmoon82** 开发并维护。

- **版权所有**: © 2026 halfmoon82. All rights reserved.
- **官方发布**: [ClawHub](https://clawhub.ai/halfmoon82/semantic-router)
- **许可证**: 本技能采用 MIT 许可证。您可以自由使用、修改和分发，但必须保留原始作者信息及此版权声明。
- **贡献与支持**: 欢迎通过 ClawHub 提交 Issue 或参与讨论。

---
