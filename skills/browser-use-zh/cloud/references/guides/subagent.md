# 指南：将 Browser-Use 作为子代理

从你的编排器将整个 Web 任务委托给 browser-use。任务输入 → 结果输出 — browser-use 自主处理所有浏览操作。

## 目录
- [何时使用此模式](#何时使用此模式)
- [选择你的集成方式](#选择你的集成方式)
- [Shell 命令代理（CLI）](#shell-命令代理cli)
- [Python 代理（Cloud SDK）](#python-代理cloud-sdk)
- [TypeScript/JS 代理](#typescriptjs-代理)
- [MCP 原生代理](#mcp-原生代理)
- [HTTP / 工作流引擎](#http--工作流引擎)
- [跨切面关注点](#跨切面关注点)

---

## 何时使用此模式

你的系统有一个编排器 — 某个代理、管道或工作流引擎来协调多个能力。在某个时刻它决定"我需要从 Web 获取数据"或"我需要与网站交互"。它将任务委托给 browser-use，后者自主导航、点击、提取并返回结果。编排器从不接触浏览器。

**使用子代理当：**
- 你想要一个黑盒：任务输入 → 结果输出
- Web 任务是自包含的（搜索、提取、填表）
- 你不需要逐步控制

**改用 [工具集成](tools-integration.md) 当：**
- 你的代理需要做单独的浏览器决策（点击这个，然后检查那个）
- 你想让代理的推理循环来驱动浏览器

## 选择你的集成方式

| 你的代理类型 | 最佳方案 |
|-------------|----------|
| 沙箱中的 CLI 编码代理（Claude Code、Codex、OpenCode、Cline、Windsurf、Cursor 后台、Hermes、OpenClaw） | [CLI 云透传](#shell-命令代理cli) |
| Python 框架（LangChain、CrewAI、AutoGen、PydanticAI、自定义） | [Python Agent 封装](#python-代理cloud-sdk) |
| TypeScript/JS（Vercel AI SDK、LangChain.js、自定义） | [Cloud SDK](#typescriptjs-代理) |
| MCP 客户端（Claude Desktop、带 MCP 的 Cursor） | [MCP browser_task 工具](#mcp-原生代理) |
| 工作流引擎（n8n、Make、Zapier、Temporal）或任何 HTTP 客户端 | [Cloud REST API](#http--工作流引擎) |

---

## Shell 命令代理（CLI）

**适用于：** 在有终端访问的沙箱/虚拟机中运行的代理。

代理通过 CLI 命令将完整任务委托给云端。无需 Python 导入。

```bash
# 1. 设置 API Key（一次）
browser-use cloud login $BROWSER_USE_API_KEY

# 2. 发送任务
browser-use cloud v2 POST /tasks '{"task": "Find the top HN post and return title and URL"}'
# 返回：{"id": "<task-id>", "sessionId": "<session-id>"}

# 3. 轮询直到完成（阻塞）
browser-use cloud v2 poll <task-id>

# 4. 获取结果
browser-use cloud v2 GET /tasks/<task-id>
# 返回完整的 TaskView，包含 output、steps、outputFiles
```

结构化输出，传递 JSON Schema：
```bash
browser-use cloud v2 POST /tasks '{
  "task": "Find the CEO of OpenAI",
  "structuredOutput": "{\"type\":\"object\",\"properties\":{\"name\":{\"type\":\"string\"},\"company\":{\"type\":\"string\"}},\"required\":[\"name\",\"company\"]}"
}'
```

---

## Python 代理（Cloud SDK）

**适用于：** LangChain、CrewAI、AutoGen、PydanticAI、Semantic Kernel 或自定义 Python 代理。使用 Cloud SDK — 无需本地浏览器。

```python
from browser_use_sdk import AsyncBrowserUse
from pydantic import BaseModel

client = AsyncBrowserUse()

# 简单用法
async def browse(task: str) -> str:
    result = await client.run(task)
    return result.output

# 结构化输出
class SearchResult(BaseModel):
    title: str
    url: str

async def browse_structured(task: str) -> SearchResult:
    result = await client.run(task, output_schema=SearchResult)
    return result.output  # SearchResult 实例
```

使用 `keep_alive` 的多步任务：
```python
session = await client.sessions.create(proxy_country_code="us")
await client.run("Log into site", session_id=str(session.id), keep_alive=True)
result = await client.run("Extract data", session_id=str(session.id))
await client.sessions.stop(str(session.id))
```

---

## TypeScript/JS 代理

**适用于：** Vercel AI SDK、LangChain.js 或自定义 TypeScript 代理。

```typescript
import { BrowserUse } from "browser-use-sdk";
import { z } from "zod";

const client = new BrowserUse();

// 简单用法
async function browse(task: string): Promise<string> {
  const result = await client.run(task);
  return result.output;
}

// 结构化
const SearchResult = z.object({
  title: z.string(),
  url: z.string(),
});

async function browseStructured(task: string) {
  const result = await client.run(task, { schema: SearchResult });
  return result.output; // { title: string, url: string }
}
```

使用 `keepAlive` 的多步任务：
```typescript
const session = await client.sessions.create({ proxyCountryCode: "us" });
await client.run("Log into site", { sessionId: session.id, keepAlive: true });
const result = await client.run("Extract data", { sessionId: session.id });
await client.sessions.stop(session.id);
```

---

## MCP 原生代理

**适用于：** Claude Desktop、启用 MCP 的 Cursor、任何 MCP 客户端。

### Cloud MCP（完整任务委托）

添加到 MCP 配置：
```json
{
  "mcpServers": {
    "browser-use": {
      "url": "https://api.browser-use.com/mcp",
      "headers": { "X-Browser-Use-API-Key": "YOUR_KEY" }
    }
  }
}
```

代理获得 `browser_task` 工具。用任务描述调用它，获取结果。

### Local MCP（免费、开源）

`retry_with_browser_use_agent` 工具将整个任务委托给本地 Agent：

```bash
uvx --from 'browser-use[cli]' browser-use --mcp
```

---

## HTTP / 工作流引擎

**适用于：** n8n、Make、Zapier、Temporal、Serverless 函数、任何 HTTP 客户端。

### 创建任务 → 轮询 → 获取结果

```bash
# 1. 创建任务
curl -X POST https://api.browser-use.com/api/v2/tasks \
  -H "X-Browser-Use-API-Key: $BROWSER_USE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"task": "Find the top HN post and return title+URL"}'
# → {"id": "task-uuid", "sessionId": "session-uuid"}

# 2. 轮询状态
curl https://api.browser-use.com/api/v2/tasks/<task-id>/status \
  -H "X-Browser-Use-API-Key: $BROWSER_USE_API_KEY"
# → {"status": "finished"}

# 3. 获取结果
curl https://api.browser-use.com/api/v2/tasks/<task-id> \
  -H "X-Browser-Use-API-Key: $BROWSER_USE_API_KEY"
# → 完整的 TaskView，包含 output、steps、outputFiles
```

或使用 Webhook 进行事件驱动的工作流（参见 `../features.md`）。

---

## 跨切面关注点

### 结构化输出

- **Cloud SDK Python：** `output_schema=MyPydanticModel` → `result.output`（类型化）
- **Cloud SDK TypeScript：** `{ schema: ZodSchema }` → `result.output`（类型化）
- **Cloud REST：** `"structuredOutput": "<json-schema-string>"` → 响应中的 `output`

### 错误处理

```python
from browser_use_sdk import AsyncBrowserUse, BrowserUseError

try:
    result = await client.run(task, max_cost_usd=0.10)
except TimeoutError:
    pass  # 轮询超时（默认 5 分钟）
except BrowserUseError as e:
    pass  # API 错误
```

### 成本控制

- **Cloud v2：** 按步计费。使用 `max_steps` 限制。
- **Cloud v3：** `max_cost_usd=0.10` 限制支出。查看 `result.total_cost_usd`。

### 清理

完成后始终停止会话：
```python
session = await client.sessions.create(proxy_country_code="us")
try:
    result = await client.run(task, session_id=str(session.id))
finally:
    await client.sessions.stop(str(session.id))
```
