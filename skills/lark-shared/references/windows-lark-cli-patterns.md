# Windows 上 lark-cli 的执行模式

## 核心问题

lark-cli 是通过 npm 安装的 Node.js 程序 (`@larksuite/cli`)。在 Windows 上：

1. **命令名**：不是 `lark`，而是 `lark-cli` 或 `lark-cli.cmd`
2. **Bash 层编码问题**：通过 Git Bash / MSYS 调用时，stdout 输出是 UTF-16LE 编码，直接读取会看到 `\u0000` 交替的乱码
3. **阻塞命令**：`config init` 和 `auth login` 会阻塞等待用户在浏览器完成操作

## 推荐执行方式

### 方式一：Python subprocess（最可靠）

```python
import subprocess, os

env = os.environ.copy()
result = subprocess.run(
    ["lark-cli.cmd", "config", "show"],  # 注意用 .cmd 后缀
    capture_output=True, timeout=10,
    cwd="C:\\Users\\Administrator",
    env=env
)
stdout = result.stdout.decode("utf-8", errors="replace")
stderr = result.stderr.decode("utf-8", errors="replace")
```

- stderr 通常是 JSON 格式的结构化输出
- stdout 通常是格式化的显示文本

### 方式二：文件重定向（用于阻塞命令）

```python
import subprocess, os, time

outfile = "C:\\Users\\Administrator\\lark_init_output.txt"
proc = subprocess.Popen(
    ["lark-cli.cmd", "config", "init", "--new", "--force-init"],
    stdout=open(outfile, "wb"),
    stderr=subprocess.STDOUT,
    cwd="C:\\Users\\Administrator",
    env=os.environ.copy()
)

time.sleep(5)  # 等待 URL 出现

with open(outfile, "rb") as f:
    text = f.read().decode("utf-8", errors="replace")
# 从 text 中提取 URL
```

### 不推荐的方式

- `terminal()` 通过 bash 执行 `lark-cli` — UTF-16LE 乱码
- `terminal(background=True)` + `process(poll)` — 同样的编码问题
- `cmd /c "lark-cli ..."` — 有时可用但输出仍可能是 UTF-16LE

## config init 输出格式

成功时输出包含：
1. ASCII art QR 码
2. `打开以下链接配置应用:` 提示文字
3. `https://open.feishu.cn/page/cli?user_code=XXXX-XXXX&...` 授权 URL

从输出中提取 URL 的正则：`r'https://open\.feishu\.cn/page/cli\?user_code=[A-Z0-9]{4}-[A-Z0-9]{4}[^\s]*'`

## lark-cli 输出的 JSON 结构

大多数命令的 stderr 是 JSON：
- 成功：`{"ok": true, ...}` 或直接是数据对象
- 失败：`{"ok": false, "error": {"type": "...", "message": "...", "hint": "..."}}`
- 更新提示：`{"_notice": {"update": {"message": "...", "command": "..."}}}`

## 应用切换完整流程

当用户需要切换到新的飞书应用时：

1. `lark-cli config remove` — 删除旧配置
2. Python subprocess + 文件重定向执行 `lark-cli config init --new --force-init` — 创建新应用
3. 提取授权 URL，用户在浏览器完成配置
4. 更新 `.env`：`FEISHU_APP_ID` 和 `FEISHU_APP_SECRET`
5. 更新 `config.yaml`：`feishu.app_id` 和 `feishu.app_secret: ${FEISHU_APP_SECRET}`
6. `lark-cli config bind --source hermes --identity bot-only` — 绑定到 Hermes
7. `hermes gateway restart` — 重启 Gateway
