# 浏览器 API（直接 CDP 访问）

通过 Chrome DevTools Protocol 直接连接 Browser Use 隐身浏览器。

## 目录
- [WebSocket 连接](#websocket-连接)
- [SDK 方式](#sdk-方式)
- [Playwright 集成](#playwright-集成)
- [Puppeteer 集成](#puppeteer-集成)
- [Selenium 集成](#selenium-集成)

---

## WebSocket 连接

单一 URL，所有配置作为查询参数。浏览器**连接时自动启动**，**断开时自动停止** — 无需 REST 调用来启动或停止。

```
wss://connect.browser-use.com?apiKey=YOUR_KEY&proxyCountryCode=us&timeout=30
```

也支持通过 HTTPS 进行 CDP 发现（适用于使用 HTTP 自动发现的工具）：
```
https://connect.browser-use.com/json/version?apiKey=YOUR_API_KEY
```

### 查询参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `apiKey` | **是** | API Key |
| `proxyCountryCode` | 否 | 住宅代理国家（195+ 国家） |
| `profileId` | 否 | 浏览器配置文件 UUID |
| `timeout` | 否 | 会话超时分钟数（最大 240） |
| `browserScreenWidth` | 否 | 浏览器宽度（像素） |
| `browserScreenHeight` | 否 | 浏览器高度（像素） |
| `customProxy.host` | 否 | 自定义代理主机 |
| `customProxy.port` | 否 | 自定义代理端口 |
| `customProxy.username` | 否 | 自定义代理用户名 |
| `customProxy.password` | 否 | 自定义代理密码 |

## SDK 方式

```python
# 创建浏览器
browser = await client.browsers.create(
    profile_id="uuid",
    proxy_country_code="us",
    timeout=60,
)

print(browser.cdp_url)   # wss://... 用于 CDP 连接
print(browser.live_url)  # 在浏览器中查看

# 停止（未使用的时间退款）
await client.browsers.stop(browser.id)
```

## Playwright 集成

```python
from playwright.async_api import async_playwright

# 创建云端浏览器
browser_session = await client.browsers.create(proxy_country_code="us")

# 连接 Playwright
pw = await async_playwright().start()
browser = await pw.chromium.connect_over_cdp(browser_session.cdp_url)
page = browser.contexts[0].pages[0]

# 正常的 Playwright 代码
await page.goto("https://example.com")
await page.fill("#email", "user@example.com")
await page.click("button[type=submit]")
content = await page.content()

# 清理
await pw.stop()
await client.browsers.stop(browser_session.id)
```

## Puppeteer 集成

```javascript
const puppeteer = require('puppeteer-core');

const browser = await client.browsers.create({ proxyCountryCode: 'us' });
const puppeteerBrowser = await puppeteer.connect({ browserWSEndpoint: browser.cdpUrl });
const page = (await puppeteerBrowser.pages())[0];

await page.goto('https://example.com');
// ... 正常的 Puppeteer 代码

await puppeteerBrowser.close();
await client.browsers.stop(browser.id);
```

## Selenium 集成

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

browser_session = await client.browsers.create(proxy_country_code="us")

options = Options()
options.debugger_address = browser_session.cdp_url.replace("wss://", "").replace("ws://", "").replace("/devtools/browser/", "")
driver = webdriver.Chrome(options=options)

driver.get("https://example.com")
# ... 正常的 Selenium 代码

driver.quit()
await client.browsers.stop(browser_session.id)
```

### 会话限制

- 免费：最多 15 分钟
- 付费：最多 4 小时
- 定价：$0.05/小时，预先计费，提前停止按比例退款，最少 1 分钟
