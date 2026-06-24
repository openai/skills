# Browser Automation 与飞书集成

## 典型场景

用户通过飞书消息远程控制 Hermes，让它操作浏览器：

1. 用户发消息给飞书 bot（如"帮我查一下百度"）
2. Hermes Gateway 收到消息 → agent 处理
3. Agent 调用 browser 工具控制 Chrome
4. 结果通过飞书消息返回给用户

## 配置要点

- Gateway 必须 connected（`hermes status` → Feishu ✓ connected）
- 飞书 bot 必须开启了 `im.message.receive_v1` 事件订阅
- Chrome CDP 端口 9222 必须在本地可访问

## 验证联动是否正常

1. 直接给 bot 发消息 → 应该收到回复
2. Gateway 日志有 `Inbound ... message received`
3. Chrome 在本地运行（`netstat -an | findstr 9222`）

## 常用组合命令

```bash
# 检查飞书连接状态
hermes status

# 检查 Gateway 日志
hermes logs --tail 20

# 检查 Chrome 是否运行
netstat -an | findstr 9222

# 重启 Gateway
hermes gateway restart
```