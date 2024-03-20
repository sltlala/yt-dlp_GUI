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


# ℹ️ 请参阅 help(yt_dlp.YoutubeDL) 中的 "progress_hooks"。
def my_hook(d):
    if d["status"] == "finished":
        print("Done downloading, now post-processing ...")


ydl_opts = {
    "logger": MyLogger(),
    "progress_hooks": [my_hook],
    "proxy": "http://127.0.0.1:8888",
    # 'forcejson': True
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    # ydl.download(URLS)
    info = ydl.extract_info(URLS[0], download=False)
    formats_info = info["formats"]


# with open('info.json', 'r', encoding='utf-8') as f:
#     formats_info = json.load(f)
#     print(formats_info[55]['format_id'], format_filesize(formats_info[55], 49))
#     print(formats_info[54]['format_id'], format_filesize(formats_info[54]))
#     print(formats_info[14]['format_id'], format_filesize(formats_info[14]))
#     print(formats_info[44]['format_id'], format_filesize(formats_info[44]))
#     # print(formats_info[44]['filesize_approx'])
#     # ℹ️ ydl.sanitize_info 使信息可 json 序列化
#     # print(json.dumps(ydl.sanitize_info(info)))


with open("format_info.json", "w", encoding="utf-8") as f:
    # f.write(json.dumps(ydl.sanitize_info(info)))
    f.write(json.dumps(formats_info))
    f.close()
