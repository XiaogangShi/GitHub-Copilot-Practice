#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
切水果游戏 - 主程序入口
启动游戏并运行主循环
"""

import pygame
import sys
from game import Game

def main():
    """游戏主函数"""
    # 初始化pygame
    pygame.init()

    # 创建游戏实例
    game = Game()

    try:
        # 运行游戏主循环
        game.run()
    except Exception as e:
        print(f"游戏运行出错: {e}")
    finally:
        # 退出游戏
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()