# particle_system.py - 粒子系统核心逻辑
import pygame
import random
import math

class Particle:
    """单个粒子类"""

    def __init__(self, pos, vel, color, size, lifetime, size_change=0, fade_out=True):
        """
        初始化粒子

        参数:
        pos: 初始位置 (x, y)
        vel: 初始速度 (vx, vy)
        color: 颜色 (r, g, b) 或 (r, g, b, a)
        size: 初始尺寸
        lifetime: 生命周期（秒）
        size_change: 尺寸变化率（像素/秒），正数表示增大，负数表示缩小
        fade_out: 是否淡出
        """
        self.pos = list(pos)  # 位置 [x, y]
        self.vel = list(vel)  # 速度 [vx, vy]
        self.color = color if len(color) == 4 else (*color, 255)  # 确保有alpha通道
        self.initial_color = self.color
        self.size = size
        self.initial_size = size
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size_change = size_change
        self.fade_out = fade_out

    def update(self, dt):
        """
        更新粒子状态

        参数:
        dt: 时间增量（秒）
        """
        # 更新位置
        self.pos[0] += self.vel[0] * dt * 60  # 乘以60转换为像素/帧
        self.pos[1] += self.vel[1] * dt * 60

        # 更新生命周期
        self.lifetime -= dt

        # 更新尺寸
        self.size += self.size_change * dt

        # 更新颜色透明度（淡出效果）
        if self.fade_out and self.lifetime > 0:
            alpha = int(255 * (self.lifetime / self.max_lifetime))
            self.color = (self.initial_color[0],
                         self.initial_color[1],
                         self.initial_color[2],
                         alpha)

        # 返回粒子是否还存活
        return self.lifetime > 0 and self.size > 0

    def draw(self, surface):
        """在指定Surface上绘制粒子"""
        if self.size > 0:
            # 创建临时颜色，确保alpha值有效
            draw_color = (self.color[0], self.color[1], self.color[2],
                         max(0, min(255, self.color[3])))

            # 绘制圆形粒子
            pygame.draw.circle(
                surface,
                draw_color,
                (int(self.pos[0]), int(self.pos[1])),
                max(1, int(self.size))
            )

class ParticleEmitter:
    """粒子发射器类，管理一次爆炸的所有粒子"""

    def __init__(self):
        """初始化发射器"""
        self.particles = []  # 所有活跃粒子列表
        self.is_active = False

    def trigger(self, pos):
        """
        在指定位置触发爆炸效果

        参数:
        pos: 爆炸位置 (x, y)
        """
        # 阶段一：闪光
        self._create_flash(pos)

        # 阶段二：火星
        self._create_sparks(pos)

        # 阶段三：烟雾
        self._create_smoke(pos)

        self.is_active = True

    def _create_flash(self, pos):
        """创建闪光粒子"""
        # 创建1个白色大圆粒子，生命周期极短
        flash_particle = Particle(
            pos=pos,
            vel=(0, 0),  # 静止
            color=(255, 255, 255, 255),  # 纯白色
            size=30,  # 初始尺寸较大
            lifetime=0.05,  # 约3帧（60FPS）
            size_change=-600,  # 快速缩小
            fade_out=True
        )
        self.particles.append(flash_particle)

    def _create_sparks(self, pos):
        """创建火星粒子"""
        num_sparks = random.randint(120, 150)  # 火星数量

        for _ in range(num_sparks):
            # 随机方向（0-360度）
            angle = random.uniform(0, 2 * math.pi)

            # 随机速度大小（较快）
            speed = random.uniform(200, 400)

            # 计算速度向量
            vel_x = math.cos(angle) * speed
            vel_y = math.sin(angle) * speed

            # 随机颜色（橙黄色系）
            r = random.randint(200, 255)
            g = random.randint(100, 180)
            b = random.randint(0, 80)

            # 创建火星粒子
            spark = Particle(
                pos=pos,
                vel=(vel_x, vel_y),
                color=(r, g, b, 255),
                size=random.uniform(3, 5),
                lifetime=random.uniform(0.5, 1.0),  # 生命周期较短
                size_change=-4,  # 逐渐缩小
                fade_out=True
            )
            self.particles.append(spark)

    def _create_smoke(self, pos):
        """创建烟雾粒子"""
        num_smoke = random.randint(20, 50)  # 烟雾数量

        for _ in range(num_smoke):
            # 主要向上运动，带有随机水平偏移
            vel_x = random.uniform(-20, 20)  # 水平随机偏移
            vel_y = random.uniform(-80, -40)  # 向上运动

            # 灰色，半透明
            gray_value = random.randint(80, 120)
            alpha = random.randint(100, 180)

            # 创建烟雾粒子
            smoke = Particle(
                pos=pos,
                vel=(vel_x, vel_y),
                color=(gray_value, gray_value, gray_value, alpha),
                size=random.uniform(8, 12),
                lifetime=random.uniform(1.5, 2.5),  # 生命周期较长
                size_change=5,  # 缓慢增大
                fade_out=True
            )
            self.particles.append(smoke)

    def update(self, dt):
        """更新所有粒子"""
        # 更新每个粒子，移除已死亡的粒子
        self.particles = [p for p in self.particles if p.update(dt)]

        # 如果没有活跃粒子，标记为非活跃状态
        if not self.particles:
            self.is_active = False

    def draw(self, surface):
        """绘制所有粒子"""
        # 为了正确的混合效果，按尺寸从大到小排序绘制
        sorted_particles = sorted(self.particles, key=lambda p: p.size, reverse=True)

        for particle in sorted_particles:
            particle.draw(surface)