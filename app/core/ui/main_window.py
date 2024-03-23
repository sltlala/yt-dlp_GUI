import os
import sys

from PySide6 import QtWidgets, QtCore

from PySide6.QtCore import QDir, Qt
from PySide6.QtGui import QIcon, QAction, QFont, QGuiApplication
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

from app.core.command import CommandThread
from app.core.ui.customized_class import ErrorMessageBox
from app.core.ui.subwindow import Console
from app.core.ui import customized_class
from app.core import database
from app.utils.utils import is_valid_url

style_file = "app/resources/style.css"  # 样式表的路径
preset_table_name = "commandPreset"
final_command = ""

db = database.Database()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.setup_gui()
        self.status = self.statusBar()
        self.load_style_sheet()

    def setup_gui(self):
        self.tabs = QTabWidget(parent=None)
        self.setCentralWidget(self.tabs)
        self.adjustSize()
        self.resize(700, 600)
        screen = QGuiApplication.primaryScreen().geometry()
        self.move(screen.width() / 2 - self.width() / 2, screen.height() / 2 - self.height() / 2)
        # self.setMinimumSize(500, 500)

        self.ytdlpMainTab = YtdlpMainTab()  # 主界面
        self.configTab = ConfigTab()  # 配置界面
        self.helpTab = HelpTab()  # 帮助界面

        self.tabs.addTab(self.ytdlpMainTab, "yt-dlp")
        self.tabs.addTab(self.configTab, self.tr("设置"))
        self.tabs.addTab(self.helpTab, self.tr("帮助"))

        self.setWindowTitle("yt-dlp_GUI")
        self.setFont(QFont("Microsoft YaHei UI", 10))
        self.setWindowIcon(QIcon("app/resources/favicon.ico"))

    # 加载样式表
    def load_style_sheet(self) -> None:
        global style_file
        try:
            with open(style_file, "r", encoding="UTF-8") as style:
                self.setStyleSheet(style.read())
                self.status.showMessage(self.tr("已成功更新主题"), 800)
        except FileNotFoundError:
            QMessageBox.warning(
                self,
                self.tr("主题载入错误"),
                self.tr("未能成功载入主题，请确保软件资源目录有 'style.css' 文件存在。"),
            )
        except UnicodeDecodeError:
            self.status.showMessage(self.tr("文件编码错误,请使用UTF8编码"), 800)

    def keyPressEvent(self, event) -> None:
        # 在按下 F5 的时候重载 style.css 主题
        if event.key() == Qt.Key.Key_F5:
            self.load_style_sheet()


# 系统托盘
class SystemTray(QSystemTrayIcon):
    def __init__(self, icon, main_window):
        super(SystemTray, self).__init__(icon)
        self.window = main_window
        self.setIcon(icon)
        self.setParent(main_window)
        self.activated.connect(self.tray_event)  # 设置托盘点击事件处理函数
        self.tray_menu = QMenu()  # 创建菜单
        # 添加一级菜单动作选项(还原主窗口)

        # 添加一级菜单动作选项(退出程序)
        self.QuitAction = QAction(self.tr("退出"), self, triggered=self.quit)
        self.StyleAction = QAction(
            self.tr("更新主题"), self, triggered=main_window.load_style_sheet
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


# ytdlp 主界面
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
        self.init_value()

    def init_value(self):
        # 检查数据库是否存在
        db.create_present_table()
        # 刷新预设列表
        self.refresh_list()

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

            # 下载选项
            if True:
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

            # 文件命名格式
            if True:
                self.save_name_format_label = QLabel(self.tr("文件命名格式："))
                self.save_name_format_edit = customized_class.SaveNameFormatComboBox()
                self.save_name_format_edit.currentTextChanged.connect(self.generate_final_command)

                self.save_name_format_box = QHBoxLayout()
                self.save_name_format_box.addWidget(self.save_name_format_edit)

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

            # 设置Cookies
            if True:
                self.set_cookies_label = QLabel(self.tr("设置Cookies："))
                self.set_cookies_edit = QComboBox()
                self.set_cookies_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                self.set_cookies_edit.addItems(["", "edge", "chrome", "firefox"])
                self.set_cookies_edit.currentTextChanged.connect(self.generate_final_command)

                self.set_cookies_button = QPushButton(self.tr("选择文件"))
                self.set_cookies_button.clicked.connect(self.choose_file_button_clicked)

                self.set_cookies_hbox = QHBoxLayout()
                self.set_cookies_hbox.addWidget(self.set_cookies_edit, 2)
                self.set_cookies_hbox.addWidget(self.set_cookies_button, 1)

            # 输出格式和封面元数据
            if True:
                self.output_format_label = QLabel(self.tr("输出格式："))
                self.output_format_edit = QComboBox()
                self.output_format_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                self.output_format_edit.addItems(["mp4", "mkv", "flv", "webm", "mp3", "m4a", "flac", "wav"])
                self.output_format_edit.currentTextChanged.connect(self.generate_final_command)

                self.embed_thumbnail_checkbox = QCheckBox(self.tr("封面-元数据"))
                self.embed_thumbnail_checkbox.stateChanged.connect(self.generate_final_command)

                self.output_format_hbox = QHBoxLayout()
                self.output_format_hbox.addWidget(self.output_format_edit, 2)
                self.output_format_hbox.addWidget(self.embed_thumbnail_checkbox, 1)

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

            self.download_button = QPushButton(self.tr("开始下载"))
            self.download_button.setFixedHeight(40)
            self.download_button.clicked.connect(self.run_final_command_button_clicked)

            # 主布局设置
            self.main_formlayout = QFormLayout()
            self.main_formlayout.addRow(self.url_label, self.download_hbox)
            self.main_formlayout.addRow(self.save_label, self.select_dir_hbox)
            self.main_formlayout.addRow(self.save_name_format_label, self.save_name_format_box)
            self.main_formlayout.addRow(self.download_format_label, self.download_format_hbox)
            self.main_formlayout.addRow(self.set_cookies_label, self.set_cookies_hbox)
            self.main_formlayout.addRow(self.output_format_label, self.output_format_hbox)
            self.main_formlayout.addRow(None, self.download_button)
            self.main_formlayout.addRow(self.output_label, self.output_options_hbox)

            self.main_widget = QWidget()
            self.main_widget.setMinimumSize(450, 300)
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
            self.preset_widget.setMinimumSize(200, 350)
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

            self.final_command_vbox = QVBoxLayout()
            self.final_command_vbox.addWidget(self.final_command_text_edit)
            self.final_command_widget = QWidget()
            self.final_command_widget.setLayout(self.final_command_vbox)

        # 放置三个主要控件
        if True:
            self.left_widget = QSplitter(Qt.Horizontal)
            self.left_widget.addWidget(self.main_widget)
            self.left_widget.addWidget(self.preset_widget)
            self.left_widget.setCollapsible(0, False)
            self.left_widget.setCollapsible(1, False)

            self.under_widget = QSplitter(Qt.Vertical)
            self.under_widget.addWidget(self.left_widget)
            self.under_widget.addWidget(self.final_command_widget)
            self.under_widget.setCollapsible(0, False)
            self.under_widget.setCollapsible(1, False)

            self.top_hbox = QHBoxLayout()
            self.top_hbox.addWidget(self.under_widget)
            self.setLayout(self.top_hbox)

    # 将数据库的预设填入列表（更新列表）
    def refresh_list(self):
        # 改用主数据库
        cursor = db.cursor
        preset_data = cursor.execute("select id, name, outputOption from %s order by id" % (preset_table_name))
        self.preset_list.clear()
        for i in preset_data:
            self.preset_list.addItem(i[1])

    # 生成总命令
    @QtCore.Slot()
    def generate_final_command(self):
        global final_command
        print("generateFinalCommand")
        if self.url_line_edit.text() != "":
            final_command = "yt-dlp"
            if self.url_line_edit.text() != "":
                final_command += " %s" % self.url_line_edit.text()
            if self.save_path_box.currentText() != "":
                final_command += " -P %s" % self.save_path_box.currentText()
            if self.set_cookies_edit.currentText() != "":
                final_command += " --cookies-from-browser %s" % self.set_cookies_edit.currentText()
            if self.save_name_format_edit.currentText() != "":
                final_command += " -o '" + self.save_name_format_edit.currentText() + "'"
            if self.download_format_edit.text() != "":
                final_command += " --format '" + self.download_format_edit.text() + "'"
            if self.output_format_edit.currentText() != "":
                final_command += " --merge-output-format %s" % self.output_format_edit.currentText()
            if self.embed_thumbnail_checkbox.isChecked():
                final_command += " --embed-thumbnail --embed-metadata"
        else:
            ErrorMessageBox(self.tr("请填入视频链接！"))
        self.final_command_text_edit.setPlainText(final_command)
        return final_command

    # 选择文件夹
    @QtCore.Slot()
    def choose_dir_button_clicked(self):
        default_directory = QDir.homePath() + "/videos"
        folder_path = QFileDialog.getExistingDirectory(
            self, self.tr("选择文件夹"), default_directory, self.tr("所有文件(*.*)")
        )
        if folder_path != "":
            self.save_path_box.setEditText(folder_path)
        return folder_path

    # 选择文件
    @QtCore.Slot()
    def choose_file_button_clicked(self):
        default_directory = QDir.homePath()
        file_path = QFileDialog.getOpenFileName(self, self.tr("选择文件"), default_directory, self.tr("所有文件(*.*)"))
        if file_path != "":
            self.set_cookies_edit.addItem(file_path[0])
            self.set_cookies_edit.setCurrentText(file_path[0])
        return file_path

    # 点击运行按钮
    @QtCore.Slot()
    def run_final_command_button_clicked(self):
        print("runFinalCommandButtonClicked")
        final_command = self.generate_final_command()
        if final_command != "":
            if is_valid_url(self.url_line_edit.text()):
                self.command_run(final_command)
            else:
                ErrorMessageBox(self.tr("请填入正确的视频链接！"))
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

    # 点击列出格式id
    @QtCore.Slot()
    def check_info_button_clicked(self):
        # TODO 1. 列出格式id，弹窗选择(视频音频各选一个)
        #      2. 保存上次运行过后的各个设置
        print("checkInfoButtonClicked")
        if self.url_line_edit.text() != "":
            finalCommand = "yt-dlp"
            finalCommand += " --cookies-from-browser %s" % self.set_cookies_edit.currentText()
            finalCommand += " --proxy %s" % "http://127.0.0.1:8888"
            finalCommand += " %s -F" % self.url_line_edit.text()
            print(finalCommand)
            self.command_run(finalCommand)
        else:
            ErrorMessageBox(self.tr("请填入视频链接！"))

    # 执行命令
    def command_run(self, command):
        thread = CommandThread()
        thread.command = command
        window = Console(self)
        window.thread = thread
        output = window.console_box
        output_ytdlp = window.console_box_ytdlp
        thread.output = output
        thread.signal.connect(output.print)
        thread.signal_ytdlp.connect(output_ytdlp.print)
        thread.start()


# 配置页面
class ConfigTab(QWidget):
    def __init__(self):
        super().__init__()
        self.config_vbox = None
        self.setup_gui()
        # TODO: 1. 配置页面，代理、全局下载路径、下载存档
        #       2. 外部下载器aria2设置 ffmpeg设置以及测试可用性(测试命令行程序版本)
        #       3.
        # self.initValue()

    def setup_gui(self):
        self.config_vbox = QVBoxLayout()


class HelpTab(QWidget):
    def __init__(self):
        super().__init__()
        self.help_vbox = None
        self.setup_gui()
        # TODO: 1. 程序更新
        #       2. yt-dlp命令行使用方法
        #       3. 问题反馈 日志提交
        #       4. 作者信息
        # self.initValue()

    def setup_gui(self):
        self.help_vbox = QVBoxLayout()
