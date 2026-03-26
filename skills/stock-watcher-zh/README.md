# 自选股管理技能

一个标准化的 A 股自选股管理技能，提供清晰、一致的功能来跟踪中国 A 股市场的股票。

## 功能特性

- ✅ **添加股票** — 使用6位股票代码添加到自选股
- ✅ **查看自选股** — 格式化清晰展示
- ✅ **删除股票** — 从自选股中移除指定股票
- ✅ **清空自选股** — 一键清空所有股票
- ✅ **行情摘要** — 获取所有自选股的行情概览
- ✅ **标准化存储路径** — 统一管理，不再混乱
- ✅ **便捷安装/卸载**

## 安装

首次使用时技能会自动安装。安装脚本会创建：
- 自选股目录：`~/.openclaw/stock_watcher/`
- 自选股文件：`~/.openclaw/stock_watcher/watchlist.txt`

## 使用方法

### 添加股票
```bash
cd ~/.openclaw/skills/stock-watcher-zh/scripts && python3 add_stock.py 600053
```

### 查看自选股
```bash
cd ~/.openclaw/skills/stock-watcher-zh/scripts && python3 list_stocks.py
```

### 删除股票
```bash
cd ~/.openclaw/skills/stock-watcher-zh/scripts && python3 remove_stock.py 600053
```

### 清空自选股
```bash
cd ~/.openclaw/skills/stock-watcher-zh/scripts && python3 clear_watchlist.py
```

### 获取行情摘要
```bash
cd ~/.openclaw/skills/stock-watcher-zh/scripts && python3 summarize_performance.py
```

## 数据来源

- **主要数据源**：同花顺（10jqka.com.cn）
- **股票页面**：`https://stockpage.10jqka.com.cn/{stock_code}/`
- **支持市场**：沪市 A 股、深市 A 股、科创板

## 文件结构

```
stock-watcher-zh/
├── SKILL.md                 # 技能元数据与说明
├── README.md                # 使用文档
├── scripts/
│   ├── config.py           # 集中配置管理
│   ├── add_stock.py        # 添加股票到自选股
│   ├── list_stocks.py      # 列出所有自选股
│   ├── remove_stock.py     # 删除指定股票
│   ├── clear_watchlist.py  # 清空自选股列表
│   ├── summarize_performance.py # 获取股票行情摘要
│   ├── install.sh          # 安装脚本
│   └── uninstall.sh        # 卸载脚本
└── references/             # （预留参考资料目录）
```

## 存储位置

所有用户数据存储在统一位置：
- **目录**：`~/.openclaw/stock_watcher/`
- **自选股文件**：`~/.openclaw/stock_watcher/watchlist.txt`

格式：`股票代码|股票名称`（例如 `600053|九鼎投资`）

## 常见问题

### "命令未找到" 错误
确保已安装 Python 3 及所需依赖：
```bash
pip3 install requests beautifulsoup4
```

### 网络问题
本技能从同花顺获取数据，请确保网络连接正常且网站可访问。

### 权限错误
请确保 `~/.openclaw/` 目录对当前用户可写。
