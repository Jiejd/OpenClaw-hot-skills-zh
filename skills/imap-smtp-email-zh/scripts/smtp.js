#!/usr/bin/env node

/**
 * SMTP 邮件命令行工具
 * 通过 SMTP 协议发送邮件。兼容 Gmail、Outlook、163.com 及任何标准 SMTP 服务器。
 * 支持附件、HTML 内容和多收件人。
 */

const nodemailer = require('nodemailer');
const path = require('path');
const os = require('os');
const fs = require('fs');
const config = require('./config');

function validateReadPath(inputPath) {
  let realPath;
  try {
    realPath = fs.realpathSync(inputPath);
  } catch {
    realPath = path.resolve(inputPath);
  }

  if (!config.allowedReadDirs.length) {
    throw new Error('未在 .env 中设置 ALLOWED_READ_DIRS，文件读取功能已禁用。');
  }

  const allowedDirs = config.allowedReadDirs.map(d =>
    path.resolve(d.replace(/^~/, os.homedir()))
  );

  const allowed = allowedDirs.some(dir =>
    realPath === dir || realPath.startsWith(dir + path.sep)
  );

  if (!allowed) {
    throw new Error(`访问被拒绝：'${inputPath}' 不在允许的读取目录范围内`);
  }

  return realPath;
}

// 解析命令行参数
function parseArgs() {
  const args = process.argv.slice(2);
  const command = args[0];
  const options = {};
  const positional = [];

  for (let i = 1; i < args.length; i++) {
    const arg = args[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      const value = args[i + 1];
      options[key] = value || true;
      if (value && !value.startsWith('--')) i++;
    } else {
      positional.push(arg);
    }
  }

  return { command, options, positional };
}

// 创建 SMTP 传输器
function createTransporter() {
  if (!config.smtp.host || !config.smtp.user || !config.smtp.pass) {
    throw new Error('缺少 SMTP 配置。请检查配置文件 ~/.config/imap-smtp-email/.env');
  }

  return nodemailer.createTransport({
    host: config.smtp.host,
    port: config.smtp.port,
    secure: config.smtp.secure,
    auth: {
      user: config.smtp.user,
      pass: config.smtp.pass,
    },
    tls: {
      rejectUnauthorized: config.smtp.rejectUnauthorized,
    },
  });
}

// 发送邮件
async function sendEmail(options) {
  const transporter = createTransporter();

  // 验证连接
  try {
    await transporter.verify();
    console.error('SMTP 服务器就绪，可以发送邮件');
  } catch (err) {
    throw new Error(`SMTP 连接失败：${err.message}`);
  }

  const mailOptions = {
    from: options.from || config.smtp.from,
    to: options.to,
    cc: options.cc || undefined,
    bcc: options.bcc || undefined,
    subject: options.subject || '(无主题)',
    text: options.text || undefined,
    html: options.html || undefined,
    attachments: options.attachments || [],
  };

  // 如果未提供 text 和 html，使用默认文本
  if (!mailOptions.text && !mailOptions.html) {
    mailOptions.text = options.body || '';
  }

  const info = await transporter.sendMail(mailOptions);

  return {
    success: true,
    messageId: info.messageId,
    response: info.response,
    to: mailOptions.to,
  };
}

// 读取附件文件内容
function readAttachment(filePath) {
  validateReadPath(filePath);
  if (!fs.existsSync(filePath)) {
    throw new Error(`未找到附件文件：${filePath}`);
  }
  return {
    filename: path.basename(filePath),
    path: path.resolve(filePath),
  };
}

// 发送带文件内容的邮件
async function sendEmailWithContent(options) {
  // 处理附件
  if (options.attach) {
    const attachFiles = options.attach.split(',').map(f => f.trim());
    options.attachments = attachFiles.map(f => readAttachment(f));
  }

  return await sendEmail(options);
}

// 测试 SMTP 连接
async function testConnection() {
  const transporter = createTransporter();

  try {
    await transporter.verify();
    const info = await transporter.sendMail({
      from: config.smtp.from || config.smtp.user,
      to: config.smtp.user,
      subject: 'SMTP 连接测试',
      text: '这是一封来自 IMAP/SMTP 邮件技能的测试邮件。',
      html: '<p>这是一封来自 IMAP/SMTP 邮件技能的<strong>测试邮件</strong>。</p>',
    });

    return {
      success: true,
      message: 'SMTP 连接成功',
      messageId: info.messageId,
    };
  } catch (err) {
    throw new Error(`SMTP 测试失败：${err.message}`);
  }
}

// 以表格形式显示账号列表
function displayAccounts(accounts, configPath) {
  // 处理无配置文件的情况
  if (!configPath) {
    console.error('未找到配置文件。');
    console.error('请运行 "bash setup.sh" 来配置您的邮箱账号。');
    process.exit(1);
  }

  // 处理无账号的情况
  if (accounts.length === 0) {
    console.error(`在 ${configPath} 中未配置任何账号`);
    process.exit(0);
  }

  // 显示标题和配置路径
  console.log(`已配置的账号（来自 ${configPath}）：\n`);

  // 计算列宽
  const maxNameLen = Math.max(6, ...accounts.map(a => a.name.length)); // 6 = '账号'.length
  const maxEmailLen = Math.max(5, ...accounts.map(a => a.email.length)); // 5 = '邮箱'.length
  const maxImapLen = Math.max(4, ...accounts.map(a => a.imapHost.length)); // 4 = 'IMAP'.length
  const maxSmtpLen = Math.max(4, ...accounts.map(a => a.smtpHost.length)); // 4 = 'SMTP'.length

  // 表头
  const header = `  ${padRight('账号', maxNameLen)}  ${padRight('邮箱', maxEmailLen)}  ${padRight('IMAP', maxImapLen)}  ${padRight('SMTP', maxSmtpLen)}  状态`;
  console.log(header);

  // 分隔线
  const separator = '  ' + '─'.repeat(maxNameLen) + '  ' + '─'.repeat(maxEmailLen) + '  ' + '─'.repeat(maxImapLen) + '  ' + '─'.repeat(maxSmtpLen) + '  ' + '────────────────';
  console.log(separator);

  // 表格行
  for (const account of accounts) {
    const statusIcon = account.isComplete ? '✓' : '⚠';
    const statusText = account.isComplete ? '完整' : '不完整';
    const row = `  ${padRight(account.name, maxNameLen)}  ${padRight(account.email, maxEmailLen)}  ${padRight(account.imapHost, maxImapLen)}  ${padRight(account.smtpHost, maxSmtpLen)}  ${statusIcon} ${statusText}`;
    console.log(row);
  }

  // 页脚
  console.log(`\n  共 ${accounts.length} 个账号`);
}

// 辅助函数：右填充字符串到指定宽度
function padRight(str, len) {
  return (str + ' '.repeat(len)).slice(0, len);
}

// 主命令行处理
async function main() {
  const { command, options, positional } = parseArgs();

  try {
    let result;

    switch (command) {
      case 'send':
        if (!options.to) {
          throw new Error('缺少必填参数：--to <邮箱>');
        }
        if (!options.subject && !options['subject-file']) {
          throw new Error('缺少必填参数：--subject <文本> 或 --subject-file <文件>');
        }

        // 从文件读取主题（如果指定）
        if (options['subject-file']) {
          validateReadPath(options['subject-file']);
          options.subject = fs.readFileSync(options['subject-file'], 'utf8').trim();
        }

        // 从文件读取正文（如果指定）
        if (options['body-file']) {
          validateReadPath(options['body-file']);
          const content = fs.readFileSync(options['body-file'], 'utf8');
          if (options['body-file'].endsWith('.html') || options.html) {
            options.html = content;
          } else {
            options.text = content;
          }
        } else if (options['html-file']) {
          validateReadPath(options['html-file']);
          options.html = fs.readFileSync(options['html-file'], 'utf8');
        } else if (options.body) {
          options.text = options.body;
        }

        result = await sendEmailWithContent(options);
        break;

      case 'test':
        result = await testConnection();
        break;

      case 'list-accounts':
        {
          const { listAccounts } = require('./config');
          const { accounts, configPath } = listAccounts();
          displayAccounts(accounts, configPath);
        }
        return;  // 提前退出，无 JSON 输出

      default:
        console.error('未知命令：', command);
        console.error('可用命令：send, test, list-accounts');
        console.error('\n用法：');
        console.error('  send   --to <邮箱> --subject <文本> [--body <文本>] [--html] [--cc <邮箱>] [--bcc <邮箱>] [--attach <文件>]');
        console.error('  send   --to <邮箱> --subject <文本> --body-file <文件> [--html-file <文件>] [--attach <文件>]');
        console.error('  test   测试 SMTP 连接');
        process.exit(1);
    }

    console.log(JSON.stringify(result, null, 2));
  } catch (err) {
    console.error('错误：', err.message);
    process.exit(1);
  }
}

main();
