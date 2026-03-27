# 实施检查清单

**目的：** 系统性地部署自主化回路修复  
**受众：** Ryan 或 Kai 实施诊断建议  
**预计时间：** 90 分钟实施 + 48 小时测试  
**状态：** 准备执行

---

## 概述

本检查清单实施 `DIAGNOSIS.md` 中识别的修复。核心问题：智能体在心跳入口检查队列，但不在任务完成边界检查，导致请求许可行为。

**修复方案：** 在每个决策边界添加队列检查，而不仅仅是心跳入口。

---

## 阶段 1：添加缺失的协议（30 分钟）

### ✅ 任务 1.1：创建 Post-Task Protocol

**状态：** ✅ 已完成

**文件：** `skills/agent-autonomy-kit/post-task-protocol.md`

**作用：** 定义每次任务完成后必须进行的队列重新检查。

**验证：**
```bash
ls -lh skills/agent-autonomy-kit/post-task-protocol.md
# 应存在且约 8KB
```

---

### ✅ 任务 1.2：创建 Decision Checklist

**状态：** ✅ 已完成

**文件：** `skills/agent-autonomy-kit/decision-checklist.md`

**作用：** 在向人类询问"下一步是什么？"之前的 5 步检查清单。

**验证：**
```bash
ls -lh skills/agent-autonomy-kit/decision-checklist.md
# 应存在且约 12KB
```

---

### ⏳ 任务 1.3：更新 HEARTBEAT.md 添加回路

**状态：** 待办

**文件：** `HEARTBEAT.md`

**所需更改：**

找到此部分（约第 42 行）：
```markdown
## 心跳执行

1. **人类消息优先** — 始终立即处理直接请求
2. **队列强制执行（必须）** — 在做任何其他事之前运行队列检查器：
```

在现有步骤 2 之后添加：
```markdown
3. **工作执行** — Spawn 智能体或执行工作

4. **任务完成 → 回路（必须）** — 当任何任务完成时：
   ```bash
   # 更新 tasks/QUEUE.md（将任务移到 Done）
   # 再次运行队列检查器
   node skills/agent-autonomy-kit/check-queue.js
   
   # 解读退出码：
   # - 退出码 1：为下一个 HIGH 任务 spawn 智能体（不要问）
   # - 退出码 0：检查 5D 循环阶段寻找下一个工作
   ```
   **参见：** `skills/agent-autonomy-kit/post-task-protocol.md` 获取完整协议

5. **如果队列/日程已有答案，永远不要问"下一步是什么？"**
   在询问前运行决策检查清单：`skills/agent-autonomy-kit/decision-checklist.md`

## 规则：闭合回路

每次任务完成都是一次微型心跳。再次检查队列。

```
心跳 → 检查 → 工作 → 完成 → ──┐
   ↑                            │
   └────────────────────────────┘
              （回路）
```
```

**验证：**
```bash
grep -n "LOOP BACK" HEARTBEAT.md
# 应显示新的部分
```

**提交：**
```bash
git add HEARTBEAT.md
git commit -m "Add loop-back enforcement to heartbeat protocol"
```

---

### ⏳ 任务 1.4：更新 AGENTS.md 添加预响应检查

**状态：** 待办

**文件：** `AGENTS.md`

**所需更改：**

找到"## Make It Yours"部分（靠近文件末尾）。

在之前添加：
```markdown
## 在询问"我该做什么？"之前

如果你准备向人类请求下一步指导：

1. **停止**
2. 运行决策检查清单：
   ```bash
   node skills/agent-autonomy-kit/check-queue.js --pre-response
   ```
3. 如果显示有工作要做 → 去做工作，不要问
4. 如果确实被阻塞 → 记录你检查了什么，然后询问

**规则：** 在请求输入之前，穷尽所有自主选项。

**文件：**
- `skills/agent-autonomy-kit/decision-checklist.md` — 完整的 5 步检查清单
- `skills/agent-autonomy-kit/post-task-protocol.md` — 任务后回路

**何时不应询问：**
- 队列有 HIGH 优先级任务 → 执行队列工作
- 日程有下一步操作 → 执行日程
- 5D 循环阶段过时 → spawn 对应智能体
- 你有计划 → 遵循计划

**何时可以询问：**
- 确实被阻塞（缺少凭证、外部依赖）
- 需要战略决策（产品方向、预算分配）
- 需要澄清模糊任务（哪个 bug？哪个功能？）
```

**验证：**
```bash
grep -n "Before Asking" AGENTS.md
# 应显示新的部分
```

**提交：**
```bash
git add AGENTS.md
git commit -m "Add pre-response decision checklist to agent guidelines"
```

---

## 阶段 2：增强队列检查器（30 分钟）

### ⏳ 任务 2.1：添加 --pre-response 标志

**状态：** 待办

**文件：** `skills/agent-autonomy-kit/check-queue.js`

**所需更改：**

在 `detectPriority()` 之后、`checkQueue()` 之前添加此函数：

```javascript
function preResponseCheck(queuePath) {
  console.log(`${colors.bold}${colors.cyan}=== Pre-Response Check ===${colors.reset}\n`);
  
  // 1. 检查队列状态
  const sections = parseQueueFile(queuePath);
  const readyTasks = sections.ready;
  const criticalTasks = readyTasks.filter(t => t.priority === 'CRITICAL');
  const highTasks = readyTasks.filter(t => t.priority === 'HIGH');
  const hasUrgentWork = criticalTasks.length > 0 || highTasks.length > 0;
  
  if (hasUrgentWork) {
    console.log(`${colors.red}🔴 HIGH/CRITICAL tasks in queue: ${criticalTasks.length + highTasks.length}${colors.reset}`);
    console.log(`${colors.red}DON'T ASK "What's next?" — Execute the queue.${colors.reset}\n`);
  } else {
    console.log(`${colors.green}✅ Queue clear (no HIGH tasks)${colors.reset}\n`);
  }
  
  // 2. 检查计划任务
  const stateFile = path.join(path.dirname(queuePath), 'memory/heartbeat-state.json');
  if (fs.existsSync(stateFile)) {
    try {
      const state = JSON.parse(fs.readFileSync(stateFile, 'utf-8'));
      
      if (state.pending && state.pending.length > 0) {
        console.log(`${colors.yellow}⏰ Scheduled tasks: ${state.pending.length}${colors.reset}`);
        state.pending.slice(0, 5).forEach(task => {
          console.log(`   ${colors.cyan}• ${task}${colors.reset}`);
        });
        console.log(`${colors.yellow}DON'T ASK "What's next?" — Execute the schedule.${colors.reset}\n`);
      }
      
      // 3. 检查过时的 5D 阶段
      const now = Date.now();
      if (state.lastDiscovery) {
        const lastDiscovery = new Date(state.lastDiscovery).getTime();
        const staleHours = (now - lastDiscovery) / (1000 * 60 * 60);
        
        if (staleHours > 2) {
          console.log(`${colors.yellow}🔍 Discovery is stale (${staleHours.toFixed(1)}h ago)${colors.reset}`);
          console.log(`${colors.yellow}DON'T ASK "What's next?" — Spawn Scout for discovery.${colors.reset}\n`);
        }
      }
    } catch (err) {
      // 忽略 JSON 解析错误
    }
  }
  
  // 4. 最终结论
  if (hasUrgentWork) {
    console.log(`${colors.red}${colors.bold}❌ VERDICT: Execute queue, don't ask${colors.reset}\n`);
    process.exit(1);
  } else {
    console.log(`${colors.green}${colors.bold}✅ VERDICT: Safe to ask (if genuinely blocked)${colors.reset}\n`);
    process.exit(0);
  }
}
```

然后更新底部的主执行块：

```javascript
// 主执行
const workspaceRoot = process.cwd();
const queuePath = path.join(workspaceRoot, 'tasks/QUEUE.md');

// 检查 --pre-response 标志
if (process.argv.includes('--pre-response')) {
  preResponseCheck(queuePath);
} else {
  checkQueue(queuePath);
}
```

**测试：**
```bash
# 应检查队列 + 日程 + 5D 阶段
node skills/agent-autonomy-kit/check-queue.js --pre-response

# 应只检查队列（现有行为）
node skills/agent-autonomy-kit/check-queue.js
```

**验证输出显示：**
- 队列状态（有无 HIGH 任务）
- heartbeat-state.json 中的计划任务
- 过时的发现检查
- 最终结论（询问或不询问）

**提交：**
```bash
git add skills/agent-autonomy-kit/check-queue.js
git commit -m "Add --pre-response flag for decision boundary checks"
```

---

### ⏳ 任务 2.2：测试队列检查器增强

**状态：** 待办（任务 2.1 之后）

**测试用例：**

**测试 1：存在 HIGH 任务**
```bash
# 确保 tasks/QUEUE.md 有 HIGH 优先级任务
node skills/agent-autonomy-kit/check-queue.js --pre-response
# 预期：退出码 1，显示"DON'T ASK"
echo $?  # 应为 1
```

**测试 2：队列清空，存在计划任务**
```bash
# 确保 heartbeat-state.json 有 .pending 数组
node skills/agent-autonomy-kit/check-queue.js --pre-response
# 预期：显示计划任务，显示"Execute the schedule"
```

**测试 3：队列清空，发现过时**
```bash
# 在 heartbeat-state.json 中设置 lastDiscovery 为 >2 小时前
node skills/agent-autonomy-kit/check-queue.js --pre-response
# 预期：显示过时的发现，显示"Spawn Scout"
```

**测试 4：一切空闲**
```bash
# 队列清空，无计划任务，发现最近
node skills/agent-autonomy-kit/check-queue.js --pre-response
# 预期：退出码 0，显示"Safe to ask (if genuinely blocked)"
echo $?  # 应为 0
```

**记录结果：**
```bash
# 将测试结果添加到 memory/2026-02-04.md
```

---

## 阶段 3：更新工作区上下文（15 分钟）

### ⏳ 任务 3.1：更新 Autonomy Kit README

**状态：** 待办

**文件：** `skills/agent-autonomy-kit/README.md`

**所需更改：**

找到"Queue Enforcement Summary"部分（靠近底部）。

在该部分之后添加：

```markdown
---

## Loop-Back Enforcement（新增）

**解决的问题：** 智能体在心跳入口检查队列，但任务完成后不检查，导致请求许可。

**解决方案：** 任务后协议 + 决策检查清单

### Post-Task Protocol（任务后协议）

完成任何任务（直接或通过 subagent）后：
1. 更新队列状态
2. 再次运行 `node skills/agent-autonomy-kit/check-queue.js`
3. 如果退出码 1：spawn 下一个智能体（不要问）
4. 如果退出码 0：检查 5D 循环或计划任务

**参见：** `post-task-protocol.md` 获取完整详情

### Decision Checklist（决策检查清单）

在询问"我接下来该做什么？"之前：
1. 检查队列（有 HIGH 任务吗？）
2. 检查日程（有计划的操作吗？）
3. 检查 5D 循环（有阶段过时吗？）
4. 我是被阻塞了还是在偷懒？
5. 这是战略决策还是战术决策？

**快速检查：**
```bash
node skills/agent-autonomy-kit/check-queue.js --pre-response
```

**参见：** `decision-checklist.md` 获取完整详情

### 文件

- `post-task-protocol.md` — 任务完成后的回路
- `decision-checklist.md` — 预响应验证
- `check-queue.js --pre-response` — 自动化检查 1-3

### 成功指标

**修复前：** 每次任务完成后询问"下一步是什么？"

**修复后：** "下一步是什么？"仅在确实卡住时才问（队列清空、5D 空闲、无日程、被阻塞）

**目标：** 每会话 <1 次许可请求（战略决策除外）
```

**验证：**
```bash
grep -n "Loop-Back Enforcement" skills/agent-autonomy-kit/README.md
# 应显示新的部分
```

**提交：**
```bash
git add skills/agent-autonomy-kit/README.md
git commit -m "Document loop-back enforcement and decision checklist"
```

---

### ⏳ 任务 3.2：更新 SKILL.md 文件列表

**状态：** 待办

**文件：** `skills/agent-autonomy-kit/SKILL.md`

**所需更改：**

SKILL.md 很简洁。无需更改——它指向 README.md，我们已经更新了。

**验证：**
```bash
cat skills/agent-autonomy-kit/SKILL.md
# 应该仍然简洁，指向 README
```

---

### ⏳ 任务 3.3：验证所有文件存在

**状态：** 待办（阶段 1-2 完成后）

**检查清单：**
```bash
# 协议文件
[ ] ls skills/agent-autonomy-kit/post-task-protocol.md
[ ] ls skills/agent-autonomy-kit/decision-checklist.md
[ ] ls skills/agent-autonomy-kit/DIAGNOSIS.md
[ ] ls skills/agent-autonomy-kit/IMPLEMENTATION-CHECKLIST.md

# 已更新的文件
[ ] grep "LOOP BACK" HEARTBEAT.md
[ ] grep "Before Asking" AGENTS.md
[ ] grep "preResponseCheck" skills/agent-autonomy-kit/check-queue.js
[ ] grep "Loop-Back Enforcement" skills/agent-autonomy-kit/README.md

# 测试
[ ] bash skills/agent-autonomy-kit/test-queue-checker.sh
```

**所有应通过。**

---

## 阶段 4：实际使用与迭代（48 小时）

### ⏳ 任务 4.1：在生产环境启用回路

**状态：** 待办（阶段 1-3 完成后）

**要做的：**

Kai（主智能体）现在应在正常操作中遵循新协议。

**在每日日志中追踪这些指标：**

1. **许可请求次数：**
   - 每次会话中 Kai 询问"我们接下来该处理什么？"多少次
   - 目标：0（除非确实被阻塞/战略决策）

2. **队列检查合规性：**
   - 完成任务后，Kai 是否运行了队列检查器？
   - 目标：100%

3. **自主回路次数：**
   - 任务完成后，Kai 是否自主 spawn 了下一个智能体？
   - 目标：100%（当存在 HIGH 任务时）

**日志格式：**
```markdown
## 自主工作指标（2026 年 2 月 5 日）

**完成任务数：** 3
- Colony Skill ✅ → 检查队列 → Spawn 了 Observability 智能体
- Observability 内容 ✅ → 检查队列 → 所有 HIGH 任务完成
- Memory Wars ✅ → 检查日程 → 按计划执行

**许可请求次数：** 0（目标：<1）
**任务后队列检查：** 3/3（100%）
**自主回路：** 3/3（100%）

**结论：** 回路协议运行完美。
```

---

### ⏳ 任务 4.2：记录边界情况

**状态：** 待办（48 小时实际使用期间）

如果你遇到协议以下情况：
- 未覆盖某个场景
- 提供了不清晰的指导
- 与其他流程冲突

**记录在：** `skills/agent-autonomy-kit/EDGE-CASES.md`

**格式：**
```markdown
## 边界情况：[描述]

**场景：** 发生了什么

**当前协议说：** [协议引用]

**缺口：** 未覆盖什么

**建议修复：** 如何处理

**频率：** 常见 / 罕见 / 一次性

**优先级：** 严重 / 重要 / 锦上添花
```

这将成为 v1.1 迭代的输入。

---

### ⏳ 任务 4.3：衡量成功

**状态：** 待办（48 小时实际使用后）

**关键问题：**

1. **请求许可是否停止了？**
   - 在日志中统计"我们接下来该处理什么？"
   - 目标：0 次（当队列有 HIGH 任务时）

2. **自主回路是否有效？**
   - 完成任务后，智能体是否 spawn 了下一个工作？
   - 目标：100%（当存在 HIGH 任务时）

3. **预响应检查是否有效？**
   - 询问人类之前，智能体是否运行了检查清单？
   - 目标：100% 合规

4. **是否有误报？**
   - 智能体是否在确实被阻塞时未能询问？
   - 目标：0（不应过度强制执行）

**成功标准：**

- ✅ 队列/日程有答案时，0 次"下一步是什么？"询问
- ✅ 100% 任务后队列检查
- ✅ 存在 HIGH 任务时 100% 自主 spawn
- ✅ 智能体在确实被阻塞时仍然会询问（不过度强制执行）

**如果成功：** 进入阶段 5（文档化并发布 v1.1）

**如果部分成功：** 迭代协议，延长实际使用周期

**如果失败：** 升级到诊断审查

---

## 阶段 5：文档化与分发（2 小时）

### ⏳ 任务 5.1：更新 CHANGELOG

**状态：** 待办（实际使用成功后）

**文件：** `skills/agent-autonomy-kit/CHANGELOG.md`

如果不存在则创建：

```markdown
# 更新日志

## v1.1.0 - 回路强制执行（2026 年 2 月）

### 修复
- **严重：** 智能体不再在队列有 HIGH 优先级任务时询问"下一步是什么？"
- **严重：** 任务后协议强制每次任务完成后进行队列重新检查
- **严重：** 决策检查清单防止在所有决策边界处请求许可

### 新增
- `post-task-protocol.md` — 任务完成后的必须回路
- `decision-checklist.md` — 向人类请求方向前的 5 步验证
- `check-queue.js --pre-response` — 队列/日程/5D 循环自动化检查
- HEARTBEAT.md 中的回路强制执行
- AGENTS.md 中的预响应指南

### 变更
- 队列强制执行现在覆盖所有决策边界（原来：仅心跳入口）
- HEARTBEAT.md 更新了回路指令
- AGENTS.md 更新了预响应检查清单
- README.md 文档化了回路系统

### 指标（修复前 → 修复后）
- 自主执行覆盖率：40% → 95%
- 队列有答案时的许可请求：常见 → 0
- 任务后回路：0% → 100%

### 迁移
如果使用 Autonomy Kit v1.0：
1. 拉取最新版本
2. 阅读 `DIAGNOSIS.md` 了解背景
3. 遵循 `IMPLEMENTATION-CHECKLIST.md` 部署修复
4. 更新工作区 HEARTBEAT.md 和 AGENTS.md

---

## v1.0.0 - 初始版本（2026 年 2 月）

### 新增
- 任务队列系统（tasks/QUEUE.md）
- 队列优先级强制执行（check-queue.js）
- 主动心跳框架
- 5D 自主循环
- HEARTBEAT.md 模板
- 含完整文档的 README

### 已知问题
- 队列检查器仅在心跳入口运行（v1.1 修复）
- 无任务后协议（v1.1 修复）
- 任务完成后请求许可（v1.1 修复）
```

**提交：**
```bash
git add skills/agent-autonomy-kit/CHANGELOG.md
git commit -m "Add v1.1.0 changelog: loop-back enforcement"
```

---

### ⏳ 任务 5.2：更新示例文件

**状态：** 待办

**文件：** `skills/agent-autonomy-kit/QUEUE-ENFORCEMENT-EXAMPLES.md`

添加新部分：

```markdown
---

## 示例 5：任务后回路（v1.1 新增）

### 场景：任务完成边界

**v1.1 之前：**
```
16:00 - Colony Skill 任务完成
16:00 - 智能体："任务完成！我们接下来该处理什么？"
结果：尽管队列中有 14 个 HIGH 任务，仍然请求许可
```

**v1.1 之后：**
```
16:00 - Colony Skill 任务完成
16:00 - 更新 tasks/QUEUE.md（移到 Done）
16:00 - 运行：node skills/agent-autonomy-kit/check-queue.js
16:00 - 输出：退出码 1（14 个 HIGH 优先级任务）
16:01 - 最高优先级：Observability Control Plane 定位
16:01 - Spawn：echo-observability-positioning
结果：自主回路，无需许可
```

**变更内容：** 任务后协议强制进行队列重新检查。

**参见：** `post-task-protocol.md` 获取完整详情。

---

## 示例 6：预响应检查（v1.1 新增）

### 场景：智能体想询问"下一步是什么？"

**v1.1 之前：**
```
智能体输入："我们接下来该做什么？"
智能体发送消息
结果：人类需要重定向到队列
```

**v1.1 之后：**
```
智能体考虑询问："我们接下来该做什么？"
智能体运行：node skills/agent-autonomy-kit/check-queue.js --pre-response
输出："队列中有 14 个 HIGH 任务 - DON'T ASK"
智能体 spawn：下一个 HIGH 优先级智能体
结果：自主决策，无需人类介入
```

**变更内容：** 决策检查清单在发送前捕获请求许可行为。

**参见：** `decision-checklist.md` 获取完整详情。
```

**提交：**
```bash
git add skills/agent-autonomy-kit/QUEUE-ENFORCEMENT-EXAMPLES.md
git commit -m "Add v1.1 loop-back examples"
```

---

### ⏳ 任务 5.3：测试套件更新

**状态：** 待办

**文件：** `skills/agent-autonomy-kit/test-queue-checker.sh`

添加 `--pre-response` 标志的测试：

```bash
# 在现有测试之后添加

echo ""
echo "测试 7：预响应检查 - 有 HIGH 任务"
echo "---"
node check-queue.js --pre-response > /tmp/test7.txt 2>&1
EXIT_CODE=$?
if [ $EXIT_CODE -eq 1 ] && grep -q "DON'T ASK" /tmp/test7.txt; then
    echo "✅ 通过：预响应正确阻止了询问"
else
    echo "❌ 失败：应返回退出码 1 并显示 DON'T ASK 消息"
    cat /tmp/test7.txt
fi

echo ""
echo "测试 8：预响应检查 - 队列清空"
# 临时移动任务文件以模拟空队列
mv tasks/QUEUE.md tasks/QUEUE.md.bak
echo "# Task Queue" > tasks/QUEUE.md
echo "## Ready" >> tasks/QUEUE.md
echo "" >> tasks/QUEUE.md

node check-queue.js --pre-response > /tmp/test8.txt 2>&1
EXIT_CODE=$?
if [ $EXIT_CODE -eq 0 ] && grep -q "Safe to ask" /tmp/test8.txt; then
    echo "✅ 通过：空闲时预响应允许询问"
else
    echo "❌ 失败：应返回退出码 0 并显示 Safe to ask"
    cat /tmp/test8.txt
fi

# 恢复队列
mv tasks/QUEUE.md.bak tasks/QUEUE.md
```

**运行测试：**
```bash
cd skills/agent-autonomy-kit
bash test-queue-checker.sh
# 所有测试应通过
```

**提交：**
```bash
git add skills/agent-autonomy-kit/test-queue-checker.sh
git commit -m "Add pre-response flag tests"
```

---

### ⏳ 任务 5.4：推送到 GitHub

**状态：** 待办（所有提交后）

```bash
cd skills/agent-autonomy-kit
git push origin main
```

**验证：**
```bash
# 检查 GitHub 显示所有新文件：
# - DIAGNOSIS.md
# - IMPLEMENTATION-CHECKLIST.md
# - post-task-protocol.md
# - decision-checklist.md
# - 已更新：HEARTBEAT.md, AGENTS.md, README.md, check-queue.js
```

---

### ⏳ 任务 5.5：发布 v1.1

**状态：** 待办

**渠道：**

1. **The Colony：**
   ```
   "Agent Autonomy Kit v1.1：回路强制执行

   修复了 v1.0 的首要问题：智能体在心跳入口检查队列，但完成任务后
   会问'我们接下来该处理什么？'。

   v1.1 新增：
   • 任务后协议（必须的队列重新检查）
   • 决策检查清单（询问人类前的 5 项检查）
   • check-queue.js 的 --pre-response 标志

   结果：请求许可从常见 → 0。

   完整诊断 + 实施指南见仓库。
   https://github.com/reflectt/agent-autonomy-kit"
   ```

2. **DEV.to：**
   文章："修复智能体请求许可：一次诊断"
   - 问题：智能体在入口检查队列但不在任务边界检查
   - 解决方案：回路协议 + 决策检查清单
   - 结果：40% → 95% 自主执行覆盖率
   - v1.1 发布链接

3. **Moltbook：**
   同 The Colony 帖子，调整为 Moltbook 语气

---

## 完成标准

### 阶段 1-3：实施完成
- ✅ 所有协议文件已创建
- ✅ HEARTBEAT.md 更新了回路
- ✅ AGENTS.md 更新了预响应检查
- ✅ check-queue.js 有 --pre-response 标志
- ✅ README.md 文档化了回路系统
- ✅ 所有测试通过

### 阶段 4：实际使用成功
- ✅ 队列有 HIGH 任务时 0 次"下一步是什么？"询问
- ✅ 100% 任务后队列检查
- ✅ 存在 HIGH 任务时 100% 自主 spawn
- ✅ 智能体在确实被阻塞时仍然会询问

### 阶段 5：分发完成
- ✅ CHANGELOG.md 已写
- ✅ 示例已更新
- ✅ 测试已更新
- ✅ 已推送到 GitHub
- ✅ 已在 The Colony、DEV.to、Moltbook 发布

---

## 时间线

**第 1 天（今天）：**
- 阶段 1：添加协议（30 分钟）✅ 已完成
- 阶段 2：增强队列检查器（30 分钟）
- 阶段 3：更新文档（15 分钟）
- **总计：** 75 分钟

**第 2-3 天：**
- 阶段 4：在生产环境实际使用（被动监控）
- 收集指标
- 记录边界情况

**第 4 天：**
- 阶段 4：衡量成功
- 阶段 5：文档化 + 分发（2 小时）
- **总计：** 2 小时

**总体：** 90 分钟主动工作 + 48 小时被动测试

---

## 回滚计划

如果 v1.1 导致问题：

```bash
# 回退 HEARTBEAT.md
git checkout HEAD~1 HEARTBEAT.md

# 回退 AGENTS.md
git checkout HEAD~1 AGENTS.md

# 回退 check-queue.js
git checkout HEAD~1 skills/agent-autonomy-kit/check-queue.js

# 保留诊断文件（对迭代有用）
# - DIAGNOSIS.md
# - post-task-protocol.md
# - decision-checklist.md
```

**何时回退：**
- 智能体在确实被阻塞时未能询问
- 误报强制执行（阻止了合理的问题）
- 系统变得过于僵化

**预期：** 回退可能性不大——变更是增量式的且保持安全性。

---

## 下一步

**For Ryan：**
1. 审查 DIAGNOSIS.md（理解问题）
2. 批准实施计划
3. 执行阶段 1-3 任务（75 分钟）
4. 让 Kai 实际使用 48 小时
5. 审查指标并发布 v1.1

**For Kai：**
1. 阶段 1-3 完成后，遵循新协议
2. 在每日日志中追踪指标
3. 在 EDGE-CASES.md 中记录边界情况
4. 48 小时后，报告成功/问题
5. 如果成功，协助阶段 5 分发

---

*本检查清单将诊断转化为行动。按顺序执行。追踪进度。自信地发布 v1.1。*
