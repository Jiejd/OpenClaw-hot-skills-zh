# 更新日志 - Web Search Plus

## [2.9.0] - 2026-03-12

### ✨ 新提供商：Querit（多语言 AI 搜索）

[Querit.ai](https://querit.ai) 是一家总部位于新加坡的多语言 AI 搜索 API，专为 LLM 和 RAG 管道设计。拥有 3000 亿页面索引，覆盖 20+ 国家，支持 10+ 种语言。

- 新增 **Querit** 作为第 7 个搜索提供商，通过 `https://api.querit.ai/v1/search` 接入
- 通过 `QUERIT_API_KEY` 配置 — 可选，未设置时自动跳过
- 路由评分：`research * 0.65 + rag * 0.35 + recency * 0.45` — 适合多语言和实时查询
- 正确处理 Querit 特有的 `error_code=200` 响应为成功（而非错误）
- 处理 `IncompleteRead` 为瞬态/可重试失败
- 通过 10 个基准测试查询 ✅

### 🔧 修复：回退链在遇到未配置提供商时崩溃

- `validate_api_key()` 中的 `sys.exit(1)` 抛出 `SystemExit`（继承自 `BaseException`），绕过了 `except Exception` 回退循环，直接终止了进程而不是尝试下一个提供商
- 替换为可捕获的 `ProviderConfigError` — 回退链现在能正确遍历所有已配置的提供商

### 🔧 修复：Perplexity 引用是通用占位符

- 之前通过正则从回答文本中提取引用 URL，导致通用的"来源 1"/"来源 2" 标签
- 现在直接使用 Perplexity API 响应中的结构化 `data["citations"]` 数组 — 结果具有可读标题
- 正则提取保留为 API 未返回 `citations` 字段时的回退方案

### ✨ 改进：德语区域路由模式

- 添加了德语本地和新闻查询的信号模式
- 改善了 `"aktuelle Nachrichten"`、`"beste Restaurants Graz"`、`"KI Regulierung Europa"` 等查询的自动路由

### 📝 文档更新

- 将 Querit 添加到 README 提供商表格、路由示例和 API 密钥设置部分
- 将 `querit_api_key` 添加到 `config.example.json`
- 更新 SKILL.md 中的提供商描述和环境元数据
- 版本号更新到 `2.9.0`


## [2.8.6] - 2026-03-03

### 变更
- 记录了 Perplexity Sonar Pro 的使用方式并刷新了发布文档。

## [2.8.5] - 2026-02-20

### ✨ 功能：Perplexity 时效性过滤器

- 为 Perplexity 提供商添加了 `freshness` 参数（`day`、`week`、`month`、`year`）
- 映射到 Perplexity 原生的 `search_recency_filter` 参数
- 示例：`python3 scripts/search.py -p perplexity -q "最新 AI 新闻" --freshness day`
- 与 Serper 和 Brave 提供商的时效性支持保持一致

## [2.8.4] - 2026-02-20

### 🔒 安全修复：设置向导中的 SSRF 防护

- **修复：** `setup.py` 中 SearXNG 连接测试没有 SSRF 防护（与 `search.py` 不同）
- **之前：** 运营方可能在设置过程中被诱导探测内网
- **之后：** 与 `search.py` 相同的 IP 验证 — 阻止私有 IP、云元数据、环回地址
- **致谢：** ClawHub 安全扫描器

## [2.8.3] - 2026-02-20

### 🐛 关键修复：Perplexity 结果为空

- **修复：** Perplexity 提供商返回 0 个结果，因为 AI 合成的回答未映射到结果数组
- **之前：** 仅返回从回答文本中提取的 URL 作为结果（通常为 0）
- **之后：** 完整回答现在作为主要结果（标题、清理后文本的摘要），提取的来源 URL 作为附加结果
- **影响：** Perplexity 查询现在至少返回 1 个带合成回答的结果

## [2.8.0] - 2026-02-20

### 🆕 新提供商：Perplexity（AI 合成回答）

通过 Kilo Gateway 添加 Perplexity 作为第 6 个搜索提供商 — 第一个返回**带引用的直接回答**而非仅链接的提供商：

#### 功能
- **AI 合成回答**：获取完整答案，而非链接列表
- **行内引用**：每个声明都有 `[1][2][3]` 来源引用
- **实时网络搜索**：Perplexity 实时搜索网络、阅读页面并总结
- **零额外配置**：通过 Kilo Gateway 使用你现有的 `KILOCODE_API_KEY`
- **模型：** `perplexity/sonar-pro`（最佳质量，支持复杂查询）

#### 自动路由信号
新的直接回答意图检测会将以下查询路由到 Perplexity：
- 状态查询："status of"、"current state of"、"what is the status"
- 本地信息："events in [city]"、"things to do in"、"what's happening in"
- 直接问题："what is"、"who is"、"when did"、"how many"
- 时事："this week"、"this weekend"、"right now"、"today"

#### 使用示例
```bash
# 自动路由
python3 scripts/search.py -q "格拉茨这周末有什么活动"  # → Perplexity
python3 scripts/search.py -q "以太坊当前升级状态"       # → Perplexity

# 显式指定
python3 scripts/search.py -p perplexity -q "最新 AI 监管新闻"
```

#### 配置
需要 `KILOCODE_API_KEY` 环境变量（Kilo Gateway 账户）。
无需额外 API 密钥 — Perplexity 通过 Kilo 统一 API 接入。

```bash
export KILOCODE_API_KEY="你的-kilo-密钥"
```

### 🔧 路由再平衡

自动路由置信度评分的重大改版，修复 Serper 独大问题：

#### 问题
Serper（Google）因以下原因赢得约 90% 的查询：
- 高时效性乘数让 Serper 在任何含日期/年份的查询上都胜出
- 默认提供商优先级在平局时将 Serper 排在第一
- 研究和发现信号不够强以覆盖

#### 变更
- **降低 Serper 时效性乘数** — 提到日期不再自动路由到 Google
- **增强 Tavily 的研究信号**：
  - 新增："status of"、"what happened with"、"how does X compare"
  - 提升对比模式的权重（4.0 → 5.0）
- **增强 Exa 的发现信号**：
  - 新增："events in"、"things to do in"、"startups similar to"
  - 提升本地发现模式的权重
- **更新提供商优先级顺序**：`tavily → exa → perplexity → serper → you → searxng`
  - Serper 从平局第 1 降至第 4
  - 研究/发现提供商现在在模糊查询中胜出

## [2.7.0] - 2026-02-14

### ✨ 新增
- `.cache/provider_health.json` 中的提供商冷却追踪
- 提供商故障时指数冷却：**1分钟 → 5分钟 → 25分钟 → 1小时（上限）**
- 瞬态故障的重试策略（超时、429、503）：最多 2 次重试，退避 **1秒 → 3秒 → 9秒**
- 更智能的缓存键，基于完整请求上下文的哈希（查询/提供商/max_results + 区域、时效性、时间范围、主题、搜索引擎、include_news 等）
- 回退合并时按标准化 URL 进行跨提供商结果去重

### 🔧 变更
- 冷却中的提供商在路由时被跳过
- 成功请求后提供商健康状态自动重置
- 回退输出现在包含去重元数据

## [2.6.5] - 2026-02-11

### 🆕 基于文件的搜索结果缓存

添加本地缓存以节省重复搜索的 API 费用。

## [2.6.1] - 2026-02-04

- 隐私清理：从文档中移除硬编码路径和个人信息

## [2.5.0] - 2026-02-03

### 🆕 新提供商：SearXNG（隐私优先元搜索）

添加 SearXNG 作为第 5 个搜索提供商，专注于隐私和自托管搜索。

## [2.4.4] - 2026-02-03

### 📝 文档：提供商数量修正

- **修复：** "你可以使用 1、2 或 3 个" → "1、2、3 或全部 4 个"（我们现在有 4 个提供商了！）

## [2.4.3] - 2026-02-03

### 📝 文档：更新 README

- **新增：** SKILL.md 中 You.com 的 "v2.4.2 新增" 标记

## [2.4.2] - 2026-02-03

### 🐛 关键修复：You.com API 配置

- **修复：** 错误的主机名（`api.ydc-index.io` → `ydc-index.io`）
- **修复：** 错误的请求头名称（`X-API-Key` → `X-API-KEY` 大写）
- **影响：** You.com 现在正常工作 — 之前一直返回 403 Forbidden

## [2.4.1] - 2026-02-03

### 🐛 修复：You.com URL 编码

- **修复：** You.com 查询的 URL 编码问题 — 空格和特殊字符现在能正确编码

## [2.4.0] - 2026-02-03

### 🆕 新提供商：You.com

添加 You.com 作为第 4 个搜索提供商，为 RAG 应用和实时信息优化。

## [2.1.5] - 2026-01-27

### 📝 文档

- 添加关于不要在核心 OpenClaw 配置中使用 Tavily/Serper/Exa 的警告
- 核心 OpenClaw 仅支持 `brave` 作为内置提供商
- 本技能的提供商必须通过环境变量和脚本使用，而非 `openclaw.json`

## [2.1.0] - 2026-01-23

### 🧠 智能多信号路由

完全重构自动路由，引入精密的查询分析。

## [2.0.0] - 2026-01-23

### 🎉 主要功能

- **智能自动路由** — 基于查询分析的自动提供商选择
- **用户配置** — config.json 完整控制自动路由行为
- **调试工具** — --explain-routing 查看提供商选择原因

## [1.0.x] - 初始版本

- 多提供商搜索：Serper、Tavily、Exa
- 手动提供商选择 `-p`
- 统一 JSON 输出格式
- 提供商特定选项
