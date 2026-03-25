#!/usr/bin/env node

const path = require('path');
const os = require('os');
const fs = require('fs');
const dotenv = require('dotenv');

// 配置文件路径
const PRIMARY_ENV_PATH = path.join(os.homedir(), '.config', 'imap-smtp-email', '.env');
const FALLBACK_ENV_PATH = path.resolve(__dirname, '../.env');

// 查找 .env 文件：优先使用主路径，其次使用回退路径
function findEnvPath() {
  if (fs.existsSync(PRIMARY_ENV_PATH)) return PRIMARY_ENV_PATH;
  if (fs.existsSync(FALLBACK_ENV_PATH)) return FALLBACK_ENV_PATH;
  return null;
}

// 解析并移除 --account <名称> 参数
// 之后 process.argv[2] 始终是命令
function parseAccountFromArgv(argv) {
  const args = argv.slice(2);
  const idx = args.indexOf('--account');
  if (idx !== -1 && idx + 1 < args.length) {
    const name = args[idx + 1];
    args.splice(idx, 2);
    return { accountName: name, remainingArgs: args };
  }
  return { accountName: null, remainingArgs: args };
}

// 从环境变量构建配置对象
// prefix: 大写账号名（如 'WORK'）或 null 表示默认账号
function buildConfig(env, prefix) {
  const p = prefix ? `${prefix}_` : '';

  // 命名账号存在性检查
  if (prefix && !env[`${p}IMAP_HOST`]) {
    console.error(`错误：在配置中未找到账号 "${prefix.toLowerCase()}"。请检查 ~/.config/imap-smtp-email/.env`);
    process.exit(1);
  }

  return {
    imap: {
      host: env[`${p}IMAP_HOST`] || '127.0.0.1',
      port: parseInt(env[`${p}IMAP_PORT`]) || 1143,
      user: env[`${p}IMAP_USER`],
      pass: env[`${p}IMAP_PASS`],
      tls: env[`${p}IMAP_TLS`] === 'true',
      rejectUnauthorized: env[`${p}IMAP_REJECT_UNAUTHORIZED`] !== 'false',
      mailbox: env[`${p}IMAP_MAILBOX`] || 'INBOX',
    },
    smtp: {
      host: env[`${p}SMTP_HOST`],
      port: parseInt(env[`${p}SMTP_PORT`]) || 587,
      user: env[`${p}SMTP_USER`],
      pass: env[`${p}SMTP_PASS`],
      secure: env[`${p}SMTP_SECURE`] === 'true',
      from: env[`${p}SMTP_FROM`] || env[`${p}SMTP_USER`],
      rejectUnauthorized: env[`${p}SMTP_REJECT_UNAUTHORIZED`] !== 'false',
    },
    allowedReadDirs: (env.ALLOWED_READ_DIRS || '').split(',').map(d => d.trim()).filter(Boolean),
    allowedWriteDirs: (env.ALLOWED_WRITE_DIRS || '').split(',').map(d => d.trim()).filter(Boolean),
  };
}

// 从 .env 文件列出所有已配置的账号
// 返回 { accounts: Array, configPath: String|null }
function listAccounts() {
  const envPath = findEnvPath();
  if (!envPath) {
    return { accounts: [], configPath: null };
  }

  // 重新解析 env 文件以获取所有账号前缀
  const dotenvResult = dotenv.config({ path: envPath });
  const env = dotenvResult.parsed || {};
  const accounts = [];
  const seen = new Set();

  // 检查默认账号（无前缀）
  if (env.IMAP_HOST) {
    accounts.push(createAccountObject(env, '', 'default'));
    seen.add('default');
  }

  // 扫描命名账号（模式：XXX_IMAP_HOST）
  for (const key of Object.keys(env)) {
    const match = key.match(/^([A-Z0-9]+)_IMAP_HOST$/);
    if (match) {
      const prefix = match[1];
      const name = prefix.toLowerCase();
      if (!seen.has(name)) {
        accounts.push(createAccountObject(env, prefix + '_', name));
        seen.add(name);
      }
    }
  }

  return { accounts, configPath: envPath };
}

// 从环境变量创建账号对象
function createAccountObject(env, prefix, name) {
  const p = prefix;
  return {
    name,
    email: env[`${p}IMAP_USER`] || env[`${p}SMTP_FROM`] || '-',
    imapHost: env[`${p}IMAP_HOST`] || '-',
    smtpHost: env[`${p}SMTP_HOST`] || '-',
    isComplete: isAccountComplete(env, prefix)
  };
}

// 检查账号是否具有完整配置
function isAccountComplete(env, prefix) {
  const p = prefix;
  return !!(
    env[`${p}IMAP_HOST`] &&
    env[`${p}IMAP_USER`] &&
    env[`${p}IMAP_PASS`] &&
    env[`${p}SMTP_HOST`]
  );
}

// --- 模块初始化 ---
const envPath = findEnvPath();
if (envPath) {
  dotenv.config({ path: envPath });
}

const { accountName, remainingArgs } = parseAccountFromArgv(process.argv);
const prefix = accountName ? accountName.toUpperCase() : null;

// 从 process.argv 中移除 --account，使调用者在 argv[2] 处看到命令
process.argv = [process.argv[0], process.argv[1], ...remainingArgs];

const config = buildConfig(process.env, prefix);

module.exports = config;
module.exports.listAccounts = listAccounts;
