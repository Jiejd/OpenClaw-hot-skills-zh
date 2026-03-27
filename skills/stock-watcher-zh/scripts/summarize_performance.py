#!/usr/bin/env python3
"""
获取自选股中所有股票的行情摘要。
此脚本从同花顺获取每只股票的当前数据，并提供近期表现摘要。
"""
import os
import sys
import requests
from bs4 import BeautifulSoup
import time

# 自选股文件路径
WATCHLIST_FILE = os.path.expanduser("~/.openclaw/stock_watcher/watchlist.txt")

def fetch_stock_data(stock_code):
    """从同花顺获取股票数据。"""
    url = f"https://stockpage.10jqka.com.cn/{stock_code}/"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            return None
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取基本信息
        title = soup.find('title')
        stock_name = ""
        if title:
            title_text = title.get_text()
            if '(' in title_text and ')' in title_text:
                stock_name = title_text.split('(')[0].strip()
        
        # 查找行情数据
        performance_data = {}
        
        # 尝试查找近期表现指标
        text_content = soup.get_text()
        
        if '涨跌幅' in text_content:
            import re
            percentages = re.findall(r'[-+]?\d+\.?\d*%', text_content)
            if percentages:
                performance_data['recent_changes'] = percentages[:3]
        
        return {
            'code': stock_code,
            'name': stock_name,
            'url': url,
            'performance': performance_data
        }
        
    except Exception as e:
        print(f"获取 {stock_code} 数据时出错: {e}", file=sys.stderr)
        return None

def summarize_performance():
    """汇总自选股中所有股票的行情。"""
    if not os.path.exists(WATCHLIST_FILE):
        return
    
    with open(WATCHLIST_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    if not lines or all(not line.strip() for line in lines):
        return
    
    # 直接输出行情摘要
    for line in lines:
        line = line.strip()
        if line:
            parts = line.split('|')
            if len(parts) == 2:
                code, name = parts
                
                # 获取数据
                stock_data = fetch_stock_data(code)
                if stock_data:
                    if stock_data['performance']:
                        for i, change in enumerate(stock_data['performance'].get('recent_changes', []), 1):
                            print(f"{code} - {name} - 指标{i}: {change}")
                    else:
                        print(f"{code} - {name} - 行情数据暂不可用")
                else:
                    print(f"{code} - {name} - 获取数据失败")
                
                # 控制请求频率
                time.sleep(1)

if __name__ == "__main__":
    summarize_performance()
