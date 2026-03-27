# 队列强制执行示例

**问题：** 在队列强制执行之前，智能体会跳过 HIGH 优先级任务并说 HEARTBEAT_OK。

**解决方案：** 队列检查器脚本使跳过队列任务变得**不可能**。

---

## 工作原理

### 步骤 1：运行队列检查器

每次心跳，在做任何其他事之前：

```bash
node skills/agent-autonomy-kit/check-queue.js
```

### 步骤 2：解读退出码

- **退出码 0**：队列已清空 → 安全继续其他工作
- **退出码 1**：存在 HIGH/Critical 任务 → **必须 spawn 智能体**

### 步骤 3：强制执行规则

如果退出码为 1，你**不能**：
- 说"HEARTBEAT_OK"
- 做自己的小项目
- 做发现或主动工作
- 检查邮件或社交媒体

你**必须**：
- 为最高优先级任务 spawn subagent
- 等待完成或交接给下一次心跳
- 任务完成后更新队列

---

## 真实示例：心跳流程

### 场景：智能体收到心跳

```
[15:30] 心跳收到
```

**步骤 1：运行队列检查器**

```bash
$ node skills/agent-autonomy-kit/check-queue.js

=== Queue Priority Check ===

🔴 HIGH priority tasks: 3
   • Fix authentication bug in production
   • Deploy security hotfix
   • Update API documentation

❌ CANNOT SKIP QUEUE
You must spawn an agent for HIGH/CRITICAL tasks before doing other work.

Top priority task:
Fix authentication bug in production

Exit code: 1
```

**步骤 2：智能体看到退出码 1**

智能体逻辑：
```
IF queue_checker_exit_code == 1:
    MUST spawn agent for top task
    CANNOT say HEARTBEAT_OK
```

**步骤 3：Spawn subagent**

```bash
openclaw spawn \
  --label "fix-auth-bug" \
  --message "HIGH PRIORITY: Fix authentication bug in production. See tasks/QUEUE.md for details. Update queue when complete."
```

**步骤 4：记录并退出**

```markdown
# memory/2026-02-04.md

15:30 - 心跳收到
15:30 - 队列检查器检测到 HIGH 优先级任务（共 3 个）
15:30 - Spawn 智能体：fix-auth-bug 处理最高优先级任务
15:31 - 等待任务完成后再进行下一次心跳循环
```

---

## 示例 2：队列清空

### 场景：无 HIGH 优先级任务

**步骤 1：运行队列检查器**

```bash
$ node skills/agent-autonomy-kit/check-queue.js

=== Queue Priority Check ===

🟢 LOW priority tasks: 2

✅ Safe to continue
No HIGH/CRITICAL tasks in queue. You can proceed with other work.

Exit code: 0
```

**步骤 2：智能体看到退出码 0**

智能体逻辑：
```
IF queue_checker_exit_code == 0:
    安全继续：
    - 5D 循环阶段
    - 主动发现
    - 文档改进
    - 调研任务
```

**步骤 3：智能体可以做其他工作**

智能体现在可以自由地：
- 检查审查关卡
- 运行 Scout 进行发现
- 更新文档
- 如果愿意，处理 LOW 优先级任务

---

## 示例 3：多个 HIGH 优先级任务

### 场景：队列中有 12 个 HIGH 优先级任务

**步骤 1：运行队列检查器**

```bash
$ node skills/agent-autonomy-kit/check-queue.js

=== Queue Priority Check ===

🔴 HIGH priority tasks: 12
   • DEV.to follow-up article
   • The Colony post
   • Moltbook announcements
   • Token Budget Tracking
   • Memory Kit v2
   • Team Kit improvements
   • Vercel Analytics integration
   • Blog content series
   • Premium features
   • Favicon design
   • Agent profile additions
   • Show HN post

❌ CANNOT SKIP QUEUE
You must spawn an agent for HIGH/CRITICAL tasks before doing other work.

Top priority task:
DEV.to follow-up article

Exit code: 1
```

**步骤 2：只为最高优先级任务 spawn**

不要试图一次做所有 12 个。只为**第一个** spawn：

```bash
openclaw spawn \
  --label "devto-article" \
  --message "HIGH PRIORITY: Write DEV.to follow-up article 'Why We Built 9 Agent Kits in 1 Day'. See tasks/QUEUE.md for details."
```

**步骤 3：下一次心跳处理下一个任务**

第一个任务完成后：
- 队列检查器再次运行
- 现在显示 11 个 HIGH 优先级任务
- 为新的最高优先级任务 spawn 智能体
- 重复直到所有 HIGH 任务被处理

**这防止了：**
- 用 12 个并行智能体压垮系统
- Token 预算耗尽
- 上下文切换混乱

**这确保了：**
- 重要工作的顺序处理
- 任务之间的正确交接
- 清晰的进度追踪

---

## 示例 4：CRITICAL 任务（放下一切）

### 场景：生产环境宕机

**QUEUE.md 中的任务：**
```markdown
## 🔥 High Priority

- [ ] [CRITICAL] 🔥 Production database connection failing - users locked out
```

**队列检查器输出：**

```bash
$ node skills/agent-autonomy-kit/check-queue.js

=== Queue Priority Check ===

🔥 CRITICAL tasks: 1
   • [CRITICAL] 🔥 Production database connection failing - users locked out

❌ CANNOT SKIP QUEUE
You must spawn an agent for HIGH/CRITICAL tasks before doing other work.

Top priority task:
[CRITICAL] 🔥 Production database connection failing - users locked out

Exit code: 1
```

**智能体响应：**

立即以最高优先级 spawn：

```bash
openclaw spawn \
  --label "critical-db-fix" \
  --model "claude-opus-4" \
  --thinking "high" \
  --message "🔥 CRITICAL: Production database connection failing. Users locked out. Investigate and fix immediately. Escalate to Ryan if needed."
```

通知人类：

```bash
openclaw message send \
  --target "ryan" \
  --message "🚨 CRITICAL task detected: Production DB failing. Spawned agent 'critical-db-fix' to investigate. Standing by for escalation if needed."
```

---

## 反模式（不要这样做）

### ❌ 错误：队列有 HIGH 任务时说 HEARTBEAT_OK

```
智能体："队列有 3 个 HIGH 优先级任务，但我先做发现吧。HEARTBEAT_OK。"
```

**为什么错误：** 跳过了明确需求去做推测性工作。

### ❌ 错误："解读"掉优先级

```
智能体："任务说 HIGH 但它已经在这里 2 天了，所以不可能那么紧急。HEARTBEAT_OK。"
```

**为什么错误：** 智能体自行判断违背了队列的目的。

### ❌ 错误：为所有 HIGH 任务 spawn 多个智能体

```
智能体："检测到 12 个 HIGH 任务。正在 spawn 12 个智能体..."
```

**为什么错误：** 压垮资源、消耗 token、制造混乱。

### ❌ 错误：忽略退出码

```
智能体："队列检查器返回退出码 1，但我真的很想做这个很酷的功能。HEARTBEAT_OK。"
```

**为什么错误：** 破坏了程序化强制执行。

---

## 正确模式（应该这样做）

### ✅ 正确：尊重退出码

```
智能体检查队列 → 退出码 1 → 为最高优先级任务 spawn → 更新队列 → 完成
```

### ✅ 正确：顺序处理

```
心跳 1：为任务 #1 spawn
心跳 2：检查完成 → 任务 #1 完成 → 为任务 #2 spawn
心跳 3：检查完成 → 任务 #2 完成 → 为任务 #3 spawn
...
```

### ✅ 正确：完成后更新队列

当 subagent 完成时，更新 `tasks/QUEUE.md`：
```markdown
## ✅ Done Today
- [x] DEV.to follow-up article（由 @echo 完成）
```

将任务从"Ready"移到"Done"，以便下一次心跳看到准确的状态。

### ✅ 正确：受阻时升级

如果 HIGH 任务被阻塞：
```markdown
## 🔵 Blocked
- [ ] Deploy to production (needs: Ryan's approval)
```

将其从"Ready"移到"Blocked"，使队列检查器不会持续为其 spawn。

---

## 集成检查清单

- [ ] 队列检查器脚本已安装：`skills/agent-autonomy-kit/check-queue.js`
- [ ] HEARTBEAT.md 更新了必须的队列检查
- [ ] 智能体理解退出码（0 = 清空，1 = 必须 spawn）
- [ ] 队列优先级已文档化（CRITICAL、HIGH、MEDIUM、LOW）
- [ ] 工作流已测试：HIGH 任务 → 队列检查器 → spawn 智能体 → 更新队列

---

## 成功指标

**队列强制执行之前：**
- 智能体跳过 HIGH 优先级任务
- 不检查队列就说"HEARTBEAT_OK"
- 人类需要提醒智能体处理紧急工作

**队列强制执行之后：**
- 退出码 1 = 不可能跳过 HIGH 任务
- 智能体自动为队列优先级 spawn 工作
- 队列被系统地消化
- 人类只在阻塞任务或战略决策时介入

---

**规则：** 如果 `check-queue.js` 返回退出码 1，你必须 spawn 智能体。没有例外。没有自行判断。没有"但我觉得其他事情更重要"。

**结果：** 自主智能体真正处理重要的事情，而不是有趣的事情。
