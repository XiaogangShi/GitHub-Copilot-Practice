"""
音频控制器模块
封装Pygame的音频操作，提供稳定的控制接口
"""
import pygame
import os


class AudioController:
    """音频控制器类，负责管理Pygame音频操作"""

    def __init__(self):
        """初始化音频控制器"""
        pygame.mixer.init()
        self.current_file = None  # 当前加载的文件路径
        self.is_playing = False   # 是否正在播放
        self.is_paused = False    # 是否已暂停

    def load(self, file_path):
        """
        加载音频文件

        Args:
            file_path: 音频文件路径

        Returns:
            bool: 加载是否成功
        """
        try:
            # 如果当前有音频在播放，先停止
            if pygame.mixer.music.get_busy():
                self.stop()

            # 加载新文件
            pygame.mixer.music.load(file_path)
            self.current_file = file_path
            self.is_playing = False
            self.is_paused = False
            return True
        except Exception as e:
            print(f"加载文件失败: {e}")
            return False

    def play(self):
        """开始播放音频"""
        if self.current_file:
            pygame.mixer.music.play()
            self.is_playing = True
            self.is_paused = False

    def pause(self):
        """暂停播放"""
        if self.is_playing and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True

    def unpause(self):
        """继续播放"""
        if self.is_playing and self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False

    def stop(self):
        """停止播放并重置到开头"""
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False

    def get_length(self):
        """
        获取音频总长度（秒）

        Returns:
            float: 音频总长度（秒），失败返回0
        """
        try:
            # 使用pygame.mixer.Sound获取音频长度
            if self.current_file:
                sound = pygame.mixer.Sound(self.current_file)
                return sound.get_length()
        except Exception as e:
            print(f"获取音频长度失败: {e}")
        return 0

    def get_pos(self):
        """
        获取当前播放位置（秒）

        Returns:
            float: 当前播放位置（秒）
        """
        # pygame.mixer.music.get_pos()返回毫秒
        return pygame.mixer.music.get_pos() / 1000.0

    def cleanup(self):
        """清理资源"""
        self.stop()
        pygame.mixer.quit()