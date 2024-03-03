import os
import sys

from PySide6 import QtWidgets, QtCore

from PySide6.QtCore import QTranslator, QDir
from PySide6.QtGui import QIcon, Qt, QAction, QFont, QScreen
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
    QFileDialog,
    QPlainTextEdit,
    QComboBox,
)

from app.core.utils import helper_functions
from app.core.ui import customized_class


styleFile = "./core/ui/resources/stylesheets/style.css"  # 样式表的路径
finalCommand = ""


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.setupGui()
        self.loadStyleSheet()
        self.status = self.statusBar()

    def setupGui(self):
        self.tabs = QTabWidget(parent=None)
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
        self.setFont(QFont("Microsoft YaHei UI", 12))
        self.setWindowIcon(QIcon("./core/ui/resources/icons/favicon.ico"))

    def loadStyleSheet(self):
        global styleFile
        try:
            with open(styleFile, "r", encoding="UTF-8") as style:
                self.setStyleSheet(style.read())
        except FileNotFoundError:
            QMessageBox.warning(
                self,
                title="主题载入错误",
                text="未能成功载入主题，请确保软件资源目录有 'style.css' 文件存在。",
            )
        except UnicodeDecodeError:
            self.status.showMessage("文件编码错误,请使用UTF8编码", 800)


"""
    def keyPressEvent(self, event) -> None:
        # 在按下 F5 的时候重载 style.css 主题
        if event.key() == Qt.Key.Key_F5:
            self.loadStyleSheet()
            self.status.showMessage("已成功更新主题", 800)
"""


class SystemTray(QSystemTrayIcon):
    def __init__(self, icon, mainWindow):
        super(SystemTray, self).__init__(icon)
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

        self.userPath = os.path.expanduser("~").replace("\\", "/")
        self.userVideoPath = self.userPath + "/Videos"
        self.userDownloadPath = self.userPath + "/Downloads"
        self.userDesktopPath = self.userPath + "/Desktop"

        self.setupGui()
        # self.initValue()

    def setupGui(self):
        # 下载链接输入
        if True:
            self.url_label = QLabel(self.tr("视频链接："))
            self.url_line_edit = customized_class.AutoPasteLineEdit()
            self.url_line_edit.setPlaceholderText(self.tr("输入要下载的视频链接"))
            self.url_line_edit.setToolTip(self.tr("输入要下载的视频链接"))
            self.url_line_edit.setMaxLength(100)
            self.url_line_edit.textChanged.connect(self.generateFinalCommand)
            self.download_button = QPushButton(self.tr("开始下载"))
            self.download_button.clicked.connect(self.runFinalCommandButtonClicked)

            self.download_hbox = QHBoxLayout()
            self.download_hbox.addWidget(self.url_label)
            self.download_hbox.addWidget(self.url_line_edit)
            self.download_hbox.addWidget(self.download_button)
            self.download_hbox_control = QWidget()
            self.download_hbox_control.setLayout(self.download_hbox)

        # 下载选项
        if True:
            # TODO：{
            #  --format ba+bv,b*
            #  --output -o '%(channel)s/%(title)s.%(ext)s'
            #  --merge-output-format MP4,MKV
            #  --cookies-from-browser chrome,edge,firefox
            #  --downloader
            #  --downloader-args aria2c:'-x 16 -k 1M'
            #  --download-dir D:/
            #  --paths
            #  --download-archive './%(channel)s/archive.txt'
            #  --proxy  http://127.0.0.1:3030/
            #  }

            # 保存路径选择框
            self.save_label = QLabel(self.tr("保存路径："))
            self.save_path_box = QComboBox()
            self.save_path_box.setEditable(True)
            self.save_path_box.setEditText(self.userVideoPath)
            self.save_path_box.setToolTip(self.tr("填入下载保存目录"))
            self.save_path_box.addItems(
                [self.userVideoPath, self.userPath, self.userDownloadPath, self.userDesktopPath]
            )

            self.save_path_box.currentTextChanged.connect(self.generateFinalCommand)
            # self.save_path_box.textChanged.connect(self.generateFinalCommand)
            self.select_dir_button = QPushButton(self.tr("选择目录"))
            self.select_dir_button.clicked.connect(self.chooseDirButtonClicked)

            self.select_dir_hbox = QHBoxLayout()
            self.select_dir_hbox.addWidget(self.save_label)
            self.select_dir_hbox.addWidget(self.save_path_box)
            self.select_dir_hbox.addWidget(self.select_dir_button)
            self.select_dir_hbox_control = QWidget()
            self.select_dir_hbox_control.setLayout(self.select_dir_hbox)

        if True:
            self.final_command_label = QLabel(self.tr("总命令："))
            self.final_command_text_edit = QPlainTextEdit()
            self.final_command_text_edit.setReadOnly(True)

        self.top_widget_hbox = QVBoxLayout()
        self.top_widget_hbox.addWidget(self.download_hbox_control)
        self.top_widget_hbox.addWidget(self.select_dir_hbox_control)
        self.setLayout(self.top_widget_hbox)

    @QtCore.Slot()
    def generateFinalCommand(self):
        print("generateFinalCommand")
        return None

    # 选择文件夹
    @QtCore.Slot()
    def chooseDirButtonClicked(self):
        default_directory = QDir.homePath() + "/videos"
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹", default_directory)
        if folder_path != "":
            self.save_path_box.setEditText(folder_path)
        return folder_path

    @QtCore.Slot()
    # 点击运行按钮
    def runFinalCommandButtonClicked(self):
        return None


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
