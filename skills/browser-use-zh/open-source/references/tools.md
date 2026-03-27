# 工具与自定义动作

## 目录
- [快速示例](#快速示例)
- [添加自定义工具](#添加自定义工具)
- [可注入参数](#可注入参数)
- [内置默认工具](#内置默认工具)
- [移除工具](#移除工具)
- [工具响应（ActionResult）](#工具响应actionresult)

---

## 快速示例

```python
from browser_use import Tools, ActionResult, BrowserSession

tools = Tools()

@tools.action('Ask human for help with a question')
async def ask_human(question: str, browser_session: BrowserSession) -> ActionResult:
    answer = input(f'{question} > ')
    return ActionResult(extracted_content=f'The human responded with: {answer}')

agent = Agent(task='Ask human for help', llm=llm, tools=tools)
```

> **警告：** 参数必须命名为 `browser_session: BrowserSession`，而不是 `browser: Browser`。代理通过名称匹配注入 — 错误的名称会静默失败。

## 添加自定义工具

```python
@tools.action(description='Fill out banking forms', allowed_domains=['https://mybank.com'])
async def fill_bank_form(account_number: str) -> ActionResult:
    return ActionResult(extracted_content=f'Filled form for account {account_number}')
```

**装饰器参数：**
- `description`（必填）：工具的功能描述 — LLM 用它来决定何时调用
- `allowed_domains`：工具可运行的域名（默认：所有域名）

### Pydantic 输入

```python
from pydantic import BaseModel, Field

class Car(BaseModel):
    name: str = Field(description='Car name, e.g. "Toyota Camry"')
    price: int = Field(description='Price in USD')

@tools.action(description='Save cars to file')
def save_cars(cars: list[Car]) -> str:
    with open('cars.json', 'w') as f:
        json.dump([c.model_dump() for c in cars], f)
    return f'Saved {len(cars)} cars'
```

### 在自定义工具中与浏览器交互

```python
@tools.action(description='Click submit button via CSS selector')
async def click_submit(browser_session: BrowserSession):
    page = await browser_session.must_get_current_page()
    elements = await page.get_elements_by_css_selector('button[type="submit"]')
    if not elements:
        return ActionResult(extracted_content='No submit button found')
    await elements[0].click()
    return ActionResult(extracted_content='Clicked!')
```

## 可注入参数

代理按名称填充函数参数。以下特殊名称会自动注入：

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `browser_session` | `BrowserSession` | 当前浏览器会话（CDP 访问） |
| `cdp_client` | | 直接 Chrome DevTools Protocol 客户端 |
| `page_extraction_llm` | `BaseChatModel` | 传递给代理的 LLM |
| `file_system` | `FileSystem` | 文件系统访问 |
| `available_file_paths` | `list[str]` | 可用于上传/处理的文件 |
| `has_sensitive_data` | `bool` | 动作是否包含敏感数据 |

### 页面方法（通过 browser_session）

```python
page = await browser_session.must_get_current_page()

# CSS 选择器
elements = await page.get_elements_by_css_selector('button.submit')

# LLM 驱动（自然语言）
element = await page.get_element_by_prompt("login button", llm=page_extraction_llm)
element = await page.must_get_element_by_prompt("login button", llm=page_extraction_llm)  # 找不到时抛出异常
```

## 内置默认工具

来源：[tools/service.py](https://github.com/browser-use/browser-use/blob/main/browser_use/tools/service.py)

### 导航与浏览器控制
- `search` — 搜索查询（DuckDuckGo、Google、Bing）
- `navigate` — 导航到 URL
- `go_back` — 后退
- `wait` — 等待指定秒数

### 页面交互
- `click` — 按索引点击元素
- `input` — 在表单字段中输入文本
- `upload_file` — 上传文件
- `scroll` — 向上/向下滚动页面
- `find_text` — 滚动到指定文本
- `send_keys` — 发送按键（Enter、Escape、Tab 等）

### JavaScript
- `evaluate` — 执行自定义 JS（Shadow DOM、选择器、提取）

### 标签页管理
- `switch` — 在标签页之间切换
- `close` — 关闭标签页

### 内容提取
- `extract` — 使用 LLM 提取数据

### 视觉
- `screenshot` — 在下次浏览器状态中请求截图

### 表单控件
- `dropdown_options` — 获取下拉菜单选项
- `select_dropdown` — 选择下拉菜单选项

### 文件操作
- `write_file` — 写入文件
- `read_file` — 读取文件
- `replace_file` — 替换文件中的文本

### 任务完成
- `done` — 完成任务（始终可用）

## 移除工具

```python
tools = Tools(exclude_actions=['search', 'wait'])
agent = Agent(task='...', llm=llm, tools=tools)
```

## 工具响应

### 简单返回

```python
@tools.action('My tool')
def my_tool() -> str:
    return "Task completed successfully"
```

### ActionResult（完全控制）

```python
@tools.action('Advanced tool')
def advanced_tool() -> ActionResult:
    return ActionResult(
        extracted_content="Main result",
        long_term_memory="Remember this for all future steps",
        error="Something went wrong",
        is_done=True,
        success=True,
        attachments=["file.pdf"],
    )
```

### ActionResult 字段

| 字段 | 默认值 | 说明 |
|------|--------|------|
| `extracted_content` | None | 传递给 LLM 的主要结果 |
| `include_extracted_content_only_once` | False | 大内容仅显示一次，之后省略 |
| `long_term_memory` | None | 始终包含在后续所有步骤的 LLM 输入中 |
| `error` | None | 错误信息（自动捕获的异常会设置此项） |
| `is_done` | False | 工具完成整个任务 |
| `success` | None | 任务是否成功（仅在 `is_done=True` 时） |
| `attachments` | None | 要显示给用户的文件 |
| `metadata` | None | 调试/可观测性数据 |

### 上下文控制策略

1. **短内容，始终可见**：返回字符串
2. **长内容显示一次 + 持久摘要**：`extracted_content` + `include_extracted_content_only_once=True` + `long_term_memory`
3. **永不显示，仅记忆**：单独使用 `long_term_memory`
