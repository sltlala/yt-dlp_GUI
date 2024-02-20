import sys

from PySide6 import QtWidgets
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication
from app.core.ui.main_window import MainWindow  # 导入你的主窗口类
from qt_material import apply_stylesheet


def main():
    # 创建应用程序对象
    app = QApplication(sys.argv)

    # 创建主窗口
    main_window = MainWindow()
    # print(QtWidgets.QStyleFactory.keys())
    extra = {
        # Font
        "font_family": "monospace",
        "font_size": "16px",
        "line_height": "13px",
        # Density Scale
        "density_scale": "4",
        # environ
        "pyside6": True,
    }

    apply_stylesheet(app, theme="light_blue.xml", invert_secondary=False, extra=extra)
    app.setFont(QFont("Microsoft YaHei UI", 14))

    # 显示主窗口
    main_window.show()

    # 运行应用程序
    app.exec()


if __name__ == "__main__":
    main()
