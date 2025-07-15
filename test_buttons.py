#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
按钮测试脚本
验证按钮是否正确显示
"""

import tkinter as tk
from tkinter import messagebox

def test_buttons():
    """测试按钮显示"""
    root = tk.Tk()
    root.title("按钮测试")
    root.geometry("400x300")
    root.configure(bg='#f0f0f0')
    
    # 标题
    title_label = tk.Label(root, text="按钮显示测试", 
                          font=("Arial", 16, "bold"), 
                          bg='#f0f0f0', fg='#333')
    title_label.pack(pady=20)
    
    # 按钮框架
    button_frame = tk.Frame(root, bg='#f0f0f0')
    button_frame.pack(pady=20)
    
    # 第一行按钮
    button_row1 = tk.Frame(button_frame, bg='#f0f0f0')
    button_row1.pack(pady=5)
    
    # 测试按钮1
    btn1 = tk.Button(button_row1, text="开始", 
                    command=lambda: messagebox.showinfo("测试", "开始按钮点击"),
                    font=("Arial", 12, "bold"),
                    bg='#4CAF50', fg='white',
                    width=12, height=2,
                    relief='raised', bd=2)
    btn1.pack(side='left', padx=8)
    
    # 测试按钮2
    btn2 = tk.Button(button_row1, text="设置", 
                    command=lambda: messagebox.showinfo("测试", "设置按钮点击"),
                    font=("Arial", 12),
                    bg='#2196F3', fg='white',
                    width=12, height=2,
                    relief='raised', bd=2)
    btn2.pack(side='left', padx=8)
    
    # 第二行按钮
    button_row2 = tk.Frame(button_frame, bg='#f0f0f0')
    button_row2.pack(pady=5)
    
    # 测试按钮3
    btn3 = tk.Button(button_row2, text="自定义按键", 
                    command=lambda: messagebox.showinfo("测试", "自定义按键按钮点击"),
                    font=("Arial", 12),
                    bg='#9C27B0', fg='white',
                    width=12, height=2,
                    relief='raised', bd=2)
    btn3.pack(side='left', padx=8)
    
    # 测试按钮4
    btn4 = tk.Button(button_row2, text="清空历史", 
                    command=lambda: messagebox.showinfo("测试", "清空历史按钮点击"),
                    font=("Arial", 12),
                    bg='#ff9800', fg='white',
                    width=12, height=2,
                    relief='raised', bd=2)
    btn4.pack(side='left', padx=8)
    
    # 关闭按钮
    close_btn = tk.Button(root, text="关闭测试", 
                         command=root.destroy,
                         font=("Arial", 12),
                         bg='#f44336', fg='white',
                         width=15, height=2)
    close_btn.pack(pady=20)
    
    print("✅ 按钮测试窗口已打开")
    print("请检查按钮是否正确显示")
    
    root.mainloop()

if __name__ == "__main__":
    test_buttons() 