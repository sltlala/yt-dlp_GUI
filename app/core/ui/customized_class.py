import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QLineEdit,
    QMenu,
    QApplication,
    QComboBox,
    QSizePolicy,
    QDialog,
    QLabel,
    QPlainTextEdit,
    QTextEdit,
    QPushButton,
    QFormLayout,
    QHBoxLayout,
    QWidget,
    QVBoxLayout,
)

from app.core import database

db = database.Database()


# 自动粘贴单行文本框
class AutoPasteLineEdit(QLineEdit):
    """实现自动粘贴填充功能"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    # 设置右键选项
    def show_context_menu(self, pos):
        context_menu = QMenu(self)

        # 添加粘贴动作
        paste_action = QAction("粘贴", self)
        paste_action.triggered.connect(self.paste)
        context_menu.addAction(paste_action)
        context_menu.exec_(self.mapToGlobal(pos))

    def paste(self):
        clipboard = QApplication.clipboard()
        self.setText(self.text().strip() + clipboard.text())

    # 若文本框空白，点击自动填充
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            clipboard = QApplication.clipboard()
            clipboard_text = clipboard.text()
            if self.text().strip() == "":
                self.setText(clipboard_text)

        super().mousePressEvent(event)


# 可拖入文件的单行编辑框
class DragFileLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()


class SavePathComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.userPath = os.path.expanduser("~").replace("\\", "/")
        self.userVideoPath = self.userPath + "/Videos"
        self.userDownloadPath = self.userPath + "/Downloads"
        self.userDesktopPath = self.userPath + "/Desktop"
        self.setup()

    def setup(self):
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setEditable(True)
        self.setEditText(self.userVideoPath)
        self.addItems([self.userVideoPath, self.userPath, self.userDownloadPath, self.userDesktopPath])


class SaveNameFormatComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup()

    def setup(self):
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setEditable(False)
        # self.setEditText("%(title)s.%(ext)s")
        self.addItems(
            [
                "%(title)s.%(ext)s",
                "%(id)s.%(ext)s",
                "%(uploader)s - %(title)s.%(ext)s",
                "%(uploader)s/%(title)s.%(ext)s",
            ]
        )


# 添加预设对话框
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
