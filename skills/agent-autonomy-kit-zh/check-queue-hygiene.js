#!/usr/bin/env node
/**
 * check-queue-hygiene.js
 *
 * 强制 tasks/QUEUE.md 保持可执行状态：
 * - "High Priority / Ready" 分区中不得有已完成项（[x]）。
 *
 * 原因：在 Ready 中保留已完成项会导致团队停止推进
 * （他们认为工作已经完成）并使队列检查器失去作用。
 *
 * 退出码：
 * - 0：正常
 * - 1：卫生违规
 */

const fs = require('fs');
const path = require('path');

const queuePath = path.resolve(process.cwd(), 'tasks/QUEUE.md');

function die(msg) {
  process.stderr.write(`${msg}\n`);
  process.exit(1);
}

if (!fs.existsSync(queuePath)) {
  die(`未找到队列文件：${queuePath}`);
}

const text = fs.readFileSync(queuePath, 'utf8');

const startHeader = '## 🔥 High Priority / Ready';
const startIdx = text.indexOf(startHeader);
if (startIdx === -1) {
  die(`未找到分区标题：${startHeader}`);
}

// 找到此分区的结尾：start 之后的下一个"## "标题
const afterStart = text.slice(startIdx + startHeader.length);
const nextHeaderMatch = afterStart.match(/\n##\s+/);
const endIdx = nextHeaderMatch
  ? startIdx + startHeader.length + nextHeaderMatch.index
  : text.length;

const readySection = text.slice(startIdx, endIdx);

const completedLines = readySection
  .split(/\r?\n/)
  .filter((l) => /^- \[x\]/i.test(l.trim()));

if (completedLines.length > 0) {
  die(
    [
      '队列卫生检查失败：在"High Priority / Ready"中发现了已完成任务。',
      '请将这些项移到"✅ Recently Completed"（或删除），保持 Ready 分区可执行：',
      ...completedLines.map((l) => `  ${l.trim()}`),
    ].join('\n')
  );
}

process.stdout.write('队列卫生检查通过：High Priority / Ready 中无已完成项。\n');
process.exit(0);
