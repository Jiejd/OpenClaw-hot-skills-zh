#!/usr/bin/env node
'use strict';

/**
 * 自主化看门狗：检查是否有 subagent 会话真正处于活跃状态。
 *
 * 原因：会话在完成后可能仍然显示为"最近更新"。
 * 此脚本避免将最近完成的 subagent 误判为"活跃工作"。
 *
 * 输出：
 * - 默认输出人类可读格式。
 * - 使用 --json 获取机器可读输出。
 *
 * 退出码：
 * - 0：未检测到活跃的 subagent
 * - 1：检测到至少一个活跃的 subagent
 */

const { execSync } = require('child_process');
const path = require('path');

const {
  getLastRecordInfo,
  isSessionActive,
} = require('./lib/sessionActivity');

function parseArgs(argv) {
  const out = { json: false, activeMinutes: 10 };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--json') out.json = true;
    if (a === '--active-minutes') {
      out.activeMinutes = parseInt(argv[i + 1], 10);
      i++;
    }
  }
  return out;
}

function main() {
  const args = parseArgs(process.argv.slice(2));

  const raw = execSync(`openclaw sessions --json --active ${args.activeMinutes}`, { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });
  const parsed = JSON.parse(raw);

  const sessions = Array.isArray(parsed.sessions) ? parsed.sessions : [];
  const sessionsStorePath = parsed.path;
  const sessionsDir = sessionsStorePath ? path.dirname(sessionsStorePath) : null;

  const nowMs = Date.now();

  const subagents = sessions.filter(s => typeof s.key === 'string' && s.key.includes(':subagent:'));

  const results = [];
  for (const s of subagents) {
    const updatedAt = s.updatedAt;
    const sessionId = s.sessionId;

    let classification = { status: 'unknown', reason: 'no_sessions_dir' };
    let jsonlPath = null;
    if (sessionsDir && sessionId) {
      const info = getLastRecordInfo({ sessionsDir, sessionId });
      classification = info.classification;
      jsonlPath = info.jsonlPath;
    }

    const active = isSessionActive({
      updatedAt,
      nowMs,
      lastRecordStatus: classification.status,
    });

    results.push({
      key: s.key,
      kind: s.kind,
      sessionId,
      updatedAt,
      ageMs: nowMs - updatedAt,
      lastRecordStatus: classification.status,
      lastRecordReason: classification.reason,
      jsonlPath,
      active,
    });
  }

  const activeOnes = results.filter(r => r.active);

  if (args.json) {
    process.stdout.write(JSON.stringify({
      checkedAt: new Date().toISOString(),
      activeMinutes: args.activeMinutes,
      subagentsChecked: results.length,
      activeSubagents: activeOnes.length,
      results,
    }, null, 2) + '\n');
  } else {
    if (results.length === 0) {
      console.log('未在最近的会话列表中找到 subagent 会话。');
    } else if (activeOnes.length === 0) {
      console.log(`未检测到活跃的 subagent（已检查 ${results.length} 个）。`);
      for (const r of results) {
        console.log(`- 空闲: ${r.key} 存活=${Math.round(r.ageMs/1000)}s 上次状态=${r.lastRecordStatus} (${r.lastRecordReason})`);
      }
    } else {
      console.log(`检测到活跃的 subagent（${activeOnes.length}/${results.length}）：`);
      for (const r of activeOnes) {
        console.log(`- 活跃: ${r.key} 存活=${Math.round(r.ageMs/1000)}s 上次状态=${r.lastRecordStatus} (${r.lastRecordReason})`);
      }
    }
  }

  process.exit(activeOnes.length > 0 ? 1 : 0);
}

main();
