# BU Agent API（v3 — 实验性）

下一代代理 API。基于会话、Token 计费、工作区、消息历史。

## 目录
- [认证](#认证)
- [SDK 设置](#sdk-设置)
- [run() — 执行任务](#run--执行任务)
- [REST 端点](#rest-端点)
- [会话](#会话)
- [消息](#消息)
- [文件](#文件)
- [工作区](#工作区)
- [轮询与终态](#轮询与终态)
- [错误处理](#错误处理)
- [会话状态与枚举](#会话状态与枚举)
- [响应 Schema](#响应-schema)

---

## 认证

- **请求头：** `X-Browser-Use-API-Key: <your-key>`
- **基础 URL：** `https://api.browser-use.com/api/v3`
- **获取 Key：** https://cloud.browser-use.com/new-api-key

与 v2 使用相同的包，不同的导入路径：

## SDK 设置

```python
# Python（异步 — 推荐）
from browser_use_sdk.v3 import AsyncBrowserUse
client = AsyncBrowserUse()  # 使用 BROWSER_USE_API_KEY 环境变量

# Python（同步）
from browser_use_sdk.v3 import BrowserUse
client = BrowserUse()
```

```typescript
// TypeScript
import { BrowserUse } from "browser-use-sdk/v3";
const client = new BrowserUse();
```

构造函数：`api_key`、`base_url`、`timeout`（HTTP 请求超时，非轮询超时）。

## run() — 执行任务

```python
result = await client.run("Find the top HN post")
print(result.output)    # str
print(result.id)        # session UUID
print(result.status)    # 例如 "idle"
print(result.total_cost_usd)  # 成本明细
```

### 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| task | string | **必填。** 要做什么。 |
| model | string | `"bu-mini"`（默认，更快/更便宜）或 `"bu-max"`（更强） |
| output_schema | Pydantic/Zod | 结构化输出 Schema |
| session_id | string | 复用已有会话 |
| keep_alive | boolean | 任务完成后保持会话空闲（默认：false） |
| max_cost_usd | float | 美元成本上限；超出时代理停止 |
| profile_id | string | 浏览器配置文件 UUID |
| proxy_country_code | string | 住宅代理国家（195+ 国家） |
| workspace_id | string | 附加工作区用于文件 I/O |

### 结构化输出

```python
from pydantic import BaseModel

class Product(BaseModel):
    name: str
    price: float

result = await client.run("Get product info", output_schema=Product)
print(result.output)  # Product 实例
```

### SessionResult 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| output | str / BaseModel | 任务结果（提供了 Schema 则为类型化结果） |
| id | uuid | 会话 ID |
| status | string | 会话状态 |
| model | string | bu-mini 或 bu-max |
| title | string? | 自动生成的标题 |
| live_url | string | 实时浏览器监控 URL |
| profile_id | string? | 请求参数的回显 |
| proxy_country_code | string? | 请求参数的回显 |
| max_cost_usd | float? | 请求参数的回显 |
| total_input_tokens | int | 使用的输入 Token 数 |
| total_output_tokens | int | 使用的输出 Token 数 |
| llm_cost_usd | string | LLM 成本 |
| proxy_cost_usd | string | 代理成本 |
| proxy_used_mb | string | 使用的代理数据量 |
| total_cost_usd | string | 总成本 |
| created_at | datetime | 会话创建时间 |
| updated_at | datetime | 最后更新时间 |

---

## REST 端点

v3 API 中全部 16 个端点：

### 会话

**POST /sessions** — 创建会话和/或分派任务。
请求体：`{ task?, model?, session_id?, keep_alive?, max_cost_usd?, profile_id?, proxy_country_code?, output_schema? (JSON Schema dict) }`
响应：SessionView

**GET /sessions** — 列出会话。
查询参数：`page?`（int）、`page_size?`（int）
响应：`{ sessions: SessionView[], total, page, page_size }`

**GET /sessions/{id}** — 获取会话详情（包含成本明细）。
响应：SessionView

**DELETE /sessions/{id}** — 删除会话。
响应：204

**POST /sessions/{id}/stop** — 停止会话或任务。
查询参数：`strategy?` — `"session"`（默认，销毁沙箱）或 `"task"`（仅停止任务，保持会话活跃）
响应：200

### 消息

**GET /sessions/{id}/messages** — 基于游标的分页消息历史。

| 参数 | 类型 | 说明 |
|------|------|------|
| limit | int | 每页最大消息数（默认 50，最大 100） |
| after | string | 向前分页的游标 |
| before | string | 向后分页的游标 |

响应：`{ messages: [{ id, role: "user"|"assistant", data: string, timestamp }], next_cursor?, has_more: boolean }`

### 文件

**GET /sessions/{id}/files** — 列出会话工作区中的文件。

| 参数 | 类型 | 说明 |
|------|------|------|
| include_urls | boolean | 包含预签名下载 URL（60 秒过期） |
| prefix | string | 按路径前缀过滤（例如 `"outputs/"`） |
| limit | int | 每页最大数量（默认 50，最大 100） |
| cursor | string | 分页游标 |

响应：`{ files: [{ path, size, last_modified, url? }], next_cursor?, has_more }`

**POST /sessions/{id}/files/upload** — 获取预签名上传 URL。
请求体：`{ files: [{ name: string, content_type: string }] }`
响应：`{ files: [{ name, upload_url, path }] }`

通过 **PUT** 上传到 `upload_url`，使用匹配的 `Content-Type` 请求头。每批最多 **10 个文件**。预签名 URL 在 **120 秒** 后过期。最大文件大小：**10 MB**。

### 工作区

**POST /workspaces** — 创建持久工作区。
请求体：`{ name?: string, metadata?: object }`
响应：WorkspaceView

**GET /workspaces** — 列出工作区。
查询参数：`page?`、`page_size?`
响应：`{ items: WorkspaceView[], total, page, page_size }`

**GET /workspaces/{id}** — 获取工作区详情。

**PATCH /workspaces/{id}** — 更新工作区。
请求体：`{ name?: string, metadata?: object }`

**DELETE /workspaces/{id}** — 删除工作区和所有文件（不可逆）。

**GET /workspaces/{id}/files** — 列出工作区文件。
查询参数：`include_urls?`、`prefix?`、`limit?`、`cursor?`
响应：与会话文件格式相同

**GET /workspaces/{id}/size** — 存储使用量。
响应：`{ size_bytes: int, quota_bytes: int }`

**POST /workspaces/{id}/files/upload** — 上传文件到工作区。
与会话文件上传格式相同。

---

## 轮询与终态

`run()` 自动轮询：
- **间隔：** 2 秒
- **超时：** 300 秒（5 分钟）— 超出时抛出 `TimeoutError`
- **终态：** `idle`、`stopped`、`timed_out`、`error`

### 停止策略

| 策略 | 行为 |
|------|------|
| `"session"`（默认） | 完全销毁沙箱 |
| `"task"` | 停止当前任务，保持会话活跃以便后续操作 |

```python
await client.sessions.stop(session_id, strategy="task")   # 保持会话
await client.sessions.stop(session_id, strategy="session") # 销毁会话
```

---

## 错误处理

```python
from browser_use_sdk.v3 import AsyncBrowserUse, BrowserUseError

try:
    result = await client.run("Do something")
except TimeoutError:
    print("Polling timed out (5 min default)")
except BrowserUseError as e:
    print(f"API error: {e}")
```

---

## 会话状态与枚举

| 状态 | 说明 |
|------|------|
| `created` | 会话已创建，尚未运行 |
| `idle` | 任务已完成，会话仍活跃（keep_alive=True） |
| `running` | 任务进行中 |
| `stopped` | 手动停止 |
| `timed_out` | 会话超时 |
| `error` | 会话出错 |

**模型：** `bu-mini`（默认，更快/更便宜）、`bu-max`（更强）

## 响应 Schema

**SessionView（v3）：** id、status、model、title?、live_url、output?、profile_id?、proxy_country_code?、max_cost_usd?、total_input_tokens、total_output_tokens、llm_cost_usd、proxy_cost_usd、proxy_used_mb、total_cost_usd、created_at、updated_at

**MessageView：** id、role（"user"|"assistant"）、data（string）、timestamp

**FileInfo：** path、size、last_modified、url?

**WorkspaceView：** id、name?、metadata?、created_at、updated_at、size_bytes?

**核心概念：**
- **自主执行** — 代理自行决定步数（无 max_steps 参数）
- **成本控制** — `max_cost_usd` 限制支出；通过 `total_cost_usd` 查看结果
- **集成** — 代理自动发现第三方服务（邮件、Slack、日历）
- **文件 I/O** — 任务前上传，任务后从工作区下载。每批最多 10 个文件，下载 URL 在 60 秒后过期
