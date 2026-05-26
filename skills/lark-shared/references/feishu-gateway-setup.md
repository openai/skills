# Feishu Gateway 连接配置参考

## 环境

- Windows 11, Hermes Agent v0.14.0
- 飞书应用类型：机器人（bot）模式
- APP ID: `cli_a9660bd345f89cd2`

## 发现

Gateway 有**两层独立配置**，必须同时满足：

| 层 | 配置方式 | 验证 |
|---|---|---|
| lark-cli API 绑定 | `lark-cli config bind --source hermes --identity bot-only` | `hermes status` 显示 `Feishu ✓ configured` |
| Gateway 平台接入 | `config.yaml` 的 `feishu:` 节 或 `hermes gateway setup` TUI | `Feishu ✓ connected` + `gateway_state.json` 里 `"state": "connected"` |

两层都成功后，bot 才能响应消息。

## config.yaml 方式（推荐）

写入 `~/.hermes/config.yaml` 的 `feishu:` 节，Gateway 重启后自动连接：

```yaml
feishu:
  enabled: true
  app_id: "cli_a9660bd345f89cd2"
  app_secret: "JcaGNl...gfam"   # 从 .env 读取
  connection_mode: websocket    # 必须安装 websockets 库
  allow_bots: none             # 必须是 none，不能是 false
```

 Gateway 日志确认成功：
```
[Feishu] Connected in websocket mode (feishu)
✓ feishu connected
Gateway running with 1 platform(s)
```

## 排查

- `hermes status` 显示 `Feishu ✗ not configured`：config.yaml 未写入或 gateway 未重启
- `hermes status` 显示 `Feishu ✓ configured` 但 bot 无响应：两层中只有 API 层连了，Gateway 未接入
- `hermes gateway status` 显示 `not running`：gateway 进程死了，需要 `hermes gateway run` 重启
- `schtasks /Create failed (code 1)`：普通终端没有管理员权限导致计划任务创建失败，需要**管理员权限终端**执行 `hermes gateway install`

## allow_bots 值

| 值 | 含义 |
|---|---|
| `none` | 只接收真人消息 |
| `mentions` | 群里需要 @bot 才响应 |
| `all` | 所有人（包括其他 bot）都接收 |

`allow_bots: false` 会产生警告并 fallback 到 none，不影响连接但有副作用：
```
[Feishu] Unknown allow_bots='false', falling back to 'none'.
```

## Bot 无响应排查路径

**前提：Gateway 已显示 `feishu connected`（`gateway_state.json` 里 `state: "connected"`），但给 bot 发消息没有反应。**

按顺序检查：

1. **是否和 bot 开启了 P2P 会话**
   - 搜索 bot 名称（如「Hermes主脑」）→ 点击进入 → 发送任意消息
   - 用 API 验证：`lark-cli api GET /open-apis/im/v1/chats?page_size=5` → 确认有 chat 记录
   - 0 个聊天记录 = 还没有 P2P 会话

2. **飞书后台是否添加了 `im.message.receive_v1` 事件订阅**
   - 打开 https://open.feishu.cn/app/<APP_ID>/event
   - 确认「事件与回调」里添加了 `im.message.receive_v1` 订阅
   - 没有事件订阅 = Gateway 收不到任何消息

3. **GATEWAY_ALLOW_ALL_USERS 是否为 true**
   - 确认 `.env` 里 `GATEWAY_ALLOW_ALL_USERS=true`（否则 bot 会拒绝所有用户）

4. **检查 Gateway 日志**
   - 有 `Inbound ... message received` = 消息已收到，排查 downstream
   - 只有 `Connected in websocket mode` 没有 inbound = 飞书侧没有推过来事件
   - 重点看步骤 2