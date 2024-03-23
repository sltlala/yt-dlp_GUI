import io
import subprocess

from PySide6.QtCore import QThread, Signal


subprocessStartUpInfo = subprocess.STARTUPINFO()
subprocessStartUpInfo.dwFlags = subprocess.STARTF_USESHOWWINDOW
subprocessStartUpInfo.wShowWindow = subprocess.SW_HIDE


class CommandThread(QThread):
    signal = Signal(str)
    signal_ytdlp = Signal(str)

    output = None  # 用于显示输出的控件，如一个 QEditBox，它需要有自定义的 print 方法。
    command = None

    def __init__(self, parent=None):
        super(CommandThread, self).__init__(parent)

    def print(self, text):
        self.signal.emit(text)

    def print_ytdlp(self, text):
        self.signal_ytdlp.emit(text)

    def run(self):
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
        except subprocess.CalledProcessError:
            self.print(self.tr("出错了，本次运行的命令是：\n\n%s") % self.command)
        try:
            stdout = BufferedReader(self.process.stdout.raw)
            while True:
                line = stdout.readline()
                if not line:
                    break
                try:
                    self.print_ytdlp(line.decode("utf-8"))
                except UnicodeDecodeError:
                    self.print_ytdlp(line.decode("gbk"))
        except AttributeError:
            self.print(self.tr("出错了，本次运行的命令是：\n\n%s") % self.command)
        self.print(self.tr("\n命令执行完毕\n"))


"""# 执行命令
def execute(command):
    # 判断一下系统，如果是windows系统，就直接将命令在命令行窗口中运行，避免在程序中运行时候的卡顿。
    # system = platform.system()
    # if system == 'Windows':
    #     os.system('start cmd /k ' + command)
    # else:
    #     console = Console(mainWindow)
    #     console.runCommand(command)

    # 新方法，执行子进程，在新窗口输出
    thread = CommandThread()  # 新建一个子进程
    thread.command = command  # 将要执行的命令赋予子进程
    window = Console(main_window)  # 显示一个新窗口，用于显示子进程的输出
    output = window.console_box  # 获得新窗口中的输出控件
    outputForFFmpeg = window.console_box_ytdlp
    thread.signal.connect(output.print)  # 将 子进程中的输出信号 连接到 新窗口输出控件的输出槽
    thread.signal_ytdlp.connect(outputForFFmpeg.print)  # 将 子进程中的输出信号 连接到 新窗口输出控件的输出槽
    window.thread = thread  # 把这里的剪辑子进程赋值给新窗口，这样新窗口就可以在关闭的时候也把进程退出
    thread.start()
"""


class BufferedReader(io.BufferedReader):
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
            # Windows
            if res.endswith(b"\r"):
                if self.peek(1).startswith(b"\n"):
                    # \r\n encountered
                    res += self.read(1)
                break

        return bytes(res)
