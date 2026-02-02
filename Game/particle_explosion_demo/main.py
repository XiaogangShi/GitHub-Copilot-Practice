# main.py - 程序主入口
import pygame
import sys
from particle_system import ParticleEmitter

def main():
    # 初始化Pygame
    pygame.init()

    # 设置窗口
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("粒子爆炸演示")

    # 创建时钟对象控制帧率
    clock = pygame.time.Clock()
    FPS = 60

    # 加载音效
    try:
        explosion_sound = pygame.mixer.Sound("assets/sounds/explosion.wav")
    except FileNotFoundError:
        print("警告: 未找到音效文件 assets/sounds/explosion.wav")
        print("请确保音效文件存在，或注释掉音效播放代码")
        explosion_sound = None

    # 创建粒子发射器
    emitter = ParticleEmitter()

    # 主循环
    running = True
    while running:
        # 计算时间增量（秒）
        dt = clock.tick(FPS) / 1000.0

        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 鼠标左键
                    # 触发粒子爆炸
                    emitter.trigger(event.pos)

                    # 播放爆炸音效
                    if explosion_sound:
                        explosion_sound.play()

        # 清屏为黑色
        screen.fill((0, 0, 0))

        # 更新并绘制粒子系统
        emitter.update(dt)
        emitter.draw(screen)

        # 更新显示
        pygame.display.flip()

    # 退出程序
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()