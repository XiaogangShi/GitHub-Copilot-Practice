# 用 python和 Flask 编写一个 web 应用，将当前目录的 images 子目录作为图像存储的路径，通过 GET 请求在浏览器中查看 images 子目录中的图像，图像会直接在浏览器中显示。
# 格式为 http://localhost:1234/images/123.jpg。给出完整的代码和中文注释。

# updated requirement : 增加功能：1，浏览器访问 http://localhost:1234/images/ 可以看到所有的图像； 2， 再添加一个路由，支持 GET 请求，该路由接收一个查询字符串参数 query,
#  并且在 images 子目录中查找该文件（不包括扩展名），搜索文件名时，只要文件名中包含查询字符串即可。然后返回搜索到的所有图像文件的相对路径，以字符串形式返回，路径之间使用逗号分隔

# 导入 Flask 模块和 send_from_directory 函数
from flask import Flask, send_from_directory, request
import os
from flask_cors import CORS

# 创建 Flask 应用实例
app = Flask(__name__)
# 启用 CORS，允许所有来源访问所有路由
# 注意：在生产环境中应该限制 origins
CORS(app)

# 获取当前脚本文件所在的目录路径
# 这将作为我们查找 'images' 文件夹的基准路径
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# 定义图像存储的目录
# os.path.join 会智能地拼接路径，确保跨操作系统兼容性
IMAGES_DIR = os.path.join(CURRENT_DIR, 'images')

# 设置路由，用于处理对 /images/<filename> 的 GET 请求
# <filename> 是一个变量，会捕获 URL 中图像的文件名
@app.route('/images/<filename>')
def serve_image(filename):
    """
    处理图像请求，从 'images' 目录中发送指定的文件。
    """
    try:
        # 使用 send_from_directory 函数安全地发送文件
        # 第一个参数是文件所在的目录
        # 第二个参数是要发送的文件名
        return send_from_directory(IMAGES_DIR, filename)
    except FileNotFoundError:
        # 如果文件未找到，返回 404 错误
        return "Image not found", 404
    except Exception as e:
        # 捕获其他可能的错误
        return f"An error occurred: {e}", 500


# 列表展示 images 目录下所有图像的路由
@app.route('/images')
@app.route('/images/')
def list_images():
    """
    在浏览器中以简单的 HTML 画廊形式展示 images 目录下的所有图像。
    """
    try:
        if not os.path.isdir(IMAGES_DIR):
            return "Images directory not found", 404

        # 只展示常见的图片扩展名
        exts = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg'}
        files = [f for f in os.listdir(IMAGES_DIR)
                 if os.path.isfile(os.path.join(IMAGES_DIR, f)) and os.path.splitext(f)[1].lower() in exts]

        # 构造简单的 HTML 画廊
        parts = ["<html><head><title>Images</title></head><body>"]
        parts.append(f"<h2>Images in {os.path.basename(IMAGES_DIR)}</h2>")
        for fn in files:
            # 缩略图：点击缩略图会打开一个单独的页面以窗口大小显示该图片
            parts.append(f'<div style="display:inline-block;margin:8px;text-align:center;">')
            parts.append(f'<a href="/images/view/{fn}"><img src="/images/{fn}" style="max-width:200px;max-height:200px;display:block;"/></a>')
            parts.append(f'<div>{fn}</div>')
            parts.append('</div>')

        parts.append('</body></html>')
        return '\n'.join(parts)
    except Exception as e:
        return f"An error occurred: {e}", 500


# 点击缩略图后放大查看单张图片（在浏览器窗口内）
@app.route('/images/view/<filename>')
def view_image(filename):
        """
        返回一个 HTML 页面，用于在浏览器窗口中放大显示指定图片，并提供上一张/下一张和键盘导航支持。
        """
        try:
                img_path = os.path.join(IMAGES_DIR, filename)
                if not os.path.isfile(img_path):
                        return "Image not found", 404

                # 与 gallery 相同的扩展名集合和排序逻辑，确保前后导航一致
                exts = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg'}
                files = sorted([f for f in os.listdir(IMAGES_DIR)
                                                if os.path.isfile(os.path.join(IMAGES_DIR, f)) and os.path.splitext(f)[1].lower() in exts])

                # 找到当前图片在列表中的索引
                try:
                        idx = files.index(filename)
                except ValueError:
                        # 文件名不在列表中
                        idx = None

                prev_link = ''
                next_link = ''
                if idx is not None:
                        if idx > 0:
                                prev_fn = files[idx - 1]
                                prev_link = f'/images/view/{prev_fn}'
                        if idx < len(files) - 1:
                                next_fn = files[idx + 1]
                                next_link = f'/images/view/{next_fn}'

                # 构建 HTML，增加 Prev/Next 按钮与键盘支持（Esc 返回，左右键切换）
                html = f'''<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>{filename}</title>
    <style>
        html,body{{height:100%;margin:0;background:#000;color:#fff;font-family:Arial,Helvetica,sans-serif}}
        .wrap{{height:100%;display:flex;align-items:center;justify-content:center;}}
        img{{max-width:100vw;max-height:100vh;object-fit:contain;}}
        .nav-btn{{position:fixed;top:50%;transform:translateY(-50%);color:#fff;text-decoration:none;font-size:28px;background:rgba(0,0,0,0.4);padding:12px;border-radius:6px}}
        .prev{{left:10px}}
        .next{{right:10px}}
        .close-link{{position:fixed;top:10px;left:10px;color:#fff;text-decoration:none;font-size:18px;background:rgba(0,0,0,0.4);padding:6px 10px;border-radius:4px}}
    </style>
</head>
<body>
    <a class="close-link" href="/images/">← Back</a>
    {f'<a class="nav-btn prev" href="{prev_link}">◀</a>' if prev_link else ''}
    {f'<a class="nav-btn next" href="{next_link}">▶</a>' if next_link else ''}
    <div class="wrap">
        <img id="theImg" src="/images/{filename}" alt="{filename}" />
    </div>

    <script>
        // 键盘支持：Esc 返回，左右键跳转
        document.addEventListener('keydown', function(e) {{
            // 左箭头
            if (e.key === 'ArrowLeft') {{
                const prev = '{prev_link}';
                if (prev) window.location.href = prev;
            }}
            // 右箭头
            if (e.key === 'ArrowRight') {{
                const next = '{next_link}';
                if (next) window.location.href = next;
            }}
            // Esc 返回图库
            if (e.key === 'Escape') {{
                window.location.href = '/images/';
            }}
        }});
        // 点击图片也可放大/还原（简单行为：点击图片无操作，但可扩展）
    </script>
</body>
</html>'''
                return html
        except Exception as e:
                return f"An error occurred: {e}", 500


# 搜索路由：接收 query 参数，查找文件名中包含 query（不包括扩展名）的所有图像
@app.route('/images/search')
def search_images():
    """
    GET 参数: query
    在 images 子目录中查找文件名（不包括扩展名）包含 query 的文件。
    返回值: 以逗号分隔的相对路径列表，例如 "images/1.jpg,images/foo.png"
    """
    query = request.args.get('query', '')
    if not query:
        # 未提供查询参数，返回空字符串
        return ''

    try:
        if not os.path.isdir(IMAGES_DIR):
            return ''

        exts = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg'}
        matches = []
        for f in os.listdir(IMAGES_DIR):
            full = os.path.join(IMAGES_DIR, f)
            if not os.path.isfile(full):
                continue
            name, ext = os.path.splitext(f)
            if ext.lower() not in exts:
                continue
            if query.lower() in name.lower():
                # 返回相对路径
                matches.append(os.path.join('images', f))

        # 以逗号加换行分隔返回所有匹配的文件路径
        return ',\n '.join(matches)
    except Exception:
        return ''

# 当直接运行此脚本时，启动 Flask 开发服务器
if __name__ == '__main__':
    # 打印提示信息，告知用户服务器将要启动
    print(f"Server will be running on http://localhost:1234")
    print(f"Images are served from: {IMAGES_DIR}")
    print(f"Example URL: http://localhost:1234/images/image1.jpg") # 请替换为images目录中的实际文件名

    # 运行 Flask 应用
    # host='0.0.0.0' 使应用可以在网络中被访问（如果需要）
    # port=1234 指定服务器运行的端口
    # debug=True 可以在开发过程中提供更多的错误信息和自动重载功能
    app.run(host='127.0.0.1', port=1234, debug=True)
