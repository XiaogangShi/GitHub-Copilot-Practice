"""
配置文件 - 定义模拟程序的常量和参数
"""

# 窗口设置
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
BACKGROUND_COLOR = (0, 0, 0)  # 黑色

# 小球设置
NUM_BALLS = 6
MIN_RADIUS = 15
MAX_RADIUS = 25

# 运动参数
MIN_SPEED = 3.0
MAX_SPEED = 6.0
BROWNIAN_RANGE = 0.5  # 布朗运动扰动范围

# 物理参数
FPS = 60  # 帧率
DT = 1.0 / FPS  # 时间步长

# 颜色列表 - 6种不同颜色
BALL_COLORS = [
    (255, 0, 0),      # 红色
    (0, 255, 0),      # 绿色
    (0, 0, 255),      # 蓝色
    (255, 255, 0),    # 黄色
    (255, 0, 255),    # 品红
    (0, 255, 255)     # 青色
]