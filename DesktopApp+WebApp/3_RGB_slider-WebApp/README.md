# Github Copilot 实现，Prompt
将此 python 程序转换为 html,CSS 和 JavaScript实现的 web 应用，放置在当前目录下的 3_RGB_slider-Web-App 文件夹下。请创建这个文件夹，并且 web 代码的实现放置在新的 html，CSS, javascript 文件中，并创建 README.md

# RGB 颜色选择器 Web 版 (RGB Color Picker Web App)，等价于 ../3_RGB_sliders.py

这是一个基于 HTML, CSS, JavaScript 的简单 Web 应用，复刻了原 Python (PyQt6) 版本的 RGB 颜色选择器功能。

## 功能

-   提供红、绿、蓝三个滑块 (0-255)。
-   实时预览 RGB 混合后的颜色背景。
-   实时显示对应的十六进制颜色代码 (Hex Code)。
-   自动调整文本颜色（黑/白）以保持对比度。

## 文件结构

-   `index.html`: 页面结构 (文本区域, 标签, 滑块)。
-   `style.css`: 样式文件，模仿原桌面应用的布局。
-   `script.js`: 逻辑脚本，处理滑块事件和颜色计算。

## 如何使用

1.  直接双击打开 `index.html` 文件，或者将其拖入浏览器中。
2.  拖动滑块即可看到颜色变化。
