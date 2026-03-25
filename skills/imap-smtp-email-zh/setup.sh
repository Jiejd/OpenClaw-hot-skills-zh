#!/bin/bash

# IMAP/SMTP 邮件技能配置助手

CONFIG_DIR="$HOME/.config/imap-smtp-email"
CONFIG_FILE="$CONFIG_DIR/.env"

echo "================================"
echo "  IMAP/SMTP 邮件技能配置"
echo "================================"
echo ""

# 确定配置模式
SETUP_MODE="default"
ACCOUNT_PREFIX=""
ACCOUNT_NAME=""

if [ -f "$CONFIG_FILE" ]; then
  echo "已找到现有配置文件：$CONFIG_FILE"
  echo ""
  echo "请选择操作："
  echo "  1) 重新配置默认账号"
  echo "  2) 添加新账号"
  echo ""
  read -p "请输入选项 (1-2): " SETUP_CHOICE

  case $SETUP_CHOICE in
    1)
      SETUP_MODE="reconfigure"
      ;;
    2)
      SETUP_MODE="add"
      while true; do
        read -p "账号名称（仅限字母和数字，如 work）: " ACCOUNT_NAME
        if [[ "$ACCOUNT_NAME" =~ ^[a-zA-Z0-9]+$ ]]; then
          ACCOUNT_PREFIX="$(echo "$ACCOUNT_NAME" | tr '[:lower:]' '[:upper:]')_"
          # 检查账号是否已存在
          if grep -q "^${ACCOUNT_PREFIX}IMAP_HOST=" "$CONFIG_FILE" 2>/dev/null; then
            read -p "账号 \"$ACCOUNT_NAME\" 已存在，是否覆盖？(y/n): " OVERWRITE
            if [ "$OVERWRITE" != "y" ]; then
              echo "已取消。"
              exit 0
            fi
            SETUP_MODE="overwrite"
          fi
          break
        else
          echo "名称无效，请仅使用字母和数字。"
        fi
      done
      ;;
    *)
      echo "无效选项"
      exit 1
      ;;
  esac
fi

echo ""
echo "本脚本将帮助您配置邮箱凭据。"
echo ""

# 选择邮箱服务商
echo "请选择邮箱服务商："
echo "  1) Gmail"
echo "  2) Outlook"
echo "  3) 163.com"
echo "  4) vip.163.com"
echo "  5) 126.com"
echo "  6) vip.126.com"
echo "  7) 188.com"
echo "  8) vip.188.com"
echo "  9) yeah.net"
echo " 10) QQ 邮箱"
echo " 11) 自定义"
echo ""
read -p "请输入选项 (1-11): " PROVIDER_CHOICE

case $PROVIDER_CHOICE in
  1)
    IMAP_HOST="imap.gmail.com"
    IMAP_PORT="993"
    SMTP_HOST="smtp.gmail.com"
    SMTP_PORT="587"
    SMTP_SECURE="false"
    IMAP_TLS="true"
    echo ""
    echo "⚠️  Gmail 需要使用应用专用密码——您的普通 Google 密码将无法使用。"
    echo "   1. 前往：https://myaccount.google.com/apppasswords"
    echo "   2. 生成应用专用密码（需要已开启两步验证）"
    echo "   3. 在下方输入生成的 16 位密码"
    echo ""
    ;;
  2)
    IMAP_HOST="outlook.office365.com"
    IMAP_PORT="993"
    SMTP_HOST="smtp.office365.com"
    SMTP_PORT="587"
    SMTP_SECURE="false"
    IMAP_TLS="true"
    ;;
  3)
    IMAP_HOST="imap.163.com"
    IMAP_PORT="993"
    SMTP_HOST="smtp.163.com"
    SMTP_PORT="465"
    SMTP_SECURE="true"
    IMAP_TLS="true"
    ;;
  4)
    IMAP_HOST="imap.vip.163.com"
    IMAP_PORT="993"
    SMTP_HOST="smtp.vip.163.com"
    SMTP_PORT="465"
    SMTP_SECURE="true"
    IMAP_TLS="true"
    ;;
  5)
    IMAP_HOST="imap.126.com"
    IMAP_PORT="993"
    SMTP_HOST="smtp.126.com"
    SMTP_PORT="465"
    SMTP_SECURE="true"
    IMAP_TLS="true"
    ;;
  6)
    IMAP_HOST="imap.vip.126.com"
    IMAP_PORT="993"
    SMTP_HOST="smtp.vip.126.com"
    SMTP_PORT="465"
    SMTP_SECURE="true"
    IMAP_TLS="true"
    ;;
  7)
    IMAP_HOST="imap.188.com"
    IMAP_PORT="993"
    SMTP_HOST="smtp.188.com"
    SMTP_PORT="465"
    SMTP_SECURE="true"
    IMAP_TLS="true"
    ;;
  8)
    IMAP_HOST="imap.vip.188.com"
    IMAP_PORT="993"
    SMTP_HOST="smtp.vip.188.com"
    SMTP_PORT="465"
    SMTP_SECURE="true"
    IMAP_TLS="true"
    ;;
  9)
    IMAP_HOST="imap.yeah.net"
    IMAP_PORT="993"
    SMTP_HOST="smtp.yeah.net"
    SMTP_PORT="465"
    SMTP_SECURE="true"
    IMAP_TLS="true"
    ;;
  10)
    IMAP_HOST="imap.qq.com"
    IMAP_PORT="993"
    SMTP_HOST="smtp.qq.com"
    SMTP_PORT="587"
    SMTP_SECURE="false"
    IMAP_TLS="true"
    ;;
  11)
    read -p "IMAP 主机: " IMAP_HOST
    read -p "IMAP 端口: " IMAP_PORT
    read -p "SMTP 主机: " SMTP_HOST
    read -p "SMTP 端口: " SMTP_PORT
    read -p "IMAP 是否使用 TLS？(true/false): " IMAP_TLS
    read -p "SMTP 是否使用 SSL？(true/false): " SMTP_SECURE
    ;;
  *)
    echo "无效选项"
    exit 1
    ;;
esac

echo ""
read -p "邮箱地址: " EMAIL
read -s -p "密码 / 应用专用密码 / 授权码: " PASSWORD
echo ""
read -p "是否接受自签名证书？(y/n): " ACCEPT_CERT
if [ "$ACCEPT_CERT" = "y" ]; then
  REJECT_UNAUTHORIZED="false"
else
  REJECT_UNAUTHORIZED="true"
fi

# 仅在首次配置或重新配置时询问共享设置
ASK_SHARED=false
if [ "$SETUP_MODE" = "default" ] || [ "$SETUP_MODE" = "reconfigure" ]; then
  ASK_SHARED=true
fi

if [ "$ASK_SHARED" = true ]; then
  read -p "允许读取文件的目录（逗号分隔，如 ~/Downloads,~/Documents）: " ALLOWED_READ_DIRS
  read -p "允许保存附件的目录（逗号分隔，如 ~/Downloads）: " ALLOWED_WRITE_DIRS
fi

# 创建配置目录
mkdir -p -m 700 "$CONFIG_DIR"

# 构建账号变量块
ACCOUNT_VARS="# ${ACCOUNT_NAME:-默认} 账号
${ACCOUNT_PREFIX}IMAP_HOST=$IMAP_HOST
${ACCOUNT_PREFIX}IMAP_PORT=$IMAP_PORT
${ACCOUNT_PREFIX}IMAP_USER=$EMAIL
${ACCOUNT_PREFIX}IMAP_PASS=$PASSWORD
${ACCOUNT_PREFIX}IMAP_TLS=$IMAP_TLS
${ACCOUNT_PREFIX}IMAP_REJECT_UNAUTHORIZED=$REJECT_UNAUTHORIZED
${ACCOUNT_PREFIX}IMAP_MAILBOX=INBOX
${ACCOUNT_PREFIX}SMTP_HOST=$SMTP_HOST
${ACCOUNT_PREFIX}SMTP_PORT=$SMTP_PORT
${ACCOUNT_PREFIX}SMTP_SECURE=$SMTP_SECURE
${ACCOUNT_PREFIX}SMTP_USER=$EMAIL
${ACCOUNT_PREFIX}SMTP_PASS=$PASSWORD
${ACCOUNT_PREFIX}SMTP_FROM=$EMAIL
${ACCOUNT_PREFIX}SMTP_REJECT_UNAUTHORIZED=$REJECT_UNAUTHORIZED"

case $SETUP_MODE in
  "default")
    # 首次配置：写入完整文件
    cat > "$CONFIG_FILE" << EOF
$ACCOUNT_VARS

# 文件访问白名单（安全限制）
ALLOWED_READ_DIRS=${ALLOWED_READ_DIRS:-$HOME/Downloads,$HOME/Documents}
ALLOWED_WRITE_DIRS=${ALLOWED_WRITE_DIRS:-$HOME/Downloads}
EOF
    ;;
  "reconfigure")
    # 仅保留命名账号行（模式：NAME_IMAP_* 或 NAME_SMTP_*）
    TEMP_FILE=$(mktemp)
    grep -E '^[A-Z0-9]+_(IMAP_|SMTP_)' "$CONFIG_FILE" > "$TEMP_FILE.named" 2>/dev/null || true

    cat > "$TEMP_FILE" << EOF
$ACCOUNT_VARS

# 文件访问白名单（安全限制）
ALLOWED_READ_DIRS=${ALLOWED_READ_DIRS:-$HOME/Downloads,$HOME/Documents}
ALLOWED_WRITE_DIRS=${ALLOWED_WRITE_DIRS:-$HOME/Downloads}
EOF

    # 如果有命名账号行则追加
    if [ -s "$TEMP_FILE.named" ]; then
      echo "" >> "$TEMP_FILE"
      echo "# 命名账号" >> "$TEMP_FILE"
      cat "$TEMP_FILE.named" >> "$TEMP_FILE"
    fi
    mv "$TEMP_FILE" "$CONFIG_FILE"
    rm -f "$TEMP_FILE.named"
    ;;
  "add")
    # 追加命名账号到现有文件
    echo "" >> "$CONFIG_FILE"
    echo "$ACCOUNT_VARS" >> "$CONFIG_FILE"
    ;;
  "overwrite")
    # 移除该账号前缀的现有行，然后追加新行
    TEMP_FILE=$(mktemp)
    grep -v "^${ACCOUNT_PREFIX}\(IMAP_\|SMTP_\)" "$CONFIG_FILE" | grep -vi "^# ${ACCOUNT_NAME} account" > "$TEMP_FILE" 2>/dev/null || true
    # 移除末尾空行
    content=$(cat "$TEMP_FILE") && printf '%s\n' "$content" > "$TEMP_FILE"
    echo "" >> "$TEMP_FILE"
    echo "$ACCOUNT_VARS" >> "$TEMP_FILE"
    mv "$TEMP_FILE" "$CONFIG_FILE"
    ;;
esac

echo ""
echo "✅ 配置已保存到 $CONFIG_FILE"
chmod 600 "$CONFIG_FILE"
echo "✅ 文件权限已设置为 600（仅所有者可读写）"
echo ""
echo "正在测试连接..."
echo ""

# 构建测试命令的账号参数
ACCOUNT_FLAG=""
if [ -n "$ACCOUNT_NAME" ]; then
  ACCOUNT_FLAG="--account $ACCOUNT_NAME"
fi

# 测试 IMAP 连接
echo "正在测试 IMAP..."
if node scripts/imap.js $ACCOUNT_FLAG list-mailboxes >/dev/null 2>&1; then
    echo "✅ IMAP 连接成功！"
else
    echo "❌ IMAP 连接测试失败"
    echo "   请检查您的凭据和设置"
fi

# 测试 SMTP 连接
echo ""
echo "正在测试 SMTP..."
echo "  （将向您的邮箱 $EMAIL 发送一封测试邮件）"
if node scripts/smtp.js $ACCOUNT_FLAG test >/dev/null 2>&1; then
    echo "✅ SMTP 连接成功！"
else
    echo "❌ SMTP 连接测试失败"
    echo "   请检查您的凭据和设置"
fi

echo ""
echo "配置完成！试试以下命令："
if [ -n "$ACCOUNT_NAME" ]; then
  echo "  node scripts/imap.js --account $ACCOUNT_NAME check"
  echo "  node scripts/smtp.js --account $ACCOUNT_NAME send --to recipient@example.com --subject 测试 --body '你好世界'"
else
  echo "  node scripts/imap.js check"
  echo "  node scripts/smtp.js send --to recipient@example.com --subject 测试 --body '你好世界'"
fi
