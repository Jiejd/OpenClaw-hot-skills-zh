# 监控与可观测性

## 目录
- [成本追踪](#成本追踪)
- [Laminar](#laminar)
- [OpenLIT（OpenTelemetry）](#openlit-opentelemetry)
- [遥测](#遥测)

---

## 成本追踪

```python
agent = Agent(task="...", llm=llm, calculate_cost=True)
history = await agent.run()

# 访问使用量数据
usage = history.usage
# 或通过服务
summary = await agent.token_cost_service.get_usage_summary()
```

## Laminar

原生 AI 代理监控集成，支持浏览器会话视频回放。

### 设置

```bash
pip install lmnr
```

```python
from lmnr import Laminar

Laminar.initialize()  # 设置 LMNR_PROJECT_API_KEY 环境变量
```

### 功能

- 代理执行步骤捕获，附带时间线
- 浏览器会话录制（完整视频回放）
- 成本和 Token 追踪
- 追踪可视化

### 认证

使用 `browser-use auth` 进行云端同步（OAuth 设备流程），或自托管 Laminar。

## OpenLIT（OpenTelemetry）

零代码 OpenTelemetry 接入：

### 设置

```bash
pip install openlit browser-use
```

```python
import openlit

openlit.init()  # 就这么简单 — 自动接入 browser-use
```

### 功能

- 执行流程可视化
- 成本和 Token 追踪
- 通过代理思考过程调试失败
- 性能优化建议

### 自定义 OTLP 端点

```python
openlit.init(otlp_endpoint="http://your-collector:4318")
```

### 集成

支持：Jaeger、Prometheus、Grafana、Datadog、New Relic、Elastic APM。

### 自托管

```bash
docker run -d -p 3000:3000 -p 4318:4318 openlit/openlit
```

## 遥测

Browser Use 通过 PostHog 收集匿名使用数据。

### 退出遥测

```bash
ANONYMIZED_TELEMETRY=false
```

或在 Python 中：

```python
import os
os.environ["ANONYMIZED_TELEMETRY"] = "false"
```

零性能影响。来源：[遥测服务](https://github.com/browser-use/browser-use/tree/main/browser_use/telemetry)。
