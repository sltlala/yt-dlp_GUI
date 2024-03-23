import os
import sys

from PySide6.QtWidgets import QApplication
from app.core.ui.main_window import MainWindow


def main():
    # 创建应用程序对象
    app = QApplication()

    # 创建主窗口
    main_window = MainWindow()

    # 显示主窗口
    main_window.show()
    # 运行应用程序
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
