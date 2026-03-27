# 浏览器配置

## 目录
- [基本用法](#基本用法)
- [所有参数](#所有参数)
- [认证策略](#认证策略)
- [真实浏览器连接](#真实浏览器连接)
- [远程/云端浏览器](#远程-云端浏览器)

---

## 基本用法

```python
from browser_use import Agent, Browser, ChatBrowserUse

browser = Browser(
    headless=False,
    window_size={'width': 1000, 'height': 700},
)

agent = Agent(task='Search for Browser Use', browser=browser, llm=ChatBrowserUse())
await agent.run()
```

`Browser` 是 `BrowserSession` 的别名 — 同一个类。

## 所有参数

### 核心
- `cdp_url`：已有浏览器的 CDP URL（例如 `"http://localhost:9222"`）

### 显示与外观
- `headless`（默认：`None`）：自动检测显示器。`True`/`False`/`None`
- `window_size`：`{'width': 1920, 'height': 1080}` 或 `ViewportSize`
- `window_position`（默认：`{'width': 0, 'height': 0}`）
- `viewport`：内容区域大小
- `no_viewport`（默认：`None`）：禁用视口模拟
- `device_scale_factor`：DPI（Retina 屏为 `2.0`）

### 浏览器行为
- `keep_alive`（默认：`None`）：代理完成后保持浏览器运行
- `allowed_domains`：使用模式限制导航：
  - `'example.com'` → `https://example.com/*`
  - `'*.example.com'` → 域名 + 子域名
  - `'http*://example.com'` → 两种协议
  - `'chrome-extension://*'` → 扩展
  - 不支持 TLD 通配符（`example.*`）
  - 超过 100 个域名时自动优化为集合（O(1) 查找）
- `prohibited_domains`：阻止域名（相同模式）。`allowed_domains` 优先
- `enable_default_extensions`（默认：`True`）：uBlock Origin、Cookie 处理器、ClearURLs
- `cross_origin_iframes`（默认：`False`）
- `is_local`（默认：`True`）：远程浏览器设为 `False`

### 用户数据与配置文件
- `user_data_dir`（默认：自动临时）：配置文件数据目录。`None` 表示隐身模式
- `profile_directory`（默认：`'Default'`）：Chrome 配置文件名
- `storage_state`：Cookie/localStorage，文件路径或字典

### 网络与安全
- `proxy`：`ProxySettings(server='http://host:8080', bypass='localhost', username='user', password='pass')`
- `permissions`（默认：`['clipboardReadWrite', 'notifications']`）
- `headers`：远程浏览器的 HTTP 头

### 浏览器启动
- `executable_path`：自定义浏览器路径
- `channel`：`'chromium'`、`'chrome'`、`'chrome-beta'`、`'msedge'`
- `args`：额外 CLI 参数列表
- `env`：环境变量字典
- `chromium_sandbox`（默认：`True`，Docker 中除外）
- `devtools`（默认：`False`）：需要 `headless=False`
- `ignore_default_args`：列表或 `True` 表示全部

### 时间与性能
- `minimum_wait_page_load_time`（默认：`0.25`）
- `wait_for_network_idle_page_load_time`（默认：`0.5`）
- `wait_between_actions`（默认：`0.5`）

### AI 集成
- `highlight_elements`（默认：`True`）
- `paint_order_filtering`（默认：`True`）：移除隐藏元素（实验性）

### 下载与文件
- `accept_downloads`（默认：`True`）
- `downloads_path`：下载目录
- `auto_download_pdfs`（默认：`True`）

### 设备模拟
- `user_agent`：自定义 User Agent 字符串
- `screen`：屏幕尺寸信息

### 录制与调试
- `record_video_dir`：保存为 `.mp4`
- `record_video_size`（默认：ViewportSize）
- `record_video_framerate`（默认：`30`）
- `record_har_path`：网络追踪保存为 `.har`
- `traces_dir`：完整追踪文件
- `record_har_content`（默认：`'embed'`）：`'omit'`/`'embed'`/`'attach'`
- `record_har_mode`（默认：`'full'`）：`'full'`/`'minimal'`

### 高级
- `disable_security`（默认：`False`）：**不推荐**
- `deterministic_rendering`（默认：`False`）：**不推荐**

### 类方法

```python
# 自动检测 Chrome 和第一个可用配置文件
browser = Browser.from_system_chrome()
browser = Browser.from_system_chrome(profile_directory='Profile 5')

# 列出可用配置文件
profiles = Browser.list_chrome_profiles()
# [{'directory': 'Default', 'name': 'Person 1'}, {'directory': 'Profile 1', 'name': 'Work'}]
```

---

## 认证策略

| 方式 | 最适用于 | 设置难度 |
|------|----------|----------|
| 真实浏览器 | 个人自动化、已有登录 | 低 |
| 存储状态 | 生产环境、CI/CD、无头模式 | 中 |
| TOTP 2FA | 身份验证器应用 | 低 |
| 邮件/SMS 2FA | 邮件/SMS 验证 | 中 |

### 存储状态持久化

```python
# 导出 Cookie/localStorage
await browser.export_storage_state('auth.json')

# 下次运行时加载
browser = Browser(storage_state='auth.json')
```

会定期自动保存，关闭时自动保存。启动时自动加载并合并。

### TOTP 2FA

在 `sensitive_data` 中传入以 `bu_2fa_code` 结尾的密钥名：

```python
agent = Agent(
    task="Login to my account",
    llm=llm,
    sensitive_data={
        'google_bu_2fa_code': 'JBSWY3DPEHPK3PXP'  # TOTP 密钥
    },
)
```

代理按需生成新的 6 位验证码。密钥获取方式：
- 1Password：编辑项目 → 一次性密码 → 显示密钥
- Google Authenticator：设置过程中的"无法扫描？"
- Authy：桌面应用设置 → 导出

### 邮件/SMS 2FA

- **AgentMail**：用于邮件验证的一次性邮箱
- **1Password SDK**：从密码管理器获取验证码
- **Gmail API**：读取 2FA 验证码（需要 OAuth 2.0 设置）

### 安全最佳实践

- 限制域名：`Browser(allowed_domains=['*.example.com'])`
- 敏感页面禁用视觉：`Agent(use_vision=False)`
- 尽可能使用存储状态而非密码

---

## 真实浏览器连接

使用已有的 Chrome 及其保存的登录状态：

```python
# 自动检测（推荐）
browser = Browser.from_system_chrome()

# 手动指定路径
browser = Browser(
    executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    user_data_dir='~/Library/Application Support/Google/Chrome',
    profile_directory='Default',
)
```

运行前请完全关闭 Chrome。

### 平台路径

| 平台 | executable_path | user_data_dir |
|------|----------------|---------------|
| macOS | `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome` | `~/Library/Application Support/Google/Chrome` |
| Windows | `C:\Program Files\Google\Chrome\Application\chrome.exe` | `%LocalAppData%\Google\Chrome\User Data` |
| Linux | `/usr/bin/google-chrome` | `~/.config/google-chrome` |

---

## 远程/云端浏览器

### Browser-Use Cloud（推荐）

```python
# 简单用法
browser = Browser(use_cloud=True)

# 高级用法 — 绕过验证码、地理位置限制
browser = Browser(
    cloud_profile_id='your-profile-id',
    cloud_proxy_country_code='us',  # us, uk, fr, it, jp, au, de, fi, ca, in
    cloud_timeout=30,               # 分钟（免费：15，付费：240）
)
```

**前置条件：** 从 https://cloud.browser-use.com/new-api-key 获取 `BROWSER_USE_API_KEY` 环境变量

### CDP URL（任意提供商）

```python
browser = Browser(cdp_url="http://remote-server:9222")
```

### 使用代理

```python
from browser_use.browser import ProxySettings

browser = Browser(
    proxy=ProxySettings(
        server="http://proxy-server:8080",
        username="proxy-user",
        password="proxy-pass"
    ),
    cdp_url="http://remote-server:9222"
)
```
