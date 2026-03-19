# 百度 API 密钥配置指南（OpenClaw）

## BAIDU_API_KEY 未配置

当 `BAIDU_API_KEY` 环境变量未设置时，请按以下步骤操作：

### 1. 获取 API 密钥
访问：**https://console.bce.baidu.com/ai-search/qianfan/ais/console/apiKey**

- 登录百度智能云账号
- 创建应用或查看已有的 API 密钥
- 复制您的 **API Key**（只需 API Key）

### 2. 配置 OpenClaw
编辑 OpenClaw 配置文件：`~/.openclaw/openclaw.json`

添加或合并以下配置：

```json
{
  "skills": {
    "entries": {
      "baidu-search-zh": {
        "env": {
          "BAIDU_API_KEY": "您的实际API密钥"
        }
      }
    }
  }
}
```

将 `"您的实际API密钥"` 替换为您的真实 API 密钥。

### 3. 验证配置
```bash
# 检查 JSON 格式
cat ~/.openclaw/openclaw.json | python3 -m json.tool
```

### 4. 重启 OpenClaw
```bash
openclaw gateway restart
```

### 5. 测试
```bash
cd ~/.openclaw/workspace/skills/baidu-search-zh
python3 scripts/search.py '{"query": "测试搜索"}'
```

## 故障排除
- 确保 `~/.openclaw/openclaw.json` 存在且 JSON 格式正确
- 确认 API 密钥有效且百度 AI 搜索服务已开通
- 检查百度智能云账户余额
- 修改配置后需重启 OpenClaw

**建议**：使用 OpenClaw 配置文件进行集中管理
