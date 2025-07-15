#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复按钮显示问题
"""

import tkinter as tk
from tkinter import messagebox

def fix_button_display():
    """修复按钮显示问题"""
    root = tk.Tk()
    root.title("自动按键程序 - 修复版")
    root.geometry("700x600")
    root.configure(bg='#f0f0f0')
    
    # 主容器
    main_container = tk.Frame(root, bg='#f0f0f0')
    main_container.pack(fill='both', expand=True, padx=10, pady=10)
    
    # 标题
    title_label = tk.Label(main_container, text="自动按键程序", 
                          font=("Arial", 18, "bold"), 
                          bg='#f0f0f0', fg='#333')
    title_label.pack(pady=10)
    
    # 副标题
    subtitle_label = tk.Label(main_container, text="循环按键：反引号(`) → 向上键(↑) → 回车键(↵)", 
                            font=("Arial", 11), 
                            bg='#f0f0f0', fg='#666')
    subtitle_label.pack(pady=5)
    
    # 状态显示
    status_frame = tk.LabelFrame(main_container, text="程序状态", 
                               font=("Arial", 12), 
                               bg='#f0f0f0', fg='#333')
    status_frame.pack(pady=5, fill='x')
    
    status_label = tk.Label(status_frame, text="状态: 未启动", 
                           font=("Arial", 11), 
                           bg='#f0f0f0', fg='#666')
    status_label.pack(pady=5)
    
    count_label = tk.Label(status_frame, text="按键次数: 0", 
                          font=("Arial", 11), 
                          bg='#f0f0f0', fg='#666')
    count_label.pack(pady=5)
    
    # 当前按键显示
    key_frame = tk.LabelFrame(main_container, text="当前按键", 
                            font=("Arial", 12), 
                            bg='#f0f0f0', fg='#333')
    key_frame.pack(pady=5, fill='x')
    
    current_key_label = tk.Label(key_frame, text="等待开始...", 
                               font=("Arial", 20, "bold"), 
                               bg='#f0f0f0', fg='#007acc',
                               height=2)
    current_key_label.pack(pady=10)
    
    # 历史记录（固定高度）
    history_frame = tk.LabelFrame(main_container, text="按键历史", 
                                font=("Arial", 12), 
                                bg='#f0f0f0', fg='#333')
    history_frame.pack(pady=5, fill='both', expand=True)
    
    # 固定历史记录高度
    history_frame.pack_propagate(False)
    history_frame.configure(height=120)
    
    history_text = tk.Text(history_frame, height=6, width=70, 
                          font=("Consolas", 10), 
                          bg='#fff', fg='#333')
    history_text.pack(fill='both', expand=True, padx=5, pady=5)
    
    # 按钮区域 - 确保显示在底部
    button_container = tk.Frame(main_container, bg='#f0f0f0', height=100)
    button_container.pack(side='bottom', fill='x', pady=10)
    button_container.pack_propagate(False)
    
    # 第一行按钮
    button_row1 = tk.Frame(button_container, bg='#f0f0f0')
    button_row1.pack(pady=5)
    
    def test_start():
        messagebox.showinfo("测试", "开始按钮被点击")
        status_label.config(text="状态: 运行中", fg='#4CAF50')
        current_key_label.config(text="测试中...")
        history_text.insert(tk.END, "[10:00:00] 程序启动\n")
    
    def test_settings():
        messagebox.showinfo("测试", "设置按钮被点击")
    
    def test_custom():
        messagebox.showinfo("测试", "自定义按键按钮被点击")
    
    def test_clear():
        history_text.delete(1.0, tk.END)
        messagebox.showinfo("测试", "历史记录已清空")
    
    # 开始按钮
    start_button = tk.Button(button_row1, text="开始", 
                           command=test_start,
                           font=("Arial", 12, "bold"),
                           bg='#4CAF50', fg='white',
                           width=12, height=2,
                           relief='raised', bd=2)
    start_button.pack(side='left', padx=8)
    
    # 设置按钮
    settings_button = tk.Button(button_row1, text="设置", 
                              command=test_settings,
                              font=("Arial", 12),
                              bg='#2196F3', fg='white',
                              width=12, height=2,
                              relief='raised', bd=2)
    settings_button.pack(side='left', padx=8)
    
    # 第二行按钮
    button_row2 = tk.Frame(button_container, bg='#f0f0f0')
    button_row2.pack(pady=5)
    
    # 自定义按键按钮
    custom_button = tk.Button(button_row2, text="自定义按键", 
                            command=test_custom,
                            font=("Arial", 12),
                            bg='#9C27B0', fg='white',
                            width=12, height=2,
                            relief='raised', bd=2)
    custom_button.pack(side='left', padx=8)
    
    # 清空历史按钮
    clear_button = tk.Button(button_row2, text="清空历史", 
                           command=test_clear,
                           font=("Arial", 12),
                           bg='#ff9800', fg='white',
                           width=12, height=2,
                           relief='raised', bd=2)
    clear_button.pack(side='left', padx=8)
    
    # 提示信息
    tip_frame = tk.Frame(main_container, bg='#f0f0f0')
    tip_frame.pack(side='bottom', pady=5)
    
    tip_label1 = tk.Label(tip_frame, text="💡 提示：按 ESC 键可随时停止程序", 
                         font=("Arial", 10), 
                         bg='#f0f0f0', fg='#666')
    tip_label1.pack()
    
    tip_label2 = tk.Label(tip_frame, text="⚠️  注意：程序启动后有3秒准备时间，请切换到目标窗口", 
                         font=("Arial", 10), 
                         bg='#f0f0f0', fg='#ff6b35')
    tip_label2.pack()
    
    print("✅ 修复版本已启动")
    print("按钮应该显示在窗口底部")
    
    root.mainloop()

if __name__ == "__main__":
    fix_button_display() 