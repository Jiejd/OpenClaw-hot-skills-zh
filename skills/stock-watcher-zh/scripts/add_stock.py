#!/usr/bin/env python3
"""
添加股票到自选股
用法: python3 add_stock.py <股票代码> [股票名称]
"""
import sys
import os
import requests
from bs4 import BeautifulSoup
from config import WATCHLIST_FILE

def get_stock_name_from_code(stock_code):
    """通过同花顺获取股票名称"""
    try:
        url = f"https://stockpage.10jqka.com.cn/{stock_code}/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.find('title')
            if title:
                title_text = title.get_text()
                if '(' in title_text and ')' in title_text:
                    stock_name = title_text.split('(')[0].strip()
                    return stock_name
    except Exception as e:
        pass
    return None

def add_stock(stock_code, stock_name=None):
    """添加股票到自选股文件"""
    # 确保目录存在
    os.makedirs(os.path.dirname(WATCHLIST_FILE), exist_ok=True)
    
    # 如果没有提供股票名称，则从网上获取
    if not stock_name:
        stock_name = get_stock_name_from_code(stock_code)
        if not stock_name:
            stock_name = stock_code  # 获取失败时使用代码作为名称
    
    # 读取现有自选股
    existing_stocks = []
    if os.path.exists(WATCHLIST_FILE):
        with open(WATCHLIST_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    existing_stocks.append(line)
    
    # 检查股票是否已存在
    stock_entry = f"{stock_code}|{stock_name}"
    stock_exists = False
    for existing in existing_stocks:
        if existing.startswith(f"{stock_code}|"):
            stock_exists = True
            break
    
    if stock_exists:
        print(f"股票 {stock_code} 已在自选股中")
        return False
    
    # 添加新股票
    existing_stocks.append(stock_entry)
    
    # 写回文件
    with open(WATCHLIST_FILE, 'w', encoding='utf-8') as f:
        for stock in existing_stocks:
            f.write(stock + '\n')
    
    print(f"已添加股票 {stock_code}（{stock_name}）到自选股")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 add_stock.py <股票代码> [股票名称]")
        sys.exit(1)
    
    stock_code = sys.argv[1]
    stock_name = sys.argv[2] if len(sys.argv) > 2 else None
    add_stock(stock_code, stock_name)
