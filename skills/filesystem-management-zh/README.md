# 📁 文件系统管理

面向 AI 智能体的高级文件系统操作工具。提供全面的文件和目录操作能力，包括智能过滤、搜索和批量处理功能。

[![版本](https://img.shields.io/badge/版本-1.0.2-blue)](https://clawdhub.com/unknown/clawdbot-filesystem)
[![许可证](https://img.shields.io/badge/许可证-MIT-green)](LICENSE)
[![Node.js](https://img.shields.io/badge/node-%3E%3D14.0.0-brightgreen)](https://nodejs.org/)

## 🚀 功能特性

### 📋 **智能文件列表**
- **高级过滤** — 按文件类型、模式、大小和日期过滤
- **递归遍历** — 深度目录扫描，支持深度控制
- **丰富格式** — 表格、树形和 JSON 输出格式
- **排序选项** — 按名称、大小、日期或类型排序

### 🔍 **强大搜索**
- **模式匹配** — 支持 Glob 模式和正则表达式
- **内容搜索** — 文件内全文搜索
- **多条件组合** — 同时按文件名和内容搜索
- **上下文显示** — 显示匹配行及其上下文

### 🔄 **批量操作**
- **安全复制** — 基于模式的文件复制，带验证机制
- **预览模式** — 执行前预览操作结果
- **进度追踪** — 实时操作进度显示
- **错误处理** — 优雅的故障恢复机制

### 🌳 **目录分析**
- **树形可视化** — ASCII 树形结构展示
- **统计信息** — 文件计数、大小分布、类型分析
- **空间分析** — 识别大文件和大目录
- **性能指标** — 操作计时和优化建议

## 📦 安装

### 通过 ClawdHub（推荐）

```bash
clawdhub install filesystem
```

### 手动安装

```bash
# 克隆技能仓库
git clone https://github.com/gtrusler/clawdbot-filesystem.git
cd clawdbot-filesystem

# 设置可执行权限
chmod +x filesystem

# 可选：全局安装
npm install -g .
```

## 🛠️ 使用方法

### 基础命令

```bash
# 列出当前目录文件
filesystem list

# 带详细信息和过滤的列表
filesystem list --path ./src --recursive --filter "*.js" --details

# 搜索文件内容
filesystem search --pattern "TODO" --path ./src --content

# 安全复制文件
filesystem copy --pattern "*.log" --to ./backup/ --dry-run

# 显示目录树
filesystem tree --path ./ --depth 3

# 分析目录
filesystem analyze --path ./logs --stats --largest 10
```

### 高级示例

#### 开发工作流
```bash
# 查找项目中所有 JavaScript 文件
filesystem list --path ./src --recursive --filter "*.js" --sort size

# 搜索 TODO 注释（含上下文）
filesystem search --pattern "TODO|FIXME|HACK" --content --context 3

# 复制所有配置文件
filesystem copy --pattern "*.config.*" --to ./backup/configs/ --preserve

# 分析项目结构
filesystem tree --depth 2 --size
```

#### 系统管理
```bash
# 查找大日志文件
filesystem analyze --path /var/log --sizes --largest 15

# 搜索日志中的错误模式
filesystem search --pattern "ERROR|FATAL" --path /var/log --content --include "*.log"

# 列出最近修改的文件
filesystem list --path /tmp --sort date --details

# 删除前分析
filesystem list --path /tmp --filter "*.tmp" --details
```

## ⚙️ 配置说明

技能使用 `config.json` 文件管理默认设置：

```json
{
  "defaultPath": "./",
  "maxDepth": 10,
  "excludePatterns": ["node_modules", ".git", ".DS_Store"],
  "outputFormat": "table",
  "colorOutput": true,
  "performance": {
    "maxFileSize": 52428800,
    "maxFiles": 10000
  },
  "safety": {
    "requireConfirmation": true,
    "preventSystemPaths": true
  }
}
```

## 📖 命令参考

### `filesystem list`
带高级过滤的文件和目录列表。

| 参数 | 说明 | 默认值 |
|--------|-------------|---------|
| `--path, -p` | 目标目录 | 当前目录 |
| `--recursive, -r` | 包含子目录 | false |
| `--filter, -f` | 按模式过滤 | `*` |
| `--details, -d` | 显示文件详情 | false |
| `--sort, -s` | 排序字段 | name |
| `--format` | 输出格式 | table |

### `filesystem search`
按文件名模式或内容搜索文件。

| 参数 | 说明 | 默认值 |
|--------|-------------|---------|
| `--pattern` | 搜索模式 | 必填 |
| `--path, -p` | 搜索目录 | 当前目录 |
| `--content, -c` | 搜索文件内容 | false |
| `--context` | 上下文行数 | 2 |
| `--include` | 包含的文件模式 | 全部文件 |
| `--exclude` | 排除的文件模式 | 无 |

### `filesystem copy`
带模式匹配的批量文件复制。

| 参数 | 说明 | 默认值 |
|--------|-------------|---------|
| `--pattern` | 源文件模式 | `*` |
| `--to` | 目标目录 | 必填 |
| `--dry-run` | 仅预览 | false |
| `--overwrite` | 允许覆盖 | false |
| `--preserve` | 保留时间戳 | false |

### `filesystem tree`
以树形结构显示目录。

| 参数 | 说明 | 默认值 |
|--------|-------------|---------|
| `--path, -p` | 根目录 | 当前目录 |
| `--depth, -d` | 最大深度 | 3 |
| `--dirs-only` | 仅显示目录 | false |
| `--size` | 显示文件大小 | false |
| `--no-color` | 禁用颜色 | false |

### `filesystem analyze`
分析目录结构和统计信息。

| 参数 | 说明 | 默认值 |
|--------|-------------|---------|
| `--path, -p` | 目标目录 | 当前目录 |
| `--stats` | 显示统计信息 | true |
| `--types` | 分析文件类型 | false |
| `--sizes` | 大小分布 | false |
| `--largest` | 显示最大的 N 个文件 | 10 |

## 🛡️ 安全特性

- **路径验证** — 防止目录遍历攻击
- **权限检查** — 操作前验证访问权限
- **预览模式** — 预览破坏性操作
- **受保护路径** — 阻止系统目录访问
- **大小限制** — 防止处理超大文件
- **超时保护** — 防止无限操作

## 🔧 集成

### 与其他技能协作

```bash
# 与安全技能配合使用
security validate-command "filesystem list --path /etc"

# 管道输出到分析工具
filesystem list --format json | jq '.[] | select(.size > 1000000)'

# 与 Git 工作流集成
filesystem list --filter "*.js" --format json | git-analyze-changes
```

### 自动化示例

```bash
# 每日日志分析
filesystem analyze --path /var/log --stats --largest 5

# 代码质量检查
filesystem search --pattern "TODO|FIXME" --content --path ./src

# 备份准备
filesystem copy --pattern "*.config*" --to ./backup/$(date +%Y%m%d)/
```

## 🧪 测试

测试安装是否成功：

```bash
# 基础功能
filesystem help
filesystem list --path . --details

# 搜索能力
echo "TODO: 测试此函数" > test.txt
filesystem search --pattern "TODO" --content

# 树形可视化
filesystem tree --depth 2 --size

# 分析功能
filesystem analyze --stats --types
```

## 🐛 常见问题

### 权限被拒绝
```bash
# 检查文件权限
ls -la filesystem
chmod +x filesystem
```

### 大目录性能问题
```bash
# 使用过滤缩小范围
filesystem list --filter "*.log" --exclude "node_modules/*"

# 限制树形操作深度
filesystem tree --depth 2
```

### 大文件内存问题
```bash
# 超过 50MB 的文件默认跳过
# 检查当前限制
node -e "console.log(require('./config.json').performance)"
```

## 📈 性能提示

- 使用 `--filter` 缩小文件范围
- 为树形操作设置合适的 `--depth` 限制
- 为常见构建目录启用排除模式
- 批量操作前先使用 `--dry-run`
- 大目录使用 `--stats` 监控输出

## 🤝 贡献

1. **报告问题** — 提交 Bug 和功能请求
2. **添加模式** — 贡献常用文件模式
3. **性能优化** — 提交优化改进
4. **文档完善** — 帮助改进示例和指南

## 📄 许可证

MIT 许可证 — 个人和商业使用均免费。

详见 [LICENSE](LICENSE) 文件。

## 🔗 链接

- **ClawdHub** — [clawdhub.com/unknown/clawdbot-filesystem](https://clawdhub.com/unknown/clawdbot-filesystem)
- **问题反馈** — [GitHub Issues](https://github.com/gtrusler/clawdbot-filesystem/issues)
- **文档** — [Clawdbot 文档](https://docs.clawd.bot)

---

**为 Clawdbot 社区用心构建** ❤️
