# Cloud 功能

## 目录
- [代理与隐身](#代理与隐身)
- [Webhook](#webhook)
- [工作区](#工作区)
- [Skills](#skills)
- [MCP 服务器](#mcp-服务器)
- [实时视图](#实时视图)

---

## 代理与隐身

隐身模式默认开启 — 反指纹识别、CAPTCHA 解决、广告/Cookie 阻止、Cloudflare 绕过。

### 住宅代理（195+ 国家）

默认：美国住宅代理始终活跃。

```python
# 常用国家
session = await client.sessions.create(proxy_country_code="us")  # 或 gb, de, fr, jp, au, br, in, kr, ca, es, it, nl, se, sg...
```

### 自定义代理（HTTP 或 SOCKS5）

```python
from browser_use_sdk import CustomProxy

session = await client.sessions.create(
    custom_proxy=CustomProxy(
        url="http://proxy-host:8080",
        username="user",
        password="pass",
    )
)
```

### 禁用代理（不推荐）

```python
session = await client.sessions.create(proxy_country_code=None)
```

---

## Webhook

任务完成时的实时通知。

### 事件

| 事件 | 说明 |
|------|------|
| `agent.task.status_update` | 任务状态变更（started/finished/stopped） |
| `test` | 测试 Webhook 投递 |

### 负载

```json
{
  "type": "agent.task.status_update",
  "timestamp": "2025-01-15T10:30:00Z",
  "payload": {
    "task_id": "task_abc123",
    "session_id": "session_xyz",
    "status": "finished",
    "metadata": {}
  }
}
```

### 签名验证（HMAC-SHA256）

请求头：`X-Browser-Use-Signature`、`X-Browser-Use-Timestamp`

签名基于 `{timestamp}.{body}` 计算，其中 body 是键排序且无多余空格的 JSON。拒绝超过 5 分钟的请求以防止重放攻击。

```python
import hmac, hashlib, json, time

def verify_webhook(body: bytes, signature: str, timestamp: str, secret: str) -> bool:
    # 拒绝超过 5 分钟的请求
    try:
        ts = int(timestamp)
    except (ValueError, TypeError):
        return False
    if abs(time.time() - ts) > 300:
        return False
    try:
        payload = json.loads(body)
    except (json.JSONDecodeError, ValueError):
        return False
    message = f"{timestamp}.{json.dumps(payload, separators=(',', ':'), sort_keys=True)}"
    expected = hmac.new(secret.encode(), message.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)
```

---

## 工作区

跨会话的持久文件存储（v3 API）。每次上传最多 10 个文件。

```python
from browser_use_sdk.v3 import AsyncBrowserUse
client = AsyncBrowserUse()

# 创建工作区
workspace = await client.workspaces.create(name="my-data")

# 创建会话
session = await client.sessions.create()

# 任务前上传文件
await client.sessions.upload_files(
    session.id,
    workspace_id=workspace.id,
    files=[open("input.pdf", "rb")]
)

# 任务后下载文件
files = await client.sessions.files(session.id)
for f in files:
    url = f.download_url  # 预签名 URL（60 秒过期）

# 管理工作区
workspaces = await client.workspaces.list()
await client.workspaces.delete(workspace.id)
```

---

## Skills

将网站交互转换为可复用的、确定性的 API 端点。

### 结构

- **Goal（目标）**：包含参数和返回数据的完整规格
- **Demonstration（演示）**：agent_prompt 展示如何执行一次任务

### 创建与执行

```python
# 创建（约 30 秒，按量付费 $2）
skill = await client.skills.create(
    goal="Extract product price from Amazon",
    demonstration="Navigate to product page, find price element..."
)

# 执行（按量付费 $0.02）
result = await client.skills.execute(skill.id, params={"url": "https://amazon.com/dp/..."})

# 优化（免费）
await client.skills.refine(skill.id, feedback="Also extract the rating")
```

### 市场

```python
skills = await client.marketplace.list()
cloned = await client.marketplace.clone(skill_id)
result = await client.marketplace.execute(skill_id, params={})
```

在 [cloud.browser-use.com/skills](https://cloud.browser-use.com/skills) 浏览。

### 在本地 Agent 中加载 Skills

```python
agent = Agent(
    task="...",
    skills=['skill-uuid-1', 'skill-uuid-2'],  # 或 ['*'] 加载全部
    llm=ChatBrowserUse()
)
```

---

## MCP 服务器

基于 HTTP 的 MCP，地址为 `https://api.browser-use.com/mcp`

| 工具 | 费用 | 说明 |
|------|------|------|
| `browser_task` | $0.01 + 按步计费 | 运行自动化任务 |
| `execute_skill` | $0.02 | 执行技能 |
| `list_skills` | 免费 | 列出技能 |
| `get_cookies` | 免费 | 获取 Cookie |
| `list_browser_profiles` | 免费 | 列出配置文件 |
| `monitor_task` | 免费 | 检查任务进度 |

设置：参见 `references/open-source/integrations.md` 获取 Claude/Cursor/Windsurf 配置。

---

## 实时视图

### 人工接管

暂停代理，让人类通过 `liveUrl` 接管：

```python
session = await client.sessions.create(keep_alive=True)  # v3
await client.run("Navigate to checkout", session_id=session.id)
# 代理在结账页面暂停

print(session.live_url)  # 人类打开此链接，输入支付信息

await client.run("Confirm the order", session_id=session.id)
await client.sessions.stop(session.id)
```

`liveUrl` 提供完整的鼠标/键盘控制。

### Iframe 嵌入

在你的应用中嵌入实时视图 — 无 X-Frame-Options 或 CSP 限制：

```html
<iframe
  src="{session.live_url}"
  width="1280"
  height="720"
  style="border: none;"
></iframe>
```

无需轮询 — 实时更新。
