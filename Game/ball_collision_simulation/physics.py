"""
物理计算模块 - 处理弹性碰撞的物理计算
"""
import math

def elastic_collision(ball1, ball2):
    """
    计算两个小球之间的完全弹性碰撞

    参数:
        ball1, ball2: 两个Ball对象

    返回:
        更新两个小球的速度向量
    """
    # 计算两球之间的向量
    dx = ball2.pos[0] - ball1.pos[0]
    dy = ball2.pos[1] - ball1.pos[1]
    distance = math.sqrt(dx*dx + dy*dy)

    # 避免除零错误
    if distance == 0:
        return

    # 归一化碰撞法向量
    nx = dx / distance
    ny = dy / distance

    # 计算切向量（垂直于法向量）
    tx = -ny
    ty = nx

    # 将速度分解为法向和切向分量
    # 球1的速度分解
    v1n = ball1.vel[0] * nx + ball1.vel[1] * ny
    v1t = ball1.vel[0] * tx + ball1.vel[1] * ty

    # 球2的速度分解
    v2n = ball2.vel[0] * nx + ball2.vel[1] * ny
    v2t = ball2.vel[0] * tx + ball2.vel[1] * ty

    # 计算质量（假设质量与半径平方成正比）
    m1 = ball1.radius ** 2
    m2 = ball2.radius ** 2

    # 一维弹性碰撞公式计算新的法向速度
    v1n_new = (v1n * (m1 - m2) + 2 * m2 * v2n) / (m1 + m2)
    v2n_new = (v2n * (m2 - m1) + 2 * m1 * v1n) / (m1 + m2)

    # 切向速度保持不变
    v1t_new = v1t
    v2t_new = v2t

    # 将新的法向和切向速度合成新的速度向量
    # 球1的新速度
    ball1.vel[0] = v1n_new * nx + v1t_new * tx
    ball1.vel[1] = v1n_new * ny + v1t_new * ty

    # 球2的新速度
    ball2.vel[0] = v2n_new * nx + v2t_new * tx
    ball2.vel[1] = v2n_new * ny + v2t_new * ty

    # 分离小球，防止重叠
    overlap = ball1.radius + ball2.radius - distance
    if overlap > 0:
        separation = overlap / 2
        ball1.pos[0] -= nx * separation
        ball1.pos[1] -= ny * separation
        ball2.pos[0] += nx * separation
        ball2.pos[1] += ny * separation