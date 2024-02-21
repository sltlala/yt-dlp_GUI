from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QLineEdit, QMenu, QApplication


class AutoPasteLineEdit(QLineEdit):
    """实现自动粘贴填充功能"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, pos):
        context_menu = QMenu(self)

        # 添加粘贴动作
        paste_action = QAction("粘贴", self)
        paste_action.triggered.connect(self.auto_paste)
        context_menu.addAction(paste_action)

        context_menu.exec_(self.mapToGlobal(pos))

    def auto_paste(self):
        clipboard = QApplication.clipboard()
        clipboard_text = clipboard.text()

        # 在这里你可以对剪贴板中的文本进行处理
        # 例如，可以将其自动填充到 QLineEdit 中
        self.setText(self.text().strip() + clipboard_text)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            clipboard = QApplication.clipboard()
            clipboard_text = clipboard.text()
            if self.text().strip() == "":
                self.setText(clipboard_text)

        super().mousePressEvent(event)
