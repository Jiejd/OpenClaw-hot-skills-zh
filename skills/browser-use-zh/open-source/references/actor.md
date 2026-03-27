# Actor API（旧版直接浏览器控制）

基于 CDP 的底层类 Playwright 浏览器自动化。用于在 AI 代理旁边进行精确、确定性的操作。

## 目录
- [架构](#架构)
- [Browser 方法](#browser-方法)
- [Page 方法](#page-方法)
- [Element 方法](#element-方法)
- [Mouse 方法](#mouse-方法)
- [示例](#示例)

---

## 架构

```
Browser (BrowserSession) → Page → Element
                                → Mouse
                                → AI Features (extract, find by prompt)
```

不是 Playwright — 基于 CDP 构建，提供 Playwright API 的子集。主要区别：
- `get_elements_by_css_selector()` 立即返回（不等待可见性）
- 导航后需要手动等待
- `evaluate()` 需要箭头函数格式：`() => {}`

## Browser 方法

```python
browser = Browser()
await browser.start()

page = await browser.new_page("https://example.com")  # 打开新标签页
pages = await browser.get_pages()                       # 列出所有页面
current = await browser.get_current_page()              # 当前活跃页面
await browser.close_page(page)                          # 关闭标签页
await browser.stop()                                    # 清理
```

## Page 方法

### 导航
- `goto(url: str)` — 导航到 URL
- `go_back()` — 后退
- `go_forward()` — 前进
- `reload()` — 刷新页面

### 元素查找
- `get_elements_by_css_selector(selector: str) -> list[Element]` — 立即返回
- `get_element(backend_node_id: int) -> Element` — 通过 CDP 节点 ID
- `get_element_by_prompt(prompt: str, llm) -> Element | None` — LLM 驱动
- `must_get_element_by_prompt(prompt: str, llm) -> Element` — 找不到时抛出异常

### JavaScript 与控件
- `evaluate(page_function: str, *args) -> str` — 执行 JS（箭头函数格式）
- `press(key: str)` — 键盘输入
- `set_viewport_size(width: int, height: int)`
- `screenshot(format='jpeg', quality=None) -> str` — Base64 截图

### 信息
- `get_url() -> str`
- `get_title() -> str`
- `mouse -> Mouse` — Mouse 实例

### AI 功能
- `extract_content(prompt: str, structured_output: type[T], llm) -> T` — LLM 驱动的提取

## Element 方法

### 交互
- `click(button='left', click_count=1, modifiers=None)`
- `fill(text: str, clear=True)` — 清空字段并输入
- `hover()`
- `focus()`
- `check()` — 切换复选框/单选按钮
- `select_option(values: str | list[str])` — 选择下拉菜单
- `drag_to(target: Element | Position)`

### 属性
- `get_attribute(name: str) -> str | None`
- `get_bounding_box() -> BoundingBox | None`
- `get_basic_info() -> ElementInfo`
- `screenshot(format='jpeg') -> str`

## Mouse 方法

```python
mouse = page.mouse
await mouse.click(x=100, y=200, button='left', click_count=1)
await mouse.move(x=500, y=600, steps=1)
await mouse.down(button='left')
await mouse.up(button='left')
await mouse.scroll(x=0, y=100, delta_x=None, delta_y=-500)
```

## 示例

### 混合 Agent + Actor

```python
async def main():
    llm = ChatOpenAI(api_key="your-key")
    browser = Browser()
    await browser.start()

    # Actor：精确导航
    page = await browser.new_page("https://github.com/login")
    email = await page.must_get_element_by_prompt("username field", llm=llm)
    await email.fill("your-username")

    # Agent：AI 驱动的完成
    agent = Agent(browser=browser, llm=llm)
    await agent.run("Complete login and navigate to repositories")

    await browser.stop()
```

### JavaScript 执行

```python
title = await page.evaluate('() => document.title')
result = await page.evaluate('(x, y) => x + y', 10, 20)
stats = await page.evaluate('''() => ({
    url: location.href,
    links: document.querySelectorAll('a').length
})''')
```

### LLM 驱动的提取

```python
from pydantic import BaseModel

class ProductInfo(BaseModel):
    name: str
    price: float

product = await page.extract_content("Extract product name and price", ProductInfo, llm=llm)
```

### 最佳实践

- 导航触发的动作后使用 `asyncio.sleep()`
- 检查 URL/标题变化以验证状态转换
- 为不稳定的元素实现重试逻辑
- 始终调用 `browser.stop()` 进行清理
