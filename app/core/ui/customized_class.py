import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QTextCursor
from PySide6.QtWidgets import (
    QLineEdit,
    QMenu,
    QApplication,
    QComboBox,
    QSizePolicy,
    QTextEdit,
    QMessageBox,
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


# 命令输出窗口中的多行文本框
class OutputBox(QTextEdit):
    # 定义一个 QTextEdit 类，写入 print 方法。用于输出显示。
    def __init__(self, parent=None):
        super(OutputBox, self).__init__(parent)
        self.setReadOnly(True)

    def print(self, text):
        try:
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.End)
            cursor.insertText(text)
            self.setTextCursor(cursor)
            self.ensureCursorVisible()
        except AttributeError:
            pass


# 错误提示框
class ErrorMessageBox(QMessageBox):
    def __init__(self, message_text=None):
        super().__init__()
        self.setWindowTitle("错误")
        self.setIcon(QMessageBox.Critical)
        self.setStandardButtons(QMessageBox.Ok)
        self.setText(message_text)
        # 确认按钮点击后关闭
        self.buttonClicked.connect(self.close)
        self.exec_()
