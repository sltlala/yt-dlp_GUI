from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent
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

        self.submit_button = QPushButton(self.tr("确定"))
        self.submit_button.clicked.connect(self.submitButtonClicked)
        self.cancel_button = QPushButton(self.tr("取消"))
        self.cancel_button.clicked.connect(lambda: self.close())

        self.preset_item_layout = QFormLayout()
        self.preset_item_layout.addRow(self.preset_name_label, self.preset_name_edit)
        self.preset_item_layout.addRow(self.output_option_label, self.output_option_edit)
        self.preset_item_layout.addRow(self.description_label, self.description_edit)

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.submit_button)
        self.button_layout.addWidget(self.cancel_button)

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
                self.preset_name = preset_data[2]
                self.outputOption = preset_data[3]
                self.description = preset_data[4]


class Console(QMainWindow):
    # 这个 console 是个子窗口，调用的时候要指定父窗口。例如：window = Console(mainWindow)
    # 里面包含一个 OutputBox, 可以将信号导到它的 print 方法。
    thread = None

    def __init__(self, parent=None):
        super(Console, self).__init__(parent)
        self.setup_gui()

    def setup_gui(self):
        self.setWindowTitle(self.tr("命令运行输出窗口"))
        self.resize(600, 500)
        self.console_box = OutputBox()  # 他就用于输出用户定义的打印信息
        self.console_box_ytdlp = OutputBox()  # 把ffmpeg的输出信息用它输出
        self.console_box.setParent(self)
        self.console_box_ytdlp.setParent(self)

        self.split = QSplitter(Qt.Vertical)
        self.split.addWidget(self.console_box)
        self.split.addWidget(self.console_box_ytdlp)
        self.setCentralWidget(self.split)
        self.show()

    def closeEvent(self, a0: QCloseEvent) -> None:
        try:
            self.thread.process.kill()
        except AttributeError:
            self.thread.process.terminate()

        self.thread.exit()
        self.thread.setTerminationEnabled(True)
        self.thread.terminate()
