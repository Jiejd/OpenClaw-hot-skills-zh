# 指南：为你的代理添加 Browser-Use 工具

将单独的浏览器动作添加到现有代理的工具集中。你的代理保持控制，逐步驱动浏览器。

## 目录
- [何时使用此模式](#何时使用此模式)
- [选择你的集成方式](#选择你的集成方式)
- [Shell 命令代理（CLI）](#shell-命令代理cli)
- [TypeScript/JS：CDP + Playwright](#typescriptjs-cdp--playwright)
- [MCP 原生代理](#mcp-原生代理)
- [已有的 Playwright/Puppeteer/Selenium](#已有的-playwrightpuppeteerselenium)
- [决策总结](#决策总结)

---

## 何时使用此模式

你的代理已有工具（搜索、代码执行、文件 I/O 等）和自己的推理循环。你想要添加浏览器能力 — 导航、点击、输入、提取 — 作为代理可以调用的工具。你不想将控制权交给 browser-use 的 Agent；你的代理来做决策。

**使用工具集成当：**
- 你的代理需要逐步的浏览器控制
- 你想让浏览器动作和其他工具并存
- 代理的推理应该驱动点击/输入操作

**改用 [子代理](subagent.md) 当：**
- 你想将整个 Web 任务作为黑盒委托
- 你不需要对单个浏览器动作的控制

## 选择你的集成方式

| 你的代理类型 | 最佳方案 | 控制级别 |
|-------------|----------|----------|
| 沙箱中的 CLI 编码代理 | [CLI 命令](#shell-命令代理cli) | 逐命令 |
| TypeScript/JS | [CDP + Playwright](#typescriptjs-cdp--playwright) | Playwright API |
| MCP 客户端（Claude Desktop、Cursor） | [本地 MCP 服务器](#mcp-原生代理) | MCP 工具 |
| 已有 Playwright/Puppeteer/Selenium | [CDP WebSocket（隐身）](#已有的-playwrightpuppeteerselenium) | 你已有的 API |
| 仅 HTTP / 任何语言 | Cloud REST: `POST /browsers` → CDP URL | CDP |

---

## Shell 命令代理（CLI）

**适用于：** Claude Code、Codex、OpenCode、Cline、Windsurf、Cursor 后台代理、Hermes、OpenClaw — 任何在有终端访问的虚拟机/容器中运行的编码代理。

**设置：** 安装 CLI 并将 browser-use SKILL.md 加载到代理的上下文中。代理将浏览器命令作为 Shell 工具调用。

```bash
uv pip install 'browser-use[cli]'
```

**核心工作流程** — 代理逐个调用这些命令，每个命令之间读取输出：

```bash
# 1. 导航
browser-use open https://example.com

# 2. 观察 — 始终先运行 state 获取元素索引
browser-use state
# 输出：URL、标题、可点击元素列表及索引
# 例如 [0] <input type="search" placeholder="Search...">
#      [1] <button>Submit</button>
#      [2] <a href="/about">About</a>

# 3. 交互 — 使用 state 返回的索引
browser-use input 0 "search query"    # 在元素 0 中输入
browser-use click 1                   # 点击元素 1

# 4. 验证 — 重新运行 state 查看结果
browser-use state

# 5. 提取数据
browser-use get text 3               # 获取元素文本
browser-use get html --selector "h1" # 获取限定范围的 HTML
browser-use eval "document.title"    # 执行 JavaScript
browser-use screenshot result.png    # 捕获视觉状态

# 6. 等待动态内容
browser-use wait selector ".results" # 等待元素
browser-use wait text "Success"      # 等待文本

# 7. 清理
browser-use close
```

**关键细节：**
- 后台守护进程在命令之间保持浏览器活跃（每次调用约 50ms 延迟）
- 代理的推理循环决定下一步调用哪个命令
- `state` 输出是代理的"眼睛" — 它读取元素索引并决定点击什么
- 当不需要中间输出时，命令可以用 `&&` 链接
- `--json` 标志用于机器可读输出
- `--headed` 用于可见浏览器（调试）
- `--profile "Default"` 用于使用已保存 Chrome 登录的认证浏览

---

## TypeScript/JS：CDP + Playwright

**适用于：** 需要浏览器原语的 TypeScript 代理。将 Playwright 连接到云端隐身浏览器。

```typescript
import { chromium } from "playwright";

// 连接到云端隐身浏览器（无需本地 Chrome）
const browser = await chromium.connectOverCDP(
  "wss://connect.browser-use.com?apiKey=YOUR_KEY&proxyCountryCode=us"
);
const page = browser.contexts()[0].pages()[0];

// 你的代理将这些作为工具调用：
await page.goto("https://example.com");
await page.fill("#search", "query");
await page.click("button[type=submit]");
const text = await page.textContent(".result");
const screenshot = await page.screenshot();

await browser.close();
// WebSocket 断开时浏览器自动停止
```

本地浏览器（无云端）：
```typescript
import { chromium } from "playwright";

const browser = await chromium.launch();
const page = await browser.newPage();
// ... 相同的 Playwright API
await browser.close();
```

---

## MCP 原生代理

**适用于：** Claude Desktop、带 MCP 的 Cursor、任何通过协议发现工具的 MCP 客户端。

启动本地 MCP 服务器：
```bash
uvx --from 'browser-use[cli]' browser-use --mcp
```

代理获得单独的浏览器工具：
- `browser_navigate(url)` — 导航到 URL
- `browser_click(index)` — 按索引点击元素
- `browser_type(index, text)` — 在元素中输入
- `browser_get_state(include_screenshot)` — 获取页面状态及元素索引
- `browser_extract_content(query)` — LLM 驱动的提取
- `browser_screenshot(full_page)` — 捕获页面
- `browser_scroll(direction)` — 向上/向下滚动
- `browser_go_back()` — 浏览器后退
- `browser_list_tabs()`、`browser_switch_tab(id)`、`browser_close_tab(id)` — 标签页管理

代理逐个调用这些工具，使用自己的推理来决定下一步动作。

---

## 已有的 Playwright/Puppeteer/Selenium

**适用于：** 你已有浏览器自动化脚本，想在隐身基础设施（反指纹识别、CAPTCHA 处理、住宅代理）上运行。

零代码变更 — 只需更改连接 URL：

### Playwright
```python
# 之前：本地浏览器
browser = await playwright.chromium.launch()

# 之后：云端隐身浏览器
browser = await playwright.chromium.connect_over_cdp(
    "wss://connect.browser-use.com?apiKey=KEY&proxyCountryCode=us"
)
# 你的其余代码完全不变
```

### Puppeteer
```javascript
// 之前
const browser = await puppeteer.launch();

// 之后
const browser = await puppeteer.connect({
  browserWSEndpoint: "wss://connect.browser-use.com?apiKey=KEY&proxyCountryCode=us"
});
```

浏览器连接时自动启动，断开时自动停止。定价：$0.05/小时。

---

## 决策总结

| 条件 | 最佳选项 |
|------|----------|
| 代理有终端访问（沙箱/虚拟机） | CLI 命令 |
| TypeScript/JS | CDP WebSocket + Playwright |
| MCP 客户端（Claude Desktop、Cursor） | 本地 MCP 服务器 |
| 仅 HTTP / 任何语言 | Cloud REST: `POST /browsers` → CDP URL |
| 已有 Playwright/Puppeteer 脚本 | CDP WebSocket（云端隐身浏览器） |

> **注意：** 对于希望通过直接导入（Actor API、Tools Registry、MCPClient）进行精细浏览器控制的 Python 代理，请参阅 **open-source** 技能的参考文档。
