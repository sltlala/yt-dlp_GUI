import os
import sys

from PySide6 import QtWidgets

from PySide6.QtCore import QTranslator
from PySide6.QtGui import QIcon, Qt, QAction, QFont
from PySide6.QtWidgets import (
    QMessageBox,
    QTabWidget,
    QSystemTrayIcon,
    QApplication,
    QMenu,
    QWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QPushButton,
)

from app.core.utils import helper_functions
from app.core.ui import customized_class

# from PySide6.QtGui import QIcon, QFont, QPixmap, QImage
# from PySide6.QtGui import QCursor, QKeySequence, QFontDatabase

styleFile = "./core/ui/resources/stylesheets/style.css"  # 样式表的路径
finalCommand = ""


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.tabs = None
        self.ytdlpMainTab = None
        self.configTab = None
        self.helpTab = None
        self.setupGui()
        self.loadStyleSheet()

    def setupGui(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.resize(600, 600)
        self.setMinimumSize(500, 500)
        self.setMaximumSize(750, 600)

        self.ytdlpMainTab = YtdlpMainTab()  # 主界面
        self.configTab = ConfigTab()  # 配置界面
        self.helpTab = HelpTab()  # 帮助界面

        self.tabs.addTab(self.ytdlpMainTab, "yt-dlp")
        self.tabs.addTab(self.configTab, "设置")
        self.tabs.addTab(self.helpTab, "帮助")

        self.setWindowTitle("yt-dlp_GUI")
        self.setFont(QFont("Microsoft YaHei UI", 10))
        self.setWindowIcon(QIcon("./core/ui/resources/icons/favicon.ico"))

    def loadStyleSheet(self):
        global styleFile
        try:
            with open(styleFile, "r", encoding="UTF-8") as style:
                self.setStyleSheet(style.read())
        except FileNotFoundError:
            QMessageBox.warning(
                self,
                "主题载入错误",
                "未能成功载入主题，请确保软件资源目录有 'style.css' 文件存在。",
            )
        except UnicodeDecodeError:
            self.statusBar().showMessage("文件编码错误,请使用UTF8编码", 800)


"""
    def keyPressEvent(self, event) -> None:
        # 在按下 F5 的时候重载 style.css 主题
        if event.key() == Qt.Key.Key_F5:
            self.loadStyleSheet()
            self.statusBar().showMessage("已成功更新主题", 800)
"""


class SystemTray(QSystemTrayIcon):
    def __init__(self, icon, mainWindow):
        super(SystemTray, self).__init__()
        self.window = mainWindow
        self.setIcon(icon)
        self.setParent(mainWindow)
        self.activated.connect(self.trayEvent)  # 设置托盘点击事件处理函数
        self.tray_menu = QMenu()  # 创建菜单
        # 添加一级菜单动作选项(还原主窗口)

        self.QuitAction = QAction(
            self.tr("退出"), self, triggered=self.quit
        )  # 添加一级菜单动作选项(退出程序)
        self.StyleAction = QAction(
            self.tr("更新主题"), self, triggered=mainWindow.loadStyleSheet
        )  # 添加一级菜单动作选项(更新 QSS)
        self.tray_menu.addAction(self.QuitAction)
        self.tray_menu.addAction(self.StyleAction)
        self.setContextMenu(self.tray_menu)  # 设置系统托盘菜单
        self.show()

    def showWindow(self):
        self.window.showNormal()
        self.window.activateWindow()
        # self.window.setWindowFlags(Qt.Window)
        self.window.show()

    def quit(self):
        sys.stdout = sys.__stdout__
        self.hide()
        QApplication.quit()

    def trayEvent(self, reason):
        # 鼠标点击icon传递的信号会带有一个整形的值，
        # 1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击
        if reason == 2 or reason == 3:
            if MainWindow.isMinimized() or not MainWindow.isVisible():
                # 若是最小化或者最小化到托盘，则先正常显示窗口，再变为活动窗口（暂时显示在最前面）
                self.window.showNormal()
                self.window.activateWindow()
                # self.window.setWindowFlags(Qt.Window)
                self.window.show()
            else:
                # 若不是最小化，则最小化
                # self.window.showMinimized()
                # self.window.show()
                pass


class YtdlpMainTab(QWidget):
    def __init__(self):
        super().__init__()
        self.download_button = None
        self.download_vbox = None
        self.url_line_edit = None
        self.url_label = None
        self.download_vbox_control = None
        self.top_widget_hbox = None
        self.main_widget = None
        self.setupGui()
        # self.initValue()

    def setupGui(self):
        self.download_vbox = QHBoxLayout()
        self.url_label = QLabel(self.tr("视频链接："))
        self.url_line_edit = customized_class.AutoPasteLineEdit()
        self.url_line_edit.setPlaceholderText(self.tr("输入要下载的视频链接"))
        self.url_line_edit.setToolTip(self.tr("输入要下载的视频链接"))

        self.download_button = QPushButton(self.tr("开始下载"))
        self.download_button.clicked.connect(helper_functions.generateFinalCommand(self))

        self.download_vbox.addWidget(self.url_label)
        self.download_vbox.addWidget(self.url_line_edit)
        self.download_vbox.addWidget(self.download_button)
        self.download_vbox_control = QWidget()
        self.download_vbox_control.setLayout(self.download_vbox)

        # self.main_widget = QVBoxLayout()
        # self.main_widget.addLayout(self.download_vbox)
        self.top_widget_hbox = QVBoxLayout()
        self.top_widget_hbox.addWidget(self.download_vbox_control)
        self.setLayout(self.top_widget_hbox)


class ConfigTab(QWidget):
    def __init__(self):
        super().__init__()
        self.config_vbox = None
        self.setupGui()
        # self.initValue()

    def setupGui(self):
        self.config_vbox = QVBoxLayout()


class HelpTab(QWidget):
    def __init__(self):
        super().__init__()
        self.help_vbox = None
        self.setupGui()
        # self.initValue()

    def setupGui(self):
        self.help_vbox = QVBoxLayout()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
