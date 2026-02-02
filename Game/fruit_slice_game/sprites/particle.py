# -*- coding: utf-8 -*-
"""
粒子精灵类
管理粒子效果的行为和渲染
"""

import pygame
import random

class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity_x, velocity_y, color, size, lifetime):
        """初始化粒子"""
        super().__init__()

        # 粒子属性
        self.color = color
        self.size = size
        self.lifetime = lifetime * 1000  # 转换为毫秒
        self.age = 0

        # 运动参数
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.gravity = 0.2  # 重力效果
        self.friction = 0.98  # 阻力效果

        # 创建粒子表面
        self.image = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (size, size), size)

        # 设置矩形位置
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, game):
        """更新粒子状态"""
        # 更新年龄
        self.age += game.clock.get_time()

        # 检查粒子是否过期
        if self.age >= self.lifetime:
            self.kill()
            return

        # 应用阻力和重力
        self.velocity_x *= self.friction
        self.velocity_y *= self.friction
        self.velocity_y += self.gravity

        # 更新位置
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        # 计算透明度（根据剩余寿命）
        alpha = int(255 * (1 - self.age / self.lifetime))
        if alpha < 0:
            alpha = 0

        # 更新粒子透明度
        self.image.set_alpha(alpha)

        # 检查是否移出屏幕
        if (self.rect.right < 0 or self.rect.left > game.WIDTH or
            self.rect.bottom < 0 or self.rect.top > game.HEIGHT):
            self.kill()