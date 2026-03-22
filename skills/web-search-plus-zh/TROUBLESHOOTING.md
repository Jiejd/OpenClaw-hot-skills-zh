# 排障指南

## 缓存问题 (v2.7.0+)

### 缓存不工作 / 总是重新获取

**症状：**
- 每次请求都打到 API
- 即使重复查询也显示 `"cached": false`

**解决方案：**
1. 检查缓存目录是否存在且可写：
   ```bash
   ls -la .cache/  # 应该在技能目录下存在
   ```
2. 确认没有传递 `--no-cache`
3. 检查磁盘空间是否已满
4. 确保查询完全相同（包括提供商和 max_results）

### 缓存结果过时

**症状：**
- 获取到过时信息
- 缓存 TTL 似乎太长

**解决方案：**
1. 用 `--no-cache` 强制获取最新结果
2. 降低 TTL：`--cache-ttl 1800`（30 分钟）
3. 清除缓存：`python3 scripts/search.py --clear-cache`

### 缓存文件越来越大

**症状：**
- 磁盘空间不足
- `.cache/` 中有很多 .json 文件

**解决方案：**
1. 定期清除缓存：
   ```bash
   python3 scripts/search.py --clear-cache
   ```
2. 设置定时任务每周清除
3. 使用更小的 TTL 让条目更快过期

### 缓存时出现"权限被拒绝"

**症状：**
- stderr 中有缓存写入错误
- 搜索正常但不缓存

**解决方案：**
1. 检查目录权限：`chmod 755 .cache/`
2. 使用自定义缓存目录：`export WSP_CACHE_DIR="/tmp/wsp-cache"`

---

## 常见问题

### "找不到 API 密钥"错误

**症状：**
```
Error: No API key found for serper
```

**解决方案：**
1. 检查技能目录下是否存在 `.env` 文件，格式为 `export VAR=value`
2. 从 v2.2.0 起，密钥会从技能的 `.env` 自动加载
3. 或在系统环境中设置：`export SERPER_API_KEY="..."`
4. 验证 config.json 中的密钥格式：
   ```json
   { "serper": { "api_key": "你的密钥" } }
   ```

**优先级顺序：** config.json > .env > 环境变量

---

### 搜索结果为空

**症状：**
- 搜索没有返回结果
- JSON 输出中显示 `"results": []`

**解决方案：**
1. 检查 API 密钥是否有效（试试提供商的 Web 控制台）
2. 用 `-p` 尝试不同的提供商
3. 有些查询确实没有结果（非常冷门的话题）
4. 检查提供商是否被限流
5. 验证网络连接

**调试：**
```bash
python3 scripts/search.py -q "测试查询" --verbose
```

---

### 频率限制

**症状：**
```
Error: 429 Too Many Requests
Error: Rate limit exceeded
```

**好消息：** 从 v2.2.5 起，自动回退机制已生效！如果某个提供商达到频率限制，脚本会自动尝试下一个提供商。

**解决方案：**
1. 等待频率限制重置（通常是 1 小时或当天结束）
2. 使用不同的提供商：用 `-p tavily` 替代 `-p serper`
3. 检查免费额度限制：
   - Serper: 2,500 次免费（总共）
   - Tavily: 每月 1,000 次免费
   - Exa: 每月 1,000 次免费
4. 升级到付费套餐获取更高限制
5. 使用 SearXNG（自托管，无限）

**回退信息：** 使用回退时，响应中会包含 `routing.fallback_used: true`。

---

### SearXNG："403 Forbidden"

**症状：**
```
Error: 403 Forbidden
Error: JSON format not allowed
```

**原因：** 大多数公共 SearXNG 实例禁用 JSON API 以防止机器人滥用。

**解决方案：** 自托管你自己的实例：
```bash
docker run -d -p 8080:8080 searxng/searxng
```
然后在 `settings.yml` 中启用 JSON：
```yaml
search:
  formats:
    - html
    - json  # 添加这行！
```

重启容器并更新你的配置：
```json
{
  "searxng": {
    "instance_url": "http://localhost:8080"
  }
}
```

---

### SearXNG：响应慢

**症状：**
- SearXNG 需要 2-5 秒
- 其他提供商更快

**解释：** 这是正常行为。SearXNG 并行查询 70+ 上游引擎，比直接 API 调用耗时更长。

**权衡：** 更慢但保护隐私 + 多源 + $0 费用。

**解决方案：**
1. 为了隐私收益接受这个权衡
2. 限制引擎以加快速度：
   ```bash
   python3 scripts/search.py -p searxng -q "查询" --engines "google,bing"
   ```
3. 把 SearXNG 作为回退（排在优先级列表最后）

---

### 自动路由选错了提供商

**症状：**
- 研究查询被路由到了 Serper
- 购物查询被路由到了 Tavily

**调试：**
```bash
python3 scripts/search.py --explain-routing -q "你的查询"
```

会显示完整分析：
```json
{
  "query": "iPhone 16 Pro 多少钱",
  "routing_decision": {
    "provider": "serper",
    "confidence": 0.68,
    "reason": "moderate_confidence_match"
  },
  "scores": {"serper": 7.0, "tavily": 0.0, "exa": 0.0},
  "top_signals": [
    {"matched": "how much", "weight": 4.0},
    {"matched": "brand + product detected", "weight": 3.0}
  ]
}
```

**解决方案：**
1. 用显式提供商覆盖：`-p tavily`
2. 重新表述查询使意图更明确
3. 在 config.json 中调整 `confidence_threshold`（默认：0.3）

---

### 配置未加载

**症状：**
- config.json 的更改未生效
- 使用默认值

**解决方案：**
1. 检查 JSON 语法（用验证器）
2. 确保文件在技能目录中：`/path/to/skills/web-search-plus/config.json`
3. 检查文件权限
4. 运行设置向导重新生成：
   ```bash
   python3 scripts/setup.py --reset
   ```

**验证 JSON：**
```bash
python3 -m json.tool config.json
```

---

### Python 依赖缺失

**症状：**
```
ModuleNotFoundError: No module named 'requests'
```

**解决方案：**
```bash
pip3 install requests
```

或安装所有依赖：
```bash
pip3 install -r requirements.txt
```

---

### 超时错误

**症状：**
```
Error: Request timeout after 30s
```

**原因：**
- 网络连接慢
- 提供商 API 问题
- SearXNG 实例过载

**解决方案：**
1. 重试（临时问题）
2. 切换提供商：`-p serper`
3. 检查你的网络连接
4. 如果使用 SearXNG，检查实例健康状态

---

### 重复结果

**症状：**
- 同一结果出现多次
- 不同提供商的结果重叠

**解决方案：** 使用自动回退或多个提供商时这是正常的。技能不会跨提供商去重。

单提供商结果：
```bash
python3 scripts/search.py -p serper -q "查询"
```

---

## 调试模式

详细调试：

```bash
# 详细输出
python3 scripts/search.py -q "查询" --verbose

# 显示路由决策
python3 scripts/search.py -q "查询" --explain-routing

# 试运行（不实际搜索）
python3 scripts/search.py -q "查询" --dry-run

# 测试特定提供商
python3 scripts/search.py -p tavily -q "查询" --verbose
```

---

## 获取帮助

**还是搞不定？**

1. 查看完整文档 `README.md`
2. 运行设置向导：`python3 scripts/setup.py`
3. 查看 `FAQ.md` 了解常见问题
4. 提交 issue：https://github.com/robbyczgw-cla/web-search-plus/issues
