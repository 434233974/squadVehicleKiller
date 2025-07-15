#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动按键程序 - 功能演示
展示程序的所有功能特性
"""

import sys
import os

def print_demo():
    """打印功能演示"""
    print("=" * 60)
    print("🎯 自动按键程序 - 功能演示")
    print("=" * 60)
    
    print("\n📋 核心功能：")
    print("✅ 循环按键：反引号(`) → 向上键(↑) → 回车键(↵)")
    print("✅ 实时显示当前按键状态")
    print("✅ 按键计数统计")
    print("✅ 详细的按键历史记录")
    
    print("\n🎛️ 高级功能：")
    print("✅ 自定义按键序列配置")
    print("✅ 可调节按键延迟时间（0.1-5.0秒）")
    print("✅ 预设按键序列模板")
    print("✅ 安全机制开关")
    
    print("\n🔒 安全机制：")
    print("✅ ESC键快速停止")
    print("✅ 鼠标左上角失效保护")
    print("✅ 异常处理自动停止")
    print("✅ 可配置的安全选项")
    
    print("\n📦 使用方式：")
    print("1. 双击 start_with_dependencies.bat（推荐）")
    print("2. 直接运行 dist\\自动按键程序_GUI版.exe")
    print("3. 源码运行：python auto_key_presser_gui.py")
    
    print("\n🎨 界面功能：")
    print("✅ 开始/停止按钮")
    print("✅ 设置按钮（延迟、安全选项）")
    print("✅ 自定义按键按钮（序列配置）")
    print("✅ 清空历史按钮")
    print("✅ 实时状态显示")
    
    print("\n⚙️ 设置选项：")
    print("✅ 按键延迟时间调节")
    print("✅ 失效保护开关")
    print("✅ ESC键停止开关")
    
    print("\n🎯 自定义按键：")
    print("✅ 默认序列：反引号(`) → 向上键(↑) → 回车键(↵)")
    print("✅ 方向键序列：上(↑) → 下(↓) → 左(←) → 右(→)")
    print("✅ 数字键序列：1 → 2 → 3 → 4 → 5")
    print("✅ 自定义序列：支持任意按键组合")
    
    print("\n📝 使用提示：")
    print("⚠️  程序启动后有3秒准备时间")
    print("⚠️  请在此期间切换到目标应用程序窗口")
    print("⚠️  按ESC键或点击停止按钮可随时停止")
    print("⚠️  建议在测试环境中先行测试")
    
    print("\n" + "=" * 60)
    print("🚀 现在可以启动程序体验所有功能！")
    print("=" * 60)

def check_files():
    """检查必要文件是否存在"""
    print("\n📁 文件检查：")
    
    files = [
        ("auto_key_presser_gui.py", "主程序文件"),
        ("start_with_dependencies.bat", "智能启动脚本"),
        ("requirements.txt", "依赖包列表"),
        ("README.md", "使用说明文档"),
        ("dist/自动按键程序_GUI版.exe", "可执行文件")
    ]
    
    all_exist = True
    for file_path, description in files:
        if os.path.exists(file_path):
            print(f"✅ {description}: {file_path}")
        else:
            print(f"❌ {description}: {file_path} (缺失)")
            all_exist = False
    
    return all_exist

def main():
    """主函数"""
    print_demo()
    
    if check_files():
        print("\n🎉 所有文件检查通过！程序已准备就绪。")
    else:
        print("\n⚠️  部分文件缺失，请检查项目完整性。")
    
    print("\n💡 启动建议：")
    print("1. 首次使用：双击 start_with_dependencies.bat")
    print("2. 日常使用：双击 dist\\自动按键程序_GUI版.exe")
    print("3. 开发调试：python auto_key_presser_gui.py")

if __name__ == "__main__":
    main() 