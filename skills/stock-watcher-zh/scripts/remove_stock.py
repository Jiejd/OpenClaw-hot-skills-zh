#!/usr/bin/env python3
"""
从自选股中删除股票
用法: python3 remove_stock.py <股票代码>
"""
import sys
import os

# 自选股文件路径
WATCHLIST_DIR = os.path.expanduser("~/.openclaw/stock_watcher")
WATCHLIST_FILE = os.path.join(WATCHLIST_DIR, "watchlist.txt")

def remove_stock(stock_code):
    """从自选股中删除指定股票。"""
    if not os.path.exists(WATCHLIST_FILE):
        print("自选股列表为空。")
        return False
    
    # 读取现有自选股
    existing_stocks = []
    with open(WATCHLIST_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                existing_stocks.append(line)
    
    # 查找并删除股票
    stock_found = False
    updated_stocks = []
    for stock in existing_stocks:
        if stock.startswith(f"{stock_code}|"):
            stock_found = True
        else:
            updated_stocks.append(stock)
    
    if not stock_found:
        print(f"未在自选股中找到股票 {stock_code}")
        return False
    
    # 写回文件
    with open(WATCHLIST_FILE, 'w', encoding='utf-8') as f:
        for stock in updated_stocks:
            f.write(stock + '\n')
    
    print(f"已从自选股中删除股票 {stock_code}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 remove_stock.py <股票代码>")
        sys.exit(1)
    
    stock_code = sys.argv[1]
    remove_stock(stock_code)
