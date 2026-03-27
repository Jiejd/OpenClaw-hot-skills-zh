# Cloud 快速开始、定价与常见问题

## 目录
- [概述](#概述)
- [设置](#设置)
- [首个任务](#首个任务)
- [结构化输出](#结构化输出)
- [实时视图](#实时视图)
- [定价](#定价)
- [常见问题与故障排除](#常见问题与故障排除)

---

## 概述

Browser Use Cloud 是网页自动化的托管平台。提供隐身浏览器（反指纹识别）、CAPTCHA 解决、195+ 个国家的住宅代理。通过 API Key 按使用量计费。

- Web 应用：https://cloud.browser-use.com/
- API 基础 URL：`https://api.browser-use.com/api/v2/`
- 认证头：`X-Browser-Use-API-Key: <key>`

## 设置

### Python

```bash
pip install browser-use-sdk
```

```python
from browser_use_sdk import BrowserUse
client = BrowserUse()  # 使用 BROWSER_USE_API_KEY 环境变量
```

### TypeScript

```bash
npm install browser-use-sdk
```

```typescript
import BrowserUse from 'browser-use-sdk';
const client = new BrowserUse();  // 使用 BROWSER_USE_API_KEY 环境变量
```

### cURL

```bash
export BROWSER_USE_API_KEY=your-key
```

## 首个任务

### SDK

```python
result = await client.run("Search for top Hacker News post and return title and URL")
print(result.output)
```

### cURL

```bash
curl -X POST https://api.browser-use.com/api/v2/tasks \
     -H "X-Browser-Use-API-Key: $BROWSER_USE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"task": "Search for the top Hacker News post and return the title and url."}'
```

响应：`{"id": "<task-id>", "sessionId": "<session-id>"}`

## 结构化输出

```python
from pydantic import BaseModel

class HNPost(BaseModel):
    title: str
    url: str
    points: int

result = await client.run(
    "Find top Hacker News post",
    output_schema=HNPost
)
print(result.output)  # HNPost 实例
```

## 实时视图

每个会话都有一个 `liveUrl`：

```bash
curl https://api.browser-use.com/api/v2/sessions/<sessionId> \
     -H "X-Browser-Use-API-Key: $BROWSER_USE_API_KEY"
```

打开 `liveUrl` 实时观看代理工作。

---

## 定价

### AI Agent 任务
$0.01 初始化 + 按步计费（因模型而异）：

| 模型 | 每步费用 |
|------|----------|
| Browser Use LLM | $0.002 |
| Browser Use 2.0 | $0.006 |
| Gemini Flash Lite | $0.005 |
| GPT-4.1 Mini | $0.004 |
| O3 | $0.03 |
| Claude Sonnet 4.6 | $0.05 |

典型任务：10 步 ≈ $0.03（使用 Browser Use LLM）

### V3 API（基于 Token）
| 模型 | 输入/百万 Token | 输出/百万 Token |
|------|----------------|----------------|
| BU Mini（Gemini 3 Flash） | ~$0.72 | ~$4.20 |
| BU Max（Claude Sonnet 4.6） | ~$3.60 | ~$18.00 |

### 浏览器会话
- 按量付费：$0.06/小时
- Business：$0.03/小时
- 预先计费，停止时按比例退款。最少 1 分钟。

### Skills
- 创建：$2（按量付费），$1（Business）。优化免费。
- 执行：$0.02（按量付费），$0.01（Business）

### 代理
- 按量付费：$10/GB，Business：$5/GB，Scaleup：$4/GB

### 套餐等级
- **Business**：每步费用 25% 折扣，会话/Skills/代理 50% 折扣
- **Scaleup**：每步费用 50% 折扣，代理 60% 折扣
- **Enterprise**：联系获取 ZDR、合规、本地部署方案

---

## 常见问题与故障排除

**任务很慢？**
- 切换模型（Browser Use LLM 最快）
- 设置 `start_url` 跳过导航
- 使用更近的代理国家

**代理失败了？**
- 查看 `liveUrl` 了解发生了什么
- 简化指令
- 设置 `start_url`

**登录问题？**
- 配置文件同步（最简单）：`curl -fsSL https://browser-use.com/profile.sh | sh`
- Secrets（按域名凭据）
- 1Password（最安全，自动 2FA）

**被网站阻止？**
- 隐身模式默认开启
- 尝试不同的代理国家
- 设置 `flash_mode=False`（更慢但更仔细）

**被限速？**
- 自动重试并退避
- 如果持续限速请升级套餐

**停止会话：**
```bash
curl -X PATCH https://api.browser-use.com/api/v2/sessions/<id> \
     -H "X-Browser-Use-API-Key: $BROWSER_USE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"action": "stop"}'
```
