# 快速开始与生产部署

## 目录
- [安装](#安装)
- [环境变量](#环境变量)
- [首个 Agent](#首个-agent)
- [使用 @sandbox 的生产部署](#使用-sandbox-的生产部署)

---

## 安装

```bash
pip install uv
uv venv --python 3.12
source .venv/bin/activate   # Windows: .venv\Scripts\activate
uv pip install browser-use
uvx browser-use install     # 下载 Chromium
```

## 环境变量

```bash
# Browser Use（推荐）— https://cloud.browser-use.com/new-api-key
BROWSER_USE_API_KEY=

# Google — https://aistudio.google.com/app/u/1/apikey
GOOGLE_API_KEY=

# OpenAI
OPENAI_API_KEY=

# Anthropic
ANTHROPIC_API_KEY=
```

## 首个 Agent

### ChatBrowserUse（推荐 — 最快、最便宜、准确率最高）

```python
from browser_use import Agent, ChatBrowserUse
from dotenv import load_dotenv
import asyncio

load_dotenv()

async def main():
    llm = ChatBrowserUse()
    agent = Agent(task="Find the number 1 post on Show HN", llm=llm)
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())
```

### Google Gemini

```python
from browser_use import Agent, ChatGoogle
from dotenv import load_dotenv
import asyncio

load_dotenv()

async def main():
    llm = ChatGoogle(model="gemini-flash-latest")
    agent = Agent(task="Find the number 1 post on Show HN", llm=llm)
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())
```

### OpenAI

```python
from browser_use import Agent, ChatOpenAI
from dotenv import load_dotenv
import asyncio

load_dotenv()

async def main():
    llm = ChatOpenAI(model="gpt-4.1-mini")
    agent = Agent(task="Find the number 1 post on Show HN", llm=llm)
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())
```

### Anthropic

```python
from browser_use import Agent, ChatAnthropic
from dotenv import load_dotenv
import asyncio

load_dotenv()

async def main():
    llm = ChatAnthropic(model='claude-sonnet-4-0', temperature=0.0)
    agent = Agent(task="Find the number 1 post on Show HN", llm=llm)
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())
```

所有 15+ 提供商请参见 `references/open-source/models.md`。

---

## 使用 @sandbox 的生产部署

`@sandbox` 装饰器是最简单的生产部署方式。代理在云基础设施上与浏览器相邻运行，延迟极低。

### 基础部署

```python
from browser_use import Browser, sandbox, ChatBrowserUse
from browser_use.agent.service import Agent
import asyncio

@sandbox()
async def my_task(browser: Browser):
    agent = Agent(task="Find the top HN post", browser=browser, llm=ChatBrowserUse())
    await agent.run()

asyncio.run(my_task())
```

### 使用代理

```python
@sandbox(cloud_proxy_country_code='us')
async def stealth_task(browser: Browser):
    agent = Agent(task="Your task", browser=browser, llm=ChatBrowserUse())
    await agent.run()
```

### 使用认证（配置文件同步）

1. 同步本地 Cookie：
```bash
export BROWSER_USE_API_KEY=your_key && curl -fsSL https://browser-use.com/profile.sh | sh
```

2. 使用返回的 profile_id：
```python
@sandbox(cloud_profile_id='your-profile-id')
async def authenticated_task(browser: Browser):
    agent = Agent(task="Your authenticated task", browser=browser, llm=ChatBrowserUse())
    await agent.run()
```

### Sandbox 参数

| 参数 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `BROWSER_USE_API_KEY` | str | API Key（环境变量） | 必填 |
| `cloud_profile_id` | str | 浏览器配置文件 UUID | None |
| `cloud_proxy_country_code` | str | us, uk, fr, it, jp, au, de, fi, ca, in | None |
| `cloud_timeout` | int | 分钟（免费最多 15 分钟，付费最多 240 分钟） | None |
| `on_browser_created` | Callable | 接收 `data.live_url` | None |
| `on_log` | Callable | 接收 `log.level`、`log.message` | None |
| `on_result` | Callable | 成功回调 | None |
| `on_error` | Callable | 接收 `error.error` | None |

### 事件回调

```python
from browser_use.sandbox import BrowserCreatedData, LogData, ResultData, ErrorData

@sandbox(
    cloud_profile_id='your-profile-id',
    cloud_proxy_country_code='us',
    on_browser_created=lambda data: print(f'Live: {data.live_url}'),
    on_log=lambda log: print(f'{log.level}: {log.message}'),
    on_result=lambda result: print('Done!'),
    on_error=lambda error: print(f'Error: {error.error}'),
)
async def task(browser: Browser):
    agent = Agent(task="your task", browser=browser, llm=ChatBrowserUse())
    await agent.run()
```

所有回调可以是同步或异步函数。

### 本地开发

```bash
git clone https://github.com/browser-use/browser-use
cd browser-use
uv sync --all-extras --dev

# 辅助脚本
./bin/setup.sh   # 完整设置
./bin/lint.sh    # 格式化、代码检查、类型检查
./bin/test.sh    # CI 测试套件

# 运行示例
uv run examples/simple.py
```

### 遥测

使用 `ANONYMIZED_TELEMETRY=false` 环境变量退出遥测。零性能影响。
