"""
小球类 - 定义小球的属性和行为
"""
import pygame
import random
import math
from config import *

class Ball:
    def __init__(self, color_index):
        """
        初始化一个小球

        参数:
            color_index: 颜色索引，用于从BALL_COLORS中选择颜色
        """
        # 随机生成半径
        self.radius = random.randint(MIN_RADIUS, MAX_RADIUS)

        # 设置颜色
        self.color = BALL_COLORS[color_index % len(BALL_COLORS)]

        # 随机生成初始位置（确保不会在边界上）
        self.pos = [
            random.randint(self.radius, SCREEN_WIDTH - self.radius),
            random.randint(self.radius, SCREEN_HEIGHT - self.radius)
        ]

        # 随机生成初始速度
        speed = random.uniform(MIN_SPEED, MAX_SPEED)
        angle = random.uniform(0, 2 * math.pi)
        self.vel = [speed * math.cos(angle), speed * math.sin(angle)]

        # 计算质量（与半径平方成正比）
        self.mass = self.radius ** 2

    def update(self):
        """更新小球状态：应用布朗运动并更新位置"""
        # 布朗运动：给速度添加随机扰动
        self.vel[0] += random.uniform(-BROWNIAN_RANGE, BROWNIAN_RANGE)
        self.vel[1] += random.uniform(-BROWNIAN_RANGE, BROWNIAN_RANGE)

        # 限制最大速度，防止数值过大
        speed = math.sqrt(self.vel[0]**2 + self.vel[1]**2)
        if speed > MAX_SPEED * 2:
            scale = MAX_SPEED * 2 / speed
            self.vel[0] *= scale
            self.vel[1] *= scale

        # 更新位置
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

    def check_boundary(self):
        """检查并处理边界碰撞（完全弹性反弹）"""
        # 检查左右边界
        if self.pos[0] - self.radius <= 0:  # 左边界
            self.pos[0] = self.radius  # 调整位置防止卡在边界外
            self.vel[0] = abs(self.vel[0])  # 向右反弹
        elif self.pos[0] + self.radius >= SCREEN_WIDTH:  # 右边界
            self.pos[0] = SCREEN_WIDTH - self.radius
            self.vel[0] = -abs(self.vel[0])  # 向左反弹

        # 检查上下边界
        if self.pos[1] - self.radius <= 0:  # 上边界
            self.pos[1] = self.radius
            self.vel[1] = abs(self.vel[1])  # 向下反弹
        elif self.pos[1] + self.radius >= SCREEN_HEIGHT:  # 下边界
            self.pos[1] = SCREEN_HEIGHT - self.radius
            self.vel[1] = -abs(self.vel[1])  # 向上反弹

    def check_collision(self, other):
        """
        检测与另一个小球是否发生碰撞

        参数:
            other: 另一个Ball对象

        返回:
            bool: 是否发生碰撞
        """
        # 计算圆心距离
        dx = self.pos[0] - other.pos[0]
        dy = self.pos[1] - other.pos[1]
        distance = math.sqrt(dx*dx + dy*dy)

        # 如果距离小于两球半径之和，则发生碰撞
        return distance < (self.radius + other.radius)

    def draw(self, screen):
        """在屏幕上绘制小球"""
        pygame.draw.circle(screen, self.color,
                          (int(self.pos[0]), int(self.pos[1])),
                          self.radius)

        # 可选：绘制小球轮廓，增加视觉效果
        pygame.draw.circle(screen, (255, 255, 255),
                          (int(self.pos[0]), int(self.pos[1])),
                          self.radius, 1)