"""
程序入口模块
"""
import sys
from PyQt6.QtWidgets import QApplication
from player_window import PlayerWindow


def main():
    """主函数"""
    # 创建Qt应用
    app = QApplication(sys.argv)

    # 创建并显示主窗口
    window = PlayerWindow()
    window.show()

    # 运行应用
    sys.exit(app.exec())


if __name__ == "__main__":
    main()