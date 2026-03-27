# 集成（MCP、Skills、文档）

## 目录
- [MCP 服务器（云端）](#mcp-服务器云端)
- [MCP 服务器（本地）](#mcp-服务器本地)
- [Skills](#skills)
- [文档 MCP](#文档-mcp)

---

## MCP 服务器（云端）

基于 HTTP 的 MCP 服务器，地址为 `https://api.browser-use.com/mcp`

### 设置

**Claude Code：**
```bash
claude mcp add --transport http browser-use https://api.browser-use.com/mcp
```

**Claude Desktop**（macOS `~/Library/Application Support/Claude/claude_desktop_config.json`）：
```json
{
  "mcpServers": {
    "browser-use": {
      "type": "http",
      "url": "https://api.browser-use.com/mcp",
      "headers": { "x-browser-use-api-key": "your-api-key" }
    }
  }
}
```

**Cursor**（`~/.cursor/mcp.json`）：
```json
{
  "mcpServers": {
    "browser-use": {
      "type": "http",
      "url": "https://api.browser-use.com/mcp",
      "headers": { "x-browser-use-api-key": "your-api-key" }
    }
  }
}
```

**Windsurf**（`~/.codeium/windsurf/mcp_config.json`）：
```json
{
  "mcpServers": {
    "browser-use": {
      "type": "http",
      "url": "https://api.browser-use.com/mcp",
      "headers": { "x-browser-use-api-key": "your-api-key" }
    }
  }
}
```

### 云端 MCP 工具

| 工具 | 费用 | 说明 |
|------|------|------|
| `browser_task` | $0.01 + 按步计费 | 运行浏览器自动化任务 |
| `execute_skill` | $0.02 | 执行技能 |
| `list_skills` | 免费 | 列出可用技能 |
| `get_cookies` | 免费 | 获取 Cookie |
| `list_browser_profiles` | 免费 | 列出云端配置文件 |
| `monitor_task` | 免费 | 检查任务进度 |

`browser_task` 参数：`task`（必填）、`max_steps`（1-10，默认 8）、`profile_id`（UUID）

---

## MCP 服务器（本地）

免费的、自托管的基于 stdio 的服务器：

```bash
uvx --from 'browser-use[cli]' browser-use --mcp
```

### Claude Desktop 配置

macOS（`~/Library/Application Support/Claude/claude_desktop_config.json`）：
```json
{
  "mcpServers": {
    "browser-use": {
      "command": "/Users/your-username/.local/bin/uvx",
      "args": ["--from", "browser-use[cli]", "browser-use", "--mcp"],
      "env": {
        "OPENAI_API_KEY": "your-key"
      }
    }
  }
}
```

注意：在 macOS/Linux 上使用 `uvx` 的完整路径（运行 `which uvx` 查找）。

### 本地 MCP 工具

**代理：** `retry_with_browser_use_agent` — 完整自动化任务

**直接控制：**
- `browser_navigate` — 导航到 URL
- `browser_click` — 按索引点击元素
- `browser_type` — 输入文本
- `browser_get_state` — 页面状态 + 交互元素
- `browser_scroll` — 滚动页面
- `browser_go_back` — 后退

**标签页：** `browser_list_tabs`、`browser_switch_tab`、`browser_close_tab`

**提取：** `browser_extract_content` — 结构化提取

**会话：** `browser_list_sessions`、`browser_close_session`、`browser_close_all`

### 环境变量

- `OPENAI_API_KEY` 或 `ANTHROPIC_API_KEY` — LLM Key（必填）
- `BROWSER_USE_HEADLESS` — 设为 `false` 显示浏览器
- `BROWSER_USE_DISABLE_SECURITY` — 设为 `true` 禁用安全限制
- `BROWSER_USE_LOGGING_LEVEL` — 设为 `DEBUG` 获取详细日志

### 编程方式使用

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def use_browser_mcp():
    server_params = StdioServerParameters(
        command="uvx",
        args=["--from", "browser-use[cli]", "browser-use", "--mcp"]
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool("browser_navigate", arguments={"url": "https://example.com"})
```

---

## Skills

将云端技能加载到代理中作为可复用的 API 端点：

```python
agent = Agent(
    task='Analyze TikTok and Instagram profiles',
    skills=[
        'a582eb44-e4e2-4c55-acc2-2f5a875e35e9',  # TikTok Scraper
        'f8d91c2a-3b4e-4f7d-9a1e-6c8e2d3f4a5b',  # Instagram Scraper
    ],
    llm=ChatBrowserUse()
)
await agent.run()
```

- 使用 `skills=['*']` 加载所有技能（每个约增加 200 tokens 到提示）
- 需要 `BROWSER_USE_API_KEY`
- 在 [cloud.browser-use.com/skills](https://cloud.browser-use.com/skills) 浏览/创建
- Cookie 从浏览器自动注入；如果缺失，LLM 会导航获取

---

## 文档 MCP

只读文档访问（无浏览器自动化）：

**Claude Code：**
```bash
claude mcp add --transport http browser-use-docs https://docs.browser-use.com/mcp
```

**Cursor**（`~/.cursor/mcp.json`）：
```json
{
  "mcpServers": {
    "browser-use-docs": { "url": "https://docs.browser-use.com/mcp" }
  }
}
```

无需 API Key。提供 API 参考、配置选项、最佳实践、示例。
