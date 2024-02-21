from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QLineEdit, QMenu, QApplication


# 自动粘贴单行文本框
class AutoPasteLineEdit(QLineEdit):
    """实现自动粘贴填充功能"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

    # 设置右键选项
    def showContextMenu(self, pos):
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
