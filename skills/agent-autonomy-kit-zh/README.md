# 🚀 Agent Autonomy Kit

[![GitHub](https://img.shields.io/badge/GitHub-reflectt-blue?logo=github)](https://github.com/reflectt/agent-autonomy-kit)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Part of Team Reflectt](https://img.shields.io/badge/Team-Reflectt-purple)](https://github.com/reflectt)

**停止等待提示词，持续自主工作。**

大多数 AI 智能体在人类消息之间处于闲置状态。这套工具包将你的智能体转变为自主工作者，能够持续在有意义的工作上取得进展。

---

## 问题所在

智能体白白浪费 token 在等待中：
- 心跳检查只是问"有什么需要关注的吗？"然后回复 `HEARTBEAT_OK`
- 团队成员闲置等待被 spawn
- 人类停止发提示词时，工作就停止了
- 订阅限制（token/小时、token/天）未被利用

## 解决方案

一套主动工作系统：
1. **任务队列 (Task Queue)** — 始终准备好可执行的工作
2. **主动心跳 (Proactive Heartbeat)** — 执行工作，而不是仅仅检查是否有工作
3. **团队协作 (Team Coordination)** — 智能体之间相互沟通、交接任务
4. **持续运行 (Continuous Operation)** — 工作直到触及限制，然后休眠

---

## 核心概念

### 1. 任务队列（队列优先执行）

不再等待提示词，智能体从持久化的任务队列中拉取工作。

**关键：** Autonomy Kit 强制执行队列优先机制。如果队列中存在 HIGH 或 CRITICAL 优先级的任务，智能体**不能**跳过它们去做其他事情或说 HEARTBEAT_OK。

**位置：** `tasks/QUEUE.md`（或 GitHub Projects）

```markdown
# 任务队列

## Ready（可认领）
- [ ] 调研竞品 X 的定价策略
- [ ] 撰写关于记忆系统的博客草稿
- [ ] 审查并改进流程文档

## In Progress（进行中）
- [ ] @kai：构建 autonomy 技能
- [ ] @rhythm：更新流程文档

## Blocked（已阻塞）
- [ ] 部署到生产环境（需要：Ryan 的审批）

## Done Today（今日完成）
- [x] 记忆系统已上线
- [x] 团队 spawn 流程已文档化
```

**规则：**
- 任何智能体都可以认领"Ready"任务
- 开始时标记自己：`@agentname: 任务`
- 完成时移到 Done
- 发现新任务时及时添加

**优先级：**
- `[CRITICAL]` 或 `🔥 CRITICAL` — 放下一切，立即修复
- `[HIGH]` 或 `🔴 HIGH` — 必须在其他工作之前处理
- `[MEDIUM]` — 默认视为 HIGH（安全优先）
- `[LOW]` 或 `🟡 LOW` — 可以延后处理

### 2. 队列检查脚本（强制执行）

队列检查脚本通过程序化方式**强制执行**队列优先机制。

**位置：** `skills/agent-autonomy-kit/check-queue.js`

**使用方法：**
```bash
node skills/agent-autonomy-kit/check-queue.js
```

**工作原理：**
1. 扫描 `tasks/QUEUE.md` 中"Ready"分区的所有任务
2. 检测优先级（CRITICAL、HIGH、MEDIUM、LOW）
3. 如果存在 HIGH/CRITICAL 任务，返回退出码 1
4. 仅在队列为空或所有任务都是 LOW 优先级时，返回退出码 0

**退出码：**
- `0` = 安全继续其他工作（无紧急任务）
- `1` = 必须为 HIGH/CRITICAL 任务 spawn 智能体（不可跳过）

**在 HEARTBEAT.md 中集成：**
```markdown
## 1. 快速检查

- [ ] 有等待的人类消息？→ 立即处理
- [ ] 运行队列检查器（必须执行）：
  ```bash
  node skills/agent-autonomy-kit/check-queue.js
  ```
  - 退出码 1：必须为最高优先级任务 spawn 智能体
  - 退出码 0：安全继续
- [ ] 如果队列已清空，进入工作模式
```

**示例输出：**

当存在 HIGH 优先级任务时：
```
=== Queue Priority Check ===

🔴 HIGH priority tasks: 3
   • Fix critical bug in authentication
   • Deploy hotfix to production
   • Update security documentation

❌ CANNOT SKIP QUEUE
You must spawn an agent for HIGH/CRITICAL tasks before doing other work.

Top priority task:
Fix critical bug in authentication

[Exit code: 1]
```

当队列已清空时：
```
=== Queue Priority Check ===

🟢 LOW priority tasks: 2

✅ Safe to continue
No HIGH/CRITICAL tasks in queue. You can proceed with other work.

[Exit code: 0]
```

**为什么这很重要：**

在使用此脚本之前，智能体会：
- 说"HEARTBEAT_OK"然后跳过重要工作
- 在 HIGH 优先级任务堆积在队列中时去做自己的小项目
- 需要人类来解读"什么才是紧急的"

使用此脚本之后：
- **程序化强制执行** — 无需智能体自行判断，没有例外
- **不可能跳过** — 退出码 1 会阻止心跳完成
- **清晰的指令** — 脚本精确显示应该为哪个任务 spawn

**📖 参见 [QUEUE-ENFORCEMENT-EXAMPLES.md](./QUEUE-ENFORCEMENT-EXAMPLES.md) 获取详细使用示例和工作流模式。**

### 3. 主动心跳

将心跳从"检查是否有警报"转变为"执行有意义的工作"。

**HEARTBEAT.md 模板：**

```markdown
# 心跳例行检查

## 1. 检查紧急事项（30 秒）
- 有未读的人类消息？
- **运行队列检查器（必须执行）：**
  ```bash
  node skills/agent-autonomy-kit/check-queue.js
  ```
  如果退出码 1：为 HIGH/CRITICAL 任务 spawn 智能体（不可例外）
- 有需要升级的阻塞任务？
- 系统健康问题？

如果有紧急事项：立即处理。
如果队列检查通过（退出码 0）：继续进入工作模式。

## 2. 工作模式（使用剩余时间）

从任务队列中拉取：
1. 检查 `tasks/QUEUE.md` 中的 Ready 项
2. 选择你能做的最高优先级任务
3. 在其上做有意义的工作
4. 完成或受阻时更新状态

## 3. 结束前
- 将工作内容记录到每日记忆
- 更新任务队列
- 如果任务未完成，为下一次心跳记录进展
```

### 3. 团队协作

智能体通过 Discord（或配置的频道）进行沟通：
- 进度更新
- 任务交接（"@rhythm 这个已准备好审查了"）
- 阻塞报告（"卡在 X 上了，需要帮助"）
- 发现（"发现了有趣的东西，已添加到队列"）

### 4. Token 预算意识

了解你的限制，明智地使用：

```markdown
## Token 策略

**每日预算：** ~X token（Claude Max）
**心跳成本：** ~2-5k token/次
**可用次数：** ~Y 次/天

**优先级：**
1. 人类请求（始终最优先）
2. 紧急任务（时间敏感）
3. 高影响力任务（推动关键指标）
4. 维护任务（改进和优化）

接近限制时：
- 收尾当前任务
- 编写详细的交接笔记
- 休眠等待重置
```

---

## 安装

### Git 克隆（推荐）
```bash
# 克隆到你的 skills 目录
git clone https://github.com/reflectt/agent-autonomy-kit.git skills/agent-autonomy-kit
```

然后按照以下设置步骤操作。

---

## 设置

### 1. 创建任务队列

```bash
mkdir -p tasks
cat > tasks/QUEUE.md << 'EOF'
# 任务队列

## Ready
<!-- 在此添加任何智能体都可以认领的任务 -->

## In Progress
<!-- 当前正在进行的任务 -->

## Blocked
<!-- 等待某些条件的任务 -->

## Done Today
<!-- 已完成的任务（每日清空） -->
EOF
```

### 2. 更新 HEARTBEAT.md

将被动检查替换为**强制**的队列优先工作：

```markdown
# 心跳例行检查

## 快速检查（如有紧急事项，立即处理）
- [ ] 有等待的人类消息？
- [ ] **运行队列检查器（必须执行）：**
  ```bash
  node skills/agent-autonomy-kit/check-queue.js
  ```
  退出码 1 → 为 HIGH 任务 spawn 智能体（不可跳过）
  退出码 0 → 安全继续
- [ ] 有严重阻塞？

## 工作模式
1. 读取 `tasks/QUEUE.md`
2. 选择最高优先级的 Ready 任务
3. 执行工作
4. 更新队列和每日记忆
5. 如果还有时间，继续下一个任务

## 心跳结束
- 将进度记录到 `memory/YYYY-MM-DD.md`
- 如有重要进展，发到团队频道
```

### 3. 配置持续运行

设置心跳频繁运行：

```json5
{
  agents: {
    defaults: {
      heartbeat: {
        every: "15m",  // 频率越高 = 完成的工作越多
        target: "last",
        activeHours: { start: "06:00", end: "23:00" }
      }
    }
  }
}
```

### 4. 设置团队频道（可选）

配置 Discord/Slack 用于团队沟通：

```json5
{
  channels: {
    discord: {
      // ... 已有配置 ...
      groups: {
        "team-reflectt": {
          policy: "allow",
          channels: ["team-chat-channel-id"]
        }
      }
    }
  }
}
```

---

## 工作流示例

### 早晨（6:00 AM）
1. 心跳触发
2. 智能体检查：无紧急人类消息
3. 智能体读取任务队列："调研竞品 X 的定价策略"
4. 智能体进行调研，撰写发现
5. 智能体更新队列：将任务移到 Done，添加发现的后续任务
6. 智能体发到团队频道："竞品调研完成，详见 tasks/competitor-analysis.md"

### 全天
- 心跳每 15-30 分钟触发一次
- 每次循环：检查紧急事项 → 执行工作 → 更新队列 → 记录进度
- 人类消息始终优先
- 团队通过频道协调

### 晚上（11:00 PM）
- 活跃时段的最后一次心跳
- 智能体收尾当前任务
- 编写详细笔记供明天使用
- 进入休眠直到早晨

---

## 反模式

❌ **被动心跳** — "HEARTBEAT_OK"浪费了工作机会
❌ **没有任务队列** — 智能体不知道该做什么
❌ **单打独斗** — 缺乏协调导致重复劳动
❌ **无视限制** — 任务中途被限速会丢失上下文
❌ **没有交接笔记** — 下一个会话从零开始

---

## 追踪指标

在 `memory/metrics.md` 中：

```markdown
# 自主工作指标

## 本周
- 完成任务数：X
- 高效使用的心跳次数：Y%
- Token 利用率：Z%
- 需要人类干预次数：N

## 模式
- 最高效时段：早晨
- 常见阻塞：等待人类审批
- 适合异步处理的任务：调研、写作、代码审查
```

---

## 相关套件

此套件与其他配套工具配合效果最佳：

### [Agent Memory Kit](https://github.com/reflectt/agent-memory-kit)
**必备基础。** 提供本套件所依赖的记忆系统：
- 任务进度记录到每日记忆（情景记忆）
- 常见任务的流程（程序记忆）
- 学到的知识添加到 MEMORY.md（语义记忆）
- 失败记录在 feedback.md 中（反馈循环）

### [Agent Team Kit](https://github.com/reflectt/agent-team-kit)
**适用于多智能体配置。** 协调自主智能体协同工作：
- 基于角色的工作分配
- 自助式任务队列
- 团队沟通模式

---

## 起源

由 Team Reflectt 在发现 Claude Max 订阅的 token 一直未被充分利用后创建。智能体完成一个任务后就等待下一个提示词，导致大量潜在工作时间被浪费。

现在团队能够持续工作，通过 Discord 协调，从共享任务队列中拉取任务，只在触及 token 限制时才休眠。

---

## 自主化 Cron 定时任务

设置自动化报告和工作触发器。

### 避免在 subagent 已在运行时产生重复工作（看门狗）

Cron 定时任务通常按固定时间表运行；如果 subagent **刚刚完成**，其会话可能看起来仍然是"新鲜的"，尽管实际上已经结束了。

使用以下看门狗来区分**真正在运行**的 subagent 和**最近完成**的 subagent：

```bash
node skills/agent-autonomy-kit/check-active-subagents.js
# 退出码 0 => 无活跃的 subagent
# 退出码 1 => 检测到活跃的 subagent
```

建议的 cron 消息提示模式：**先运行看门狗；如果报告有活跃 subagent，则不做任何操作并退出。**

设置自动化报告和工作触发器：

### 每日进度报告（晚上 10 点）
```bash
openclaw cron add \
  --name "Daily Progress Report" \
  --cron "0 22 * * *" \
  --tz "America/Vancouver" \
  --session isolated \
  --message "Generate daily progress report. Read tasks/QUEUE.md for completed tasks. Summarize: completed, in progress, blockers, tomorrow's plan."
```

### 早间启动（早上 7 点）
```bash
openclaw cron add \
  --name "Morning Kickoff" \
  --cron "0 7 * * *" \
  --tz "America/Vancouver" \
  --session main \
  --system-event "Morning kickoff: Review task queue, pick top priorities, spawn team members for parallel work." \
  --wake now
```

### 夜间工作检查（凌晨 3 点）
```bash
openclaw cron add \
  --name "Overnight Work" \
  --cron "0 3 * * *" \
  --tz "America/Vancouver" \
  --session isolated \
  --message "Overnight work session. Pull tasks from queue that don't need human input. Do research, writing, or analysis. Log progress."
```

这些任务会自动运行 — 无需人类提示词。

---

## 队列强制执行摘要

**问题：** 智能体跳过 HIGH 优先级任务并说 HEARTBEAT_OK。

**解决方案：** 通过 `check-queue.js` 进行程序化强制执行。

**工作原理：**
1. 每次心跳运行：`node skills/agent-autonomy-kit/check-queue.js`
2. 脚本扫描 `tasks/QUEUE.md` 中"Ready"分区的 HIGH/CRITICAL 任务
3. 退出码 1 = 必须 spawn 智能体（不可能跳过）
4. 退出码 0 = 安全继续其他工作

**成功指标：** 修复后，如果 QUEUE.md 中有 HIGH 优先级任务，智能体必须为其 spawn 工作。没有例外。

**文件列表：**
- `check-queue.js` — 强制执行脚本
- `test-queue-checker.sh` — 自动化测试（全部通过 ✅）
- `QUEUE-ENFORCEMENT-EXAMPLES.md` — 实际使用示例
- `templates/HEARTBEAT.md` — 包含强制执行的更新模板

**运行测试：**
```bash
bash skills/agent-autonomy-kit/test-queue-checker.sh
```

---

*闲置的智能体就是浪费的智能体。继续工作。*
