#!/usr/bin/env node

/**
 * 脏仓库看门狗。
 *
 * 用法：
 *   node check-dirty-repos.js <路径> [路径2 ...]
 *
 * 退出码：
 *   0 = 全部干净
 *   1 = 至少一个仓库有未提交的更改（已修改/未跟踪）
 *   2 = 用法错误 / 仓库不存在
 */

const { spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const repos = process.argv.slice(2);
if (repos.length === 0) {
  console.error('用法：node check-dirty-repos.js <仓库路径> [仓库路径2 ...]');
  process.exit(2);
}

function isGitRepo(p) {
  try {
    return fs.existsSync(path.join(p, '.git'));
  } catch {
    return false;
  }
}

let dirty = [];
let missing = [];

for (const repoPath of repos) {
  const p = path.resolve(repoPath);
  if (!fs.existsSync(p) || !isGitRepo(p)) {
    missing.push(repoPath);
    continue;
  }

  const r = spawnSync('git', ['status', '--porcelain'], { cwd: p, encoding: 'utf8' });
  if (r.status !== 0) {
    missing.push(repoPath);
    continue;
  }

  const lines = (r.stdout || '').trim().split('\n').filter(Boolean);
  if (lines.length) dirty.push({ repoPath, count: lines.length });
}

if (missing.length) {
  console.error('[dirty-repos] 不存在或不是 git 仓库：', missing.join(', '));
  process.exit(2);
}

if (dirty.length) {
  console.log('[dirty-repos] 有未提交更改的仓库：');
  for (const d of dirty) console.log(`- ${d.repoPath}（${d.count} 项更改）`);
  process.exit(1);
}

console.log('[dirty-repos] 全部干净');
process.exit(0);
