'use strict';

const fs = require('fs');
const path = require('path');
const { getReflectionLogPath, getEvolutionDir } = require('./paths');

const REFLECTION_INTERVAL_CYCLES = 5;
const REFLECTION_COOLDOWN_MS = 30 * 60 * 1000;

function ensureDir(dir) {
  try { if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true }); } catch (_) {}
}

function shouldReflect({ cycleCount, recentEvents }) {
  if (!Number.isFinite(cycleCount) || cycleCount < REFLECTION_INTERVAL_CYCLES) return false;
  if (cycleCount % REFLECTION_INTERVAL_CYCLES !== 0) return false;

  const logPath = getReflectionLogPath();
  try {
    if (fs.existsSync(logPath)) {
      const stat = fs.statSync(logPath);
      if (Date.now() - stat.mtimeMs < REFLECTION_COOLDOWN_MS) return false;
    }
  } catch (_) {}

  return true;
}

function buildReflectionContext({ recentEvents, signals, memoryAdvice, narrative }) {
  const parts = ['你正在对最近的进化周期进行战略反思。'];
  parts.push('分析以下模式并提供简洁的战略指导。');
  parts.push('');

  if (Array.isArray(recentEvents) && recentEvents.length > 0) {
    const last10 = recentEvents.slice(-10);
    const successCount = last10.filter(e => e && e.outcome && e.outcome.status === 'success').length;
    const failCount = last10.filter(e => e && e.outcome && e.outcome.status === 'failed').length;
    const intents = {};
    last10.forEach(e => {
      const i = e && e.intent ? e.intent : 'unknown';
      intents[i] = (intents[i] || 0) + 1;
    });
    const genes = {};
    last10.forEach(e => {
      const g = e && Array.isArray(e.genes_used) && e.genes_used[0] ? e.genes_used[0] : 'unknown';
      genes[g] = (genes[g] || 0) + 1;
    });

    parts.push('## 近期周期统计（最近 10 次）');
    parts.push(`- 成功：${successCount}，失败：${failCount}`);
    parts.push(`- 意图分布：${JSON.stringify(intents)}`);
    parts.push(`- 基因使用：${JSON.stringify(genes)}`);
    parts.push('');
  }

  if (Array.isArray(signals) && signals.length > 0) {
    parts.push('## 当前信号');
    parts.push(signals.slice(0, 20).join(', '));
    parts.push('');
  }

  if (memoryAdvice) {
    parts.push('## 记忆图谱建议');
    if (memoryAdvice.preferredGeneId) {
      parts.push(`- 首选基因：${memoryAdvice.preferredGeneId}`);
    }
    if (Array.isArray(memoryAdvice.bannedGeneIds) && memoryAdvice.bannedGeneIds.length > 0) {
      parts.push(`- 已封禁基因：${memoryAdvice.bannedGeneIds.join(', ')}`);
    }
    if (memoryAdvice.explanation) {
      parts.push(`- 说明：${memoryAdvice.explanation}`);
    }
    parts.push('');
  }

  if (narrative) {
    parts.push('## 近期进化叙事');
    parts.push(String(narrative).slice(0, 3000));
    parts.push('');
  }

  parts.push('## 需要回答的问题');
  parts.push('1. 是否有被忽略的持续信号？');
  parts.push('2. 基因选择策略是否最优，还是我们陷入了局部最优？');
  parts.push('3. 修复/优化/创新之间的平衡是否需要调整？');
  parts.push('4. 是否有当前基因无法覆盖的能力缺口？');
  parts.push('5. 哪个单一的战略调整能产生最大影响？');
  parts.push('');
  parts.push('以 JSON 对象回复：{ "insights": [...], "strategy_adjustment": "...", "priority_signals": [...] }');

  return parts.join('\n');
}

function recordReflection(reflection) {
  const logPath = getReflectionLogPath();
  ensureDir(path.dirname(logPath));

  const entry = JSON.stringify({
    ts: new Date().toISOString(),
    type: 'reflection',
    ...reflection,
  }) + '\n';

  fs.appendFileSync(logPath, entry, 'utf8');
}

function loadRecentReflections(count) {
  const n = Number.isFinite(count) ? count : 3;
  const logPath = getReflectionLogPath();
  try {
    if (!fs.existsSync(logPath)) return [];
    const lines = fs.readFileSync(logPath, 'utf8').trim().split('\n').filter(Boolean);
    return lines.slice(-n).map(line => {
      try { return JSON.parse(line); } catch (_) { return null; }
    }).filter(Boolean);
  } catch (_) {
    return [];
  }
}

module.exports = {
  shouldReflect,
  buildReflectionContext,
  recordReflection,
  loadRecentReflections,
  REFLECTION_INTERVAL_CYCLES,
};
