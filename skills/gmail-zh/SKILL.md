# Gmail 智能助手 - Gmail API智能集成

## 功能简介
通过官方 Gmail API 进行收发邮件，支持 OAuth 认证的高级邮件管理功能。

## 技能能力
- **邮件读取**：读取收件箱邮件、已发送邮件、草稿等
- **邮件发送**：发送新邮件，支持 HTML 格式和附件
- **线程管理**：查看和管理邮件对话线程
- **标签管理**：创建和管理邮件标签、文件夹
- **邮件搜索**：按发件人、主题、时间等条件搜索邮件
- **多账户支持**：同时管理多个 Gmail 账户

## 安装要求
- 需要配置 MATON_API_KEY 环境变量
- 完成与 Google 的 OAuth 授权流程
- 建议访问 ctrl.maton.ai 管理连接

## 使用方法
### 基本操作
- 列出邮件：支持最大结果数限制、过滤器（如未读邮件）
- 获取邮件详情：获取完整邮件内容或仅元数据
- 发送邮件：BASE64 编码的邮件内容
- 管理标签：创建、查看、删除邮件标签
- 线程操作：查看和管理邮件对话

### 高级功能
- 连接管理：在 ctrl.maton.ai 管理多个 Gmail 连接
- 指定连接：通过 Maton-Connection 头使用特定连接
- 网关代理：所有请求通过 Maton.ai 网关自动注入 OAuth 令牌

## API 端点
- 基础URL：https://gateway.maton.ai/google-mail/{native-api-path}
- 替换 {native-api-path} 为实际的 Gmail API 路径
- 认证：Authorization: Bearer $MATON_API_KEY
- 连接管理：https://ctrl.maton.ai/connections?app=google-mail&status=ACTIVE
