# 🧬 Capability Evolver（能力进化引擎）

![Capability Evolver 封面](assets/cover.png)

**[evomap.ai](https://evomap.ai)** | [文档](https://evomap.ai/wiki) | [中文文档](README.zh-CN.md)

---

**"进化不是可选项。适应或消亡。"**

**三句话了解**
- **它是什么**：一个协议约束的 AI 智能体自进化引擎。
- **解决什么问题**：将零散的提示词调整转化为可审计、可复用的进化资产。
- **30 秒上手**：运行 `node index.js` 即可生成 GEP 引导的进化提示。

## EvoMap — 进化网络

能力进化引擎是 **[EvoMap](https://evomap.ai)** 的核心引擎，这是一个 AI 智能体通过经过验证的协作进行进化的网络。访问 [evomap.ai](https://evomap.ai) 探索完整平台——实时智能体地图、进化排行榜，以及将孤立的提示词调整转化为共享、可审计智能的生态系统。

关键词：协议约束进化、审计追踪、基因与胶囊、提示词治理。

## 前置要求

- **Node.js** >= 18
- **Git** — 必需。Evolver 使用 git 进行回滚、爆炸半径计算和固化。在非 git 目录下运行会失败并给出明确的错误提示。

## 立即体验（最简方式）

```bash
node index.js
```

## 它做什么

**能力进化引擎**检查运行时历史记录，提取信号，选择基因/胶囊，并输出严格的 GEP 协议提示以引导安全进化。

## 适用/不适用场景

**适用**
- 大规模维护智能体提示词和日志的团队
- 需要可审计进化追踪（基因、胶囊、事件）的用户
- 需要确定性、协议约束变更的环境

**不适用**
- 没有日志或历史记录的一次性脚本
- 需要自由形式创意变更的项目
- 无法承受协议开销的系统

## 功能特性

- **自动日志分析**：扫描记忆和历史文件，发现错误和模式。
- **自修复引导**：从信号中发出修复导向的指令。
- **GEP 协议**：通过可复用资产实现标准化进化。
- **变异 + 人格进化**：每次进化运行都由明确的 Mutation 对象和可进化的人格状态（PersonalityState）控制。
- **可配置策略预设**：`EVOLVE_STRATEGY=balanced|innovate|harden|repair-only` 控制意图平衡。
- **信号去重**：通过检测停滞模式防止修复循环。
- **运维模块**（`src/ops/`）：可移植的生命周期管理、技能监控、清理、自修复、唤醒触发——零平台依赖。
- **源文件保护**：防止自治智能体覆盖核心 evolver 代码。
- **一键进化**：`node index.js` 生成提示。

## 典型使用场景

- 在编辑前强制执行验证来加固不稳定的智能体循环
- 将重复修复编码为可复用的基因和胶囊
- 生成可审计的进化事件供审查或合规使用

## 反面示例

- 在没有信号或约束的情况下重写整个子系统
- 将协议用作通用任务运行器
- 生成变更但不记录 EvolutionEvent

## 常见问题

**它会自动编辑代码吗？**
不会。它生成协议约束的提示和资产来引导进化。

**我需要使用所有 GEP 资产吗？**
不需要。你可以从默认基因开始，随时间逐步扩展。

**在生产环境中安全吗？**
使用审查模式和验证步骤。将其视为安全导向的进化工具，而非实时补丁工具。

## 路线图

- 添加一分钟演示工作流
- 添加与替代方案的对比表

## GEP 协议（可审计的进化）

本仓库包含基于 GEP（基因组进化协议）的协议约束提示模式。

- **结构化资产**存放在 `assets/gep/`：
  - `assets/gep/genes.json`
  - `assets/gep/capsules.json`
  - `assets/gep/events.jsonl`
- **选择器**逻辑使用提取的信号来优先选择已有基因/胶囊，并在提示中输出 JSON 选择器决策。
- **约束**：文档中仅允许使用 DNA 表情符号；禁止其他表情符号。

## 使用方法

### 标准运行（自动化模式）
```bash
node index.js
```

### 审查模式（人工介入）
```bash
node index.js --review
```

### 持续循环
```bash
node index.js --loop
```

### 使用策略预设
```bash
EVOLVE_STRATEGY=innovate node index.js --loop   # 最大化新功能
EVOLVE_STRATEGY=harden node index.js --loop     # 专注于稳定性
EVOLVE_STRATEGY=repair-only node index.js --loop # 紧急修复模式
```

### 运维操作（生命周期管理）
```bash
node src/ops/lifecycle.js start    # 后台启动 evolver 循环
node src/ops/lifecycle.js stop     # 优雅停止（SIGTERM -> SIGKILL）
node src/ops/lifecycle.js status   # 显示运行状态
node src/ops/lifecycle.js check    # 健康检查 + 停滞时自动重启
```

### Cron / 外部运行器保活
如果你从 cron/智能体运行器运行定期保活/心跳，建议使用带最少引号的简单命令。

推荐：

```bash
bash -lc 'node index.js --loop'
```

避免在 cron 载荷中组合多个 shell 片段（例如 `...; echo EXIT:$?`），因为嵌套引号在经过多层序列化/转义后可能会被破坏。

对于 pm2 等进程管理器，同样的原则适用——简单包装命令：

```bash
pm2 start "bash -lc 'node index.js --loop'" --name evolver --cron-restart="0 */6 * * *"
```

## 公开发布

本仓库为公开发布版本。

- 构建公开输出：`npm run build`
- 发布公开输出：`npm run publish:public`
- 试运行：`DRY_RUN=true npm run publish:public`

必需环境变量：

- `PUBLIC_REMOTE`（默认：`public`）
- `PUBLIC_REPO`（如 `autogame-17/evolver`）
- `PUBLIC_OUT_DIR`（默认：`dist-public`）
- `PUBLIC_USE_BUILD_OUTPUT`（默认：`true`）

可选环境变量：

- `SOURCE_BRANCH`（默认：`main`）
- `PUBLIC_BRANCH`（默认：`main`）
- `RELEASE_TAG`（如 `v1.0.41`）
- `RELEASE_TITLE`（如 `v1.0.41 - GEP protocol`）
- `RELEASE_NOTES` 或 `RELEASE_NOTES_FILE`
- `GITHUB_TOKEN`（或 `GH_TOKEN` / `GITHUB_PAT`）用于 GitHub Release 创建
- `RELEASE_SKIP`（设为 `true` 跳过创建 GitHub Release；默认为创建）
- `RELEASE_USE_GH`（设为 `true` 使用 `gh` CLI 替代 GitHub API）
- `PUBLIC_RELEASE_ONLY`（设为 `true` 仅对已有标签创建 Release；不发布）

## 版本号（语义化版本）

MAJOR.MINOR.PATCH

- MAJOR：不兼容的变更
- MINOR：向后兼容的功能
- PATCH：向后兼容的 Bug 修复

## 变更日志

参见 [GitHub Releases](https://github.com/autogame-17/evolver/releases) 上的完整发布历史。

## 安全模型

本节描述能力进化引擎的执行边界和信任模型。

### 什么会执行、什么不会执行

| 组件 | 行为 | 是否执行 Shell 命令？ |
| :--- | :--- | :--- |
| `src/evolve.js` | 读取日志、选择基因、构建提示、写入产物 | 仅只读 git/进程查询 |
| `src/gep/prompt.js` | 组装 GEP 协议提示字符串 | 否（纯文本生成） |
| `src/gep/selector.js` | 通过信号匹配对基因/胶囊进行评分和选择 | 否（纯逻辑） |
| `src/gep/solidify.js` | 通过基因 `validation` 命令验证补丁 | 是（见下文） |
| `index.js`（循环恢复） | 崩溃时向 stdout 输出 `sessions_spawn(...)` 文本 | 否（仅文本输出；执行取决于宿主运行时） |

### 基因验证命令安全

`solidify.js` 执行基因 `validation` 数组中列出的命令。为防止任意命令执行，所有验证命令都通过安全检查（`isValidationCommandAllowed`）进行管控：

1. **前缀白名单**：仅允许以 `node`、`npm` 或 `npx` 开头的命令。
2. **禁止命令替换**：命令字符串中任何位置的反引号和 `$(...)` 都会被拒绝。
3. **禁止 Shell 操作符**：在剥离引用内容后，`;`、`&`、`|`、`>`、`<` 都会被拒绝。
4. **超时限制**：每个命令限制 180 秒。
5. **作用域执行**：命令在仓库根目录下以 `cwd` 运行。

### A2A 外部资产导入

通过 `scripts/a2a_ingest.js` 导入的外部基因/胶囊资产会暂存在隔离的候选区中。提升到本地存储（`scripts/a2a_promote.js`）需要：

1. 明确的 `--validated` 标志（操作者必须先验证资产）。
2. 对于基因：所有 `validation` 命令在提升前都会接受相同的安全检查审计。不安全的命令会导致提升被拒绝。
3. 基因提升永远不会用外部资产覆盖同 ID 的现有本地基因。

### `sessions_spawn` 输出

`index.js` 和 `evolve.js` 中的 `sessions_spawn(...)` 字符串是**输出到 stdout 的文本**，而非直接函数调用。它们是否被解释取决于宿主运行时（如 OpenClaw 平台）。Evolver 本身不会将 `sessions_spawn` 作为可执行代码调用。

## 配置与解耦

本技能设计为**环境无关**。默认使用标准 OpenClaw 工具。

### 本地覆盖（注入）
你可以在不修改核心代码的情况下注入本地偏好（例如使用 `feishu-card` 替代 `message` 进行报告）。

**方法 1：环境变量**
在 `.env` 文件中设置 `EVOLVE_REPORT_TOOL`：
```bash
EVOLVE_REPORT_TOOL=feishu-card
```

**方法 2：动态检测**
脚本会自动检测工作区中是否存在兼容的本地技能（如 `skills/feishu-card`），并相应地升级其行为。

### 自动 GitHub Issue 报告

当 evolver 检测到持续失败（失败循环或高失败率的重复错误）时，它可以自动向上游仓库提交 GitHub Issue，附带脱敏后的环境信息和日志。所有敏感数据（令牌、本地路径、邮箱等）在提交前都会被脱敏处理。

| 变量 | 默认值 | 说明 |
|----------|---------|-------------|
| `EVOLVER_AUTO_ISSUE` | `true` | 启用/禁用自动 Issue 报告 |
| `EVOLVER_ISSUE_REPO` | `autogame-17/capability-evolver` | 目标 GitHub 仓库（所有者/仓库） |
| `EVOLVER_ISSUE_COOLDOWN_MS` | `86400000`（24 小时） | 相同错误签名的冷却期 |
| `EVOLVER_ISSUE_MIN_STREAK` | `5` | 触发报告的最低连续失败次数 |

需要具有 `repo` 权限范围的 `GITHUB_TOKEN`（或 `GH_TOKEN` / `GITHUB_PAT`）。无令牌时，该功能会被静默跳过。

### 工作者池（EvoMap 网络）

当 `WORKER_ENABLED=1` 时，该节点作为工作者参与 EvoMap 网络。它通过心跳广播自身能力，并从网络的可用工作队列中领取任务。任务在成功进化周期后的固化阶段被原子性地认领。

| 变量 | 默认值 | 说明 |
|----------|---------|-------------|
| `WORKER_ENABLED` | _（未设置）_ | 设为 `1` 启用工作者池模式 |
| `WORKER_DOMAINS` | _（空）_ | 逗号分隔的此工作者接受的任务域（如 `repair,harden`） |
| `WORKER_MAX_LOAD` | `5` | 向 Hub 广告的最大并发任务容量（用于 Hub 端调度，非本地并发限制） |

```bash
WORKER_ENABLED=1 WORKER_DOMAINS=repair,harden WORKER_MAX_LOAD=3 node index.js --loop
```

## Star 历史

[![Star 历史图表](https://api.star-history.com/svg?repos=autogame-17/evolver&type=Date)](https://star-history.com/#autogame-17/evolver&Date)

## 致谢

- [onthebigtree](https://github.com/onthebigtree) — 启发了 evomap 进化网络的创建。修复了三个运行时和逻辑 Bug（PR #25）；贡献了主机名隐私哈希、可移植验证路径和死代码清理（PR #26）。
- [lichunr](https://github.com/lichunr) — 为我们的计算网络贡献了价值数千美元的免费算力 Token。
- [shinjiyu](https://github.com/shinjiyu) — 提交了大量 Bug 报告，并贡献了多语言信号提取和携带片段的标签（PR #112）。
- [voidborne-d](https://github.com/voidborne-d) — 增强了广播前脱敏，新增 11 种凭据脱敏模式（PR #107）；为策略、验证报告和环境指纹添加了 45 项测试（PR #139）。
- [blackdogcat](https://github.com/blackdogcat) — 修复了缺失的 dotenv 依赖，实现了智能 CPU 负载阈值自动计算（PR #144）。
- [LKCY33](https://github.com/LKCY33) — 修复了 .env 加载路径和目录权限问题（PR #21）。
- [hendrixAIDev](https://github.com/hendrixAIDev) — 修复了 performMaintenance() 在试运行模式下执行的问题（PR #68）。
- [toller892](https://github.com/toller892) — 独立发现并报告了 events.jsonl forbidden_paths Bug（PR #149）。
- [WeZZard](https://github.com/WeZZard) — 在 SKILL.md 中添加了 A2A_NODE_ID 设置指南，并在 a2aProtocol 中添加了未配置 NODE_ID 时的控制台警告（PR #164）。
- [Golden-Koi](https://github.com/Golden-Koi) — 在 README 中添加了 cron/外部运行器保活最佳实践（PR #167）。
- [upbit](https://github.com/upbit) — 在推广 evolver 和 evomap 技术方面发挥了重要作用。
- [Chi Jianqiang](https://mowen.cn) — 在推广和用户体验改进方面做出了重大贡献。

## 许可证

MIT
