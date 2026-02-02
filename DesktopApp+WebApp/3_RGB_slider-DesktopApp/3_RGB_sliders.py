# 用 最新的 pyQt 创建一个 300*500 的窗口，然后在窗口的垂直方向分别放一个文本组件、一个标签组件和3个滑块组件。所有滑块组件对应的最小值为 0，最大值为 255，初始化值为中间。3 个滑块组件分别对应红黄蓝三原色。
# 当滑动这 3 个滑块时。使用这 3 个滑块的当前值设置为文本组件的背景色。然后将这 3 个滑块的当前值组合成以#开头的颜色值，如#ffffff，显示在标签组件中。给出完整的代码和中文注释。


import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QSlider,
    QLabel, QTextEdit
)
from PyQt6.QtCore import Qt # 注意，Qt在这里仍然是QtCore模块的一部分
from PyQt6.QtGui import QColor

class ColorPickerWindow(QMainWindow):
    """
    一个PyQt6应用程序窗口，用于通过滑块选择RGB颜色。
    """
    def __init__(self):
        super().__init__()

        # 设置窗口标题
        self.setWindowTitle("Gemini - PyQt6 RGB 颜色选择器")
        # 设置窗口初始位置和大小 (x, y, 宽度, 高度)
        self.setGeometry(100, 100, 300, 500)

        # 创建一个中心Widget，所有的UI元素都将放在这个Widget上
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建主垂直布局，用于组织窗口内的所有组件
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # --- 1. 文本组件 (QTextEdit) ---
        # 用于显示背景颜色和一些提示文本
        self.text_component = QTextEdit("滑动滑块改变背景颜色")
        self.text_component.setFixedHeight(200) # 设置一个固定高度
        # 初始背景色为中等灰色 (#7F7F7F)，文字为白色以便在深色背景下可见
        self.text_component.setStyleSheet(
            "background-color: #7F7F7F; color: white; "
            "font-size: 20px; font-weight: bold; padding: 20px;"
        )
        # 将文本组件添加到主布局
        main_layout.addWidget(self.text_component)

        # --- 2. 标签组件 (QLabel) ---
        # 用于显示当前的十六进制颜色值
        self.label_component = QLabel("#7F7F7F") # 初始显示灰色对应的十六进制值
        self.label_component.setFixedHeight(50)
        self.label_component.setStyleSheet(
            "font-size: 28px; font-weight: bold; border: 1px solid #ccc; "
            "background-color: #f0f0f0; margin-top: 10px;" # 增加边框和背景色，增加区分度
        )
        # ！！！ PyQt6 变更：Qt.AlignCenter 变为 Qt.AlignmentFlag.AlignCenter
        self.label_component.setAlignment(Qt.AlignmentFlag.AlignCenter) # 文本居中显示
        # 将标签组件添加到主布局
        main_layout.addWidget(self.label_component)

        # --- 3. 滑块组件 ---
        # 创建一个垂直布局，将三个水平滑块各自放在单独的一行里（3 行）
        sliders_v_layout = QVBoxLayout()
        main_layout.addLayout(sliders_v_layout)

        # 红色滑块 (Red)
        # ！！！ PyQt6 变更：Qt.Horizontal 变为 Qt.Orientation.Horizontal
        self.red_slider = self._create_slider_with_label(
            "红色 (Red)", Qt.Orientation.Horizontal
        )
        sliders_v_layout.addWidget(self.red_slider)

        # 绿色滑块 (Green)
        # ！！！ PyQt6 变更：Qt.Horizontal 变为 Qt.Orientation.Horizontal
        self.green_slider = self._create_slider_with_label(
            "绿色 (Green)", Qt.Orientation.Horizontal
        )
        sliders_v_layout.addWidget(self.green_slider)

        # 蓝色滑块 (Blue)
        # ！！！ PyQt6 变更：Qt.Horizontal 变为 Qt.Orientation.Horizontal
        self.blue_slider = self._create_slider_with_label(
            "蓝色 (Blue)", Qt.Orientation.Horizontal
        )
        sliders_v_layout.addWidget(self.blue_slider)

        # 连接滑块的 valueChanged 信号到 update_color 槽函数
        # 当任何一个滑块的值改变时，都会触发 update_color 方法
        self.red_slider.findChild(QSlider).valueChanged.connect(self.update_color)
        self.green_slider.findChild(QSlider).valueChanged.connect(self.update_color)
        self.blue_slider.findChild(QSlider).valueChanged.connect(self.update_color)

        # 初始化时调用一次 update_color 来设置初始的背景色和标签文本
        self.update_color()

    # 类型注解中也需要更新 Qt.Orientation
    def _create_slider_with_label(self, label_text: str, orientation: Qt.Orientation) -> QWidget:
        """
        创建一个包含标签和滑块的垂直布局组件。

        Args:
            label_text (str): 滑块的标签文本。
            orientation (Qt.Orientation): 滑块的方向 (Qt.Orientation.Vertical 或 Qt.Orientation.Horizontal)。

        Returns:
            QWidget: 包含标签和滑块的容器Widget。
        """
        container = QWidget()
        v_layout = QVBoxLayout(container) # 为容器Widget设置垂直布局

        # 创建标签（如：红色 / 绿色 / 蓝色）并居中
        # 我们把标签设为可变的，后面会在滑块变化时更新为“颜色名：值”的形式
        label = QLabel(label_text)
        # 将颜色标签左对齐，便于阅读（例如“红色 (Red)：88”）
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        v_layout.addWidget(label)

        # 如果是水平滑块，建立一行：最小值标签 | 滑块 | 最大值标签
        if orientation == Qt.Orientation.Horizontal:
            row = QWidget()
            h_layout = QHBoxLayout(row)

            # 最小值（以十六进制显示为 00）
            min_label = QLabel("00")
            min_label.setFixedWidth(36)
            min_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # 滑块本体
            slider = QSlider(orientation)
            slider.setMinimum(0)
            slider.setMaximum(255)
            slider.setValue(127)
            slider.setTickPosition(QSlider.TickPosition.TicksBelow)
            slider.setTickInterval(15)

            # 当滑块数值改变时，更新上方的标签为类似“红色 (Red)：88”格式
            def _update_label(val, lbl=label, base_text=label_text):
                lbl.setText(f"{base_text}：{val}")

            slider.valueChanged.connect(_update_label)
            # 设置初始显示值
            _update_label(slider.value())

            # 最大值（以十六进制显示为 FF）
            max_label = QLabel("ff")
            max_label.setFixedWidth(36)
            max_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # 将最小标签、滑块、最大标签按行放置
            h_layout.addWidget(min_label)
            h_layout.addWidget(slider)
            h_layout.addWidget(max_label)

            v_layout.addWidget(row)
        else:
            # 纵向滑块（保留原有行为）
            slider = QSlider(orientation)
            slider.setMinimum(0)       # 最小值
            slider.setMaximum(255)     # 最大值
            slider.setValue(127)       # 初始值设置为中间 (0+255)/2 ≈ 127
            slider.setTickPosition(QSlider.TickPosition.TicksBelow)
            slider.setTickInterval(15)

            # 纵向滑块也同步标签显示数值
            def _update_label(val, lbl=label, base_text=label_text):
                lbl.setText(f"{base_text}：{val}")

            slider.valueChanged.connect(_update_label)
            _update_label(slider.value())
            v_layout.addWidget(slider)

        return container # 返回这个容器Widget

    def update_color(self):
        """
        根据三个滑块的当前值，更新文本组件的背景色和标签组件的文本。
        """
        # 获取红、绿、蓝滑块的当前值
        # 注意：因为_create_slider_with_label返回的是一个容器QWidget，
        # 所以我们需要通过 findChild 方法找到真正的QSlider实例。
        red = self.red_slider.findChild(QSlider).value()
        green = self.green_slider.findChild(QSlider).value()
        blue = self.blue_slider.findChild(QSlider).value()

        # 使用RGB值创建 QColor 对象
        current_color = QColor(red, green, blue)

        # 设置文本组件的背景色
        # current_color.name() 会返回如 "#RRGGBB" 格式的十六进制颜色字符串
        # 同时根据背景色计算一个对比度高的文本颜色，以确保文本可见
        text_color = self._get_contrasting_text_color(current_color)
        self.text_component.setStyleSheet(
            f"background-color: {current_color.name()}; "
            f"color: {text_color}; "
            "font-size: 20px; font-weight: bold; padding: 20px;"
        )

        # 设置标签组件的文本，显示大写的十六进制颜色值
        self.label_component.setText(current_color.name().upper())

    def _get_contrasting_text_color(self, background_color: QColor) -> str:
        """
        根据背景颜色，返回一个对比度更高的文本颜色（黑色或白色）。
        这有助于确保文本在不同背景色下始终清晰可见。
        """
        # 计算背景色的亮度 (Luminance)，基于人眼对不同颜色亮度的感知权重
        # 公式: L = 0.299*R + 0.587*G + 0.114*B
        # 亮度值范围0-255
        brightness = (background_color.red() * 299 +
                      background_color.green() * 587 +
                      background_color.blue() * 114) / 1000

        # 如果亮度高于某个阈值（通常是180），则使用黑色文本；否则使用白色文本。
        # 180是一个经验值，能让文本在较浅的背景上更清晰。
        if brightness > 180:
            return "black"
        else:
            return "white"

# 主程序入口
if __name__ == "__main__":
    # 创建 QApplication 实例
    app = QApplication(sys.argv)

    # 创建并显示主窗口
    window = ColorPickerWindow()
    window.show()

    # 启动应用程序的事件循环
    # ！！！ PyQt6 变更：app.exec_() 变为 app.exec()
    sys.exit(app.exec())
