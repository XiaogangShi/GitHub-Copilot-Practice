# Prompt 1 : 创建一个新的 python 文件，使用 python 和 Tkinter 创建一个 800*400 的窗口程序（尺寸不可改变），窗口分为上下两个区域，上面的区域从左到右分别房子一个标签组件
# （文本是“文件名“）、一个文本输入框组件和一个按钮组件（文本是“搜索“），在窗口中摆放第一个区域后，其余部分都分配给第 2 个区域。给出详细的实现代码和中文注释。

# Prompt 2: 为 button 添加单击事件，单击按钮，将访问本项目中 image_server.py 实现的基于 Flask的图像服务程序， 通过 http://localhost:1234/images/search?query=xxx 访问服务器端，
# 其中 xxx 是文本框输入的值（如果文本框为空，提示用户输入，提示内容为“您还没有输入要搜索的内容，请输入后再按【搜索】按钮“）。然后从服务器端获取搜索到的数据后(相对路径用逗号分隔)，
# 解析这些相对路径，将这些相对路径与 http://localhost:1234/images/ 组合为绝对路径，添加到一个列表中，最后将列表内容输出到 本 GUI。

# Prompt 3: 1, 在 GUI 中以缩略图/可点击列表展示（双击打开大图）2, 点击“搜索“按钮时同时将上一次的结果从第二个区域清空
# 3，将“提示：在上方输入部分或者完整文件名后点击【搜索】或按回车。“ 在 GUI 上挪到第一区域底部。

# Prompt 4（切换到 Claund Sonet 4.5）: 当前代码没有实现  ‘‘‘‘ 将文本标签组件 “提示：在上方输入部分或者完整文件名后点击【搜索】或按回车。“ 在 GUI 上挪到第一区域的按钮下方一行显示，左对齐。‘‘‘‘， GUI 上显示它们在同一行。使用 python 和 tkinter， 请修改实现。

# Prompt 5: 修改：在 GUI 的第二区域中支持可点击列表双击打开大图），单击后右侧可显示缩略图。

# Prompt 6: 已经通过 "pip install Pillow" 安装了 Pillow， 但是单击预览功能没有实现。双击看大图功能可以使用。请修改

# Prompt 7: 调整第 2区域左半部分为根据最长的一行自适应宽度；右半部分的缩略图自适应居中，调整略图大小为自适应，但不小于200 *200。

import tkinter as tk
from tkinter import messagebox
import urllib.parse
import urllib.request
from typing import List


class FileSearchApp:
    """
    一个简单的 Tkinter 窗口程序。

    窗口尺寸：800x400（固定、不可改变）。
    窗口分为上下两部分：
      - 上部：一行水平排列的控件：标签（"文件名"）、文本输入框、按钮（"搜索"）。
      - 下部：占用剩余空间的内容区（可以用来显示搜索结果或其它信息）。
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("图像搜索器")

        # 设置窗口大小为 800x400，并禁止用户调整窗口大小
        self.root.geometry("800x400")
        self.root.resizable(False, False)  # 宽、高都不可变

        # --- 上部区域：放置 Label、Entry、Button 和提示文本 ---
        # 使用一个 Frame 把上部控件包裹起来，方便后续布局和样式调整
        top_container = tk.Frame(self.root, padx=8, pady=8)
        top_container.pack(side=tk.TOP, fill=tk.X)  # 水平填充窗口宽度，但高度由内容决定

        # 第一行：搜索控件（标签、输入框、按钮）
        controls_frame = tk.Frame(top_container)
        controls_frame.pack(side=tk.TOP, fill=tk.X)

        # 标签：显示文字 "文件名"
        label = tk.Label(controls_frame, text="文件名", font=("Arial", 12))
        label.pack(side=tk.LEFT, padx=(4, 8))  # 放在左侧，右侧留一点间距

        # 文本输入框：用于输入要搜索的文件名
        # 我们让 Entry 在水平方向上可以扩展以占据剩余空间
        self.entry = tk.Entry(controls_frame, font=("Arial", 12))
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))

        # 按钮：点击开始搜索
        search_btn = tk.Button(controls_frame, text="搜索", font=("Arial", 12), command=self.on_search)
        search_btn.pack(side=tk.LEFT)

        # 支持按回车键触发搜索（便于键盘操作）
        self.entry.bind('<Return>', lambda event: self.on_search())

        # 第二行：提示文本标签（在按钮下方一行，左对齐）
        self.hint_label = tk.Label(
            top_container,
            text="提示：在上方输入部分或者完整文件名后点击【搜索】或按回车。找到图像后，单击查看预览，双击打开大图",
            fg="gray",
            anchor='w',
            justify='left',
        )
        self.hint_label.pack(side=tk.TOP, fill=tk.X, pady=(6, 0), padx=(4, 0))

        # --- 下部区域：占用剩余空间 ---
        # 使用一个 Frame 占据剩余的可用空间（fill=BOTH and expand=True）
        self.bottom_frame = tk.Frame(self.root, padx=8, pady=8, bg="#f7f7f7")
        self.bottom_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # 在下部区域放置一个可点击的列表（Listbox）用于展示结果，右侧显示缩略图预览（如可用）
        result_container = tk.Frame(self.bottom_frame)
        result_container.pack(fill=tk.BOTH, expand=True)

        # 左侧：列表（根据内容自适应宽度，不扩展）
        list_frame = tk.Frame(result_container)
        list_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.listbox = tk.Listbox(list_frame, activestyle='none', width=0)
        self.listbox.pack(side=tk.LEFT, fill=tk.Y)

        scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)

        # 右侧：预览区域（自适应扩展，缩略图居中）
        self.preview_frame = tk.Frame(result_container, bg="#eee")
        self.preview_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.preview_label = tk.Label(self.preview_frame, text="预览", bg="#eee", compound='center')
        self.preview_label.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # 绑定列表选择和双击事件
        self.listbox.bind('<<ListboxSelect>>', self.on_select)
        self.listbox.bind('<Double-Button-1>', self.on_double_click)

        # 存储当前查询结果（filename 与 URL 列表）
        self.current_files: List[str] = []
        self.current_urls: List[str] = []

        # 可选的 Pillow 支持，用于显示缩略图
        try:
            from PIL import Image, ImageTk  # type: ignore
            import io
            self.PIL_AVAILABLE = True
            self._PIL_Image = Image
            self._PIL_ImageTk = ImageTk
            self._io = io
            print("✓ Pillow 已加载，支持缩略图预览")
        except Exception as e:
            self.PIL_AVAILABLE = False
            print(f"✗ Pillow 未安装: {e}")
            print("  提示：单击列表项将只显示文件名，无法显示缩略图")

        # 初始提示（移动到了顶部，因此不在结果区显示）
        # 在 listbox 中不显示初始提示；仍保留顶部 hint_label

    def on_search(self):
        """
        搜索处理函数：
        - 从上方输入框读取查询字符串（query）；
        - 使用 HTTP GET 请求访问本地运行的 Flask 图像服务：
          http://localhost:1234/images/search?query=xxx
        - 服务器返回以逗号分隔的相对路径（例如：images/1.jpg,images/foo.png），
          将相对路径解析为绝对 URL（基于 http://localhost:1234/images/），
          并把这些 URL 列表输出到下部结果区。
        如果输入为空，会弹出提示：
        “您还没有输入要搜索的内容，请输入后再按【搜索】按钮”
        """
        query = self.entry.get().strip()
        if not query:
            messagebox.showinfo("提示", "您还没有输入要搜索的内容，请输入后再按【搜索】按钮")
            return

        # 清空上一次的搜索结果
        self.listbox.delete(0, tk.END)
        self.current_files.clear()
        self.current_urls.clear()
        self.preview_label.config(text="预览", image='')

        # 构造请求 URL
        base_search = 'http://localhost:1234/images/search'
        params = {'query': query}
        url = base_search + '?' + urllib.parse.urlencode(params)

        try:
            with urllib.request.urlopen(url, timeout=5) as resp:
                raw = resp.read().decode('utf-8')
        except Exception as e:
            messagebox.showerror("错误", f"请求图像服务失败: {e}")
            return

        # 服务器返回以逗号分隔的相对路径，可能包含换行和空格，先分割并清理
        parts = [p.strip() for p in raw.split(',') if p.strip()]

        # 将相对路径转换为绝对 URL，基准为 http://localhost:1234/images/
        base_images = 'http://localhost:1234/images/'
        filenames: List[str] = []
        abs_urls: List[str] = []

        for rel in parts:
            # rel 可能是 'images/foo.jpg' 或 'foo.jpg' 或 '/images/foo.jpg'
            r = rel.lstrip('/')
            if r.startswith('images/'):
                fname = r[len('images/'):]
            else:
                fname = r
            filenames.append(fname)
            abs_urls.append(base_images + urllib.parse.quote(fname))

        if not abs_urls:
            self.listbox.insert(tk.END, f"未找到与 '{query}' 匹配的图像。")
            self._update_listbox_width()
            return

        # 显示查询提示
        self.listbox.insert(tk.END, f"查询: {query}")
        self.listbox.insert(tk.END, "--- 以下是搜索结果---")

        # 添加搜索结果到列表，并记录文件名和 URL
        for fname, url in zip(filenames, abs_urls):
            # 在列表中显示文件名（更友好）
            self.listbox.insert(tk.END, f"📷 {fname}")
            self.current_files.append(fname)
            self.current_urls.append(url)

        # 根据最长的一行自适应调整列表宽度
        self._update_listbox_width()

    def _update_listbox_width(self):
        """
        根据列表中最长的一行自动调整 Listbox 的宽度
        """
        max_width = 0
        for i in range(self.listbox.size()):
            item = self.listbox.get(i)
            # 计算文本宽度（每个字符大约占据1个单位，emoji占2个单位）
            width = len(item)
            if width > max_width:
                max_width = width

        # 设置宽度，最小20个字符，最大60个字符
        if max_width > 0:
            # 为 emoji 和中文字符留出额外空间
            adjusted_width = min(max(20, max_width), 60)
            self.listbox.config(width=adjusted_width)

    def _append_result(self, text: str):
        """
        向下部的结果列表追加一行文本（列表展示）。
        如果结果区当前为空，则直接添加；否则追加到末尾并选中最后一行以便滚动可见。
        """
        # 如果使用 listbox 展示结果，则插入一行；否则忽略
        try:
            self.listbox.insert(tk.END, text)
            self.listbox.see(tk.END)
        except Exception:
            pass

    def on_select(self, event):
        """
        当用户在结果 Listbox 中选择某一项时，显示该项的缩略图或文件名预览。
        """
        sel = self.listbox.curselection()
        if not sel:
            return
        idx = sel[0]

        # 前两行是标题（"查询: xxx" 和 "--- 以下是搜索结果 ---"），所以实际数据从索引2开始
        # 计算在 current_urls 中的实际索引
        data_idx = idx - 2

        # 防护：索引可能超出 current_urls 或者选中了标题行
        if data_idx < 0 or data_idx >= len(self.current_urls):
            # 选中了非图像数据的文本（例如提示），在预览区域显示文本
            try:
                text = self.listbox.get(idx)
                self.preview_label.config(text=text, image='')
            except Exception:
                pass
            return

        url = self.current_urls[data_idx]
        fname = self.current_files[data_idx]

        print(f"正在加载预览: {fname}")

        if self.PIL_AVAILABLE:
            try:
                print(f"  正在从 {url} 下载图像...")
                with urllib.request.urlopen(url, timeout=5) as resp:
                    data = resp.read()
                print(f"  下载完成，大小: {len(data)} 字节")
                bio = self._io.BytesIO(data)
                im = self._PIL_Image.open(bio)
                print(f"  原始图像尺寸: {im.size}")

                # 获取预览区域的实际尺寸
                self.preview_frame.update_idletasks()
                preview_width = self.preview_frame.winfo_width() - 16  # 减去 padding
                preview_height = self.preview_frame.winfo_height() - 16

                # 计算缩略图尺寸：不小于 200x200，但要适应预览区域
                max_width = max(200, preview_width)
                max_height = max(200, preview_height)

                # 保持宽高比缩放
                im.thumbnail((max_width, max_height), self._PIL_Image.Resampling.LANCZOS)
                print(f"  缩略图尺寸: {im.size} (预览区域: {preview_width}x{preview_height})")

                photo = self._PIL_ImageTk.PhotoImage(im)
                self.preview_label.config(image=photo, text='')
                # 保存引用，避免被垃圾回收
                self.preview_image = photo
                print("  ✓ 预览加载成功")
            except Exception as e:
                # 回退到仅显示文件名
                print(f"  ✗ 预览加载失败: {e}")
                self.preview_label.config(text=f"{fname}\n\n加载失败:\n{str(e)}", image='')
        else:
            # 没有 Pillow，显示文件名
            print("  Pillow 未安装，显示文件名")
            self.preview_label.config(text=fname, image='')

    def on_double_click(self, event):
        """
        双击列表项打开该图片的大图页面（在默认浏览器中打开 /images/view/<filename>）。
        """
        sel = self.listbox.curselection()
        if not sel:
            return
        idx = sel[0]

        # 前两行是标题，实际数据从索引2开始
        data_idx = idx - 2

        if data_idx < 0 or data_idx >= len(self.current_files):
            return
        fname = self.current_files[data_idx]
        view_url = 'http://localhost:1234/images/view/' + urllib.parse.quote(fname)
        import webbrowser
        webbrowser.open(view_url)


if __name__ == '__main__':
    root = tk.Tk()
    app = FileSearchApp(root)
    root.mainloop()
