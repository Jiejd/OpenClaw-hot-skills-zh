# 常见问题

## 缓存（v2.7.0 新增！）

### 缓存是怎么工作的？
搜索结果会自动在本地缓存 1 小时（3600 秒）。当你再次执行相同查询时，会立即获得结果且 $0 API 费用。缓存键基于：查询文本 + 提供商 + max_results。

### 缓存结果存在哪里？
默认在技能目录下的 `.cache/` 中。可通过 `WSP_CACHE_DIR` 环境变量覆盖：
```bash
export WSP_CACHE_DIR="/path/to/custom/cache"
```

### 怎么查看缓存统计？
```bash
python3 scripts/search.py --cache-stats
```
会显示总条目数、大小、最旧/最新条目，以及按提供商的分布。

### 怎么清除缓存？
```bash
python3 scripts/search.py --clear-cache
```

### 可以修改缓存 TTL 吗？
可以！默认是 3600 秒（1 小时）。可按请求设置自定义 TTL：
```bash
python3 scripts/search.py -q "查询" --cache-ttl 7200  # 2 小时
```

### 怎么跳过缓存？
使用 `--no-cache` 强制获取最新结果：
```bash
python3 scripts/search.py -q "查询" --no-cache
```

### 怎么知道结果是否来自缓存？
响应中包含：
- `"cached": true/false` — 结果是否来自缓存
- `"cache_age_seconds": 1234` — 缓存结果已存在多久

---

## 一般问题

### 自动路由怎么决定用哪个提供商？
多信号分析根据以下维度为每个提供商评分：价格模式、解释短语、相似性关键词、URL、产品+品牌组合，以及查询复杂度。最高分胜出。使用 `--explain-routing` 查看详细分析。

### 选错了提供商怎么办？
用 `-p serper/tavily/exa` 手动覆盖。用 `--explain-routing` 了解为什么选了不同的提供商。

### "低置信度"是什么意思？
查询存在歧义（例如"特斯拉"可以是汽车、股票或公司）。会回退到 Serper。结果可能有差异。

### 可以禁用某个提供商吗？
可以！在 config.json 中设置：`"disabled_providers": ["exa"]`

---

## API 密钥

### 我需要哪些 API 密钥？
至少一个密钥（或 SearXNG 实例）。你可以只用 Serper、只用 Tavily、只用 Exa、只用 You.com，或只用 SearXNG。没有密钥 = 跳过该提供商。

### 去哪里获取 API 密钥？
- Serper: https://serper.dev（2,500 次免费查询，无需信用卡）
- Tavily: https://tavily.com（每月 1,000 次免费搜索）
- Exa: https://exa.ai（每月 1,000 次免费搜索）
- You.com: https://api.you.com（有限的免费额度用于测试）
- SearXNG: 自托管，无需密钥！https://docs.searxng.org/admin/installation.html

### 怎么设置 API 密钥？
两种方式（都会自动加载）：

**方式 A：.env 文件**
```bash
export SERPER_API_KEY="你的密钥"
```

**方式 B：config.json**（v2.2.1+）
```json
{ "serper": { "api_key": "你的密钥" } }
```

---

## 路由详情

### 怎么知道是哪个提供商处理了我的搜索？
查看 JSON 输出中的 `routing.provider`，或聊天回复中的 `[🔍 Searched with: 提供商]`。

### 为什么有时把研究问题路由到了 Serper？
如果查询包含品牌/产品信号（如"特斯拉 FSD 是怎么工作的"），购物意图可能盖过研究意图。用 `-p tavily` 手动覆盖。

### 置信度阈值是多少？
默认：0.3（30%）。低于此值 = 低置信度，使用回退提供商。可在 config.json 中调整。

---

## You.com 相关

### 什么时候该用 You.com 而不是其他提供商？
You.com 擅长：
- **RAG 应用**：预提取的摘要片段，可直接供 LLM 使用
- **实时信息**：时事动态、突发新闻、状态更新
- **合并来源**：网络 + 新闻结果在一次 API 调用中返回
- **摘要任务**："最新的...如何"，"...的关键要点"

### livecrawl 功能是什么？
You.com 可以按需获取完整页面内容。用 `--livecrawl web` 获取网页结果，`--livecrawl news` 获取新闻文章，或 `--livecrawl all` 两者都获取。内容以 Markdown 格式返回。

### You.com 会自动包含新闻吗？
是的！You.com 的智能分类会在查询具有新闻意图时自动包含相关新闻结果。你也可以用 `--include-news` 显式启用。

---

## SearXNG 相关

### 我需要自己的 SearXNG 实例吗？
是的！SearXNG 需要自托管。大多数公共实例为了防止机器人滥用而禁用了 JSON API。你需要运行自己的实例并启用 JSON 格式。参见：https://docs.searxng.org/admin/installation.html

### 怎么搭建 SearXNG？
Docker 是最简单的方式：
```bash
docker run -d -p 8080:8080 searxng/searxng
```
然后在 `settings.yml` 中启用 JSON：
```yaml
search:
  formats:
    - html
    - json
```

### 为什么收到"403 Forbidden"？
实例上的 JSON API 被禁用了。在 `settings.yml` 的 `search.formats` 中启用它。

### SearXNG 的 API 费用是多少？
**$0！** SearXNG 是免费开源的。你只需支付托管费用（VPS 约 $5/月）。无限查询。

### 什么时候该用 SearXNG？
- **隐私敏感查询**：无追踪、无画像
- **预算有限**：$0 API 费用
- **多元结果**：聚合 70+ 搜索引擎
- **自托管需求**：完全掌控搜索基础设施
- **回退提供商**：付费 API 被限流时

### 可以限制 SearXNG 使用的搜索引擎吗？
可以！用 `--engines google,bing,duckduckgo` 指定引擎，或在 config.json 中配置默认值。

---

## 提供商选择

### 我该用哪个提供商？

| 查询类型 | 最佳提供商 | 原因 |
|------------|---------------|-----|
| **购物**（"买笔记本电脑"、"便宜的鞋"） | **Serper** | Google 购物、价格对比、本地商店 |
| **研究**（"X 是怎么工作的？"、"解释 Y"） | **Tavily** | 深度研究、学术质量、完整页面内容 |
| **创业公司/论文**（"类似 X 的公司"、"arxiv 论文"） | **Exa** | 语义/神经搜索、创业公司发现 |
| **RAG/实时**（"总结最新"、"时事"） | **You.com** | LLM 就绪摘要、网络+新闻合一体 |
| **隐私**（"不被追踪地搜索"） | **SearXNG** | 无追踪、多源、自托管 |

**提示：** 启用自动路由，让技能自动选择！🎯

### 我需要全部 5 个提供商吗？
**不需要！** 所有提供商都是可选的。你可以使用：
- **1 个提供商**（例如只用 Serper 处理所有查询）
- **2-3 个提供商**（例如 Serper + You.com 覆盖大部分需求）
- **全部 5 个**（最大灵活性 + 回退选项）

### API 费用大概多少？

| 提供商 | 免费额度 | 付费套餐 |
|----------|-----------|-----------|
| **Serper** | 2,500 次/月 | $50/月（5,000 次） |
| **Tavily** | 1,000 次/月 | $150/月（10,000 次） |
| **Exa** | 1,000 次/月 | $1,000/月（100,000 次） |
| **You.com** | 有限免费 | ~$10/月（按用量） |
| **SearXNG** | **免费** ✅ | 仅 VPS 费用（自托管约 $5/月） |

**省钱提示：** 用 SearXNG 作为主要搜索引擎 + 其他作为回退！

### SearXNG 到底有多隐私？

| 方案 | 隐私级别 |
|-------|---------------|
| **自托管（你的 VPS）** | ⭐⭐⭐⭐⭐ 你掌控一切 |
| **自托管（Docker 本地）** | ⭐⭐⭐⭐⭐ 完全私密 |
| **公共实例** | ⭐⭐⭐ 取决于运营方的日志策略 |

**最佳实践：** 隐私关键时请自托管。

### 哪个提供商的结果最好？

| 维度 | 最优 |
|--------|--------|
| **事实准确性** | Serper (Google) |
| **研究深度** | Tavily |
| **语义查询** | Exa |
| **RAG/AI 上下文** | You.com |
| **来源多样性** | SearXNG（70+ 引擎） |
| **最隐私** | SearXNG（自托管） |

**建议：** 启用多个提供商 + 自动路由以获得最佳整体体验。

### 自动路由是怎么工作的？
技能会分析你的查询中的关键词和模式：

```python
"便宜的笔记本电脑"     → Serper（购物信号）
"AI 是怎么工作的？"    → Tavily（研究/解释）
"类似 X 的公司"        → Exa（语义/相似）
"总结最新新闻"          → You.com（RAG/实时）
"私密搜索"              → SearXNG（隐私信号）
```

**置信度阈值：** 仅在置信度 > 30% 时才路由。否则使用默认提供商。

**手动覆盖：** 用 `-p provider` 强制指定提供商。

---

## 生产使用

### 可以在生产环境使用吗？
**可以！** Web-search-plus 已准备好生产环境：
- ✅ 带自动回退的错误处理
- ✅ 频率限制保护
- ✅ 超时处理（每个提供商 30 秒）
- ✅ API 密钥安全（.env + config.json 已 gitignore）
- ✅ 5 个提供商冗余

**提示：** 监控 API 用量以避免超出免费额度！

### API 额度用完了怎么办？
1. **回退链：** 其他已启用的提供商会自动接管
2. **使用 SearXNG：** 切换到自托管（无限查询）
3. **升级套餐：** 付费套餐有更高限制
4. **临时禁用：** 用 `disabled_providers` 暂时跳过耗尽的 API

---

## 更新

### 怎么更新到最新版本？

**通过 ClawHub（推荐）：**
```bash
clawhub update web-search-plus --registry "https://www.clawhub.ai" --no-input
```

**手动更新：**
```bash
cd /path/to/workspace/skills/web-search-plus/
git pull origin main
python3 scripts/setup.py  # 重新运行以配置新功能
```

### 在哪里报告 bug 或建议功能？
- **GitHub Issues：** https://github.com/robbyczgw-cla/web-search-plus/issues
- **ClawHub：** https://www.clawhub.ai/skills/web-search-plus
