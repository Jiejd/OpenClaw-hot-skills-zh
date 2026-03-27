#!/usr/bin/env python3
"""
列出用户自选股列表中的所有股票。
此脚本从标准自选股文件中读取并显示当前自选股。
"""
import sys
import os

# 自选股文件路径
WATCHLIST_FILE = os.path.expanduser("~/.openclaw/stock_watcher/watchlist.txt")

def list_stocks():
    """列出自选股中的所有股票。"""
    if not os.path.exists(WATCHLIST_FILE):
        print("自选股列表为空。")
        return
    
    with open(WATCHLIST_FILE, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    if not lines:
        print("自选股列表为空。")
        return
    
    print("你的自选股列表：")
    print("-" * 40)
    for i, line in enumerate(lines, 1):
        parts = line.split('|')
        if len(parts) == 2:
            code, name = parts
            print(f"{i}. {code} - {name}")
        else:
            print(f"{i}. {line}")

if __name__ == "__main__":
    list_stocks()
