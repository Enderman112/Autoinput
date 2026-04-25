import time
import pyautogui
import tkinter as tk
from tkinter import ttk
import threading
from pypinyin import pinyin, Style

class AutoInputApp:
    def __init__(self, root):
        self.root = root
        self.root.title("自动输入工具")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        # 创建主框架
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(main_frame, text="自动输入工具", font=("PingFang SC", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # 输入框
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        input_label = ttk.Label(input_frame, text="要输入的文字:", font=("PingFang SC", 12))
        input_label.pack(anchor=tk.W)
        
        self.text_input = tk.Text(input_frame, height=4, width=40, wrap=tk.WORD)
        self.text_input.pack(fill=tk.X, pady=(5, 0))
        self.text_input.insert("1.0", "在这里输入要自动打字的内容...")
        self.text_input.bind("<FocusIn>", self.clear_placeholder)
        self.text_input.bind("<FocusOut>", self.add_placeholder)
        
        # 延迟设置
        delay_frame = ttk.Frame(main_frame)
        delay_frame.pack(fill=tk.X, pady=(10, 20))
        
        delay_label = ttk.Label(delay_frame, text="延迟时间 (秒):", font=("PingFang SC", 12))
        delay_label.pack(anchor=tk.W)
        
        self.delay_var = tk.DoubleVar(value=2.0)
        self.delay_scale = ttk.Scale(delay_frame, from_=0.5, to=10.0, 
                                   variable=self.delay_var, orient=tk.HORIZONTAL)
        self.delay_scale.pack(fill=tk.X, pady=(5, 0))
        
        self.delay_value_label = ttk.Label(delay_frame, text="2.0 秒", font=("PingFang SC", 12))
        self.delay_value_label.pack(anchor=tk.E)
        self.delay_scale.configure(command=self.update_delay_label)
        
        # 按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        btn_font = ("PingFang SC", 13)
        
        self.start_button = tk.Button(button_frame, text="开始自动输入", 
                                      command=self.start_auto_input,
                                      font=btn_font, padx=20, pady=8)
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = tk.Button(button_frame, text="停止", 
                                     command=self.stop_auto_input, state=tk.DISABLED,
                                     font=btn_font, padx=20, pady=8)
        self.stop_button.pack(side=tk.LEFT)
        
        # 状态显示
        self.status_label = ttk.Label(main_frame, text="就绪", foreground="green", font=("PingFang SC", 12))
        self.status_label.pack(pady=(10, 0))
        
        # 线程控制
        self.running = False
        self.auto_thread = None
        
    def clear_placeholder(self, event):
        if self.text_input.get("1.0", tk.END).strip() == "在这里输入要自动打字的内容...":
            self.text_input.delete("1.0", tk.END)
            self.text_input.configure(foreground="black")
    
    def add_placeholder(self, event):
        if not self.text_input.get("1.0", tk.END).strip():
            self.text_input.insert("1.0", "在这里输入要自动打字的内容...")
            self.text_input.configure(foreground="gray")
    
    def update_delay_label(self, value):
        self.delay_value_label.configure(text=f"{float(value):.1f} 秒")
    
    def start_auto_input(self):
        text = self.text_input.get("1.0", tk.END).strip()
        if not text or text == "在这里输入要自动打字的内容...":
            self.status_label.configure(text="请先输入要自动打字的内容", foreground="red")
            return
        
        delay = self.delay_var.get()
        self.running = True
        self.start_button.configure(state=tk.DISABLED)
        self.stop_button.configure(state=tk.NORMAL)
        self.status_label.configure(text=f"将在 {delay:.1f} 秒后开始输入...", foreground="blue")
        
        # 在新线程中运行自动输入
        self.auto_thread = threading.Thread(target=self.auto_input_thread, args=(text, delay))
        self.auto_thread.daemon = True
        self.auto_thread.start()
    
    def auto_input_thread(self, text, delay):
        try:
            # 等待指定延迟
            time.sleep(delay)
            
            if not self.running:
                return
            
            # 更新状态
            self.root.after(0, lambda: self.status_label.configure(
                text="正在输入...", foreground="orange"))
            
            # 执行自动输入（中文转拼音后输入）
            result = pinyin(text, style=Style.NORMAL)
            pinyin_str = ''.join([item[0] for item in result])
            pyautogui.write(pinyin_str)
            pyautogui.press('space')
            pyautogui.press('enter')
            
            # 完成
            self.root.after(0, lambda: self.status_label.configure(
                text="输入完成！", foreground="green"))
            self.root.after(0, lambda: self.start_button.configure(state=tk.NORMAL))
            self.root.after(0, lambda: self.stop_button.configure(state=tk.DISABLED))
            
        except Exception as e:
            self.root.after(0, lambda: self.status_label.configure(
                text=f"错误: {str(e)}", foreground="red"))
            self.root.after(0, lambda: self.start_button.configure(state=tk.NORMAL))
            self.root.after(0, lambda: self.stop_button.configure(state=tk.DISABLED))
        
        finally:
            self.running = False
    
    def stop_auto_input(self):
        self.running = False
        if self.auto_thread and self.auto_thread.is_alive():
            # 尝试中断线程（注意：这不是强制性的）
            self.auto_thread.join(0.1)
        
        self.start_button.configure(state=tk.NORMAL)
        self.stop_button.configure(state=tk.DISABLED)
        self.status_label.configure(text="已停止", foreground="red")

def main():
    root = tk.Tk()
    app = AutoInputApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()