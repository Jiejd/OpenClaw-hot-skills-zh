#!/usr/bin/env python3
"""Playwright MCP 服务器与 OpenClaw 配合使用的示例脚本。

此脚本演示如何通过编程方式与 Playwright MCP 服务器交互，
实现浏览器自动化。
"""

import subprocess
import json
import sys


def run_mcp_command(tool_name: str, params: dict) -> dict:
    """通过 playwright-mcp 运行单个 MCP 工具命令。
    
    注意：在 OpenClaw 的实际使用中，MCP 服务器会持续运行，
    工具通过 MCP 协议调用。此脚本展示概念流程。
    """
    # 构建 MCP 请求
    request = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": params
        },
        "id": 1
    }
    
    # 实际实现中，这会发送到运行中的 MCP 服务器
    # 这里仅打印将要执行的操作
    print(f"MCP 调用: {tool_name}")
    print(f"参数: {json.dumps(params, indent=2, ensure_ascii=False)}")
    return {"status": "示例", "tool": tool_name}


def example_navigate_and_click():
    """示例：导航到页面并点击按钮。"""
    print("=== 示例：导航并点击 ===\n")
    
    # 步骤 1：导航
    run_mcp_command("browser_navigate", {
        "url": "https://example.com",
        "waitUntil": "networkidle"
    })
    
    # 步骤 2：点击元素
    run_mcp_command("browser_click", {
        "selector": "button#submit",
        "timeout": 5000
    })
    
    # 步骤 3：获取文本验证
    run_mcp_command("browser_get_text", {
        "selector": ".result-message"
    })


def example_fill_form():
    """示例：填写并提交表单。"""
    print("\n=== 示例：填写表单 ===\n")
    
    steps = [
        ("browser_navigate", {"url": "https://example.com/login"}),
        ("browser_type", {"selector": "#username", "text": "myuser"}),
        ("browser_type", {"selector": "#password", "text": "mypass"}),
        ("browser_click", {"selector": "button[type=submit]"}),
    ]
    
    for tool, params in steps:
        run_mcp_command(tool, params)


def example_extract_data():
    """示例：使用 JavaScript 提取数据。"""
    print("\n=== 示例：提取数据 ===\n")
    
    run_mcp_command("browser_navigate", {
        "url": "https://example.com/products"
    })
    
    # 提取产品数据
    run_mcp_command("browser_evaluate", {
        "script": """
            () => {
                return Array.from(document.querySelectorAll('.product')).map(p => ({
                    name: p.querySelector('.name')?.textContent,
                    price: p.querySelector('.price')?.textContent
                }));
            }
        """
    })


def main():
    """运行示例。"""
    print("Playwright MCP 使用示例")
    print("=" * 50)
    print()
    print("注意：这些是概念示例，展示 MCP 工具调用方式。")
    print("实际使用中，OpenClaw 会管理 MCP 服务器的生命周期。")
    print()
    
    example_navigate_and_click()
    example_fill_form()
    example_extract_data()
    
    print("\n" + "=" * 50)
    print("实际使用时，请在 OpenClaw 配置中配置 MCP 服务器。")


if __name__ == "__main__":
    main()
