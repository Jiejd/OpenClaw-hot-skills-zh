#!/usr/bin/env node
'use strict';

const assert = require('assert');

const { classifyLastRecord, isSessionActive, MS } = require('./lib/sessionActivity');

function run() {
  const nowMs = 1_000_000;

  // 已完成标记
  {
    const rec = { type: 'message', message: { role: 'assistant', content: [] }, stopReason: 'stop' };
    const c = classifyLastRecord(rec);
    assert.equal(c.status, 'completed');

    const active = isSessionActive({ updatedAt: nowMs - 1 * MS.minute, nowMs, lastRecordStatus: c.status });
    assert.equal(active, false);
  }

  // 运行中标记：toolUse
  {
    const rec = { type: 'message', message: { role: 'assistant', content: [] }, stopReason: 'toolUse' };
    const c = classifyLastRecord(rec);
    assert.equal(c.status, 'running');

    assert.equal(isSessionActive({ updatedAt: nowMs - 4 * MS.minute, nowMs, lastRecordStatus: c.status }), true);
    assert.equal(isSessionActive({ updatedAt: nowMs - 6 * MS.minute, nowMs, lastRecordStatus: c.status }), false);
  }

  // 未知标记：仅在 <=2 分钟内视为活跃
  {
    const rec = { type: 'message', message: { role: 'assistant', content: [] }, stopReason: 'length' };
    const c = classifyLastRecord(rec);
    assert.equal(c.status, 'unknown');

    assert.equal(isSessionActive({ updatedAt: nowMs - 60 * 1000, nowMs, lastRecordStatus: c.status }), true);
    assert.equal(isSessionActive({ updatedAt: nowMs - 3 * MS.minute, nowMs, lastRecordStatus: c.status }), false);
  }

  console.log('✅ 测试通过：sessionActivity 分类 + 活跃状态判断');
}

run();
