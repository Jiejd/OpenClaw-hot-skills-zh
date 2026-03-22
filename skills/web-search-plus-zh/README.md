# Web Search Plus

> 带有**智能自动路由**的统一多提供商网络搜索 — 通过多信号分析自动在 **Serper**、**Tavily**、**Querit**、**Exa**、**Perplexity (Sonar Pro)**、**You.com** 和 **SearXNG** 之间选择，并附带置信度评分。

[![ClawHub](https://img.shields.io/badge/ClawHub-web--search--plus-blue)](https://clawhub.ai)
[![Version](https://img.shields.io/badge/version-2.9.0-green)](https://clawhub.ai)
[![GitHub](https://img.shields.io/badge/GitHub-web--search--plus-blue)](https://github.com/robbyczgw-cla/web-search-plus)

---

## 🧠 功能特性 (v2.9.0)

**智能多信号路由** — 技能使用精密的查询分析：

- **意图分类**：购物 vs 研究 vs 发现 vs RAG/实时 vs 隐私
- **语言模式**："多少钱"（价格）vs "怎么工作"（研究）vs "私密"（隐私）
- **实体检测**：产品+品牌组合、URL、域名
- **复杂度分析**：长查询更偏向研究型提供商
- **置信度评分**：了解路由决策的可靠程度

```bash
python3 scripts/search.py -q "iPhone 16 多少钱"        # → Serper（68% 置信度）
python3 scripts/search.py -q "量子纠缠是怎么工作的"      # → Tavily（86% 高）
python3 scripts/search.py -q "类似 Notion 的创业公司"    # → Exa（76% 高）
python3 scripts/search.py -q "类似 stripe.com 的公司"    # → Exa（100% 高 - 检测到 URL）
python3 scripts/search.py -q "总结 AI 的关键要点"        # → You.com（68% 中 - RAG 意图）
python3 scripts/search.py -q "私密搜索不被追踪"           # → SearXNG（74% 高 - 隐私意图）
```

---

## 🔍 什么时候用哪个提供商

### 内置 Brave 搜索（OpenClaw 默认）
- ✅ 通用网络搜索
- ✅ 注重隐私
- ✅ 快速查询
- ✅ 默认回退选项

### Serper（Google 结果）
- 🛍 **产品规格、价格、购物**
- 📍 **本地商家、地点**
- 🎯 **"Google 一下" — 需要真正的 Google 结果**
- 📰 **需要购物/图片结果**
- 🏆 **知识图谱数据**

### Tavily（AI 优化研究搜索）
- 📚 **研究问题、深度挖掘**
- 🔬 **复杂的多部分查询**
- 📄 **需要完整页面内容**（不只是摘要）
- 🎓 **学术/技术研究**
- 🔒 **域名过滤**（可信来源）

### Querit（多语言 AI 搜索）
- 🌏 **覆盖 10+ 语言的多语言 AI 搜索**
- ⚡ **快速实时回答**，延迟约 400ms
- 🗺️ **国际/跨语言查询**
- 📰 **时效感知结果**，获取最新信息
- 🤖 **适合 AI 工作流**，提供干净元数据

### Exa（神经语义搜索）
- 🔗 **查找相似页面**
- 🏢 **公司/创业公司发现**
- 📝 **研究论文**
- 💻 **GitHub 项目**
- 📅 **特定日期内容**

### Perplexity（通过 Kilo Gateway 的 Sonar Pro）
- ⚡ **直接回答**（适合"谁/什么/定义"类问题）
- 🧾 **带引用的、答案优先输出**
- 🕒 **时事/"截至"类问题**
- 🔑 通过 `KILOCODE_API_KEY` 认证（路由到 `https://api.kilo.ai`）

### You.com（RAG/实时）
- 🤖 **RAG 应用**（LLM 就绪的摘要片段）
- 📰 **网络 + 新闻合一体**（单次 API 调用）
- ⚡ **实时信息**（时事动态）
- 📋 **摘要上下文**（"最新的..."）
- 🔄 **实时爬取**（按需获取完整页面内容）

### SearXNG（隐私优先/自托管）
- 🔒 **保护隐私的搜索**（无追踪）
- 🌐 **多源聚合**（70+ 搜索引擎）
- 💰 **$0 API 费用**（自托管）
- 🎯 **多元视角**（来自多个引擎的结果）
- 🏠 **自托管环境**（完全掌控）

---

## 目录

- [快速开始](#快速开始)
- [智能自动路由](#智能自动路由)
- [配置指南](#配置指南)
- [提供商详解](#提供商详解)
- [使用示例](#使用示例)
- [工作流示例](#工作流示例)
- [优化技巧](#优化技巧)
- [常见问题与排障](#常见问题与排障)
- [API 参考](#api-参考)

---

## 快速开始

### 方式 A：交互式设置（推荐）

```bash
# 运行设置向导 — 引导你完成所有步骤
python3 scripts/setup.py
```

向导会逐一介绍每个提供商、收集你的 API 密钥，并自动创建 `config.json`。

### 方式 B：手动设置

```bash
# 1. 设置至少一个 API 密钥（或 SearXNG 实例）
export SERPER_API_KEY="你的密钥"   # https://serper.dev
export TAVILY_API_KEY="你的密钥"   # https://tavily.com
export QUERIT_API_KEY="你的密钥"   # https://querit.ai
export EXA_API_KEY="你的密钥"      # https://exa.ai
export KILOCODE_API_KEY="你的密钥" # 启用 Perplexity Sonar Pro，通过 https://api.kilo.ai
export YOU_API_KEY="你的密钥"      # https://api.you.com
export SEARXNG_INSTANCE_URL="https://your-instance.example.com"  # 自托管

# 2. 执行搜索（自动路由！）
python3 scripts/search.py -q "2024 最好的笔记本电脑"
```

### 执行搜索

```bash
# 自动路由到最佳提供商
python3 scripts/search.py -q "2024 最好的笔记本电脑"

# 或显式指定提供商
python3 scripts/search.py -p serper -q "iPhone 16 规格"
python3 scripts/search.py -p tavily -q "量子计算详解" --depth advanced
python3 scripts/search.py -p querit -q "德国最新 AI 政策动态"
python3 scripts/search.py -p exa -q "2024 AI 创业公司" --category company
python3 scripts/search.py -p perplexity -q "奥地利总统是谁？"
```

---

## 智能自动路由

### 工作原理

当你不指定提供商时，技能会分析你的查询并路由到最佳提供商：

| 查询包含 | 路由到 | 示例 |
|---------------|-----------|---------|
| "价格"、"买"、"购物"、"费用" | **Serper** | "iPhone 16 价格" |
| "附近"、"餐厅"、"酒店" | **Serper** | "我附近的披萨" |
| "天气"、"新闻"、"最新" | **Serper** | "柏林天气" |
| "怎么"、"解释"、"什么是" | **Tavily** | "TCP 是怎么工作的" |
| "研究"、"分析"、"学习" | **Tavily** | "气候研究" |
| "教程"、"指南" | **Tavily** | "Python 教程" |
| 多语言、最新状态、最新更新 | **Querit** | "德国最新 AI 政策动态" |
| "类似"、"像 X 的公司" | **Exa** | "类似 Stripe 的公司" |
| "创业公司"、"A 轮" | **Exa** | "AI 创业公司 A 轮" |
| "github"、"研究论文" | **Exa** | "LLM 论文 arxiv" |
| "私密"、"匿名"、"不追踪" | **SearXNG** | "私密搜索" |
| "多个来源"、"聚合" | **SearXNG** | "所有引擎的结果" |

### 示例

```bash
# 这些都会自动路由到最佳提供商：
python3 scripts/search.py -q "MacBook Pro M3 价格"         # → Serper
python3 scripts/search.py -q "HTTPS 是怎么工作的"          # → Tavily
python3 scripts/search.py -q "德国最新 AI 政策动态"        # → Querit
python3 scripts/search.py -q "类似 Notion 的创业公司"       # → Exa
python3 scripts/search.py -q "附近最好的寿司店"            # → Serper
python3 scripts/search.py -q "解释注意力机制"              # → Tavily
python3 scripts/search.py -q "Figma 的替代品"              # → Exa
python3 scripts/search.py -q "私密搜索不被追踪"            # → SearXNG
```

### 结果缓存（v2.7.x 引入）

搜索结果会**自动缓存** 1 小时以节省 API 费用：

```bash
# 第一次请求：从 API 获取（消耗额度）
python3 scripts/search.py -q "2024 AI 创业公司"

# 第二次请求：使用缓存（免费！）
python3 scripts/search.py -q "2024 AI 创业公司"
# 输出包含："cached": true

# 绕过缓存（强制获取最新结果）
python3 scripts/search.py -q "2024 AI 创业公司" --no-cache

# 查看缓存统计
python3 scripts/search.py --cache-stats

# 清除所有缓存
python3 scripts/search.py --clear-cache

# 自定义 TTL（秒，默认：3600 = 1 小时）
python3 scripts/search.py -q "查询" --cache-ttl 7200
```

**缓存位置：** 技能目录下的 `.cache/`（可通过 `WSP_CACHE_DIR` 环境变量覆盖）

### 调试自动路由

查看选择某个提供商的具体原因：

```bash
python3 scripts/search.py --explain-routing -q "最好的笔记本电脑推荐"
```

输出：
```json
{
  "query": "最好的笔记本电脑推荐",
  "selected_provider": "serper",
  "reason": "matched_keywords (score=2)",
  "matched_keywords": ["最好"],
  "available_providers": ["serper", "tavily", "exa"]
}
```

### 结果中的路由信息

每条搜索结果都包含路由信息：

```json
{
  "provider": "serper",
  "query": "iPhone 16 价格",
  "results": [...],
  "routing": {
    "auto_routed": true,
    "selected_provider": "serper",
    "reason": "matched_keywords (score=1)",
    "matched_keywords": ["价格"]
  }
}
```

---

## 配置指南

### 环境变量

创建 `.env` 文件或在 shell 中设置：

```bash
# 必需：至少设置一个
export SERPER_API_KEY="你的-serper-密钥"
export TAVILY_API_KEY="你的-tavily-密钥"
export EXA_API_KEY="你的-exa-密钥"
```

### 配置文件 (config.json)

`config.json` 文件让你自定义自动路由和提供商默认设置：

```json
{
  "defaults": {
    "provider": "serper",
    "max_results": 5
  },
  
  "auto_routing": {
    "enabled": true,
    "fallback_provider": "serper",
    "provider_priority": ["serper", "tavily", "exa"],
    "disabled_providers": [],
    "keyword_mappings": {
      "serper": ["价格", "买", "购物", "费用", "优惠", "附近", "天气"],
      "tavily": ["怎么", "解释", "研究", "什么是", "教程"],
      "exa": ["类似", "像...的公司", "替代品", "创业公司", "github"]
    }
  },
  
  "serper": {
    "country": "us",
    "language": "en"
  },
  
  "tavily": {
    "depth": "basic",
    "topic": "general"
  },
  
  "exa": {
    "type": "neural"
  }
}
```

### 配置示例

#### 示例 1：禁用 Exa（仅使用 Serper + Tavily）

```json
{
  "auto_routing": {
    "disabled_providers": ["exa"]
  }
}
```

#### 示例 2：将 Tavily 设为默认

```json
{
  "auto_routing": {
    "fallback_provider": "tavily"
  }
}
```

#### 示例 3：添加自定义关键词

```json
{
  "auto_routing": {
    "keyword_mappings": {
      "serper": [
        "price", "buy", "shop", "amazon", "ebay", "walmart",
        "deal", "discount", "coupon", "sale", "cheap"
      ],
      "tavily": [
        "how does", "explain", "research", "what is",
        "coursera", "udemy", "learn", "course", "certification"
      ],
      "exa": [
        "similar to", "companies like", "competitors",
        "YC company", "funded startup", "Series A", "Series B"
      ]
    }
  }
}
```

#### 示例 4：Serper 使用德语区域

```json
{
  "serper": {
    "country": "de",
    "language": "de"
  }
}
```

#### 示例 5：禁用自动路由

```json
{
  "auto_routing": {
    "enabled": false
  },
  "defaults": {
    "provider": "serper"
  }
}
```

#### 示例 6：研究密集型配置

```json
{
  "auto_routing": {
    "fallback_provider": "tavily",
    "provider_priority": ["tavily", "serper", "exa"]
  },
  "tavily": {
    "depth": "advanced",
    "include_raw_content": true
  }
}
```

---

## 提供商详解

### Serper（Google 搜索 API）

**简介：** 通过 API 直接访问 Google 搜索结果 — 和你在 google.com 上看到的一样。

#### 优势
| 优势 | 说明 |
|----------|-------------|
| 🎯 **准确性** | Google 的搜索质量、知识图谱、精选摘要 |
| 🛒 **购物** | 产品价格、评论、购物结果 |
| 📍 **本地** | 商家列表、地图、地点 |
| 📰 **新闻** | 实时新闻，整合 Google News |
| 🖼 **图片** | Google 图片搜索 |
| ⚡ **速度** | 最快响应时间（约 200-400ms） |

#### 最佳使用场景
- ✅ 产品规格和对比
- ✅ 购物和价格查询
- ✅ 本地商家搜索（"附近的餐厅"）
- ✅ 快速事实查询（天气、换算、定义）
- ✅ 新闻标题和时事
- ✅ 图片搜索
- ✅ 当你需要"Google 的结果"时

#### 获取 API 密钥
1. 访问 [serper.dev](https://serper.dev)
2. 用邮箱或 Google 注册
3. 从控制台复制 API 密钥
4. 设置 `SERPER_API_KEY` 环境变量

---

### Tavily（研究搜索）

**简介：** 为研究和 RAG 应用优化的 AI 搜索引擎 — 返回合成答案加完整内容。

#### 优势
| 优势 | 说明 |
|----------|-------------|
| 📚 **研究质量** | 为全面、准确的研究优化 |
| 💬 **AI 回答** | 返回合成答案，不只是链接 |
| 📄 **完整内容** | 可返回完整页面内容 (raw_content) |
| 🎯 **域名过滤** | 包含/排除特定域名 |
| 🔬 **深度模式** | 用于深度研究的高级搜索 |
| 📰 **主题模式** | 支持通用 vs 新闻内容 |

#### 最佳使用场景
- ✅ 需要合成答案的研究问题
- ✅ 学术或技术深度挖掘
- ✅ 需要实际页面内容（不只是摘要）
- ✅ 多源信息对比
- ✅ 特定领域研究（过滤权威来源）
- ✅ 带上下文的新闻研究
- ✅ RAG/LLM 应用

#### 获取 API 密钥
1. 访问 [tavily.com](https://tavily.com)
2. 注册并验证邮箱
3. 进入 API Keys 部分
4. 生成并复制密钥
5. 设置 `TAVILY_API_KEY` 环境变量

---

### Exa（神经搜索）

**简介：** 神经/语义搜索引擎，理解含义而非仅匹配关键词 — 查找概念相似的内容。

#### 优势
| 优势 | 说明 |
|----------|-------------|
| 🧠 **语义理解** | 按含义查找结果，而非关键词 |
| 🔗 **相似页面** | 查找与参考 URL 相似的页面 |
| 🏢 **公司发现** | 擅长发现创业公司和公司 |
| 📑 **分类过滤** | 按类型过滤（公司、论文、推文等） |
| 📅 **日期过滤** | 精确日期范围搜索 |
| 🎓 **学术** | 适合研究论文和技术内容 |

#### 最佳使用场景
- ✅ 概念性查询（"做 X 的公司"）
- ✅ 查找类似公司或页面
- ✅ 创业公司和公司发现
- ✅ 研究论文发现
- ✅ 查找 GitHub 项目
- ✅ 日期过滤搜索近期内容
- ✅ 关键词匹配失败时

#### 获取 API 密钥
1. 访问 [exa.ai](https://exa.ai)
2. 用邮箱或 Google 注册
3. 进入控制台的 API 部分
4. 复制 API 密钥
5. 设置 `EXA_API_KEY` 环境变量

---

### SearXNG（隐私优先元搜索）

**简介：** 开源自托管元搜索引擎，聚合 70+ 搜索引擎的结果且不追踪。

#### 优势
| 优势 | 说明 |
|----------|-------------|
| 🔒 **隐私优先** | 无追踪、无画像、无数据收集 |
| 🌐 **多引擎** | 聚合 Google、Bing、DuckDuckGo 等 70+ 引擎 |
| 💰 **免费** | $0 API 费用（自托管，无限查询） |
| 🎯 **多元结果** | 从多个搜索引擎获取不同视角 |
| ⚙ **可定制** | 选择使用的引擎、安全搜索、语言 |
| 🏠 **自托管** | 完全掌控你的搜索基础设施 |

#### 最佳使用场景
- ✅ 隐私敏感的搜索（无追踪）
- ✅ 想从多个引擎获取不同结果
- ✅ 预算有限（无 API 费用）
- ✅ 自托管/隔离网络环境
- ✅ 付费 API 被限流时的回退
- ✅ "聚合所有结果"为目标时

#### 搭建你的实例
```bash
# Docker（推荐，5 分钟）
docker run -d -p 8080:8080 searxng/searxng

# 在 settings.yml 中启用 JSON API：
# search:
#   formats: [html, json]
```

1. 参见 [docs.searxng.org](https://docs.searxng.org/admin/installation.html)
2. 通过 Docker、pip 或你偏好的方式部署
3. 在 `settings.yml` 中启用 JSON 格式
4. 设置 `SEARXNG_INSTANCE_URL` 环境变量

---

## 使用示例

### 自动路由搜索（推荐）

```bash
# 直接搜 — 技能帮你选择最佳提供商
python3 scripts/search.py -q "特斯拉 Model 3 价格"
python3 scripts/search.py -q "神经网络是怎么学习的"
python3 scripts/search.py -q "类似 Stripe 的 YC 创业公司"
python3 scripts/search.py -q "私密搜索不被追踪"
```

### Serper 选项

```bash
# 不同搜索类型
python3 scripts/search.py -p serper -q "游戏显示器" --type shopping
python3 scripts/search.py -p serper -q "咖啡店" --type places
python3 scripts/search.py -p serper -q "AI 新闻" --type news

# 时间过滤
python3 scripts/search.py -p serper -q "OpenAI 新闻" --time-range day

# 包含图片
python3 scripts/search.py -p serper -q "iPhone 16 Pro" --images

# 不同区域
python3 scripts/search.py -p serper -q "维也纳天气" --country at --language de
```

### Tavily 选项

```bash
# 深度研究模式
python3 scripts/search.py -p tavily -q "量子计算应用" --depth advanced

# 包含完整页面内容
python3 scripts/search.py -p tavily -q "transformer 架构" --raw-content

# 域名过滤
python3 scripts/search.py -p tavily -q "AI 研究" --include-domains arxiv.org nature.com
```

### Exa 选项

```bash
# 分类过滤
python3 scripts/search.py -p exa -q "AI 创业公司 A 轮" --category company
python3 scripts/search.py -p exa -q "注意力机制" --category "research paper"

# 日期过滤
python3 scripts/search.py -p exa -q "YC 公司" --start-date 2024-01-01

# 查找相似页面
python3 scripts/search.py -p exa --similar-url "https://stripe.com" --category company
```

### SearXNG 选项

```bash
# 基本搜索
python3 scripts/search.py -p searxng -q "linux 发行版"

# 指定引擎
python3 scripts/search.py -p searxng -q "AI 新闻" --engines "google,bing,duckduckgo"

# 安全搜索（0=关, 1=中等, 2=严格）
python3 scripts/search.py -p searxng -q "隐私工具" --searxng-safesearch 2

# 时间过滤
python3 scripts/search.py -p searxng -q "开源项目" --time-range week

# 自定义实例 URL
python3 scripts/search.py -p searxng -q "测试" --searxng-url "http://localhost:8080"
```

---

## 工作流示例

### 🛒 产品研究工作流

```bash
# 第 1 步：获取产品规格（自动路由到 Serper）
python3 scripts/search.py -q "MacBook Pro M3 Max 规格"

# 第 2 步：查看价格（自动路由到 Serper）
python3 scripts/search.py -q "MacBook Pro M3 Max 价格对比"

# 第 3 步：深度评测（自动路由到 Tavily）
python3 scripts/search.py -q "MacBook Pro M3 Max 详细评测"
```

### 📚 学术研究工作流

```bash
# 第 1 步：了解主题（自动路由到 Tavily）
python3 scripts/search.py -q "解释深度学习中的 transformer 架构"

# 第 2 步：查找最新论文（Exa）
python3 scripts/search.py -p exa -q "transformer 改进" --category "research paper" --start-date 2024-01-01

# 第 3 步：查找实现（Exa）
python3 scripts/search.py -p exa -q "transformer 实现" --category github
```

### 🏢 竞品分析工作流

```bash
# 第 1 步：查找竞品（自动路由到 Exa）
python3 scripts/search.py -q "类似 Notion 的公司"

# 第 2 步：查找类似产品（Exa）
python3 scripts/search.py -p exa --similar-url "https://notion.so" --category company

# 第 3 步：深度对比（Tavily）
python3 scripts/search.py -p tavily -q "Notion vs Coda 对比" --depth advanced
```

---

## 优化技巧

### 成本优化

| 技巧 | 节省 |
|-----|---------|
| 常规查询使用 SearXNG | **$0 API 费用** |
| 使用自动路由（默认选最便宜的 Serper） | 性价比最高 |
| 先用 Tavily `basic` 再用 `advanced` | 减少约 50% 成本 |
| 设置合适的 `max_results` | 线性节省成本 |
| 仅在语义查询时使用 Exa | 避免浪费 |

### 性能优化

| 技巧 | 影响 |
|-----|--------|
| Serper 最快（约 200ms） | 适合时间敏感查询 |
| Tavily `basic` 比 `advanced` 快 | 约快 2 倍 |
| 降低 `max_results` = 更快响应 | 线性提升 |

---

## 常见问题与排障

### 一般问题

**问：我需要为所有提供商都配 API 密钥吗？**
> 不需要。只需为你想用的提供商配置密钥。自动路由会跳过没有密钥的提供商。

**问：我应该从哪个提供商开始？**
> Serper — 最快、最便宜，且有最大的免费额度（2,500 次查询）。

**问：可以在一个工作流中使用多个提供商吗？**
> 可以！这也是推荐的方式。参见[工作流示例](#工作流示例)。

**问：怎么降低 API 费用？**
> 使用自动路由（默认选最便宜的）、降低 `max_results`、先用 Tavily `basic` 再用 `advanced`。

### 自动路由问题

**问：为什么我的查询去了"错误"的提供商？**
> 用 `--explain-routing` 调试。必要时在 config.json 中添加自定义关键词。

**问：可以添加自己的关键词吗？**
> 可以！编辑 `config.json` → `auto_routing.keyword_mappings`。

**问：关键词评分怎么工作？**
> 多词短语权重更高。"companies like"（2 个词）比 "like"（1 个词）分数更高。

**问：如果没有关键词匹配怎么办？**
> 使用回退提供商（默认：Serper）。

**问：可以强制指定某个提供商吗？**
> 可以，用 `-p serper`、`-p tavily` 或 `-p exa`。

### 排障

**错误："缺少 API 密钥"**
```bash
# 检查密钥是否设置
echo $SERPER_API_KEY

# 设置它
export SERPER_API_KEY="你的密钥"
```

**错误："API 错误 (401)"**
> 你的 API 密钥无效或已过期。请生成一个新的。

**错误："API 错误 (429)"**
> 达到频率限制。等待后重试，或升级套餐。

**空结果？**
> 试试不同的提供商、扩大查询范围或移除限制性过滤器。

**响应慢？**
> 降低 `max_results`、使用 Tavily `basic` 或用 Serper（最快）。

---

## API 参考

### 输出格式

所有提供商返回统一的 JSON：

```json
{
  "provider": "serper|tavily|exa",
  "query": "原始搜索查询",
  "results": [
    {
      "title": "页面标题",
      "url": "https://example.com/page",
      "snippet": "内容摘要...",
      "score": 0.95,
      "date": "2024-01-15",
      "raw_content": "完整页面内容（仅 Tavily）"
    }
  ],
  "images": ["url1", "url2"],
  "answer": "合成答案",
  "knowledge_graph": { },
  "routing": {
    "auto_routed": true,
    "selected_provider": "serper",
    "reason": "matched_keywords (score=1)",
    "matched_keywords": ["price"]
  }
}
```

### CLI 选项参考

| 选项 | 提供商 | 说明 |
|--------|-----------|-------------|
| `-q, --query` | 全部 | 搜索查询 |
| `-p, --provider` | 全部 | 提供商：auto, serper, tavily, querit, exa, perplexity, you, searxng |
| `-n, --max-results` | 全部 | 最大结果数（默认：5） |
| `--auto` | 全部 | 强制自动路由 |
| `--explain-routing` | 全部 | 调试自动路由 |
| `--images` | Serper, Tavily | 包含图片 |
| `--country` | Serper, You | 国家代码（默认：us） |
| `--language` | Serper, SearXNG | 语言代码（默认：en） |
| `--type` | Serper | search/news/images/videos/places/shopping |
| `--time-range` | Serper, SearXNG | hour/day/week/month/year |
| `--depth` | Tavily | basic/advanced |
| `--topic` | Tavily | general/news |
| `--raw-content` | Tavily | 包含完整页面内容 |
| `--querit-base-url` | Querit | 覆盖 Querit API 基础 URL |
| `--querit-base-path` | Querit | 覆盖 Querit API 路径 |
| `--exa-type` | Exa | neural/keyword |
| `--category` | Exa | company/research paper/news/pdf/github/tweet |
| `--start-date` | Exa | 开始日期 (YYYY-MM-DD) |
| `--end-date` | Exa | 结束日期 (YYYY-MM-DD) |
| `--similar-url` | Exa | 查找相似页面 |
| `--searxng-url` | SearXNG | 实例 URL |
| `--searxng-safesearch` | SearXNG | 0=关, 1=中等, 2=严格 |
| `--engines` | SearXNG | 指定引擎 (google,bing,duckduckgo) |
| `--categories` | SearXNG | 搜索分类 (general,images,news) |
| `--include-domains` | Tavily, Exa | 仅这些域名 |
| `--exclude-domains` | Tavily, Exa | 排除这些域名 |
| `--compact` | 全部 | 紧凑 JSON 输出 |

---

## 许可证

MIT

---

## 链接

- [Serper](https://serper.dev) — Google 搜索 API
- [Tavily](https://tavily.com) — AI 研究搜索
- [Exa](https://exa.ai) — 神经网络搜索
- [ClawHub](https://clawhub.ai) — OpenClaw 技能
