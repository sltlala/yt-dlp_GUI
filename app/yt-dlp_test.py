import json

import yt_dlp
from yt_dlp.postprocessor.common import PostProcessor


class MyLogger:
    def debug(self, msg):
        # For compatability with youtube-dl, both debug and info are passed into debug
        # You can distinguish them by the prefix '[debug] '
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


class MyCustomPP(PostProcessor):
    def run(self, info):
        self.to_screen("Doing stuff")
        return [], info


def my_hook(d):
    if d["status"] == "finished":
        print("Done downloading, now converting ...")


ydl_opts = {
    "format": "bestaudio/best",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }
    ],
    "logger": MyLogger(),
    "progress_hooks": [my_hook],
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.add_post_processor(MyCustomPP())
    info = ydl.extract_info("https://www.bilibili.com/video/BV1gt4y1R7rf/")
    print(json.dumps(ydl.sanitize_info(info)))
