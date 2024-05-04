import yt_dlp

from app.utils.utils import format_filesize, short_chars


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


def build_video_format_dict(i, duration):
    """
    构建格式字典的辅助函数。
    :param i: 格式信息字典。
    :param duration: 持续时间。
    :return: 包含格式信息的字典。
    """
    try:
        file_size = format_filesize(i, duration)  # 可能抛出异常的操作
    except Exception:
        # 在此处处理异常，例如记录日志或使用默认值
        file_size = "N/A"  # 使用默认值或进行其他处理

    f = {
        "format_id": i["format_id"],
        "file_size": file_size,
        "vcodec": short_chars(i["vcodec"]),
        "resolution": i["resolution"],
        "tbr": i["tbr"],
    }
    return f


def get_video_formats(formats_info, duration):
    video_formats = []
    for i in formats_info:
        # print(i['resolution'])
        if "x" in i["resolution"] and int(i["resolution"].split("x")[1]) >= 720:
            f = build_video_format_dict(i, duration)

            video_formats.append(f)
    return video_formats


def build_audio_format_dict(i, duration):
    """
    构建格式字典的辅助函数。
    :param i: 格式信息字典。
    :param duration: 持续时间。
    :return: 包含格式信息的字典。
    """
    try:
        file_size = format_filesize(i, duration)  # 可能抛出异常的操作
    except Exception:
        # 在此处处理异常，例如记录日志或使用默认值
        file_size = "N/A"  # 使用默认值或进行其他处理

    f = {"format_id": i["format_id"], "file_size": file_size, "tbr": i["tbr"]}

    # 默认的音频编解码器
    default_acodec = "Default"
    acodec = i.get("acodec", default_acodec)

    f["acodec"] = short_chars(acodec)
    return f


def get_audio_formats(formats_info, duration):
    audio_formats = []
    for i in formats_info:
        # 简化了条件判断，同时增加了对 'format_note' 是否存在的检查
        if i.get("resolution") == "audio only" and i.get("format_note", "").lower() not in ["drc", "ultralow"]:
            f = build_audio_format_dict(i, duration)
            audio_formats.append(f)
        elif i.get("resolution") == "audio only":
            f = build_audio_format_dict(i, duration)
            audio_formats.append(f)
    return audio_formats


# def get_audio_formats(formats_info, duration):
#     audio_formats = []
#     for i in formats_info:
#         if i['resolution'] == 'audio only' and i.get('format_note') is not None:
#             if 'DRC' not in i['format_note'] and 'ultralow' not in i['format_note']:
#                 f = {'format_id': i['format_id'], 'file_size': format_filesize(i, duration), 'tbr': i['tbr']}
#                 if 'acodec' in i:
#                     f['acodec'] = i['acodec']
#                 else:
#                     f['acodec'] = 'Default'
#             audio_formats.append(f)
#         elif i['resolution'] == 'audio only':
#             f = {'format_id': i['format_id'], 'file_size': format_filesize(i, duration), 'tbr': i['tbr']}
#             if 'acodec' in i:
#                 f['acodec'] = i['acodec']
#             else:
#                 f['acodec'] = 'Default'
#             audio_formats.append(f)
#
#     return audio_formats


class check_info:
    def my_hook(d):
        if d["status"] == "finished":
            print("Done downloading, now post-processing ...")

    def info(self, url):
        ydl_opts = {
            "logger": MyLogger(),
            "progress_hooks": [self.my_hook],
            "proxy": "http://127.0.0.1:8888",
            "cookiesfrombrowser": ["chrome"],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats_info = info["formats"]
            duration = info["duration"]
        return formats_info, duration
