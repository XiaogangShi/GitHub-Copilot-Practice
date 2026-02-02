"""
主窗口模块
实现播放器的GUI界面和主要逻辑
"""
import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QProgressBar, QFileDialog,
    QMessageBox
)
from PyQt6.QtCore import QTimer, Qt
from audio_controller import AudioController


class PlayerWindow(QMainWindow):
    """播放器主窗口类"""

    def __init__(self):
        """初始化主窗口"""
        super().__init__()
        self.audio_ctrl = AudioController()  # 音频控制器
        self.update_timer = QTimer()         # 更新UI的定时器

        self._setup_ui()      # 设置UI
        self._connect_signals()  # 连接信号
        self._set_button_states('unloaded')  # 初始状态

        self.setWindowTitle("简易MP3播放器")
        self.resize(500, 200)

    def _setup_ui(self):
        """设置用户界面"""
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局（垂直）
        main_layout = QVBoxLayout(central_widget)

        # 1. 控制按钮区域（水平布局）
        control_layout = QHBoxLayout()

        # 创建四个控制按钮
        self.open_btn = QPushButton("打开")
        self.play_btn = QPushButton("播放")
        self.pause_btn = QPushButton("暂停")
        self.stop_btn = QPushButton("停止")

        # 设置按钮固定宽度
        for btn in [self.open_btn, self.play_btn, self.pause_btn, self.stop_btn]:
            btn.setFixedWidth(80)

        # 将按钮添加到控制布局
        control_layout.addWidget(self.open_btn)
        control_layout.addWidget(self.play_btn)
        control_layout.addWidget(self.pause_btn)
        control_layout.addWidget(self.stop_btn)
        control_layout.addStretch()  # 添加弹性空间

        # 2. 信息显示区域
        # 文件名标签
        self.filename_label = QLabel("当前播放：无")
        self.filename_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

        # 时间标签
        self.time_label = QLabel("00:00 / 00:00")
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 将所有部件添加到主布局
        main_layout.addLayout(control_layout)
        main_layout.addWidget(self.filename_label)
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(self.time_label)
        main_layout.addStretch()  # 添加弹性空间

    def _connect_signals(self):
        """连接信号和槽函数"""
        # 按钮点击信号
        self.open_btn.clicked.connect(self._on_open_clicked)
        self.play_btn.clicked.connect(self._on_play_clicked)
        self.pause_btn.clicked.connect(self._on_pause_clicked)
        self.stop_btn.clicked.connect(self._on_stop_clicked)

        # 定时器信号
        self.update_timer.timeout.connect(self._update_ui)

    def _on_open_clicked(self):
        """处理打开按钮点击事件"""
        # 弹出文件选择对话框
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择MP3文件",
            "",
            "MP3文件 (*.mp3);;所有文件 (*.*)"
        )

        if file_path:  # 用户选择了文件
            # 尝试加载文件
            if self.audio_ctrl.load(file_path):
                # 更新文件名显示
                filename = os.path.basename(file_path)
                self.filename_label.setText(f"当前播放：{filename}")

                # 更新按钮状态为"已加载"
                self._set_button_states('loaded')

                # 重置进度条和时间显示
                self.progress_bar.setValue(0)
                self._update_time_display(0, self.audio_ctrl.get_length())
            else:
                # 文件加载失败
                QMessageBox.critical(
                    self,
                    "错误",
                    "无法加载文件。请确保文件是有效的MP3格式且未损坏。"
                )

    def _on_play_clicked(self):
        """处理播放按钮点击事件"""
        if not self.audio_ctrl.is_playing:
            self.audio_ctrl.play()
            self._set_button_states('playing')

            # 启动定时器更新UI
            self.update_timer.start(200)  # 每200ms更新一次

    def _on_pause_clicked(self):
        """处理暂停/继续按钮点击事件"""
        if self.audio_ctrl.is_playing:
            if not self.audio_ctrl.is_paused:
                # 当前正在播放，点击后暂停
                self.audio_ctrl.pause()
                self._set_button_states('paused')
                self.update_timer.stop()  # 停止定时器
            else:
                # 当前已暂停，点击后继续
                self.audio_ctrl.unpause()
                self._set_button_states('playing')
                self.update_timer.start(200)  # 重新启动定时器

    def _on_stop_clicked(self):
        """处理停止按钮点击事件"""
        self.audio_ctrl.stop()
        self._set_button_states('loaded')

        # 停止定时器
        self.update_timer.stop()

        # 重置进度显示
        self.progress_bar.setValue(0)
        total_length = self.audio_ctrl.get_length()
        self._update_time_display(0, total_length)

    def _update_ui(self):
        """更新UI显示（由定时器触发）"""
        if self.audio_ctrl.is_playing:
            current_pos = self.audio_ctrl.get_pos()
            total_length = self.audio_ctrl.get_length()

            # 更新进度条
            if total_length > 0:
                progress = int((current_pos / total_length) * 100)
                self.progress_bar.setValue(progress)

            # 更新时间显示
            self._update_time_display(current_pos, total_length)

            # 检查是否播放结束
            if current_pos >= total_length and total_length > 0:
                self._on_stop_clicked()

    def _update_time_display(self, current_pos, total_length):
        """
        更新时间显示标签

        Args:
            current_pos: 当前播放位置（秒）
            total_length: 音频总长度（秒）
        """
        # 格式化当前时间
        current_min = int(current_pos // 60)
        current_sec = int(current_pos % 60)
        current_str = f"{current_min:02d}:{current_sec:02d}"

        # 格式化总时间
        total_min = int(total_length // 60)
        total_sec = int(total_length % 60)
        total_str = f"{total_min:02d}:{total_sec:02d}"

        # 更新标签
        self.time_label.setText(f"{current_str} / {total_str}")

    def _set_button_states(self, state):
        """
        根据状态设置按钮的启用状态和文本

        Args:
            state: 状态字符串，可选值：
                  'unloaded' - 未加载
                  'loaded'   - 已加载（未播放）
                  'playing'  - 播放中
                  'paused'   - 已暂停
        """
        # 打开按钮始终可用
        self.open_btn.setEnabled(True)

        if state == 'unloaded':
            # 初始/未加载状态
            self.play_btn.setEnabled(False)
            self.pause_btn.setEnabled(False)
            self.pause_btn.setText("暂停")
            self.stop_btn.setEnabled(False)

        elif state == 'loaded':
            # 已加载但未播放
            self.play_btn.setEnabled(True)
            self.pause_btn.setEnabled(False)
            self.pause_btn.setText("暂停")
            self.stop_btn.setEnabled(False)

        elif state == 'playing':
            # 播放中
            self.play_btn.setEnabled(False)
            self.pause_btn.setEnabled(True)
            self.pause_btn.setText("暂停")
            self.stop_btn.setEnabled(True)

        elif state == 'paused':
            # 已暂停
            self.play_btn.setEnabled(False)
            self.pause_btn.setEnabled(True)
            self.pause_btn.setText("继续")
            self.stop_btn.setEnabled(True)

    def closeEvent(self, event):
        """窗口关闭事件处理"""
        # 清理音频资源
        self.audio_ctrl.cleanup()
        event.accept()