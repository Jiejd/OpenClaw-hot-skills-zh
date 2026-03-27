#!/usr/bin/env node
/**
 * 队列新鲜度检查器
 * 
 * 如果 tasks/QUEUE.md 超过 24 小时未更新则判定为失败。
 * 防止团队在过时的待办列表上运行，却以为一切正常。
 * 
 * 退出码 1 = 过时（必须在继续之前刷新队列）
 * 退出码 0 = 新鲜
 */

const fs = require('fs');
const path = require('path');

const MAX_AGE_HOURS = 24;

const queuePath = path.join(process.cwd(), 'tasks/QUEUE.md');

if (!fs.existsSync(queuePath)) {
  console.error('❌ tasks/QUEUE.md 不存在！请创建它。');
  process.exit(1);
}

// 检查文件修改时间
const stat = fs.statSync(queuePath);
const mtime = stat.mtimeMs;
const now = Date.now();
const ageHours = (now - mtime) / (1000 * 60 * 60);

// 同时尝试解析"Last updated"行
const content = fs.readFileSync(queuePath, 'utf-8');
const match = content.match(/Last updated:\s*(.+)/i);

if (ageHours > MAX_AGE_HOURS) {
  console.error(`❌ 队列已过时 — 上次修改于 ${ageHours.toFixed(1)} 小时前`);
  if (match) console.error(`   文件头显示："${match[1].trim()}"`);
  console.error(`   最大允许时间：${MAX_AGE_HOURS} 小时`);
  console.error('');
  console.error('需要操作：spawn Rhythm 🥁 刷新队列后再继续。');
  console.error('过时的队列意味着团队什么都不做，却报告"一切正常"。');
  process.exit(1);
} else {
  console.log(`✅ 队列是新鲜的（${ageHours.toFixed(1)} 小时前修改）`);
  if (match) console.log(`   文件头："${match[1].trim()}"`);
  process.exit(0);
}
