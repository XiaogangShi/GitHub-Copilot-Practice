# -*- coding: utf-8 -*-
"""
水果精灵类
管理水果的生成、运动和被切中的行为
"""

import pygame
import random
from sprites.particle import Particle

class Fruit(pygame.sprite.Sprite):
    def __init__(self, x, y, fruit_type, image):
        """初始化水果"""
        super().__init__()

        # 水果类型和图像
        self.fruit_type = fruit_type
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # 运动参数
        self.velocity_y = 2.0  # 初始下落速度
        self.acceleration = 0.1  # 重力加速度

        # 水果颜色映射（用于粒子效果）
        self.color_map = {
            'apple': (255, 50, 50),      # 红色
            'banana': (255, 255, 100),   # 黄色
            'pineapple': (200, 180, 50)  # 黄绿色
        }

    def update(self, game):
        """更新水果状态"""
        # 应用重力加速度
        self.velocity_y += self.acceleration

        # 更新位置
        self.rect.y += self.velocity_y

        # 检查是否移出屏幕底部
        if self.rect.top > game.HEIGHT:
            self.kill()

    def slice(self, game):
        """切碎水果"""
        # 生成粒子效果
        particle_color = self.color_map.get(self.fruit_type, (255, 255, 255))
        self.create_particles(game, particle_color)

        # 移除水果
        self.kill()

    def create_particles(self, game, color):
        """创建粒子爆炸效果"""
        # 生成15-25个粒子
        particle_count = random.randint(15, 25)

        for _ in range(particle_count):
            # 粒子初始位置在水果中心
            x, y = self.rect.center

            # 随机方向（360度）
            angle = random.uniform(0, 2 * 3.14159)

            # 随机速度
            speed = random.uniform(2, 6)

            # 计算速度向量
            velocity_x = speed * pygame.math.Vector2(1, 0).rotate_rad(angle).x
            velocity_y = speed * pygame.math.Vector2(1, 0).rotate_rad(angle).y

            # 随机粒子大小
            size = random.randint(3, 8)

            # 随机粒子寿命
            lifetime = random.uniform(0.5, 1.5)

            # 创建粒子
            particle = Particle(x, y, velocity_x, velocity_y, color, size, lifetime)

            # 添加到精灵组
            game.all_sprites.add(particle)
            game.particles.add(particle)