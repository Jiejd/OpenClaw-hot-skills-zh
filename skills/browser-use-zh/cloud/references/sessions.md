# 会话、配置文件与认证

## 目录
- [会话](#会话)
- [配置文件](#配置文件)
- [配置文件同步](#配置文件同步)
- [认证策略](#认证策略)
- [1Password 集成](#1password-集成)
- [社交媒体自动化](#社交媒体自动化)

---

## 会话

会话是有状态的浏览器环境。每个会话有一个浏览器，顺序运行代理。

### 自动创建的会话

大多数任务会自动创建会话：
```python
result = await client.run("Find top HN post")  # 会话自动创建
```

### 手动创建会话

用于多步工作流程或自定义配置：

```python
session = await client.sessions.create(
    profile_id="uuid",           # 持久配置文件
    proxy_country_code="us",     # 住宅代理
    start_url="https://example.com",
)

# 在同一会话中运行多个任务
await client.run("First task", session_id=session.id)
await client.run("Follow-up task", session_id=session.id)

# 获取实时 URL 用于监控
session_info = await client.sessions.get(session.id)
print(session_info.live_url)  # 实时观看代理

await client.sessions.stop(session.id)
```

### 实时视图与分享

每个会话都有一个 `liveUrl` 用于实时监控。可以创建公开分享链接：

```python
share = await client.sessions.create_share(session.id)
print(share.share_url)  # 任何有链接的人都可以查看
```

## 配置文件

配置文件在会话之间持久保存浏览器状态（Cookie、localStorage、密码）。

### CRUD 操作

```python
# 创建
profile = await client.profiles.create(name="my-profile")

# 列表
profiles = await client.profiles.list()

# 更新
await client.profiles.update(profile.id, name="new-name")

# 删除
await client.profiles.delete(profile.id)
```

### 使用模式

- **按用户**：每个终端用户一个配置文件，用于个性化会话
- **按网站**：每个网站一个配置文件（例如 "github-profile"、"gmail-profile"）
- **预热**：登录一次，在所有后续任务中复用

**重要提示：**
- 配置文件状态在会话结束时保存 — 始终调用 `sessions.stop()`
- 并发会话从启动时的快照读取 — 不会看到彼此的变更
- 刷新超过 7 天的配置文件

## 配置文件同步

将本地浏览器 Cookie 上传到云端配置文件：

```bash
export BROWSER_USE_API_KEY=your_key
curl -fsSL https://browser-use.com/profile.sh | sh
```

会打开一个浏览器让你登录网站。返回一个 `profile_id` 用于任务中。

## 认证策略

### 1. 配置文件同步（最简单）

本地登录，同步 Cookie 到云端：
```bash
curl -fsSL https://browser-use.com/profile.sh | sh
```

### 2. Secrets（按域名限定）

将凭据作为键值对传递，限定到域名：

```python
result = await client.run(
    task="Login and check dashboard",
    secrets={
        "username": "my-user",
        "password": "my-pass",
    },
    allowed_domains=["*.example.com"],
)
```

支持通配符和多域名用于 OAuth/SSO 流程。

### 3. 配置文件 + Secrets（组合）

使用配置文件获取 Cookie（跳过登录流程）+ Secrets 作为回退：

```python
session = await client.sessions.create(profile_id="uuid")
await client.run(
    task="Check dashboard",
    session_id=session.id,
    secrets={"password": "backup-pass"},
)
await client.sessions.stop(session.id)  # 保存配置文件状态
```

## 1Password 集成

从 1Password 保管库自动填充密码和 TOTP/2FA 验证码：

### 设置
1. 在 1Password 中创建专用保管库
2. 创建具有保管库访问权限的服务账户
3. 连接到 Browser Use Cloud（设置页面）
4. 在任务中使用 `op_vault_id` 参数

```python
result = await client.run(
    task="Login to GitHub",
    op_vault_id="vault-uuid",
    allowed_domains=["*.github.com"],
)
```

凭据永远不会出现在日志中 — 由 1Password 编程填充。

## 社交媒体自动化

反机器人检测需要一致的指纹 + IP + Cookie：

### 设置
1. 创建空白配置文件
2. 使用配置文件 + 代理打开会话 → 通过 `liveUrl` 手动登录
3. 停止会话（保存配置文件状态）

### 日常使用
- 始终使用同一配置文件 + 同一代理国家
- 刷新超过 7 天的配置文件

```python
session = await client.sessions.create(
    profile_id="social-profile-uuid",
    proxy_country_code="us",  # 始终使用同一国家
)
await client.run("Post update to Twitter", session_id=session.id)
await client.sessions.stop(session.id)
```
