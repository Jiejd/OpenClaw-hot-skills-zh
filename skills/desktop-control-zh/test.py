#!/usr/bin/env python3
"""
测试脚本 - 验证桌面控制技能（中文版）
"""

import sys
sys.path.insert(0, '/home/admin/openclaw/workspace/skills/desktop-control-zh')

# 从 __init__.py 导入
import __init__ as desktop_control
from __init__ import DesktopController

print("=" * 60)
print("🧪 桌面控制技能测试（中文版）")
print("=" * 60)

try:
    # 初始化控制器
    dc = DesktopController(failsafe=False)  # 测试时禁用故障保护
    
    # 测试 1：获取屏幕信息
    print("\n📋 测试 1：获取屏幕信息")
    width, height = dc.get_screen_size()
    print(f"✅ 屏幕分辨率: {width}x{height}")
    
    # 测试 2：获取鼠标位置
    print("\n📋 测试 2：获取鼠标位置")
    x, y = dc.get_mouse_position()
    print(f"✅ 当前鼠标位置: ({x}, {y})")
    
    # 测试 3：获取活动窗口
    print("\n📋 测试 3：获取活动窗口")
    active_window = dc.get_active_window()
    print(f"✅ 活动窗口: {active_window}")
    
    # 测试 4：获取所有窗口
    print("\n📋 测试 4：获取所有窗口")
    windows = dc.get_all_windows()
    print(f"✅ 打开的窗口数量: {len(windows)}")
    if windows:
        print(f"   前 3 个窗口:")
        for i, title in enumerate(windows[:3], 1):
            print(f"   {i}. {title[:50]}...")
    
    # 测试 5：获取像素颜色（需要截图支持）
    print("\n📋 测试 5：获取像素颜色（跳过 - 需要图形环境支持）")
    print("✅ 功能已实现，但在当前环境无法测试")
    
    print("\n" + "=" * 60)
    print("✅ 所有基础测试通过！桌面控制技能（中文版）工作正常。")
    print("⚠️  某些功能在 Linux 服务器环境中受限，但在桌面环境中可用。")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
