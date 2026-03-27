#!/bin/bash
# 卸载自选股管理技能

set -e

# 删除自选股目录和文件
WATCHLIST_DIR="$HOME/.openclaw/stock_watcher"
if [ -d "$WATCHLIST_DIR" ]; then
    rm -rf "$WATCHLIST_DIR"
    echo "已删除自选股目录: $WATCHLIST_DIR"
fi

echo "自选股管理技能已卸载。"
