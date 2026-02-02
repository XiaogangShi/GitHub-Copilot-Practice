# Github Copilot 实现，Prompt
将image_search_client.py 程序转换为 html,CSS 和 JavaScript实现的 web 应用，放置在当前目录下的 Image-Client-WebApp 文件夹下。请创建这个文件夹，并且 web 代码的实现放置在新的 html，CSS, javascript 文件中，并创建 README.md


# Image Client Web App (图像搜索 Web 客户端)

这是一个基于 HTML, CSS, JavaScript 的图像搜索客户端，复刻了 Python (Tkinter) 版本 `image_search_client.py` 的功能与布局。

## 功能

-   **搜索**: 访问本地 Flask 图片服务器 (`http://localhost:1234/images/search`) 查找图片。
-   **列表展示**: 动态显示搜索结果，列表宽度自适应内容。
-   **预览**: 单击列表项，右侧实时显示图片预览（自适应居中）。
-   **查看大图**: 双击列表项，在浏览器新标签页中打开完整图片视图。

## 文件结构

-   `index.html`: 页面骨架。
-   `style.css`: 样式布局，使用 Flexbox 模拟桌面应用的左右分栏和自适应效果。
-   `script.js`: 业务逻辑，处理 API 请求、DOM 操作和事件绑定。

## 使用前提

1.  **启动 Image Server**:
    必须先运行 Python 后端服务。
    ```bash
    cd ..
    python image_server.py
    ```

2.  **解决跨域 (CORS) 问题**:
    由于 Web 浏览器安全策略，如果直接打开 `index.html` (file:// 协议) 去请求 `http://localhost:1234`，可能会被 CORS 拦截。

    **解决方法 A (修改服务器)**:
    安装 `u` 并修改 `image_server.py`:
    ```python
    from flask_cors import CORS
    app = Flask(__name__)
    CORS(app)  # 允许所有跨域请求
    ```

    **解决方法 B (浏览器插件)**:
    在开发期间，安装浏览器插件如 "Allow CORS: Access-Control-Allow-Origin" 并开启。

## 运行

直接在浏览器中打开 `index.html` 即可。
