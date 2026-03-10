#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const TEMPLATES = {
  'session-state': `# SESSION-STATE.md — 活跃工作记忆

此文件是 Agent 的 "RAM" — 在压缩、重启、分心中存活。
聊天历史是缓冲区。此文件是存储。

## 当前任务
[无]

## 关键上下文
[暂无]

## 待处理操作
- [ ] 无

## 最近决策
[暂无]

---
*最后更新：${new Date().toISOString()}*
`,

  'memory-md': `# MEMORY.md — 长期记忆

## 关于用户
[添加用户偏好、沟通风格等]

## 项目
[活跃项目及其状态]

## 决策日志
[重要决策及其原因]

## 经验教训
[应避免的错误、有效的模式]

## 偏好
[用户偏好的工具、框架、工作流]

---
*精选记忆 — 从每日日志中提炼洞察*
`,

  'daily-template': `# {{DATE}} — 每日日志

## 已完成任务
- 

## 已做决策
- 

## 经验教训
- 

## 明日计划
- 
`
};

const commands = {
  init: () => {
    console.log('🧠 正在初始化精英长期记忆系统...\n');
    
    // 创建 SESSION-STATE.md
    if (!fs.existsSync('SESSION-STATE.md')) {
      fs.writeFileSync('SESSION-STATE.md', TEMPLATES['session-state']);
      console.log('✓ 已创建 SESSION-STATE.md（热内存）');
    } else {
      console.log('• SESSION-STATE.md 已存在');
    }
    
    // 创建 MEMORY.md
    if (!fs.existsSync('MEMORY.md')) {
      fs.writeFileSync('MEMORY.md', TEMPLATES['memory-md']);
      console.log('✓ 已创建 MEMORY.md（精选归档）');
    } else {
      console.log('• MEMORY.md 已存在');
    }
    
    // 创建 memory 目录
    if (!fs.existsSync('memory')) {
      fs.mkdirSync('memory', { recursive: true });
      console.log('✓ 已创建 memory/ 目录');
    } else {
      console.log('• memory/ 目录已存在');
    }
    
    // 创建今日日志
    const today = new Date().toISOString().split('T')[0];
    const todayFile = `memory/${today}.md`;
    if (!fs.existsSync(todayFile)) {
      const content = TEMPLATES['daily-template'].replace('{{DATE}}', today);
      fs.writeFileSync(todayFile, content);
      console.log(`✓ 已创建 ${todayFile}`);
    }
    
    console.log('\n🎉 精英长期记忆系统初始化完成！');
    console.log('\n下一步操作：');
    console.log('1. 将 SESSION-STATE.md 添加到你的 Agent 上下文');
    console.log('2. 在 clawdbot.json 中配置 LanceDB 插件');
    console.log('3. 查看 SKILL.md 获取完整设置指南');
  },
  
  today: () => {
    const today = new Date().toISOString().split('T')[0];
    const todayFile = `memory/${today}.md`;
    
    if (!fs.existsSync('memory')) {
      fs.mkdirSync('memory', { recursive: true });
    }
    
    if (!fs.existsSync(todayFile)) {
      const content = TEMPLATES['daily-template'].replace('{{DATE}}', today);
      fs.writeFileSync(todayFile, content);
      console.log(`✓ 已创建 ${todayFile}`);
    } else {
      console.log(`• ${todayFile} 已存在`);
    }
  },
  
  status: () => {
    console.log('🧠 精英长期记忆系统状态\n');
    
    // 检查 SESSION-STATE.md
    if (fs.existsSync('SESSION-STATE.md')) {
      const stat = fs.statSync('SESSION-STATE.md');
      console.log(`✓ SESSION-STATE.md (${(stat.size / 1024).toFixed(1)}KB, 修改于 ${stat.mtime.toLocaleString()})`);
    } else {
      console.log('✗ SESSION-STATE.md 缺失');
    }
    
    // 检查 MEMORY.md
    if (fs.existsSync('MEMORY.md')) {
      const stat = fs.statSync('MEMORY.md');
      const lines = fs.readFileSync('MEMORY.md', 'utf8').split('\n').length;
      console.log(`✓ MEMORY.md (${lines} 行, ${(stat.size / 1024).toFixed(1)}KB)`);
    } else {
      console.log('✗ MEMORY.md 缺失');
    }
    
    // 检查 memory 目录
    if (fs.existsSync('memory')) {
      const files = fs.readdirSync('memory').filter(f => f.endsWith('.md'));
      console.log(`✓ memory/ (${files.length} 个每日日志)`);
    } else {
      console.log('✗ memory/ 目录缺失');
    }
    
    // 检查 LanceDB
    const lancedbPath = path.join(process.env.HOME, '.clawdbot/memory/lancedb');
    if (fs.existsSync(lancedbPath)) {
      console.log('✓ LanceDB 向量已初始化');
    } else {
      console.log('• LanceDB 未初始化（可选）');
    }
  },
  
  help: () => {
    console.log(`
🧠 精英长期记忆系统 CLI

命令：
  init     在当前目录初始化记忆系统
  today    创建今日的每日日志文件
  status   检查记忆系统健康状态
  help     显示此帮助信息

用法：
  npx elite-longterm-memory init
  npx elite-longterm-memory status
`);
  }
};

const command = process.argv[2] || 'help';

if (commands[command]) {
  commands[command]();
} else {
  console.log(`未知命令：${command}`);
  commands.help();
}
