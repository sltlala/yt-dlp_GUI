import io
import os
import subprocess

from PySide6.QtCore import QThread, Signal


class CommandThread(QThread):
    signal = Signal(str)
    signalForFFmpeg = Signal(str)

    output = None  # 用于显示输出的控件，如一个 QEditBox，它需要有自定义的 print 方法。

    outputTwo = None

    command = None

    def __init__(self, parent=None):
        super(CommandThread, self).__init__(parent)

    def print(self, text):
        self.signal.emit(text)

    def printForFFmpeg(self, text):
        self.signalForFFmpeg.emit(text)

    def run(self, subprocessStartUpInfo=None):
        self.print(self.tr("开始执行命令\n"))
        try:
            # command = self.command.encode('gbk').decode('gbk')
            self.process = subprocess.Popen(
                self.command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                startupinfo=subprocessStartUpInfo,
            )

            self.process = subprocess.Popen(
                self.command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                start_new_session=True,
            )
        except subprocess.CalledProcessError:
            self.print(self.tr("出错了，本次运行的命令是：\n\n%s") % self.command)
        try:
            stdout = _BufferedReaderForFFmpeg(self.process.stdout.raw)
            while True:
                line = stdout.readline()
                if not line:
                    break
                try:
                    self.printForFFmpeg(line.decode("utf-8"))
                except UnicodeDecodeError:
                    self.printForFFmpeg(line.decode("gbk"))
        except AttributeError:
            self.print(self.tr("出错了，本次运行的命令是：\n\n%s") % self.command)
        self.print(self.tr("\n命令执行完毕\n"))


class _BufferedReaderForFFmpeg(io.BufferedReader):
    """Method `newline` overriden to *also* treat `\\r` as a line break."""

    def readline(self, size=-1):
        if hasattr(self, "peek"):

            def nreadahead():
                readahead = self.peek(1)
                if not readahead:
                    return 1
                n = (readahead.find(b"\r") + 1) or (readahead.find(b"\n") + 1) or len(readahead)
                if size >= 0:
                    n = min(n, size)
                return n
        else:

            def nreadahead():
                return 1

        if size is None:
            size = -1
        else:
            try:
                size_index = size.__index__
            except AttributeError:
                raise TypeError(f"{size!r} is not an integer") from None
            else:
                size = size_index()
        res = bytearray()
        while size < 0 or len(res) < size:
            b = self.read(nreadahead())
            if not b:
                break
            res += b
            if os.linesep == "\r\n":
                # Windows
                if res.endswith(b"\r"):
                    if self.peek(1).startswith(b"\n"):
                        # \r\n encountered
                        res += self.read(1)
                    break
            else:
                # Unix
                if res.endswith(b"\r") or res.endswith(b"\n"):
                    break
        return bytes(res)
