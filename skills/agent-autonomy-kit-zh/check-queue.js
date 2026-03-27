#!/usr/bin/env node
/**
 * 队列优先级检查器
 * 
 * 扫描 tasks/QUEUE.md 并强制执行队列优先机制。
 * 如果存在 HIGH/CRITICAL 优先级任务，返回退出码 1。
 * 如果队列为空或所有任务都是 LOW 优先级，返回退出码 0。
 * 
 * 用法：
 *   node skills/agent-autonomy-kit/check-queue.js
 * 
 * 集成方式：
 *   在说 HEARTBEAT_OK 之前运行此脚本。
 *   如果退出码为 1：为 HIGH 优先级任务 spawn 智能体。
 *   如果退出码为 0：安全继续其他工作。
 */

const fs = require('fs');
const path = require('path');

// ANSI 颜色码
const colors = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  green: '\x1b[32m',
  cyan: '\x1b[36m',
  bold: '\x1b[1m',
};

function parseQueueFile(queuePath) {
  if (!fs.existsSync(queuePath)) {
    return {
      ready: [],
      inProgress: [],
      blocked: [],
    };
  }

  const content = fs.readFileSync(queuePath, 'utf-8');
  const lines = content.split('\n');
  
  let currentSection = null;
  const sections = {
    ready: [],
    inProgress: [],
    blocked: [],
  };

  for (const line of lines) {
    const trimmed = line.trim();
    
    // 分区标题 - 更灵活的匹配
    if (trimmed.match(/^##\s+(🔥|🔴)?\s*(High Priority|Ready)/i)) {
      currentSection = 'ready';
      continue;
    }
    if (trimmed.match(/^##\s+(🟡|⏳)?\s*(Medium Priority|In Progress)/i)) {
      currentSection = 'inProgress';
      continue;
    }
    if (trimmed.match(/^##\s+(🔵|🚫)?\s*Blocked/i)) {
      currentSection = 'blocked';
      continue;
    }
    if (trimmed.match(/^##\s+(✅|✔️)?\s*Done/i)) {
      currentSection = null; // 忽略已完成任务
      continue;
    }
    if (trimmed.startsWith('##')) {
      // 未知分区 - 可能是子分区，保持当前分区不变
      continue;
    }

    // 解析任务行
    if (currentSection && trimmed.startsWith('-')) {
      const m = trimmed.match(/^-\s*\[([ x])\]\s*(.*)$/);
      if (!m) continue;

      const checked = m[1] === 'x';
      if (checked) continue; // 忽略已完成任务

      const taskText = m[2];
      const priority = detectPriority(taskText);

      sections[currentSection].push({
        text: taskText,
        priority,
        raw: line,
      });
    }
  }

  return sections;
}

function detectPriority(taskText) {
  const upper = taskText.toUpperCase();
  
  // 显式优先级标记
  if (upper.includes('[CRITICAL]') || upper.includes('🔥 CRITICAL') || upper.includes('URGENT:')) {
    return 'CRITICAL';
  }
  if (upper.includes('[HIGH]') || upper.includes('🔴 HIGH') || upper.includes('HIGH PRIORITY')) {
    return 'HIGH';
  }
  if (upper.includes('[MEDIUM]') || upper.includes('🟡 MEDIUM') || upper.includes('MEDIUM PRIORITY') || upper.includes('⭐') && upper.includes('MEDIUM')) {
    return 'MEDIUM';
  }
  if (upper.includes('[LOW]') || upper.includes('🟡 LOW') || upper.includes('LOW PRIORITY')) {
    return 'LOW';
  }

  // 基于上下文的检测
  if (upper.includes('FIX:') || upper.includes('BUG:') || upper.includes('BROKEN')) {
    return 'HIGH';
  }
  
  // 基于分区的检测（在"🔥 High Priority"标题下的任务）
  if (taskText.startsWith('**')) {
    return 'HIGH'; // 加粗的任务通常表示重要
  }

  // 默认：MEDIUM
  return 'MEDIUM';
}

function checkQueue(queuePath) {
  const sections = parseQueueFile(queuePath);
  
  // 只检查 Ready 任务（现在可以认领的任务）
  const readyTasks = sections.ready;
  
  const criticalTasks = readyTasks.filter(t => t.priority === 'CRITICAL');
  const highTasks = readyTasks.filter(t => t.priority === 'HIGH');
  const mediumTasks = readyTasks.filter(t => t.priority === 'MEDIUM');
  const lowTasks = readyTasks.filter(t => t.priority === 'LOW');

  const hasUrgentWork = criticalTasks.length > 0 || highTasks.length > 0;

  // 输出结果
  console.log(`${colors.bold}${colors.cyan}=== Queue Priority Check ===${colors.reset}\n`);
  
  if (criticalTasks.length > 0) {
    console.log(`${colors.red}${colors.bold}🔥 CRITICAL tasks: ${criticalTasks.length}${colors.reset}`);
    criticalTasks.forEach(t => console.log(`   ${colors.red}• ${t.text.substring(0, 80)}${colors.reset}`));
    console.log();
  }
  
  if (highTasks.length > 0) {
    console.log(`${colors.red}🔴 HIGH priority tasks: ${highTasks.length}${colors.reset}`);
    highTasks.forEach(t => console.log(`   ${colors.yellow}• ${t.text.substring(0, 80)}${colors.reset}`));
    console.log();
  }
  
  if (mediumTasks.length > 0) {
    console.log(`${colors.yellow}🟡 MEDIUM priority tasks: ${mediumTasks.length}${colors.reset}`);
  }
  
  if (lowTasks.length > 0) {
    console.log(`${colors.green}🟢 LOW priority tasks: ${lowTasks.length}${colors.reset}`);
  }

  if (readyTasks.length === 0) {
    console.log(`${colors.green}✅ Queue is empty - no ready tasks${colors.reset}`);
  }

  console.log();

  // 强制执行决策
  if (hasUrgentWork) {
    console.log(`${colors.red}${colors.bold}❌ CANNOT SKIP QUEUE${colors.reset}`);
    console.log(`${colors.red}You must spawn an agent for HIGH/CRITICAL tasks before doing other work.${colors.reset}`);
    console.log();
    
    // 显示最高优先级任务
    const topTask = criticalTasks.length > 0 ? criticalTasks[0] : highTasks[0];
    console.log(`${colors.bold}Top priority task:${colors.reset}`);
    console.log(`${colors.cyan}${topTask.text}${colors.reset}`);
    console.log();
    
    process.exit(1); // 退出码 1 = 必须处理队列
  } else {
    console.log(`${colors.green}${colors.bold}✅ Safe to continue${colors.reset}`);
    console.log(`${colors.green}No HIGH/CRITICAL tasks in queue. You can proceed with other work.${colors.reset}`);
    console.log();
    process.exit(0); // 退出码 0 = 队列已清空
  }
}

// 主执行
const workspaceRoot = process.cwd();
const queuePath = path.join(workspaceRoot, 'tasks/QUEUE.md');

checkQueue(queuePath);
