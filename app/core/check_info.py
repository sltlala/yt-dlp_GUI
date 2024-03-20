import json
import yt_dlp

from app.utils._utils import format_filesize

URLS = ["https://www.youtube.com/watch?v=_xXIC96jXBQ"]
URL = "https://www.youtube.com/watch?v=_xXIC96jXBQ"


class MyLogger:
    def debug(self, msg):
        # 为了与 youtube-dl 兼容，调试和信息都会传入调试程序
        # 您可以通过前缀"[debug]"来区分它们。
        if msg.startswith("[debug] "):
            pass
        else:
            self.info(msg)

    def info(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d["status"] == "finished":
        print("Done downloading, now post-processing ...")


ydl_opts = {
    "logger": MyLogger(),
    "progress_hooks": [my_hook],
    "proxy": "http://127.0.0.1:8888",
}


with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(URLS[0], download=False)
    info = ydl.sanitize_info(info)

    formats_info = info["formats"]
    print(formats_info[55]["format_id"], format_filesize(formats_info[55], info["duration"]))
