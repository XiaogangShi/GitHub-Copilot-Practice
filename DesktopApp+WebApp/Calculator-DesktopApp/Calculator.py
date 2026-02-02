# 使用 python 的 Tkinter 实现一个程序，创建一个 300*400 的窗口。窗口分为两部分，上半部分是一个文本输入框，其余部分属于下半部分。在下半部分实现类似于计算器按钮的网格布局。网格分为 4 行 4 列，每个单元格是一个按钮
# 从左到右，从上到下，按钮依次是 7 8 9 + 4 5 6 - 1 2 3 * 0 . = /
# 当点击数字按钮或小数点按钮时，文本输入框中显示相应的字符。当点击运算符按钮时，文本输入框中显示相应的运算符。当点击等号按钮时，计算文本输入框中的表达式，并将结果显示在文本输入框中
# 给出完整的代码和中文注释。

import tkinter as tk
from tkinter import messagebox
# 导入消息框模块，用于显示错误信息
class CalculatorApp:
    """
    一个简单的计算器应用程序，使用Tkinter实现。
    """
    def __init__(self, root):
        self.root = root
        self.root.title("计算器")
        self.root.geometry("300x400")

        # 创建文本输入框，用于显示和输入表达式，右对齐更像计算器的样式
        self.entry = tk.Entry(root, font=("Arial", 24), borderwidth=2, relief="groove", justify=tk.RIGHT)
        self.entry.pack(fill=tk.BOTH, padx=10, pady=10, ipady=10)
        # 双击输入框清空内容
        self.entry.bind('<Double-Button-1>', lambda e: self.entry.delete(0, tk.END))
        # 键盘输入限制：仅允许数字、小数点和运算符（由按钮定义的字符）以及控制键（回车、退格、方向键）
        self.entry.bind('<Key>', self._on_entry_key)
        # 阻止粘贴（Ctrl+V / Ctrl+v）以避免绕过输入限制
        self.entry.bind('<Control-v>', lambda e: 'break')
        self.entry.bind('<Control-V>', lambda e: 'break')

        # 创建按钮网格布局
        # 按钮顺序：从左到右、从上到下为 7 8 9 + | 4 5 6 - | 1 2 3 * | 0 . = /
        button_texts = [
            '7', '8', '9', '+',
            '4', '5', '6', '-',
            '1', '2', '3', '*',
            '0', '.', '=', '/'
        ]

        # 创建一个框架用于放置按钮
        button_frame = tk.Frame(root)
        button_frame.pack(fill=tk.BOTH, expand=True)

        # 键盘绑定：回车等同于按下 '='，退格删除最后一个字符，C 清除
        self.root.bind('<Return>', lambda e: self.on_button_click('='))
        self.root.bind('<BackSpace>', lambda e: self.on_backspace())
        self.root.bind('c', lambda e: self.on_clear())
        self.root.bind('C', lambda e: self.on_clear())

        # 创建按钮并添加到网格布局中
        for i, text in enumerate(button_texts):
            button = tk.Button(button_frame, text=text, font=("Arial", 18), command=lambda t=text: self.on_button_click(t))
            button.grid(row=i//4, column=i%4, sticky="nsew", padx=5, pady=5)

        # 配置网格行列权重，使按钮均匀分布
        for i in range(4):
            button_frame.grid_rowconfigure(i, weight=1)
            button_frame.grid_columnconfigure(i, weight=1)

    def on_button_click(self, char):
        """
        处理按钮点击事件，根据按钮字符更新文本输入框内容或计算结果。
        """
        if char == '=':
            try:
                # 计算表达式并显示结果
                result = eval(self.entry.get())
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, str(result))
            except Exception as e:
                # 如果计算出错，显示错误消息
                messagebox.showerror("错误", "无效的表达式")
                self.entry.delete(0, tk.END)
        else:
            # 向文本输入框添加字符
            self.entry.insert(tk.END, char)

    def on_backspace(self):
        """
        处理退格键：删除文本输入框中的最后一个字符。
        """
        current = self.entry.get()
        if current:
            # 删除最后一个字符
            self.entry.delete(len(current)-1, tk.END)

    def _on_entry_key(self, event):
        """
        限制直接键盘输入：只允许按下按钮定义的字符（0-9, . + - * /）和一些控制键。
        返回 'break' 可以阻止该键的默认处理，从而阻止字符被插入。
        """
        # 允许的字符（由界面按钮定义）
        allowed_chars = set('0123456789.+-*/')

        # 一些不产生字符但应允许的按键（退格、回车、方向键等）
        allowed_keysym = {
            'BackSpace', 'Return', 'KP_Enter', 'Left', 'Right', 'Home', 'End',
            'Tab', 'Shift_L', 'Shift_R', 'Control_L', 'Control_R', 'Alt_L', 'Alt_R'
        }

        # 如果是允许的控制键，放行（让已有的绑定处理，例如回车触发计算）
        if event.keysym in allowed_keysym:
            return

        ch = event.char
        # 如果没有可打印字符（例如功能键），放行
        if not ch:
            return

        # 如果字符在允许集合中，放行；否则阻止默认处理
        if ch in allowed_chars:
            return

        # 阻止所有其他键（包含粘贴等）
        return 'break'

    def on_clear(self):
        """
        清除文本输入框内容（用于按 'c' 或 'C'）。
        """
        self.entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()