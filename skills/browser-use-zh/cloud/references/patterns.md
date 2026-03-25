# Cloud 模式与教程

## 目录
- [并行执行](#并行执行)
- [流式步骤](#流式步骤)
- [地理位置爬取](#地理位置爬取)
- [文件下载](#文件下载)
- [结构化输出](#结构化输出)
- [教程](#教程)

---

## 并行执行

### 并发提取

每个 `run()` 自动创建自己的会话 — 无需手动管理：

```python
import asyncio

async def extract(query: str):
    return await client.run(f"Search for '{query}' and extract top 3 results")

results = await asyncio.gather(
    extract("AI startups"),
    extract("climate tech"),
    extract("quantum computing"),
)
```

### 共享配置（同一配置文件 + 代理）

用于需要认证的并发任务：

```python
sessions = [
    await client.sessions.create(profile_id="uuid", proxy_country_code="us")
    for _ in range(3)
]

tasks = [
    client.run(f"Task {i}", session_id=s.id)
    for i, s in enumerate(sessions)
]
results = await asyncio.gather(*tasks)

for s in sessions:
    await client.sessions.stop(s.id)
```

**注意：** 并发会话从启动时的快照读取配置文件状态 — 它们不会看到彼此的变更。适用于读密集型任务，不适用于修改状态的任务。

---

## 流式步骤

实时流式传输代理进度：

```python
async for step in client.run("Find top HN post", stream=True):
    print(f"Step {step.number}: {step.next_goal} (URL: {step.url})")
```

每步返回步骤编号、下一步目标和当前 URL。

---

## 地理位置爬取

通过住宅代理获取依赖位置的内容：

```python
from pydantic import BaseModel

class Pricing(BaseModel):
    product: str
    price: str
    currency: str

# 日本定价
result = await client.run(
    "Get iPhone 16 Pro price from Apple Japan",
    output_schema=Pricing,
    session_settings={"proxy_country_code": "jp"},
)
print(result.output)  # Pricing(product="iPhone 16 Pro", price="159,800", currency="JPY")
```

支持 195+ 个国家。结合结构化输出进行类型化对比。

---

## 文件下载

获取任务期间下载的文件：

```python
# 运行会下载文件的任务
result = await client.run("Download the Q4 report PDF from example.com")

# 获取包含输出文件的任务详情
task = await client.tasks.get(result.id)

for file in task.output_files:
    output = await client.files.task_output(task.id, file.id)
    # output.download_url — 预签名 URL，请尽快下载（很快过期）
```

上传文件：使用预签名 URL（最大 10 MB，120 秒过期）：

```python
url_info = await client.files.session_url(
    session_id,
    file_name="input.pdf",
    content_type="application/pdf",
    size_bytes=1024,
)
# 使用 url_info.url 和 url_info.fields 上传
```

---

## 结构化输出

使用 Pydantic（Python）或 Zod（TypeScript）提取类型化数据：

```python
from pydantic import BaseModel

class Company(BaseModel):
    name: str
    founded: int
    ceo: str
    revenue: str

result = await client.run(
    "Find information about OpenAI",
    output_schema=Company,
)
print(result.output)  # Company 实例
```

**提示：**
- 保持 Schema 扁平 — 嵌套会增加复杂度
- 典型任务：使用 Browser Use 2.0 时 8-12 步

---

## 教程

### 聊天界面（Next.js）

带有实时会话监控的全栈聊天界面。使用 v3 + v2 SDK。
- 源码：[github.com/browser-use/chat-ui-example](https://github.com/browser-use/chat-ui-example)
- 模式：创建空闲会话 → 导航 → 放弃式分派任务 → 轮询消息 → 嵌入 liveUrl

### n8n 集成

HTTP Request 节点（无需自定义节点）：
1. POST `/api/v2/tasks` 创建任务
2. 轮询 GET `/api/v2/tasks/{id}` 直到完成
3. 或使用 Webhook 进行事件驱动的工作流

支持 Make、Zapier、Pipedream 和自定义编排器。

### OpenClaw（WhatsApp/Telegram/Discord）

自托管 AI 网关。两种选项：
1. **通过 CDP 的云端浏览器**：在 openclaw.json 中使用查询参数配置 `cdpUrl`
2. **CLI 作为技能**：`npx skills add` — 代理学习 CLI 命令

### Playwright 集成

将 Playwright 连接到云端隐身浏览器：
```python
browser = await client.browsers.create(proxy_country_code="us")
pw_browser = await playwright.chromium.connect_over_cdp(browser.cdp_url)
# 在隐身基础设施上的正常 Playwright 代码
```

完整示例参见 `references/cloud/browser-api.md`。
