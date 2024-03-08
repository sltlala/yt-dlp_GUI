import os
import sys

from PySide6 import QtWidgets, QtCore

from PySide6.QtCore import QTranslator, QDir, Qt, QSize
from PySide6.QtGui import QIcon, QAction, QFont, QScreen
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
    QSizePolicy,
    QListWidget,
    QGridLayout,
    QSplitter,
    QLineEdit,
    QCheckBox,
    QFormLayout,
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
        self.adjustSize()
        self.resize(700, 600)
        # self.setMinimumSize(500, 500)
        # self.setMaximumSize(750, 600)

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
                title="主题载入错误",
                text="未能成功载入主题，请确保软件资源目录有 'style.css' 文件存在。",
            )
        except UnicodeDecodeError:
            self.status.showMessage("文件编码错误,请使用UTF8编码", 800)

    def keyPressEvent(self, event) -> None:
        # 在按下 F5 的时候重载 style.css 主题
        if event.key() == Qt.Key.Key_F5:
            self.loadStyleSheet()
            self.status.showMessage("已成功更新主题", 800)


class SystemTray(QSystemTrayIcon):
    def __init__(self, icon, mainWindow):
        super(SystemTray, self).__init__(icon)
        self.window = mainWindow
        self.setIcon(icon)
        self.setParent(mainWindow)
        self.activated.connect(self.tray_event)  # 设置托盘点击事件处理函数
        self.tray_menu = QMenu()  # 创建菜单
        # 添加一级菜单动作选项(还原主窗口)

        # 添加一级菜单动作选项(退出程序)
        self.QuitAction = QAction(self.tr("退出"), self, triggered=self.quit)
        self.StyleAction = QAction(
            self.tr("更新主题"), self, triggered=mainWindow.loadStyleSheet
        )  # 添加一级菜单动作选项(更新 QSS)
        self.tray_menu.addAction(self.QuitAction)
        self.tray_menu.addAction(self.StyleAction)
        self.setContextMenu(self.tray_menu)  # 设置系统托盘菜单
        self.show()

    def show_window(self):
        self.window.showNormal()
        self.window.activateWindow()
        # self.window.setWindowFlags(Qt.Window)
        self.window.show()

    def quit(self):
        sys.stdout = sys.__stdout__
        self.hide()
        QApplication.quit()

    def tray_event(self, reason):
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

        self.url_line_edit = None
        self.url_label = None

        self.setup_gui()
        # self.initValue()

    def setup_gui(self):
        # 下载链接输入和输出选项
        if True:
            # 下载链接输入
            if True:
                self.url_label = QLabel(self.tr("视频链接："))
                self.url_line_edit = customized_class.AutoPasteLineEdit()
                self.url_line_edit.setPlaceholderText(self.tr("输入要下载的视频链接"))
                self.url_line_edit.setToolTip(self.tr("输入要下载的视频链接"))
                self.url_line_edit.setMaxLength(100)
                self.url_line_edit.textChanged.connect(self.generate_final_command)

                self.only_download_sub_checkbox = QCheckBox(self.tr("只下载字幕"))

                # self.download_button = QPushButton(self.tr("开始下载"))
                # self.download_button.clicked.connect(self.run_final_command_button_clicked)

                self.download_hbox = QHBoxLayout()
                self.download_hbox.addWidget(self.url_line_edit, 2)
                self.download_hbox.addWidget(self.only_download_sub_checkbox, 1)
                self.download_hbox.setContentsMargins(0, 0, 0, 0)

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
                self.save_path_box = customized_class.SavePathComboBox()
                self.save_path_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                self.save_path_box.setToolTip(self.tr("填入下载保存目录"))

                self.save_path_box.currentTextChanged.connect(self.generate_final_command)
                # self.save_path_box.textChanged.connect(self.generateFinalCommand)
                self.select_dir_button = QPushButton(self.tr("选择目录"))
                self.select_dir_button.clicked.connect(self.choose_dir_button_clicked)

                self.select_dir_hbox = QHBoxLayout()
                self.select_dir_hbox.addWidget(self.save_path_box, 2)
                self.select_dir_hbox.addWidget(self.select_dir_button, 1)
                self.select_dir_hbox.setContentsMargins(0, 0, 0, 0)

            # 文件命名格式
            if True:
                self.save_name_format_label = QLabel(self.tr("文件命名格式："))
                self.save_name_format_edit = customized_class.SaveNameFormatComboBox()

                self.save_name_format_box = QHBoxLayout()
                self.save_name_format_box.addWidget(self.save_name_format_edit)
                self.save_name_format_box.setContentsMargins(0, 0, 0, 0)

            # 下载格式id
            if True:
                self.download_format_label = QLabel(self.tr("格式id："))
                self.download_format_edit = QLineEdit()
                self.download_format_edit.setPlaceholderText(self.tr("默认下载最高画质"))
                self.download_format_edit.setAlignment(Qt.AlignCenter)
                self.check_info_button = QPushButton(self.tr("列出格式id"))
                self.check_info_button.clicked.connect(self.check_info_button_clicked)

                self.download_format_hbox = QHBoxLayout()
                self.download_format_hbox.addWidget(self.download_format_edit, 2)
                self.download_format_hbox.addWidget(self.check_info_button, 1)
                self.download_format_hbox.setContentsMargins(0, 0, 0, 0)

            # 设置Cookies
            if True:
                self.set_cookies_label = QLabel(self.tr("设置Cookies："))
                self.set_cookies_edit = QComboBox()
                self.set_cookies_edit.setEditable(True)
                self.set_cookies_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                # self.set_cookies_edit.setEditText("edge")
                self.set_cookies_edit.addItems(["edge", "chrome", "firefox"])

                self.set_cookies_button = QPushButton(self.tr("选择文件"))
                self.set_cookies_button.clicked.connect(self.choose_file_button_clicked)

                self.set_cookies_hbox = QHBoxLayout()
                self.set_cookies_hbox.addWidget(self.set_cookies_edit, 2)
                self.set_cookies_hbox.addWidget(self.set_cookies_button, 1)
                self.set_cookies_hbox.setContentsMargins(0, 0, 0, 0)

            # 输出选项
            if True:
                self.output_label = QLabel(self.tr("输出选项："))
                self.output_options_edit = QPlainTextEdit()
                self.output_options_edit.setPlaceholderText(self.tr("填入输出选项"))
                self.output_options_edit.setToolTip(self.tr("填入输出选项"))
                # self.output_options_edit.setReadOnly(False)
                self.output_options_edit.textChanged.connect(self.generate_final_command)

                self.output_options_hbox = QHBoxLayout()
                self.output_options_hbox.addWidget(self.output_options_edit)
                self.output_options_hbox.setContentsMargins(0, 0, 0, 0)

            # self.main_hbox = QVBoxLayout()
            # self.main_hbox.addLayout(self.download_hbox)
            # self.main_hbox.addSpacing(20)
            # self.main_hbox.addLayout(self.select_dir_hbox)
            # self.main_hbox.addSpacing(20)
            # self.main_hbox.addLayout(self.output_options_hbox)
            self.main_formlayout = QFormLayout()
            self.main_formlayout.addRow(self.url_label, self.download_hbox)
            self.main_formlayout.addRow(self.save_label, self.select_dir_hbox)
            self.main_formlayout.addRow(self.save_name_format_label, self.save_name_format_box)
            self.main_formlayout.addRow(self.download_format_label, self.download_format_hbox)
            self.main_formlayout.addRow(self.set_cookies_label, self.set_cookies_hbox)
            self.main_formlayout.addRow(self.output_label, self.output_options_hbox)

            self.main_widget = QWidget()
            self.main_widget.setMinimumSize(350, 300)
            self.main_widget.setLayout(self.main_formlayout)

        # 预设列表
        if True:
            self.preset_list_label = QLabel(self.tr("选择预设："))
            self.preset_list = QListWidget()
            self.preset_list.itemClicked.connect(self.preset_item_selected)
            self.preset_list.itemDoubleClicked.connect(self.add_reset_button_clicked)

            self.add_preset_button = QPushButton("+")
            self.del_preset_button = QPushButton("-")
            self.up_preset_button = QPushButton("↑")
            self.down_preset_button = QPushButton("↓")
            self.view_preset_help = QPushButton(self.tr("查看预设帮助"))

            self.preset_vbox = QGridLayout()
            self.preset_vbox.addWidget(self.preset_list_label, 0, 0, 1, 1)
            self.preset_vbox.addWidget(self.preset_list, 1, 0, 1, 2)
            self.preset_vbox.addWidget(self.up_preset_button, 2, 0, 1, 1)
            self.preset_vbox.addWidget(self.down_preset_button, 2, 1, 1, 1)
            self.preset_vbox.addWidget(self.add_preset_button, 3, 0, 1, 1)
            self.preset_vbox.addWidget(self.del_preset_button, 3, 1, 1, 1)
            self.preset_vbox.addWidget(self.view_preset_help, 4, 0, 1, 2)

            self.preset_widget = QWidget()
            self.preset_widget.setMinimumSize(200, 300)
            self.preset_widget.setLayout(self.preset_vbox)

            self.up_preset_button.clicked.connect(self.upward_button_clicked)
            self.down_preset_button.clicked.connect(self.downward_button_clicked)
            self.add_preset_button.clicked.connect(self.add_preset_button_clicked)
            self.del_preset_button.clicked.connect(self.del_preset_button_clicked)
            self.view_preset_help.clicked.connect(self.check_preset_help_button_clicked)

        # 总命令输出框
        if True:
            self.final_command_text_edit = QPlainTextEdit()
            self.final_command_text_edit.setPlaceholderText(self.tr("自动生成的总命令"))
            self.final_command_text_edit.setReadOnly(True)
            self.final_command_text_edit.setMaximumHeight(180)
            self.final_command_run_button = QPushButton(self.tr("运行"))
            self.final_command_run_button.clicked.connect(self.run_final_command_button_clicked)

            self.final_command_vbox = QVBoxLayout()
            self.final_command_vbox.addWidget(self.final_command_text_edit)
            self.final_command_vbox.addWidget(self.final_command_run_button)
            self.final_command_widget = QWidget()
            self.final_command_widget.setLayout(self.final_command_vbox)

        # 放置三个主要控件
        if True:
            self.left_widget = QSplitter(Qt.Horizontal)
            self.left_widget.addWidget(self.main_widget)
            self.left_widget.addWidget(self.preset_widget)
            self.left_widget.setCollapsible(0, False)  # main_widget 是第一个添加的部件，所以索引是 0
            self.left_widget.setCollapsible(1, False)

            self.under_widget = QSplitter(Qt.Vertical)
            self.under_widget.addWidget(self.left_widget)
            self.under_widget.addWidget(self.final_command_widget)

            self.top_hbox = QHBoxLayout()
            self.top_hbox.addWidget(self.under_widget)
            self.setLayout(self.top_hbox)

    @QtCore.Slot()
    def generate_final_command(self):
        print("generateFinalCommand")
        return None

    # 选择文件夹
    @QtCore.Slot()
    def choose_dir_button_clicked(self):
        default_directory = QDir.homePath() + "/videos"
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹", default_directory)
        if folder_path != "":
            self.save_path_box.setEditText(folder_path)
        return folder_path

    # 选择文件
    @QtCore.Slot()
    def choose_file_button_clicked(self):
        default_directory = QDir.homePath()
        file_path = QFileDialog.getOpenFileName(self, "选择文件", default_directory, "文本文件(*.txt)")
        if file_path != "":
            self.set_cookies_edit.setEditText(file_path)
        return file_path

    @QtCore.Slot()
    # 点击运行按钮
    def run_final_command_button_clicked(self):
        print("runFinalCommandButtonClicked")
        return None

    @QtCore.Slot()
    def preset_item_selected(self):
        return None

    @QtCore.Slot()
    def add_reset_button_clicked(self):
        return None

    @QtCore.Slot()
    def upward_button_clicked(self):
        return None

    @QtCore.Slot()
    def downward_button_clicked(self):
        return None

    @QtCore.Slot()
    def add_preset_button_clicked(self):
        return None

    @QtCore.Slot()
    def del_preset_button_clicked(self):
        return None

    @QtCore.Slot()
    def check_preset_help_button_clicked(self):
        return None

    @QtCore.Slot()
    def check_info_button_clicked(self):
        return None


class ConfigTab(QWidget):
    def __init__(self):
        super().__init__()
        self.config_vbox = None
        self.setup_gui()
        # self.initValue()

    def setup_gui(self):
        self.config_vbox = QVBoxLayout()


class HelpTab(QWidget):
    def __init__(self):
        super().__init__()
        self.help_vbox = None
        self.setup_gui()
        # self.initValue()

    def setup_gui(self):
        self.help_vbox = QVBoxLayout()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
