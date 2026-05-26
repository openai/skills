---
name: lark-shared
version: 1.2.1
description: "Use when first setting up lark-cli, running auth login, switching user/bot identity (--as), handling permission denied or scope errors, needing to update lark-cli, or seeing _notice in JSON output. ALSO use when configuring Hermes-Feishu binding OR troubleshooting 'Feishu gateway connected but bot not responding' — the event subscription pitfall is covered here."
---

# lark-cli 共享规则

本技能指导你如何通过lark-cli操作飞书资源, 以及有哪些注意事项。

## 重要：命令名 on Windows

lark-cli 在 Windows 上不是 `lark` 命令，而是 `lark-cli`。subprocess 调用时需要通过 `cmd /c lark-cli` 或 `["lark-cli.cmd", ...]` 触发，或者用 `subprocess.run` 时直接写 `["lark-cli", "auth", "status"]` 会因为 PATHEXT 查找失败——用 `cmd /c lark-cli` 兜底。

> 注意：pip install lark-cli 是一个占位 stub 包（lark_cli-1.0.3），真正的 CLI 是 npm install -g @larksuite/cli。如果 pip lark-cli 和 npm @larksuite/cli 同时存在，pip 版本会优先执行并打印"请用 npm"的提示。遇到此提示直接卸载 pip 版本：`pip uninstall lark-cli -y`，然后用 npm 版本。

## Hermes–Feishu 两层配置架构（重要）

操作飞书 bot 有**两层完全独立的配置**，缺一不可：

| 层 | 工具 | 作用 |
|---|---|---|
| **lark-cli 绑定** | `lark-cli config bind --source hermes --identity bot-only` | 授予 Hermes Agent 调用飞书 **API** 的能力（发消息、查日历等） |
| **Gateway 平台接入** | `config.yaml` 的 `feishu:` 节 | 让 Hermes Gateway 能**接收和响应**飞书 bot 的消息事件 |

**常见混淆**：执行完 `lark-cli config bind` 后，`hermes status` 会显示 `Feishu ✓ configured`，这仅代表 API 层已绑定。**Gateway 层面仍然是 `No messaging platforms enabled`**，用户直接给 bot 发消息不会有任何响应。

**Gateway 平台接入：config.yaml（推荐）**

Gateway 支持通过 `~/.hermes/config.yaml` 直接配置飞书平台，写入后重启 gateway 即可自动连接。

```yaml
feishu:
  enabled: true
  app_id: "你的APP_ID"
  app_secret: "你的APP_SECRET"   # 从 .env 的 FEISHU_APP_SECRET 读取
  connection_mode: websocket      # 必须安装 websockets 库
  allow_bots: none               # 必须是 none，不能是 false
```

**必须安装 `websockets` 库**，否则 WebSocket 连接失败：
```
RuntimeError: websockets not installed; websocket mode unavailable
```
修复：`pip install websockets`（在 hermes-env venv 中执行）

**allow_bots 必须是 `none`，不能用 `false`**：
- `false` 产生警告：`Unknown allow_bots='false', falling back to 'none'`
- `none` 直接成功，无警告

**验证网关是否正常连接：**
- `hermes status` → Feishu 应显示 `✓ connected`（而非仅 `configured`）
- 或检查 `~/.hermes/gateway_state.json` 中 `"feishu": {"state": "connected"}`
- 直接给 bot 发送一条消息 → 应收到自动回复

**相关文件：**
- `references/feishu-gateway-setup.md` — 完整排查路径、allow_bots 详解、常见报错。
- `references/windows-lark-cli-patterns.md` — Windows 上 lark-cli 的执行模式、编码问题、阻塞命令处理、应用切换完整流程。

## Bot 无响应排查路径（Gateway connected 但消息无反应）

按顺序检查：

1. **是否和 bot 开启了 P2P 会话**
   - 搜索 bot 名称（如「Hermes主脑」）→ 点击进入 → 发送任意消息
   - 用 API 验证：`lark-cli api GET /open-apis/im/v1/chats?page_size=5` → 确认有 chat 记录
   - 0 个聊天记录 = 还没有 P2P 会话

2. **飞书后台是否添加了 `im.message.receive_v1` 事件订阅**（最常见遗漏）
   - 打开 https://open.feishu.cn/app/<APP_ID>/event
   - 「事件与回调」→ 添加事件 → 搜索并添加 `im.message.receive_v1`
   - **没有事件订阅 = 即使 Gateway connected，消息也永远不会推过来**
   - 这是飞书开发者后台的配置，跟 lark-cli/Gateway 是两回事

3. **GATEWAY_ALLOW_ALL_USERS 是否为 true**
   - 确认 `.env` 里 `GATEWAY_ALLOW_ALL_USERS=true`（否则 bot 会拒绝所有用户）

4. **检查 Gateway 日志**
   - 有 `Inbound ... message received` = 消息已收到，排查 downstream
   - 只有 `Connected in websocket mode` 没有 inbound = 飞书侧没有推过来事件
   - 重点看步骤 2

## Hermes 上下文绑定（首次配置时重要）

当 `lark-cli` 运行在 Hermes 环境下时（检测到 HERMES_HOME 等环境变量），会提示：

```
"lark-cli is not bound to it"
```

这是因为 lark-cli 需要和 Hermes 的飞书凭证绑定。**不要在用户确认前直接执行 bind 命令**，按以下流程：

1. 读取 `.env` 中的 `FEISHU_APP_ID`
2. 检查 `.env` 中是否有 `FEISHU_APP_SECRET`：
   - 如果只有 APP_ID 没有 APP_SECRET → 先让用户提供 AppSecret，追加到 `.env`，再执行绑定
   - AppSecret 在飞书开放平台 → 打开 https://open.feishu.cn/app/{APP_ID}/scope 凭证与基础信息 页面获取
3. 询问用户身份策略：
   - `bot-only`（默认，安全，只能用应用身份，无法访问用户个人日历/邮箱）
   - `user-default`（可代理用户身份，能访问用户个人资源）
4. 用户确认后执行：
   ```bash
   lark-cli config bind --source hermes --identity bot-only
   # 或
   lark-cli config bind --source hermes --identity user-default
   ```

## 重新连接 / 重新绑定（Hermes 环境内）

当用户想「删除飞书重新连接」时，在 Hermes 环境内**不能**用 `config init --new`（会被拒绝，即使已 remove），正确流程：

1. `lark-cli config remove` — 删除当前绑定
2. `lark-cli config bind --source hermes --identity bot-only` — 重新绑定到 Hermes 现有应用

这两步不需要用户在浏览器授权，是纯本地操作，秒级完成。

## 配置初始化

首次使用需运行 `lark-cli config init` 完成应用配置。

### 场景区分：绑定同一应用 vs 绑定新应用

| 场景 | 命令 | 说明 |
|------|------|------|
| 重新绑定 Hermes 已有的同一个飞书应用 | `lark-cli config bind --source hermes --identity bot-only` | API 凭证同步，不需要浏览器操作 |
| 绑定一个**全新的**飞书应用（替换旧应用） | `lark-cli config init --new --force-init` | 需要浏览器授权，`--force-init` 在 Hermes 上下文中必须加 |
| 只删除当前配置，不重新绑定 | `lark-cli config remove` | 清空绑定 |

**关键坑**：在 Hermes 上下文中（检测到 HERMES_HOME 等环境变量），`config init --new` 会被拒绝并提示 "config init is refused inside hermes context"。必须加 `--force-init` 标志才能创建新应用。不加会白跑一趟。

### Windows 编码问题与阻塞命令处理

`config init` 是**阻塞命令**，会等待用户在浏览器完成授权后才退出。在 Windows 上还有编码陷阱：

- `cmd /c lark-cli.cmd` 的 stdout/stderr 是 UTF-16LE 编码，通过 terminal 工具读取会显示乱码
- **解决方案**：用 `subprocess.Popen` 将输出重定向到文件（`stdout=open(outfile, "wb")`），等几秒后读文件，文件内容是正确的 UTF-8

```python
import subprocess, os, time

proc = subprocess.Popen(
    ["lark-cli.cmd", "config", "init", "--new", "--force-init"],
    stdout=open(outfile, "wb"),
    stderr=subprocess.STDOUT,
    cwd="C:\\Users\\Administrator",
    env=os.environ.copy()
)

time.sleep(5)  # 等待 URL 输出

with open(outfile, "rb") as f:
    text = f.read().decode("utf-8", errors="replace")
# text 中包含授权 URL 和 QR code
```

**URL 转发规则**：当命令输出 `verification_url`、`verification_uri_complete`、`console_url` 等 URL 字段时，必须将 URL exactly as returned by the CLI 转发给用户，并把它视为不可修改的 opaque string；不要做 URL encode/decode，不要补 `%20`、空格或标点，不要重新拼接 query，不要改写成 Markdown link text，建议用只包含原始 URL 的代码块单独输出。

**不要反复尝试失败的执行方式**：如果 execute_code 超时或编码失败，不要重复同样的方式。立即切换到文件重定向方案。

## 认证

### 身份类型

两种身份类型，通过 `--as` 切换：

| 身份 | 标识 | 获取方式 | 适用场景 |
|------|------|---------|---------|
| user 用户身份 | `--as user` | `lark-cli auth login` 等 | 访问用户自己的资源（日历、云空间等） |
| bot 应用身份 | `--as bot` | 自动，只需 appId + appSecret | 应用级操作,访问bot自己的资源 |

### 身份选择原则

输出的 `[identity: bot/user]` 代表当前身份。bot 与 user 表现差异很大，需确认身份符合目标需求：

- **Bot 看不到用户资源**：无法访问用户的日历、云空间文档、邮箱等个人资源。例如 `--as bot` 查日程返回 bot 自己的（空）日历
- **Bot 无法代表用户操作**：发消息以应用名义发送，创建文档归属 bot
- **Bot 权限**：只需在飞书开发者后台开通 scope，无需 `auth login`
- **User 权限**：后台开通 scope + 用户通过 `auth login` 授权，两层都要满足

### 权限不足处理

遇到权限相关错误时，**根据当前身份类型采取不同解决方案**。

错误响应中包含关键信息：
- `permission_violations`：列出缺失的 scope (N选1)
- `console_url`：飞书开发者后台的权限配置链接
## 配置初始化

首次使用需运行 `lark-cli config init` 完成应用配置。

### 场景一：Hermes 环境内绑定已有应用

在 Hermes 上下文中（检测到 HERMES_HOME 等环境变量），`config init --new` 会被拒绝。此时：

- **绑定到 Hermes 现有应用**（推荐）：`lark-cli config bind --source hermes --identity bot-only`
- **创建全新应用**：`lark-cli config init --new --force-init`（用户必须明确要求）

### 场景二：完全删除旧应用并创建新应用

1. 先删除旧配置：`lark-cli config remove`
2. 用 `--force-init` 创建新应用（见下文）
3. 更新 Hermes 配置：同时修改 `.env`（FEISHU_APP_ID + FEISHU_APP_SECRET）和 `config.yaml`（feishu.app_id + feishu.app_secret）
4. config.yaml 中 feishu.app_secret 应引用环境变量 `${FEISHU_APP_SECRET}`，不要硬编码
5. 重启 Gateway：`hermes gateway restart`

### 飞书应用切换注意事项

当前飞书应用（2025年5月更换）：
- APP ID: `cli_aa99eeb706b8dbcb`
- APP Secret: 存储在 `.env` 的 `FEISHU_APP_SECRET`
- Gateway 配置: `config.yaml` 的 `feishu.app_id` 和 `app_secret: ${FEISHU_APP_SECRET}`

**切换应用后的验证步骤：**
1. `hermes status` → Feishu 应显示 `✓ connected`（不是仅 `configured`）
2. 直接给 bot 发一条消息 → 应收到自动回复
3. 检查 `~/.hermes/gateway_state.json` 中 `"feishu": {"state": "connected"}`

**事件订阅必须在新的飞书开发者后台重新添加**：切换应用后，原有的 `im.message.receive_v1` 事件订阅不会迁移到新应用。打开 https://open.feishu.cn/app/<新APP_ID>/event 重新添加。

### config init 执行方法（重要：Windows 特殊处理）

`config init --new` 是**阻塞命令**，会等到用户在浏览器完成操作或超时。输出包含 QR 码 + 授权 URL。

**Windows 上有 UTF-16LE 编码问题**：通过 bash/cmd 调用 lark-cli 时，stdout 输出是 UTF-16LE 编码，直接读取会看到乱码。

**推荐方法 — Python subprocess + 文件重定向**：

```python
import subprocess, time

proc = subprocess.Popen(
    ["lark-cli.cmd", "config", "init", "--new", "--force-init"],
    stdout=open("C:\\Users\\Administrator\\lark_init_output.txt", "wb"),
    stderr=subprocess.STDOUT,
    cwd="C:\\Users\\Administrator",
    env=os.environ.copy()
)

time.sleep(5)  # 等待 URL 输出

with open("C:\\Users\\Administrator\\lark_init_output.txt", "rb") as f:
    data = f.read()

text = data.decode("utf-8", errors="replace")
# text 中包含 QR 码和 "打开以下链接配置应用:" + URL
```

**不推荐**：`terminal(background=True)` + `process(poll)` — bash 层的 UTF-16LE 输出无法正确解码。

**速度提示**：用户对等待极其敏感。用文件重定向方式可在 5 秒内拿到 URL，避免长时间阻塞。

**URL 转发规则**：当命令输出 `verification_url`、`verification_uri_complete`、`console_url` 等 URL 字段时，必须将 URL exactly as returned by the CLI 转发给用户，并把它视为不可修改的 opaque string；不要做 URL encode/decode，不要补 `%20`、空格或标点，不要重新拼接 query，不要改写成 Markdown link text，建议用只包含原始 URL 的代码块单独输出。

**规则**：auth login 必须指定范围（`--domain` 或 `--scope`）。多次 login 的 scope 会累积（增量授权）。

#### Agent 代理发起认证（推荐）

当你作为 AI agent 需要帮用户完成认证时，使用 background 方式执行以下命令发起授权流程, 并将授权链接原样发给用户。**Windows 上同样有 UTF-16LE 编码问题，用文件重定向方案（见上方「Windows 编码问题与阻塞命令处理」）：**

```python
import subprocess, os, time

proc = subprocess.Popen(
    ["lark-cli.cmd", "auth", "login", "--scope", "calendar:calendar:readonly"],
    stdout=open(outfile, "wb"),
    stderr=subprocess.STDOUT,
    cwd="C:\\Users\\Administrator",
    env=os.environ.copy()
)

time.sleep(5)
with open(outfile, "rb") as f:
    text = f.read().decode("utf-8", errors="replace")
# 提取授权 URL 发给用户
```

## 更新检查

lark-cli 命令执行后，如果检测到新版本，JSON 输出中会包含 `_notice.update` 字段（含 `message`、`command` 等）。

**当你在输出中看到 `_notice.update` 时，完成用户当前请求后，主动提议帮用户更新**：

1. 告知用户当前版本和最新版本号
2. 提议执行更新（同时更新 CLI 和 Skills）：
   ```bash
   lark-cli update
   ```
3. 更新完成后提醒用户：**退出并重新打开 AI Agent** 以加载最新 Skills

**重要**：始终使用 `lark-cli update` 更新，它会同时更新 CLI 和 AI Skills。

**规则**：不要静默忽略更新提示。即使当前任务与更新无关，也应在完成用户请求后补充告知。

## 安全规则

- **禁止输出密钥**（appSecret、accessToken）到终端明文。
- **写入/删除操作前必须确认用户意图**。
- 用 `--dry-run` 预览危险请求。

## 高风险操作的审批协议（exit 10）

lark-cli 对高风险写操作（`risk: "high-risk-write"`）有强制确认门禁。当你不带 `--yes` 调用这类命令时，CLI 会退出码 `10`、并在 stderr 返回如下结构化 envelope：

```json
{
  "ok": false,
  "error": {
    "type": "confirmation_required",
    "message": "drive +delete requires confirmation",
    "hint": "add --yes to confirm",
    "risk": {
      "level": "high-risk-write",
      "action": "drive +delete"
    }
  }
}
```

**遇到这种情况，不要当普通错误放弃。** 按以下流程处理：

1. **识别**：看到子进程 exit code = `10` 且 stderr JSON 里 `error.type == "confirmation_required"`
2. **向用户确认**：把 `error.risk.action` 和关键参数展示给用户，明确告知"这是高风险操作"，等待用户显式同意
3. **用户同意** → 在你**原始 argv 的末尾追加 `--yes`** 后重试
4. **用户拒绝** → 终止流程，不要擅自改写参数或跳过门禁

**绝对不允许**：
- 看到 exit 10 就默认加 `--yes` 静默重试（这等于禁用门禁）
- 把 `confirmation_required` 当网络错误/权限错误处理
- 在用户没明确同意的前提下追加 `--yes` 重试
- 用 `sh -c` 等 shell 方式拼接命令重试——用 `exec.Command(argv...)` 参数数组形式，避免 shell 解析把用户参数当作语法

提前预判：想先让用户 review 危险操作的具体请求，调用时加 `--dry-run`——它不触发门禁，会打印完整请求详情（URL / body / params），你可以把这个预览给用户看过再去真正执行。

### 如何识别一条命令是高风险

- shortcut：`lark-cli <service> +<cmd> --help` 顶部会显示 `Risk: high-risk-write`
- service 命令：`lark-cli schema <service>.<resource>.<method> --format json` 的返回值里 `"risk": "high-risk-write"`