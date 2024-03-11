import os
import sys

from PySide6 import QtWidgets
from PySide6.QtGui import QFont, QIcon
from PySide6.QtWidgets import QApplication
from app.core.ui.main_window import MainWindow, SystemTray

from app.core.database import Database


def main():
    # 创建应用程序对象
    app = QApplication()

    try:
        os.chdir(os.path.dirname(__file__))
        print("更改工作目录成功", os.path.dirname(__file__))
    except FileNotFoundError:
        print("更改工作目录失败")

    # 创建主窗口
    main_window = MainWindow()

    # 显示主窗口
    main_window.show()
    SystemTray(QIcon("./core/ui/resources/icons/icon.ico"), main_window)
    # 运行应用程序
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
