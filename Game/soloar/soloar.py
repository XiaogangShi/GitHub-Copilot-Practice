import pygame
import math

# 常量定义 (颜色、屏幕尺寸、天体参数等)
# 类定义 (CelestialBody, Star, Planet, Moon)
# 初始化Pygame和天体对象
# 主循环
#   事件处理
#   屏幕清空
#   (可选)绘制轨道
#   更新所有天体位置
#   绘制所有天体
#   刷新显示
# 退出
# ```**最终代码（DeepSeek 生成** ：
# ```python
# """
# 太阳系局部模型动画
# 使用Pygame实现太阳、地球、金星和月球的轨道运动
# """

import pygame
import math
import sys

# 初始化Pygame
pygame.init()

# 屏幕设置
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("太阳系局部模型")
clock = pygame.time.Clock()
FPS = 60  # 帧率

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)      # 太阳
BLUE = (100, 149, 237)      # 地球
GOLD = (255, 215, 0)        # 金星
RED = (255, 100, 100)       # 月球
GRAY = (100, 100, 100)      # 轨道线

def get_font(size):
    """获取支持中文的字体对象"""
    font_path = None

    # 尝试查找系统中的中文天体
    if sys.platform.startswith('win'):
        font_names = ['simhei', 'microsoftyahei', 'simsun', 'kaiti']
    elif sys.platform.startswith('darwin'):
        # macOS 常见中文字体
        font_names = ['pingfangsc', 'heiti', 'stsong', 'hiraginosansgb', 'arialunicode']
    else:
        # Linux 常见中文字体
        font_names = ['wenquanyizenhei', 'notosanscjk', 'wqy-microhei']

    # 尝试找到第一个可用的字体文件路径
    for name in font_names:
        font_path = pygame.font.match_font(name)
        if font_path:
            break

    # 如果找到字体路径，使用该路径加载字体
    if font_path:
        try:
            return pygame.font.Font(font_path, size)
        except:
            pass

    # 如果没找到或加载失败，尝试使用默认字体或系统字体名
    try:
        # 尝试直接使用PingFang SC (Mac特例，有时候match_font找不到但SysFont能用)
        if sys.platform.startswith('darwin'):
             return pygame.font.SysFont('pingfangsc', size)
        return pygame.font.SysFont('simhei', size)
    except:
        return pygame.font.SysFont(None, size)

# 天体参数
SUN_RADIUS = 50
EARTH_RADIUS = 15
VENUS_RADIUS = 12
MOON_RADIUS = 5

# 轨道半径（像素）
EARTH_ORBIT_RADIUS = 200
VENUS_ORBIT_RADIUS = 150
MOON_ORBIT_RADIUS = 40

# 公转速度（弧度/帧）
EARTH_SPEED = 0.01
VENUS_SPEED = 0.015  # 金星公转更快
MOON_SPEED = 0.05    # 月球公转最快

class CelestialBody:
    """天体基类"""

    def __init__(self, name, color, radius, orbit_radius, speed):
        self.name = name
        self.color = color
        self.radius = radius
        self.orbit_radius = orbit_radius
        self.speed = speed
        self.angle = 0  # 当前公转角度（弧度）
        self.x = SCREEN_WIDTH // 2  # 屏幕中心
        self.y = SCREEN_HEIGHT // 2

    def update(self):
        """更新天体位置"""
        self.angle += self.speed
        # 保持角度在0-2π范围内
        if self.angle > 2 * math.pi:
            self.angle -= 2 * math.pi

    def draw(self, surface, center_x=None, center_y=None):
        """绘制天体"""
        if center_x is None:
            center_x = SCREEN_WIDTH // 2
        if center_y is None:
            center_y = SCREEN_HEIGHT // 2

        # 计算位置
        self.x = center_x + self.orbit_radius * math.cos(self.angle)
        self.y = center_y + self.orbit_radius * math.sin(self.angle)

        # 绘制天体
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

        # 绘制天体名称
        font = get_font(20)
        text = font.render(self.name, True, WHITE)
        surface.blit(text, (int(self.x) - 15, int(self.y) - self.radius - 20))

class Star(CelestialBody):
    """恒星类（太阳）"""

    def __init__(self):
        super().__init__("太阳", YELLOW, SUN_RADIUS, 0, 0)

    def update(self):
        """太阳不移动"""
        pass

    def draw(self, surface):
        """绘制太阳"""
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)

        # 绘制太阳名称
        font = get_font(24)
        text = font.render(self.name, True, WHITE)
        surface.blit(text, (self.x - 20, self.y - self.radius - 25))

class Planet(CelestialBody):
    """行星类（地球、金星）"""

    def __init__(self, name, color, radius, orbit_radius, speed):
        super().__init__(name, color, radius, orbit_radius, speed)

class Moon(CelestialBody):
    """卫星类（月球）"""

    def __init__(self, planet):
        super().__init__("月球", WHITE, MOON_RADIUS, MOON_ORBIT_RADIUS, MOON_SPEED)
        self.planet = planet  # 所属行星

    def draw(self, surface):
        """以行星为中心绘制月球"""
        # 计算以行星为中心的位置
        moon_x = self.planet.x + self.orbit_radius * math.cos(self.angle)
        moon_y = self.planet.y + self.orbit_radius * math.sin(self.angle)

        # 绘制月球
        pygame.draw.circle(surface, self.color, (int(moon_x), int(moon_y)), self.radius)

        # 保存位置用于后续使用
        self.x = moon_x
        self.y = moon_y

def draw_orbit(surface, center_x, center_y, radius, color=GRAY):
    """绘制圆形轨道线"""
    pygame.draw.circle(surface, color, (center_x, center_y), radius, 1)

def main():
    """主函数"""

    # 创建天体对象
    sun = Star()
    earth = Planet("地球", BLUE, EARTH_RADIUS, EARTH_ORBIT_RADIUS, EARTH_SPEED)
    venus = Planet("金星", GOLD, VENUS_RADIUS, VENUS_ORBIT_RADIUS, VENUS_SPEED)
    moon = Moon(earth)

    # 主循环
    running = True
    while running:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # 清屏
        screen.fill(BLACK)

        # 绘制轨道线
        draw_orbit(screen, sun.x, sun.y, EARTH_ORBIT_RADIUS)
        draw_orbit(screen, sun.x, sun.y, VENUS_ORBIT_RADIUS)

        # 更新天体位置
        venus.update()
        earth.update()
        moon.update()

        # 绘制天体
        sun.draw(screen)
        venus.draw(screen)
        earth.draw(screen)
        moon.draw(screen)

        # 绘制月球轨道线（以地球为中心）
        draw_orbit(screen, int(earth.x), int(earth.y), MOON_ORBIT_RADIUS)

        # 显示说明文字
        font = get_font(24)
        instructions = [
            "太阳系局部模型",
            "太阳（黄色） - 中心恒星",
            "地球（蓝色） - 绕太阳公转",
            "金星（金色） - 绕太阳公转",
            "月球（白色） - 绕地球公转",
            "按ESC键或关闭窗口退出"
        ]

        for i, text in enumerate(instructions):
            rendered = font.render(text, True, WHITE)
            screen.blit(rendered, (20, 20 + i * 30))

        # 显示帧率
        fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, WHITE)
        screen.blit(fps_text, (SCREEN_WIDTH - 100, 20))

        # 刷新屏幕
        pygame.display.flip()

        # 控制帧率
        clock.tick(FPS)

    # 退出游戏
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()