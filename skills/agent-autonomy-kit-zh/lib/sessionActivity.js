'use strict';

const fs = require('fs');
const path = require('path');

/**
 * 判断会话是否正在活跃运行。
 *
 * 规范（保守策略）：
 * - 仅当 updatedAt 在最近 5 分钟内且最后事件表明仍在运行，
 *   或找不到完成标记时，才认为 subagent 会话处于活跃状态。
 * - 如果无法检测到完成标记（即最后事件是 unknown/不可读），
 *   则要求 updatedAt 在最近 2 分钟内。
 */

const MS = {
  minute: 60 * 1000,
};

function readLastJsonlRecord(jsonlPath) {
  // 安全读取小尾部：文件可能很大。
  // 策略：读取最后约 128KB 并解析最后一个非空行。
  const fd = fs.openSync(jsonlPath, 'r');
  try {
    const stat = fs.fstatSync(fd);
    const tailSize = Math.min(128 * 1024, stat.size);
    const start = Math.max(0, stat.size - tailSize);
    const buf = Buffer.alloc(tailSize);
    fs.readSync(fd, buf, 0, tailSize, start);
    const text = buf.toString('utf8');
    const lines = text.split('\n');

    // 从后向前遍历，找到最后一个非空、可解析的 JSON 行
    for (let i = lines.length - 1; i >= 0; i--) {
      const line = lines[i].trim();
      if (!line) continue;
      try {
        return JSON.parse(line);
      } catch {
        // 继续遍历，可能刚好截断在某行中间
        continue;
      }
    }
    return null;
  } finally {
    fs.closeSync(fd);
  }
}

function classifyLastRecord(rec) {
  if (!rec || typeof rec !== 'object') return { status: 'unknown', reason: 'no_record' };

  // OpenClaw 会话 jsonl 记录通常格式：
  // { type: 'message', message: { role: 'assistant'|'user'|'toolResult', ... }, stopReason?: 'stop'|'toolUse'|... }
  if (rec.type === 'message') {
    const role = rec.message && rec.message.role;

    // 完成标记：助手正常结束
    if (role === 'assistant' && (rec.stopReason === 'stop' || rec.stopReason === 'end')) {
      return { status: 'completed', reason: `assistant_stopReason:${rec.stopReason}` };
    }

    // 强运行中指标
    if (role === 'assistant' && rec.stopReason === 'toolUse') {
      return { status: 'running', reason: 'assistant_waiting_tool' };
    }
    if (role === 'toolResult') {
      return { status: 'running', reason: 'tool_result_last' };
    }

    // 弱/未知：可能是用户消息或其他助手停止原因
    return { status: 'unknown', reason: `message_role:${role || 'none'} stopReason:${rec.stopReason || 'none'}` };
  }

  return { status: 'unknown', reason: `record_type:${rec.type || 'none'}` };
}

function isSessionActive({ updatedAt, nowMs, lastRecordStatus }) {
  const ageMs = nowMs - updatedAt;
  if (!Number.isFinite(ageMs) || ageMs < 0) return false;

  if (lastRecordStatus === 'running') {
    return ageMs <= 5 * MS.minute;
  }

  if (lastRecordStatus === 'completed') {
    return false;
  }

  // 未知状态：仅在其*非常*新时才视为活跃
  return ageMs <= 2 * MS.minute;
}

function getLastRecordInfo({ sessionsDir, sessionId }) {
  const jsonlPath = path.join(sessionsDir, `${sessionId}.jsonl`);
  if (!fs.existsSync(jsonlPath)) {
    return { jsonlPath, lastRecord: null, classification: { status: 'unknown', reason: 'missing_jsonl' } };
  }

  const lastRecord = readLastJsonlRecord(jsonlPath);
  const classification = classifyLastRecord(lastRecord);
  return { jsonlPath, lastRecord, classification };
}

module.exports = {
  readLastJsonlRecord,
  classifyLastRecord,
  isSessionActive,
  getLastRecordInfo,
  MS,
};
