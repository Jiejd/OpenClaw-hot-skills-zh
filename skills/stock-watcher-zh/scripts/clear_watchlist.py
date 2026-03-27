#!/usr/bin/env python3
"""
清空整个自选股列表。
此脚本将删除自选股文件中的所有股票。
"""
import os
import sys

# 自选股文件路径
WATCHLIST_FILE = os.path.expanduser("~/.openclaw/stock_watcher/watchlist.txt")

def clear_watchlist():
    """清空整个自选股列表。"""
    # 确保目录存在
    os.makedirs(os.path.dirname(WATCHLIST_FILE), exist_ok=True)
    
    # 清空文件
    with open(WATCHLIST_FILE, 'w', encoding='utf-8') as f:
        pass
    
    print("自选股列表已清空。")

if __name__ == "__main__":
    clear_watchlist()
