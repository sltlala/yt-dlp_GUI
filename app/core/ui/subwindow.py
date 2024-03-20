# 添加预设对话框
import os
import signal
import subprocess

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QTextEdit,
    QPushButton,
    QFormLayout,
    QHBoxLayout,
    QWidget,
    QVBoxLayout,
    QSplitter,
    QMainWindow,
)

from app.core import database
from app.core.ui.customized_class import OutputBox
from app.core.command import subprocessStartUpInfo

db = database.Database()


class SetupPresetItemDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_gui()

    def setup_gui(self):
        self.setWindowTitle(self.tr("添加预设"))
        self.setFixedSize(300, 200)

        self.preset_name_label = QLabel(self.tr("预设名称"))
        self.preset_name_edit = QLineEdit()
        self.preset_name_edit.textChanged.connect(self.preset_name_edit_changed)

        self.output_option_label = QLabel(self.tr("输出选项"))
        self.output_option_edit = QPlainTextEdit()
        self.preset_option_edit.setMaximumHeight(100)

        self.description_label = QLabel(self.tr("描述"))
        self.description_edit = QTextEdit()

        self.submitButton = QPushButton(self.tr("确定"))
        self.submitButton.clicked.connect(self.submitButtonClicked)
        self.cancelButton = QPushButton(self.tr("取消"))
        self.cancelButton.clicked.connect(lambda: self.close())

        self.preset_item_layout = QFormLayout()
        self.preset_item_layout.addRow(self.preset_name_label, self.preset_name_edit)
        self.preset_item_layout.addRow(self.output_option_label, self.output_option_edit)
        self.preset_item_layout.addRow(self.description_label, self.description_edit)

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.submitButton)
        self.button_layout.addWidget(self.cancelButton)

        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.preset_item_layout)
        self.main_layout.addLayout(self.button_layout)
        self.main_widget.setLayout(self.main_layout)

    # 填入数据库内容
    def show_preset_item(self):
        global selected_preset
        if selected_preset is not None:
            preset_data = db.cursor.execute(
                'select id, name, outputOption, description from %s where name = "%s"'
                % ("commandPreset", selected_preset)
            ).fetchone()
            if preset_data is not None:
                self.inputOneOption = preset_data[2]
                self.outputOption = preset_data[3]
                self.description = preset_data[4]


class Console(QMainWindow):
    # 这个 console 是个子窗口，调用的时候要指定父窗口。例如：window = Console(mainWindow)
    # 里面包含一个 OutputBox, 可以将信号导到它的 print 方法。
    thread = None

    def __init__(self, parent=None):
        super(Console, self).__init__(parent)
        self.initGui()

    def initGui(self):
        self.setWindowTitle(self.tr("命令运行输出窗口"))
        self.resize(800, 700)
        self.consoleBox = OutputBox()  # 他就用于输出用户定义的打印信息
        self.consoleBoxForFFmpeg = OutputBox()  # 把ffmpeg的输出信息用它输出
        self.consoleBox.setParent(self)
        self.consoleBoxForFFmpeg.setParent(self)
        # self.masterLayout = QVBoxLayout()
        # self.masterLayout.addWidget(self.consoleBox)
        # self.masterLayout.addWidget(QPushButton())
        # self.setLayout(self.masterLayout)
        # self.masterWidget = QWidget()
        # self.masterWidget.setLayout(self.masterLayout)
        self.split = QSplitter(Qt.Vertical)
        self.split.addWidget(self.consoleBox)
        self.split.addWidget(self.consoleBoxForFFmpeg)
        self.setCentralWidget(self.split)
        self.show()

    def closeEvent(self) -> None:
        try:
            try:
                # 这个方法可以杀死 subprocess 用了 shell=True 开启的子进程，新测好用！
                # https://stackoverflow.com/questions/13243807/popen-waiting-for-child-process-even-when-the-immediate-child-has-terminated/13256908#13256908
                subprocess.call(
                    "TASKKILL /F /PID {pid} /T".format(pid=self.thread.process.pid), startupinfo=subprocessStartUpInfo
                )

                # 这个没新测，但是 Windows 用不了，只能用于 unix 类的系统
                # os.killpg(os.getpgid(self.thread.process.pid), signal.SIGTERM)
            except AttributeError:
                pass

            try:
                self.thread.process.terminate()
            except AttributeError:
                pass
            self.thread.exit()
            self.thread.setTerminationEnabled(True)
            self.thread.terminate()
        except AttributeError:
            pass
