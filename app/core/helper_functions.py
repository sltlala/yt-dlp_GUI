# 自动生成总命令
import os
from PySide6 import QtCore
from PySide6.QtCore import QDir
from PySide6.QtWidgets import QMessageBox, QFileDialog


@QtCore.Slot()
def generateFinalCommand():
    print("generateFinalCommand")
    return None


# 选择文件夹
@QtCore.Slot()
def chooseDirButtonClicked(self):
    default_directory = QDir.homePath() + "/videos"
    folder_path = QFileDialog().getExistingDirectory(self, "选择文件夹", default_directory)
    if folder_path != "":
        self.output_path_line_edit.setText(folder_path)
    return folder_path


@QtCore.Slot()
# 点击运行按钮
def runFinalCommandButtonClicked():
    return None


"""    finalCommand = self.总命令编辑框.toPlainText()
    outputPath = self.输出路径框.text()
    if os.path.exists(outputPath):
        overwrite = QMessageBox.information(
            self, self.tr('覆盖确认'), self.tr('输出路径对应的文件已存在，是否要覆盖？'),
            QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel)
        if overwrite != QMessageBox.Yes:
            return
    if finalCommand != '':
        execute(finalCommand)
"""


@QtCore.Slot()
# 执行命令
def execute(command):
    return None


# class CommandThread():


@QtCore.Slot()
def run(self):
    return None


@QtCore.Slot()
# 如果输入文件是拖进去的
def lineEditHasDrop(self, path):
    output_name = os.path.splitext(path)[0] + "_out" + os.path.splitext(path)[1]
    self.输出路径框.setText(output_name)
    return True
