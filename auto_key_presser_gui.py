#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动按键程序 - 带界面版本
循环按下反引号（`）、向上键和回车键
显示当前按键状态
"""

import pyautogui
import time
import threading
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from pynput import keyboard
import datetime

class AutoKeyPresserGUI:
    def __init__(self):
        self.running = False
        self.key_thread = None
        self.delay = 500  # 按键之间的延迟时间（毫秒）
        self.press_count = 0
        
        # 默认按键序列配置
        self.key_sequence = [
            ('反引号 `', '`'),
            ('向上键 ↑', 'up'),
            ('回车键 ↵', 'enter')
        ]
        
        # 安全设置
        self.failsafe_enabled = True
        self.esc_stop_enabled = True
        
        # 创建主窗口
        self.root = tk.Tk()
        self.root.title("自动按键程序")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        
        # 设置窗口图标和样式
        self.root.configure(bg='#f0f0f0')
        
        # 创建界面元素
        self.create_widgets()
        
        # 设置PyAutoGUI的安全机制
        pyautogui.FAILSAFE = self.failsafe_enabled
        pyautogui.PAUSE = 0.1
        
        # 绑定窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # 键盘监听器
        self.keyboard_listener = None
        
    def create_widgets(self):
        """创建界面元素"""
        # 主容器
        main_container = tk.Frame(self.root, bg='#f0f0f0')
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # 标题
        title_label = tk.Label(main_container, text="自动按键程序", 
                              font=("Arial", 18, "bold"), 
                              bg='#f0f0f0', fg='#333')
        title_label.pack(pady=10)
        
        # 副标题
        subtitle_label = tk.Label(main_container, text="循环按键：反引号(`) → 向上键(↑) → 回车键(↵) | 默认间隔：500毫秒", 
                                font=("Arial", 11), 
                                bg='#f0f0f0', fg='#666')
        subtitle_label.pack(pady=5)
        
        # 状态框架
        status_frame = tk.LabelFrame(main_container, text="程序状态", 
                                   font=("Arial", 12), 
                                   bg='#f0f0f0', fg='#333')
        status_frame.pack(pady=5, fill='x')
        
        # 运行状态
        self.status_label = tk.Label(status_frame, text="状态: 未启动", 
                                   font=("Arial", 11), 
                                   bg='#f0f0f0', fg='#666')
        self.status_label.pack(pady=5)
        
        # 按键计数
        self.count_label = tk.Label(status_frame, text="按键次数: 0", 
                                  font=("Arial", 11), 
                                  bg='#f0f0f0', fg='#666')
        self.count_label.pack(pady=5)
        
        # 当前按键显示框架
        key_frame = tk.LabelFrame(main_container, text="当前按键", 
                                font=("Arial", 12), 
                                bg='#f0f0f0', fg='#333')
        key_frame.pack(pady=5, fill='x')
        
        # 当前按键显示
        self.current_key_label = tk.Label(key_frame, text="等待开始...", 
                                        font=("Arial", 24, "bold"), 
                                        bg='#f0f0f0', fg='#007acc',
                                        height=2)
        self.current_key_label.pack(pady=15)
        
        # 按键历史框架
        history_frame = tk.LabelFrame(main_container, text="按键历史", 
                                    font=("Arial", 12), 
                                    bg='#f0f0f0', fg='#333')
        history_frame.pack(pady=5, fill='both', expand=True)
        
        # 限制历史记录区域的高度，为按钮留出空间
        history_frame.pack_propagate(False)
        history_frame.configure(height=120)
        
        # 创建文本框和滚动条
        text_frame = tk.Frame(history_frame, bg='#f0f0f0')
        text_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.history_text = tk.Text(text_frame, height=10, width=70, 
                                  font=("Consolas", 10), 
                                  bg='#fff', fg='#333',
                                  wrap=tk.WORD)
        
        scrollbar = tk.Scrollbar(text_frame, orient='vertical', 
                               command=self.history_text.yview)
        self.history_text.configure(yscrollcommand=scrollbar.set)
        
        self.history_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # 控制按钮框架 - 确保按钮显示在底部
        button_container = tk.Frame(main_container, bg='#f0f0f0', height=100)
        button_container.pack(side='bottom', fill='x', pady=10)
        button_container.pack_propagate(False)
        
        button_frame = tk.Frame(button_container, bg='#f0f0f0')
        button_frame.pack(pady=5)
        
        # 第一行按钮
        button_row1 = tk.Frame(button_frame, bg='#f0f0f0')
        button_row1.pack(pady=5)
        
        # 开始/停止按钮
        self.start_button = tk.Button(button_row1, text="开始", 
                                    command=self.toggle_pressing,
                                    font=("Arial", 12, "bold"),
                                    bg='#4CAF50', fg='white',
                                    width=12, height=2,
                                    relief='raised', bd=2)
        self.start_button.pack(side='left', padx=8)
        
        # 设置按钮
        settings_button = tk.Button(button_row1, text="设置", 
                                  command=self.open_settings,
                                  font=("Arial", 12),
                                  bg='#2196F3', fg='white',
                                  width=12, height=2,
                                  relief='raised', bd=2)
        settings_button.pack(side='left', padx=8)
        
        # 第二行按钮
        button_row2 = tk.Frame(button_frame, bg='#f0f0f0')
        button_row2.pack(pady=5)
        
        # 自定义按键按钮
        custom_button = tk.Button(button_row2, text="自定义按键", 
                                command=self.open_custom_keys,
                                font=("Arial", 12),
                                bg='#9C27B0', fg='white',
                                width=12, height=2,
                                relief='raised', bd=2)
        custom_button.pack(side='left', padx=8)
        
        # 清空历史按钮
        clear_button = tk.Button(button_row2, text="清空历史", 
                               command=self.clear_history,
                               font=("Arial", 12),
                               bg='#ff9800', fg='white',
                               width=12, height=2,
                               relief='raised', bd=2)
        clear_button.pack(side='left', padx=8)
        
        # 提示信息框架 - 放在按钮下方
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
        
    def toggle_pressing(self):
        """开始/停止按键"""
        if not self.running:
            self.start_pressing()
        else:
            self.stop_pressing()
            
    def start_pressing(self):
        """开始按键循环"""
        self.running = True
        self.press_count = 0
        
        # 更新界面
        self.start_button.config(text="停止", bg='#f44336')
        self.status_label.config(text="状态: 运行中", fg='#4CAF50')
        self.current_key_label.config(text="准备中...")
        
        # 添加日志
        self.add_log("程序启动")
        
        # 启动按键线程
        self.key_thread = threading.Thread(target=self.press_keys_loop)
        self.key_thread.daemon = True
        self.key_thread.start()
        
        # 启动键盘监听
        self.start_keyboard_listener()
        
    def stop_pressing(self):
        """停止按键循环"""
        self.running = False
        
        # 停止键盘监听
        if self.keyboard_listener:
            self.keyboard_listener.stop()
            self.keyboard_listener = None
        
        # 更新界面
        self.start_button.config(text="开始", bg='#4CAF50')
        self.status_label.config(text="状态: 已停止", fg='#666')
        self.current_key_label.config(text="已停止")
        
        # 添加日志
        self.add_log("程序停止")
        
    def press_keys_loop(self):
        """按键循环的主要逻辑"""
        keys = self.key_sequence
        
        # 倒计时
        for i in range(3, 0, -1):
            if not self.running:
                return
            self.update_current_key(f"倒计时 {i}")
            time.sleep(1)
        
        while self.running:
            try:
                for key_name, key_code in keys:
                    if not self.running:
                        break
                    
                    # 更新显示
                    self.update_current_key(key_name)
                    
                    # 按键
                    pyautogui.press(key_code)
                    self.press_count += 1
                    
                    # 更新计数
                    self.root.after(0, self.update_count)
                    
                    # 添加日志
                    self.add_log(f"按键: {key_name}")
                    
                    # 延迟
                    time.sleep(self.delay / 1000.0)
                
                # 循环间隔
                time.sleep(self.delay / 1000.0)
                
            except Exception as e:
                self.add_log(f"错误: {e}")
                break
                
    def update_current_key(self, key_name):
        """更新当前按键显示"""
        self.root.after(0, lambda: self.current_key_label.config(text=key_name))
        
    def update_count(self):
        """更新按键计数显示"""
        self.count_label.config(text=f"按键次数: {self.press_count}")
        
    def add_log(self, message):
        """添加日志到历史记录"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        def update_text():
            self.history_text.insert(tk.END, log_message)
            self.history_text.see(tk.END)
            
        self.root.after(0, update_text)
        
    def clear_history(self):
        """清空历史记录"""
        self.history_text.delete(1.0, tk.END)
        
    def open_settings(self):
        """打开设置窗口"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("设置")
        settings_window.geometry("450x350")
        settings_window.resizable(False, False)
        settings_window.configure(bg='#f0f0f0')
        
        # 标题
        title_label = tk.Label(settings_window, text="程序设置", 
                              font=("Arial", 16, "bold"), 
                              bg='#f0f0f0', fg='#333')
        title_label.pack(pady=15)
        
        # 延迟设置
        delay_frame = tk.LabelFrame(settings_window, text="按键延迟设置", 
                                  font=("Arial", 12, "bold"), 
                                  bg='#f0f0f0', fg='#333')
        delay_frame.pack(pady=15, padx=20, fill='x')
        
        delay_inner_frame = tk.Frame(delay_frame, bg='#f0f0f0')
        delay_inner_frame.pack(pady=10, padx=10)
        
        tk.Label(delay_inner_frame, text="按键延迟 (毫秒):", 
                font=("Arial", 12), bg='#f0f0f0').pack(side='left')
        
        delay_var = tk.StringVar(value=str(self.delay))
        delay_entry = tk.Entry(delay_inner_frame, textvariable=delay_var, width=12, 
                             font=("Arial", 12))
        delay_entry.pack(side='left', padx=15)
        
        tk.Label(delay_inner_frame, text="(10 - 5000)", 
                font=("Arial", 10), bg='#f0f0f0', fg='#666').pack(side='left')
        
        # 安全设置
        safety_frame = tk.LabelFrame(settings_window, text="安全设置", 
                                   font=("Arial", 12, "bold"), 
                                   bg='#f0f0f0', fg='#333')
        safety_frame.pack(pady=15, padx=20, fill='x')
        
        safety_inner_frame = tk.Frame(safety_frame, bg='#f0f0f0')
        safety_inner_frame.pack(pady=10, padx=10)
        
        failsafe_var = tk.BooleanVar(value=self.failsafe_enabled)
        failsafe_check = tk.Checkbutton(safety_inner_frame, text="🔒 启用失效保护（鼠标左上角停止）", 
                                      variable=failsafe_var, bg='#f0f0f0', font=("Arial", 11))
        failsafe_check.pack(anchor='w', pady=5)
        
        esc_var = tk.BooleanVar(value=self.esc_stop_enabled)
        esc_check = tk.Checkbutton(safety_inner_frame, text="⌨️  启用ESC键停止", 
                                 variable=esc_var, bg='#f0f0f0', font=("Arial", 11))
        esc_check.pack(anchor='w', pady=5)
        
        def apply_settings():
            try:
                new_delay = int(delay_var.get())
                if 10 <= new_delay <= 5000:
                    self.delay = new_delay
                    self.failsafe_enabled = failsafe_var.get()
                    self.esc_stop_enabled = esc_var.get()
                    
                    # 更新PyAutoGUI设置
                    pyautogui.FAILSAFE = self.failsafe_enabled
                    
                    messagebox.showinfo("成功", f"设置已保存\n延迟时间：{new_delay}毫秒")
                    settings_window.destroy()
                else:
                    messagebox.showerror("错误", "延迟时间必须在10-5000毫秒之间")
            except ValueError:
                messagebox.showerror("错误", "请输入有效的整数")
        
        # 按钮框架
        button_frame = tk.Frame(settings_window, bg='#f0f0f0')
        button_frame.pack(pady=20)
        
        # 应用按钮
        apply_btn = tk.Button(button_frame, text="✅ 应用", command=apply_settings,
                             font=("Arial", 12, "bold"), bg='#4CAF50', fg='white',
                             width=15, height=2, relief='raised', bd=3,
                             activebackground='#45a049', activeforeground='white')
        apply_btn.pack(side='left', padx=15)
        
        # 取消按钮
        cancel_btn = tk.Button(button_frame, text="❌ 取消", command=settings_window.destroy,
                              font=("Arial", 12), bg='#f44336', fg='white',
                              width=15, height=2, relief='raised', bd=3,
                              activebackground='#da190b', activeforeground='white')
        cancel_btn.pack(side='left', padx=15)
        
    def open_custom_keys(self):
        """打开自定义按键窗口"""
        custom_window = tk.Toplevel(self.root)
        custom_window.title("自定义按键序列")
        custom_window.geometry("600x500")
        custom_window.resizable(False, False)
        custom_window.configure(bg='#f0f0f0')
        
        # 标题
        title_label = tk.Label(custom_window, text="自定义按键序列", 
                              font=("Arial", 16, "bold"), 
                              bg='#f0f0f0', fg='#333')
        title_label.pack(pady=15)
        
        # 说明
        info_frame = tk.LabelFrame(custom_window, text="使用说明", 
                                 font=("Arial", 12, "bold"), 
                                 bg='#f0f0f0', fg='#333')
        info_frame.pack(pady=10, padx=20, fill='x')
        
        info_label = tk.Label(info_frame, 
                             text="📝 自定义按键序列（每行一个按键）\n📋 格式：显示名称,按键代码\n💡 例如：反引号 `,`",
                             font=("Arial", 11), bg='#f0f0f0', fg='#666',
                             justify='left')
        info_label.pack(pady=10, padx=10)
        
        # 按键列表框架
        list_frame = tk.LabelFrame(custom_window, text="按键序列编辑", 
                                 font=("Arial", 12, "bold"), 
                                 bg='#f0f0f0', fg='#333')
        list_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        # 创建文本框
        text_frame = tk.Frame(list_frame, bg='#f0f0f0')
        text_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.keys_text = tk.Text(text_frame, height=12, width=60, 
                               font=("Consolas", 11), 
                               bg='#fff', fg='#333')
        
        scrollbar = tk.Scrollbar(text_frame, orient='vertical', 
                               command=self.keys_text.yview)
        self.keys_text.configure(yscrollcommand=scrollbar.set)
        
        self.keys_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # 加载当前按键序列
        current_keys = []
        for name, code in self.key_sequence:
            current_keys.append(f"{name},{code}")
        self.keys_text.insert(tk.END, "\n".join(current_keys))
        
        # 预设按钮框架
        preset_frame = tk.LabelFrame(custom_window, text="预设模板", 
                                   font=("Arial", 12, "bold"), 
                                   bg='#f0f0f0', fg='#333')
        preset_frame.pack(pady=10, padx=20, fill='x')
        
        preset_inner_frame = tk.Frame(preset_frame, bg='#f0f0f0')
        preset_inner_frame.pack(pady=10, padx=10)
        
        def load_preset_1():
            """加载预设1：默认序列"""
            preset = "反引号 `,`\n向上键 ↑,up\n回车键 ↵,enter"
            self.keys_text.delete(1.0, tk.END)
            self.keys_text.insert(tk.END, preset)
        
        def load_preset_2():
            """加载预设2：方向键序列"""
            preset = "向上键 ↑,up\n向下键 ↓,down\n向左键 ←,left\n向右键 →,right"
            self.keys_text.delete(1.0, tk.END)
            self.keys_text.insert(tk.END, preset)
        
        def load_preset_3():
            """加载预设3：数字键序列"""
            preset = "数字1,1\n数字2,2\n数字3,3\n数字4,4\n数字5,5"
            self.keys_text.delete(1.0, tk.END)
            self.keys_text.insert(tk.END, preset)
        
        # 预设按钮
        preset1_btn = tk.Button(preset_inner_frame, text="🔄 默认序列", command=load_preset_1,
                               font=("Arial", 11), bg='#2196F3', fg='white',
                               width=12, height=2, relief='raised', bd=3,
                               activebackground='#1976D2', activeforeground='white')
        preset1_btn.pack(side='left', padx=10)
        
        preset2_btn = tk.Button(preset_inner_frame, text="⬆️ 方向键", command=load_preset_2,
                               font=("Arial", 11), bg='#2196F3', fg='white',
                               width=12, height=2, relief='raised', bd=3,
                               activebackground='#1976D2', activeforeground='white')
        preset2_btn.pack(side='left', padx=10)
        
        preset3_btn = tk.Button(preset_inner_frame, text="🔢 数字键", command=load_preset_3,
                               font=("Arial", 11), bg='#2196F3', fg='white',
                               width=12, height=2, relief='raised', bd=3,
                               activebackground='#1976D2', activeforeground='white')
        preset3_btn.pack(side='left', padx=10)
        
        # 应用按钮
        def apply_custom_keys():
            try:
                content = self.keys_text.get(1.0, tk.END).strip()
                if not content:
                    messagebox.showerror("错误", "请输入按键序列")
                    return
                
                new_sequence = []
                lines = content.split('\n')
                for line in lines:
                    line = line.strip()
                    if line:
                        parts = line.split(',', 1)
                        if len(parts) == 2:
                            name, code = parts[0].strip(), parts[1].strip()
                            new_sequence.append((name, code))
                        else:
                            messagebox.showerror("错误", f"格式错误：{line}\n正确格式：显示名称,按键代码")
                            return
                
                if new_sequence:
                    self.key_sequence = new_sequence
                    messagebox.showinfo("成功", f"按键序列已更新，共{len(new_sequence)}个按键")
                    custom_window.destroy()
                else:
                    messagebox.showerror("错误", "请输入有效的按键序列")
                    
            except Exception as e:
                messagebox.showerror("错误", f"保存失败：{e}")
        
        button_frame = tk.Frame(custom_window, bg='#f0f0f0')
        button_frame.pack(pady=15)
        
        # 应用按钮
        apply_custom_btn = tk.Button(button_frame, text="✅ 应用", command=apply_custom_keys,
                                    font=("Arial", 12, "bold"), bg='#4CAF50', fg='white', 
                                    width=15, height=2, relief='raised', bd=3,
                                    activebackground='#45a049', activeforeground='white')
        apply_custom_btn.pack(side='left', padx=15)
        
        # 取消按钮
        cancel_custom_btn = tk.Button(button_frame, text="❌ 取消", command=custom_window.destroy,
                                     font=("Arial", 12), bg='#f44336', fg='white', 
                                     width=15, height=2, relief='raised', bd=3,
                                     activebackground='#da190b', activeforeground='white')
        cancel_custom_btn.pack(side='left', padx=15)
        
    def start_keyboard_listener(self):
        """启动键盘监听"""
        def on_key_press(key):
            if key == keyboard.Key.esc and self.esc_stop_enabled:
                self.add_log("检测到 ESC 键，停止程序")
                self.root.after(0, self.stop_pressing)
                # 通过设置停止标志来停止监听
                if self.keyboard_listener:
                    self.keyboard_listener.stop()
        
        if self.esc_stop_enabled:
            self.keyboard_listener = keyboard.Listener(on_press=on_key_press)
            self.keyboard_listener.start()
        
    def on_closing(self):
        """窗口关闭事件"""
        if self.running:
            self.stop_pressing()
        self.root.destroy()
        
    def run(self):
        """启动GUI"""
        self.root.mainloop()

def main():
    """主函数"""
    app = AutoKeyPresserGUI()
    app.run()

if __name__ == "__main__":
    main() 