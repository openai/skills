---
name: skill-safe-install
version: 2.1.0
description: L0 级技能安全安装流程。触发“安装技能/安全安装/审查权限”时，强制执行 Step0-5（查重→检索→审查→沙箱→正式安装→白名单）。
---

# Skill Safe Install (L0)

## 触发条件（L0 强制）
当用户消息包含以下关键词时，**必须**触发本技能并执行完整流程：
- 安装技能
- 安全安装
- 技能审查
- 检查技能权限
- 安装这个 skill / install skill

> 规则：命中关键词后，不得跳过 Step 0-5 中任一步骤。

---

## 全流程（Step 0 → Step 5）

### Step 0: 查重检查
```bash
clawhub list
```
检查：
- 是否已安装
- 是否已在 `allowBundled`

### Step 1: 搜索候选
```bash
clawhub search <skill>
```
输出：候选名称、简介、热度。

### Step 2: 安全审查（必须）
```bash
clawhub inspect <skill>
```
检查：
- 作者与更新日期
- 依赖/环境变量（API Key、OAuth）
- 网络与外部系统访问面
- 命令执行风险（sudo/rm/curl|bash 等）

### Step 3: 沙箱安装（隔离目录）
> clawhub 当前无 `--sandbox` 参数，使用隔离 workdir 替代。

```bash
TMP=$(mktemp -d)
clawhub --workdir "$TMP" --dir skills install <skill>
```

### Step 4: 正式安装
```bash
clawhub install <skill>
```

### Step 5: 白名单写入（需用户明确授权）
```bash
# 备份
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup.$(date +%Y%m%d_%H%M%S)

# 写入 allowBundled
jq '.skills.allowBundled += ["<skill>"] | .skills.allowBundled |= unique' ~/.openclaw/openclaw.json > /tmp/openclaw.json.new
mv /tmp/openclaw.json.new ~/.openclaw/openclaw.json
```

---

## 风险分级建议
- 低风险：纯方法论/文本指导、无额外凭据要求
- 中风险：需要 API Key，但访问范围清晰
- 高风险：OAuth 连接多系统、可执行命令范围大

---

## 输出模板（执行时）
- `[Step 0/5] 查重：...`
- `[Step 1/5] 搜索：...`
- `[Step 2/5] 审查：风险等级=...`
- `[Step 3/5] 沙箱：通过/失败`
- `[Step 4/5] 安装：通过/失败`
- `[Step 5/5] 白名单：待授权/已写入`

---

## 示例
用户说：`安装 debug-pro`
1. `clawhub search debug-pro`
2. `clawhub inspect debug-pro`
3. 隔离目录沙箱安装
4. 正式安装
5. 征求授权后写入 allowBundled
