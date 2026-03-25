# 示例模式与模板

## 目录
- [快速 Agent](#快速-agent)
- [并行浏览器](#并行浏览器)
- [后续任务](#后续任务)
- [敏感数据](#敏感数据)
- [Playwright 集成](#playwright-集成)

---

## 快速 Agent

通过优化配置最大化速度：

```python
from browser_use import Agent, Browser, BrowserProfile, ChatGroq

# 快速 LLM（Groq 或 Gemini Flash Lite）
llm = ChatGroq(model="meta-llama/llama-4-maverick-17b-128e-instruct")

# 最小化等待时间
browser = Browser(
    minimum_wait_page_load_time=0.1,
    wait_between_actions=0.1,
)

agent = Agent(
    task="Find top HN post",
    llm=llm,
    browser=browser,
    flash_mode=True,  # 跳过 LLM 思考，仅使用记忆
    extend_system_message="Be fast. Execute multiple actions per step.",
)

await agent.run()
```

**关键优化：**
- `flash_mode=True` — 跳过评估、下一步目标、思考
- 低等待时间 — `0.1` 替代默认值
- 快速 LLM — Groq 或 Gemini Flash Lite
- 多动作提示 — 每步填写多个字段

## 并行浏览器

并发运行多个代理：

```python
import asyncio
from browser_use import Agent, Browser, ChatBrowserUse

async def run_task(task: str, index: int):
    browser = Browser(user_data_dir=f'./temp-profile-{index}')
    try:
        agent = Agent(task=task, llm=ChatBrowserUse(), browser=browser)
        result = await agent.run()
        return result
    finally:
        await browser.close()

async def main():
    tasks = [
        "Find the latest AI news on TechCrunch",
        "Get Bitcoin price from CoinGecko",
        "Find top Python packages on PyPI",
    ]
    results = await asyncio.gather(*[run_task(t, i) for i, t in enumerate(tasks)])
```

每个代理获得自己的浏览器和独立配置文件以避免冲突。

## 后续任务

在持久浏览器会话中链接任务：

```python
from browser_use import Agent, Browser, ChatBrowserUse

browser = Browser(keep_alive=True)
await browser.start()

agent = Agent(
    task="Go to GitHub and search for 'browser-use'",
    llm=ChatBrowserUse(),
    browser=browser,
)
await agent.run()

# 在同一浏览器中排队后续任务（Cookie/localStorage 保留）
agent.add_new_task("Click on the first repository and extract the star count")
await agent.run()

await browser.close()
```

`keep_alive=True` 在任务之间保持浏览器打开。代理维护记忆和浏览器状态。

## 敏感数据

在不暴露给 LLM 的情况下处理凭据：

```python
agent = Agent(
    task="Login to example.com",
    llm=llm,
    sensitive_data={
        'x_user': 'my-username',       # 所有网站
        'x_pass': 'my-password',       # 所有网站
    },
    browser=Browser(allowed_domains=['*.example.com']),
)
```

- LLM 看到的是占位符名称（`x_user`、`x_pass`），而非真实值
- 真实值在执行时注入到表单字段中
- 永远不会出现在日志或 LLM 上下文中

### 按域名设置凭据

```python
sensitive_data = {
    'github_user': 'gh-username',
    'github_pass': 'gh-password',
    'gmail_user': 'gmail-address',
}
```

### 最佳实践

- 使用 `Browser(allowed_domains=[...])` 限制导航
- 敏感页面设置 `use_vision=False`
- 优先使用 `storage_state='auth.json'` 而非发送密码
- 使用以 `bu_2fa_code` 结尾的 TOTP 密钥进行 2FA（参见 `browser.md`）

## Playwright 集成

通过 CDP 在 Playwright 和 Browser-Use 之间共享 Chrome：

```python
import subprocess
from playwright.async_api import async_playwright
from browser_use import Agent, Browser, Tools, ChatBrowserUse

# 1. 启动带远程调试的 Chrome
proc = subprocess.Popen([
    'google-chrome', '--remote-debugging-port=9222', '--user-data-dir=/tmp/chrome-debug'
])

pw = None
try:
    # 2. 连接 Playwright
    pw = await async_playwright().start()
    pw_browser = await pw.chromium.connect_over_cdp("http://localhost:9222")
    pw_page = pw_browser.contexts[0].pages[0]

    # 3. 将 Browser-Use 连接到同一个 Chrome
    browser = Browser(cdp_url="http://localhost:9222")

    # 4. 使用 Playwright 的自定义工具
    tools = Tools()

    @tools.action(description='Fill form field using Playwright selector')
    async def pw_fill(selector: str, value: str) -> str:
        await pw_page.fill(selector, value)
        return f'Filled {selector}'

    @tools.action(description='Take Playwright screenshot')
    async def pw_screenshot() -> str:
        await pw_page.screenshot(path='screenshot.png')
        return 'Screenshot saved'

    # 5. Agent 同时使用两者进行编排
    agent = Agent(task="Fill out the form", llm=ChatBrowserUse(), browser=browser, tools=tools)
    await agent.run()
finally:
    if pw:
        await pw.stop()
    proc.terminate()
    proc.wait()
```

Playwright 和 Browser-Use 通过共享的 CDP 连接操作相同的页面。
