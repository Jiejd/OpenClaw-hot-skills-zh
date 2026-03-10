# 精英长期记忆系统 🧠

**终极 AI Agent 记忆系统。** 永不丢失上下文。

[![npm version](https://img.shields.io/npm/v/elite-longterm-memory.svg?style=flat-square)](https://www.npmjs.com/package/elite-longterm-memory)
[![npm downloads](https://img.shields.io/npm/dm/elite-longterm-memory.svg?style=flat-square)](https://www.npmjs.com/package/elite-longterm-memory)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)

---

## 兼容平台

<p align="center">
  <img src="https://img.shields.io/badge/Claude-AI-orange?style=for-the-badge&logo=anthropic" alt="Claude AI" />
  <img src="https://img.shields.io/badge/GPT-OpenAI-412991?style=for-the-badge&logo=openai" alt="GPT" />
  <img src="https://img.shields.io/badge/Cursor-IDE-000000?style=for-the-badge" alt="Cursor" />
  <img src="https://img.shields.io/badge/LangChain-Framework-1C3C3C?style=for-the-badge" alt="LangChain" />
</p>

<p align="center">
  <strong>专为构建：</strong> Clawdbot • Moltbot • Claude Code • 任何 AI Agent
</p>

---

将 7 种经过验证的记忆方法整合为一个坚不可摧的架构：

- ✅ **坚不可摧的 WAL 协议** — 预写日志在压缩中存活
- ✅ **LanceDB 向量搜索** — 相关记忆的语义召回
- ✅ **Git-Notes 知识图谱** — 结构化决策，支持分支感知
- ✅ **基于文件的归档** — 人类可读的 MEMORY.md + 每日日志
- ✅ **云备份** — 可选的 SuperMemory 同步
- ✅ **记忆维护** — 保持向量精简，防止 token 浪费
- ✅ **Mem0 自动提取** — 自动事实提取，减少 80% token

## 快速开始

```bash
# 在你的工作区初始化
npx elite-longterm-memory init

# 检查状态
npx elite-longterm-memory status

# 创建今日日志
npx elite-longterm-memory today
```

## 架构

```
┌─────────────────────────────────────────────────────┐
│              精英长期记忆系统                        │
├─────────────────────────────────────────────────────┤
│  热内存           温存储            冷存储          │
│  SESSION-STATE.md → LanceDB      → Git-Notes       │
│  (在压缩中         (语义           (永久           │
│   存活)            搜索)           决策)           │
│         │              │                │          │
│         └──────────────┼────────────────┘          │
│                        ▼                           │
│                   MEMORY.md                        │
│               (精选归档)                            │
└─────────────────────────────────────────────────────┘
```

## 5 层记忆架构

| 层级 | 文件/系统 | 用途 | 持久性 |
|-----|----------|------|-------|
| 1. 热内存 | SESSION-STATE.md | 活跃任务上下文 | 在压缩中存活 |
| 2. 温存储 | LanceDB | 语义搜索 | 自动召回 |
| 3. 冷存储 | Git-Notes | 结构化决策 | 永久 |
| 4. 归档 | MEMORY.md + daily/ | 人类可读 | 精选 |
| 5. 云端 | SuperMemory | 跨设备同步 | 可选 |

## WAL 协议

**关键洞察：** 在响应之前写入状态，而非之后。

```
用户：这个项目我们用 Tailwind

Agent（内部）：
1. 写入 SESSION-STATE.md → "决策：使用 Tailwind"
2. 然后响应 → "明白了 — 就用 Tailwind..."
```

如果你先响应，在保存之前崩溃，上下文就会丢失。WAL 确保持久性。

## 为什么记忆会失败（以及如何修复）

| 问题 | 原因 | 解决方案 |
|-----|------|---------|
| 忘记一切 | memory_search 未启用 | 启用 + 添加 OpenAI 密钥 |
| 重犯错误 | 教训未记录 | 写入 memory/lessons.md |
| 子 Agent 隔离 | 无上下文继承 | 在任务提示中传递上下文 |
| 事实未捕获 | 无自动提取 | 使用 Mem0（见下文）|

## Mem0 集成（推荐）

从对话中自动提取事实。减少 80% token。

```bash
npm install mem0ai
export MEM0_API_KEY="your-key"
```

```javascript
const { MemoryClient } = require('mem0ai');
const client = new MemoryClient({ apiKey: process.env.MEM0_API_KEY });

// 从消息中自动提取事实
await client.add(messages, { user_id: "user123" });

// 获取相关记忆  
const memories = await client.search(query, { user_id: "user123" });
```

## Clawdbot/Moltbot 用户

添加到 `~/.clawdbot/clawdbot.json`：

```json
{
  "memorySearch": {
    "enabled": true,
    "provider": "openai",
    "sources": ["memory"]
  }
}
```

## 创建的文件

```
workspace/
├── SESSION-STATE.md    # 热内存（活跃上下文）
├── MEMORY.md           # 精选长期记忆
└── memory/
    ├── 2026-01-30.md   # 每日日志
    └── ...
```

## 命令

```bash
elite-memory init      # 初始化记忆系统
elite-memory status    # 检查健康状态
elite-memory today     # 创建今日日志
elite-memory help      # 显示帮助
```

## 链接

- [完整文档 (SKILL.md)](./SKILL.md)
- [ClawdHub](https://clawdhub.com/skills/elite-longterm-memory)
- [GitHub](https://github.com/NextFrontierBuilds/elite-longterm-memory)

---

由 [@NextXFrontier](https://x.com/NextXFrontier) 构建
