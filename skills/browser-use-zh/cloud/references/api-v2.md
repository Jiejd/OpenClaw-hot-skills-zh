# Cloud API v2（稳定版）

功能完整的 REST API，支持任务、会话、浏览器、配置文件、Skills 和市场。

## 目录
- [认证](#认证)
- [常用 cURL 示例](#常用-curl-示例)
- [任务](#任务)
- [会话](#会话)
- [浏览器（CDP）](#浏览器cdp)
- [文件](#文件)
- [配置文件](#配置文件)
- [Skills](#skills)
- [市场](#市场)
- [计费](#计费)
- [分页](#分页)
- [枚举](#枚举)
- [响应 Schema](#响应-schema)

---

## 认证

- **请求头：** `X-Browser-Use-API-Key: <your-key>`
- **基础 URL：** `https://api.browser-use.com/api/v2`
- **获取 Key：** https://cloud.browser-use.com/new-api-key

所有端点都需要 `X-Browser-Use-API-Key` 请求头。

## 常用 cURL 示例

### 创建任务

```bash
curl -X POST https://api.browser-use.com/api/v2/tasks \
  -H "X-Browser-Use-API-Key: $BROWSER_USE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"task": "Find the top Hacker News post and return title and URL"}'
```

响应：`{"id": "<task-id>", "sessionId": "<session-id>"}`

### 轮询任务状态

```bash
curl https://api.browser-use.com/api/v2/tasks/<task-id>/status \
  -H "X-Browser-Use-API-Key: $BROWSER_USE_API_KEY"
```

### 获取会话实时 URL

```bash
curl https://api.browser-use.com/api/v2/sessions/<session-id> \
  -H "X-Browser-Use-API-Key: $BROWSER_USE_API_KEY"
```

响应包含 `liveUrl` — 打开它观看代理工作。

### 创建 CDP 浏览器

```bash
curl -X POST https://api.browser-use.com/api/v2/browsers \
  -H "X-Browser-Use-API-Key: $BROWSER_USE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"proxyCountryCode": "us", "timeout": 30}'
```

响应包含 `cdpUrl`（WebSocket）和 `liveUrl`。

### 停止会话

```bash
curl -X PATCH https://api.browser-use.com/api/v2/sessions/<session-id> \
  -H "X-Browser-Use-API-Key: $BROWSER_USE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"action": "stop"}'
```

### 上传文件到会话

```bash
# 1. 获取预签名 URL
curl -X POST https://api.browser-use.com/api/v2/files/sessions/<session-id>/presigned-url \
  -H "X-Browser-Use-API-Key: $BROWSER_USE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"fileName": "input.pdf", "contentType": "application/pdf", "sizeBytes": 102400}'

# 2. 使用返回的 URL 和所有返回的字段通过 multipart POST 上传（S3 风格的预签名 POST）
# 将响应中 fields 对象的每个键值对作为表单字段包含：
curl -X POST "<presigned-url>" \
  -F "key=<fields.key>" \
  -F "policy=<fields.policy>" \
  -F "x-amz-algorithm=<fields.x-amz-algorithm>" \
  -F "x-amz-credential=<fields.x-amz-credential>" \
  -F "x-amz-date=<fields.x-amz-date>" \
  -F "x-amz-signature=<fields.x-amz-signature>" \
  -F "Content-Type=application/pdf" \
  -F "file=@input.pdf"
```

v2 预签名 URL 响应包含用于 multipart POST 表单上传的 `fields`（S3 风格）。**包含所有返回的字段**作为表单字段 — 它们包含签名数据。预签名 URL 在 **120 秒** 后过期。最大文件大小：**10 MB**。

---

## 任务

**GET /tasks** — 带过滤的分页列表。
查询参数：`pageSize?`、`pageNumber?`、`sessionId?`（uuid）、`filterBy?`（TaskStatus）、`after?`（datetime）、`before?`（datetime）
响应：`{ items: TaskItemView[], totalItems, pageNumber, pageSize }`

**POST /tasks** — 创建并运行任务。自动创建会话或使用已有会话。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| task | string | **是** | 任务提示（1-50,000 字符） |
| llm | SupportedLLMs | 否 | 模型（默认：browser-use-llm） |
| startUrl | string | 否 | 初始 URL（节省步骤） |
| maxSteps | integer | 否 | 代理最大步数（默认：100） |
| structuredOutput | string | 否 | JSON Schema 字符串 |
| sessionId | uuid | 否 | 在已有会话中运行 |
| metadata | object | 否 | 键值对元数据（字符串值） |
| secrets | object | 否 | 按域名限定的凭据（字符串值） |
| allowedDomains | string[] | 否 | 限制导航范围 |
| opVaultId | string | 否 | 1Password 保管库 ID |
| highlightElements | boolean | 否 | 高亮交互元素 |
| flashMode | boolean | 否 | 快速模式（跳过评估/思考） |
| thinking | boolean | 否 | 扩展推理 |
| vision | boolean\|"auto" | 否 | 截图模式 |
| systemPromptExtension | string | 否 | 追加到系统提示 |
| judge | boolean | 否 | 启用质量评估器 |
| skillIds | string[] | 否 | 任务中使用的 Skills |

响应（202）：`{ id: uuid, sessionId: uuid }`
错误：400（会话繁忙/已停止）、404（会话未找到）、422（验证失败）、429（限速）

**GET /tasks/{task_id}** — 包含步骤和输出文件的详细任务信息。
响应：TaskView

**GET /tasks/{task_id}/status** — 轮询任务状态（比完整 GET 更轻量）。
响应：`{ status: TaskStatus }`

**PATCH /tasks/{task_id}** — 控制任务执行。
请求体：`{ action: TaskUpdateAction }` — `stop`、`pause`、`resume` 或 `stop_task_and_session`
响应：TaskView。错误：404、422。

**GET /tasks/{task_id}/logs** — 执行日志的下载 URL。
响应：`{ downloadUrl: string }`。错误：404、500。

---

## 会话

**GET /sessions** — 分页列表。
查询参数：`pageSize?`、`pageNumber?`、`filterBy?`（SessionStatus）

**POST /sessions** — 创建会话。
请求体：`{ profileId?: uuid, proxyCountryCode?: string, startUrl?: string }`
响应（201）：SessionItemView。错误：404（配置文件未找到）、429（并发过多）。

**GET /sessions/{id}** — 包含任务和分享 URL 的会话详情。
响应：SessionView

**PATCH /sessions/{id}** — 停止会话和所有运行中的任务。
请求体：`{ action: "stop" }`。错误：404、422。

**POST /sessions/{id}/purge** — 清除会话数据。
响应：200。

**GET /sessions/{id}/public-share** — 获取分享信息。
响应：ShareView。错误：404。

**POST /sessions/{id}/public-share** — 创建或返回已有分享。
响应（201）：ShareView。

**DELETE /sessions/{id}/public-share** — 移除分享。
响应：204。

---

## 浏览器（CDP）

**POST /browsers** — 创建 CDP 浏览器会话。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| profileId | uuid | 否 | 浏览器配置文件 |
| proxyCountryCode | string | 否 | 住宅代理（195+ 国家） |
| timeout | integer | 否 | 会话超时分钟数（最大 240） |
| browserScreenWidth | integer | 否 | 浏览器宽度（像素） |
| browserScreenHeight | integer | 否 | 浏览器高度（像素） |
| customProxy | object | 否 | `{ host, port, username?, password? }`（HTTP 或 SOCKS5） |

**定价：** $0.05/小时。预先计费，停止时按比例退款。向上取整到最近分钟（最少 1 分钟）。免费：最多 15 分钟。付费：最多 4 小时。

响应（201）：BrowserSessionItemView（包含 `cdpUrl` 和 `liveUrl`）。
错误：403（超出免费超时）、404（配置文件未找到）、429（并发过多）。

**GET /browsers/{id}** — 浏览器会话详情。

**PATCH /browsers/{id}** — 停止浏览器（未使用的时间退款）。
请求体：`{ action: "stop" }`

---

## 文件

**POST /files/sessions/{id}/presigned-url** — 获取会话文件的上传 URL。
请求体：`{ fileName: string, contentType: UploadContentType, sizeBytes: integer }`
响应：`{ url: string, method: "POST", fields: {}, fileName: string, expiresIn: integer }`
错误：400（不支持的类型）、404、500。

**POST /files/browsers/{id}/presigned-url** — 浏览器会话同理。

**GET /files/tasks/{task_id}/output-files/{file_id}** — 任务输出的下载 URL。
响应：`{ id: uuid, fileName: string, downloadUrl: string }`
错误：404、500。

**上传流程：** 获取预签名 URL → 使用返回的 `fields` + 文件进行 POST multipart 表单上传 → URL 在 120 秒后过期 → 最大 10 MB。

---

## 配置文件

**GET /profiles** — 分页列表。查询参数：`pageSize?`、`pageNumber?`

**POST /profiles** — 创建配置文件（任务间持久保存 Cookie/localStorage）。
请求体：`{ name?: string }`。响应（201）：ProfileView。错误：402（需要订阅）。

**GET /profiles/{id}** — 配置文件详情。

**DELETE /profiles/{id}** — 永久删除。响应：204。

**PATCH /profiles/{id}** — 更新名称。请求体：`{ name?: string }`

---

## Skills

**POST /skills** — 创建技能（将网站转换为 API 端点）。
请求体：`{ goal: string, agent_prompt: string, ... }`
响应：SkillView。

**GET /skills** — 列出所有技能。

**GET /skills/{id}** — 获取技能详情。

**POST /skills/{id}/execute** — 执行技能。
请求体：`{ parameters: {} }`

**POST /skills/{id}/refine** — 根据反馈优化（免费）。
请求体：`{ feedback: string }`

**POST /skills/{id}/cancel** — 取消技能训练。

**POST /skills/{id}/rollback** — 回滚到之前的版本。

**GET /skills/{id}/executions** — 列出技能执行记录。

**GET /skills/{id}/executions/{eid}/output** — 获取执行输出。

---

## 市场

**GET /marketplace/skills** — 浏览社区技能。

**GET /marketplace/skills/{slug}** — 获取市场技能详情。

**POST /marketplace/skills/{id}/clone** — 将技能克隆到你的工作区。

**POST /marketplace/skills/{id}/execute** — 执行市场技能。
请求体：`{ parameters: {} }`

---

## 计费

**GET /billing/account** — 账户信息和额度。
响应：`{ name?, monthlyCreditsBalanceUsd, additionalCreditsBalanceUsd, totalCreditsBalanceUsd, rateLimit, planInfo: { planName, subscriptionStatus?, subscriptionId?, subscriptionCurrentPeriodEnd?, subscriptionCanceledAt? }, projectId }`

---

## 分页

所有列表端点使用基于页码的分页：

| 参数 | 类型 | 说明 |
|------|------|------|
| pageSize | integer | 每页条目数 |
| pageNumber | integer | 页码（从 1 开始） |

响应包含：`{ items: [...], totalItems, pageNumber, pageSize }`

---

## 枚举

| 枚举 | 值 |
|------|-----|
| TaskStatus | `started`、`paused`、`finished`、`stopped` |
| TaskUpdateAction | `stop`、`pause`、`resume`、`stop_task_and_session` |
| SessionStatus | `active`、`stopped` |
| BrowserSessionStatus | `active`、`stopped` |
| ProxyCountryCode | `us`、`uk`、`fr`、`it`、`jp`、`au`、`de`、`fi`、`ca`、`in`（+185 更多） |
| SupportedLLMs | `browser-use-llm`、`gpt-4.1`、`gpt-4.1-mini`、`o4-mini`、`o3`、`gemini-2.5-flash`、`gemini-2.5-pro`、`gemini-flash-latest`、`gemini-flash-lite-latest`、`claude-sonnet-4-20250514`、`gpt-4o`、`gpt-4o-mini`、`llama-4-maverick-17b-128e-instruct`、`claude-3-7-sonnet-20250219` |
| UploadContentType | `image/jpg`、`image/jpeg`、`image/png`、`image/gif`、`image/webp`、`image/svg+xml`、`application/pdf`、`application/msword`、`application/vnd.openxmlformats-officedocument.wordprocessingml.document`、`application/vnd.ms-excel`、`application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`、`text/plain`、`text/csv`、`text/markdown` |

## 响应 Schema

**TaskItemView：** id、sessionId、llm、task、status、startedAt、finishedAt?、metadata?、output?、browserUseVersion?、isSuccess?

**TaskView：** 扩展 TaskItemView + steps: TaskStepView[]、outputFiles: FileView[]

**TaskStepView：** number、memory、evaluationPreviousGoal、nextGoal、url、screenshotUrl?、actions: string[]

**FileView：** id、fileName

**SessionItemView：** id、status、liveUrl?、startedAt、finishedAt?

**SessionView：** 扩展 SessionItemView + tasks: TaskItemView[]、publicShareUrl?

**BrowserSessionItemView：** id、status、liveUrl?、cdpUrl?、timeoutAt、startedAt、finishedAt?

**ProfileView：** id、name?、lastUsedAt?、createdAt、updatedAt、cookieDomains?: string[]

**ShareView：** shareToken、shareUrl、viewCount、lastViewedAt?

**AccountView：** name?、monthlyCreditsBalanceUsd、additionalCreditsBalanceUsd、totalCreditsBalanceUsd、rateLimit、planInfo、projectId
