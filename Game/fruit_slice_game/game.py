# -*- coding: utf-8 -*-
"""
游戏主逻辑类
管理游戏状态、精灵组、碰撞检测和渲染
"""

import pygame
import random
import os
from sprites.fruit import Fruit
from sprites.particle import Particle

class Game:
    def __init__(self):
        """初始化游戏"""
        # 游戏窗口设置
        self.WIDTH = 800
        self.HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Fruit Slice Game")

        # 游戏时钟
        self.clock = pygame.time.Clock()
        self.FPS = 60

        # 游戏状态
        self.running = True
        self.score = 0

        # 精灵组
        self.all_sprites = pygame.sprite.Group()
        self.fruits = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()

        # 资源加载
        self.load_assets()

        # 游戏计时器
        self.fruit_timer = 0
        self.fruit_spawn_interval = 0  # 初始为0，立即生成第一个水果

        # 鼠标轨迹记录（用于碰撞检测）
        self.last_mouse_pos = pygame.mouse.get_pos()

        # 字体
        self.font = pygame.font.SysFont('Arial', 36)

        # 游戏背景色
        self.bg_color = (0, 0, 0)

    def load_assets(self):
        """加载游戏资源"""
        # 确保assets目录存在
        assets_dir = "assets"
        if not os.path.exists(assets_dir):
            os.makedirs(os.path.join(assets_dir, "images"))
            os.makedirs(os.path.join(assets_dir, "sounds"))
            print("请将图片文件放入 assets/images/ 目录")
            print("请将音效文件放入 assets/sounds/ 目录")

        # 加载水果图片
        self.fruit_images = {}
        fruit_types = ['apple', 'banana', 'pineapple']

        for fruit_type in fruit_types:
            try:
                img_path = os.path.join(assets_dir, "images", f"{fruit_type}.png")
                image = pygame.image.load(img_path).convert_alpha()
                # 缩放图片到合适大小（假设原始图片较大）
                image = pygame.transform.scale(image, (60, 60))
                self.fruit_images[fruit_type] = image
            except FileNotFoundError:
                print(f"警告: 找不到图片 {fruit_type}.png，将使用替代图形")
                # 创建替代图形
                surf = pygame.Surface((60, 60), pygame.SRCALPHA)
                color_map = {
                    'apple': (255, 50, 50),
                    'banana': (255, 255, 100),
                    'pineapple': (200, 180, 50)
                }
                color = color_map.get(fruit_type, (255, 255, 255))
                pygame.draw.circle(surf, color, (30, 30), 25)
                pygame.draw.circle(surf, (color[0]//2, color[1]//2, color[2]//2), (30, 30), 25, 2)
                self.fruit_images[fruit_type] = surf

        # 加载音效
        try:
            sound_path = os.path.join(assets_dir, "sounds", "slice_sound.mp3")
            self.slice_sound = pygame.mixer.Sound(sound_path)
            self.slice_sound.set_volume(0.3)
        except FileNotFoundError:
            print("警告: 找不到音效文件 slice_sound.mp3")
            # 创建替代音效（一个简单的哔声）
            self.slice_sound = None

    def spawn_fruit(self):
        """生成新的水果"""
        # 随机选择水果类型
        fruit_type = random.choice(list(self.fruit_images.keys()))

        # 随机水平位置（确保水果完全在屏幕内）
        fruit_width = self.fruit_images[fruit_type].get_width()
        x = random.randint(fruit_width, self.WIDTH - fruit_width)

        # 创建水果实例
        fruit = Fruit(x, 0, fruit_type, self.fruit_images[fruit_type])

        # 添加到精灵组
        self.all_sprites.add(fruit)
        self.fruits.add(fruit)

        # 重置生成计时器
        self.fruit_spawn_interval = random.uniform(0.5, 1.5) * 1000  # 转换为毫秒

    def check_collisions(self):
        """检测鼠标与水果的碰撞"""
        current_mouse_pos = pygame.mouse.get_pos()

        # 如果鼠标移动了，检测碰撞
        if current_mouse_pos != self.last_mouse_pos:
            # 创建从上一帧到当前帧的线段
            # 为了简化，我们检测鼠标当前位置与水果的碰撞
            # 更精确的实现可以检测线段与水果的碰撞

            # 获取鼠标按下的状态
            mouse_pressed = pygame.mouse.get_pressed()

            # 只有当鼠标左键按下时才检测碰撞（模拟切的动作）
            if mouse_pressed[0]:
                # 检测鼠标当前位置与所有水果的碰撞
                for fruit in self.fruits:
                    if fruit.rect.collidepoint(current_mouse_pos):
                        # 切中水果
                        self.score += 1
                        fruit.slice(self)

                        # 播放音效
                        if self.slice_sound:
                            self.slice_sound.play()

                        break  # 一次只切一个水果

        # 更新上一帧鼠标位置
        self.last_mouse_pos = current_mouse_pos

    def update(self):
        """更新游戏状态"""
        # 更新水果生成计时器
        self.fruit_timer += self.clock.get_time()
        if self.fruit_timer >= self.fruit_spawn_interval:
            self.spawn_fruit()
            self.fruit_timer = 0

        # 更新所有精灵
        self.all_sprites.update(self)

        # 检测碰撞
        self.check_collisions()

    def draw(self):
        """绘制游戏画面"""
        # 清屏
        self.screen.fill(self.bg_color)

        # 绘制所有精灵
        self.all_sprites.draw(self.screen)

        # 绘制分数
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

        # 绘制操作提示
        hint_font = pygame.font.SysFont('Arial', 20)
        hint_text = hint_font.render("按住鼠标左键并移动来切水果", True, (200, 200, 200))
        self.screen.blit(hint_text, (10, self.HEIGHT - 30))

        # 更新显示
        pygame.display.flip()

    def handle_events(self):
        """处理游戏事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def run(self):
        """运行游戏主循环"""
        # 立即生成第一个水果
        self.spawn_fruit()

        # 游戏主循环
        while self.running:
            # 处理事件
            self.handle_events()

            # 更新游戏状态
            self.update()

            # 绘制游戏画面
            self.draw()

            # 控制帧率
            self.clock.tick(self.FPS)