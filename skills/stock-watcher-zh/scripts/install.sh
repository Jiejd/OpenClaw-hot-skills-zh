#!/bin/bash
# 安装自选股管理技能的依赖并初始化目录

set -e

echo "正在安装自选股管理技能..."

# 创建自选股目录
mkdir -p ~/.openclaw/stock_watcher

# 如果自选股文件不存在则创建空文件
WATCHLIST_FILE="$HOME/.openclaw/stock_watcher/watchlist.txt"
if [ ! -f "$WATCHLIST_FILE" ]; then
    touch "$WATCHLIST_FILE"
    echo "已创建空自选股文件: $WATCHLIST_FILE"
fi

# 检查 Python 依赖是否可用
if ! python3 -c "import requests, bs4" 2>/dev/null; then
    echo "警告：缺少必需的 Python 包（requests、beautifulsoup4）。"
    echo "请运行以下命令安装: pip install requests beautifulsoup4"
fi

echo "自选股管理技能安装成功！"
echo "自选股目录: ~/.openclaw/stock_watcher/"
echo "自选股文件: ~/.openclaw/stock_watcher/watchlist.txt"
