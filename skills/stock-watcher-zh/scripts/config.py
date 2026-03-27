#!/usr/bin/env python3
"""
自选股管理配置文件。
集中管理路径配置，避免路径混乱。
"""
import os

# 自选股文件路径
WATCHLIST_DIR = os.path.expanduser("~/.openclaw/stock_watcher")
WATCHLIST_FILE = os.path.join(WATCHLIST_DIR, "watchlist.txt")

# 确保目录存在
os.makedirs(WATCHLIST_DIR, exist_ok=True)
