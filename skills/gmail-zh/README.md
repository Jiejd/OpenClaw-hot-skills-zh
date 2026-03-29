# Gmail 智能助手

## 快速开始

### 环境配置
```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 基本使用示例
```python
# 列出邮件
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages?maxResults=10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
```

### 创建连接
```python
import urllib.request, os, json
data = json.dumps({'app': 'google-mail'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
```

### 获取连接
打开返回的 URL 在浏览器中完成 OAuth 授权。

### 发送邮件
```python
# POST /google-mail/gmail/v1/users/me/messages/send
# Content-Type: application/json
# {"raw": "BASE64_ENCODED_EMAIL"}
```

### 查找特定邮件
```python
# 带过滤器的邮件查询
GET /google-mail/gmail/v1/users/me/messages?q=is:unread&maxResults=10
```

### 获取邮件详情
```python
# 获取邮件内容和元数据
GET /google-mail/gmail/v1/users/me/messages/{messageId}

# 仅获取元数据
GET /google-mail/gmail/v1/users/me/messages/{messageId}?format=metadata&metadataHeaders=From&metadataHeaders=Subject&metadataHeaders=Date
```

## 多账户管理

如果拥有多个 Gmail 连接，可以使用 Maton-Connection 头指定使用哪个连接：

```python
req = urllib.request.Request('https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
```

## API 参考

### 主要端点
- **邮件列表**：`GET /google-mail/gmail/v1/users/me/messages?maxResults=10`
- **邮件详情**：`GET /google-mail/gmail/v1/users/me/messages/{messageId}`
- **发送邮件**：`POST /google-mail/gmail/v1/users/me/messages/send`
- **标签管理**：`GET /google-mail/gmail/v1/users/me/labels`
- **线程管理**：`GET /google-mail/gmail/v1/users/me/threads?maxResults=10`

### 修改邮件标签
```python
# 修改邮件标签操作
POST /google-mail/gmail/v1/users/me/messages/{messageId}/modify
```
