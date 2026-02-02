"""
主程序 - 模拟程序的入口点
"""
import pygame
import sys
import random
from config import *
from ball import Ball
from physics import elastic_collision

def initialize_pygame():
    """初始化Pygame"""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("像素级碰撞检测与弹性碰撞模拟")
    clock = pygame.time.Clock()
    return screen, clock

def create_balls():
    """创建指定数量的小球"""
    balls = []
    for i in range(NUM_BALLS):
        # 确保小球不会在初始位置就重叠
        while True:
            ball = Ball(i)

            # 检查新球是否与已有球重叠
            overlap = False
            for existing_ball in balls:
                if ball.check_collision(existing_ball):
                    overlap = True
                    break

            if not overlap:
                balls.append(ball)
                break

    return balls

def main():
    """主函数"""
    # 初始化Pygame
    screen, clock = initialize_pygame()

    # 创建小球
    balls = create_balls()

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
                elif event.key == pygame.K_r:
                    # 按R键重置模拟
                    balls = create_balls()
                elif event.key == pygame.K_SPACE:
                    # 按空格键暂停/继续
                    paused = not hasattr(main, 'paused')
                    main.paused = paused

        # 检查是否暂停
        if hasattr(main, 'paused') and main.paused:
            # 显示暂停提示
            font = pygame.font.Font(None, 36)
            text = font.render("模拟已暂停 (按空格键继续)", True, (255, 255, 255))
            screen.blit(text, (SCREEN_WIDTH//2 - 150, 20))
            pygame.display.flip()
            clock.tick(FPS)
            continue

        # 更新所有小球
        for ball in balls:
            ball.update()
            ball.check_boundary()

        # 检测并处理小球之间的碰撞
        for i in range(len(balls)):
            for j in range(i + 1, len(balls)):
                if balls[i].check_collision(balls[j]):
                    elastic_collision(balls[i], balls[j])

        # 绘制
        screen.fill(BACKGROUND_COLOR)

        # 绘制所有小球
        for ball in balls:
            ball.draw(screen)

        # 显示帧率和小球数量
        font = pygame.font.Font(None, 24)
        fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255))
        balls_text = font.render(f"小球数量: {len(balls)}", True, (255, 255, 255))
        controls_text = font.render("控制: R-重置 空格-暂停/继续 ESC-退出", True, (255, 255, 255))

        screen.blit(fps_text, (10, 10))
        screen.blit(balls_text, (10, 40))
        screen.blit(controls_text, (10, SCREEN_HEIGHT - 30))

        # 更新显示
        pygame.display.flip()

        # 控制帧率
        clock.tick(FPS)

    # 退出Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()