## format_info

| 输出         | 翻译    | 示例                                              |
|------------|-------|-------------------------------------------------|
| ID         | id    | 312                                             |
| EXT        | 格式    | mp4/webm                                        |
| RESOLUTION | 分辨率   | 1920x1080                                       |
| FILESIZE   | 文件大小  | 13.51MiB/~ 22.67MiB                             |
| TBR        | 比特率   | 2319k                                           |
| PROTO      | 协议    | https/m3u8                                      |
| VCODEC     | 视频编码  | avc1.64002A<br/>vp09.00.41.08<br/>av01.0.12M.08 |
| VBR        | 视频比特率 | 2319k                                           |
| ACODEC     | 音频编码  | mp4a.40.2/opus/unknown                          |
| ABR        | 音频比特率 | 130k                                            |
| MORE INFO  | 更多信息  | 1080p60, mp4_dash<br/>1440p60, webm_dash        |

render_formats_table

format_field(f, 'filesize', ' \t%s', func=format_bytes)
or format_field(f, 'filesize_approx', '≈\t%s', func=format_bytes)

format_bytes(int(info_dict['duration'] * f['tbr'] * (1024 / 8)))


'MiB': 1024 ** 2,


"tbr": 3790.163,"vbr": 3790.163,
~ 22.67MiB

### video_format
"format_id": "311",
"format_note": "720p", "720p60",
"tbr": 3506.341,
"ext": "mp4";"webm",
"fps": 60.0, 30.0,
"vcodec": "avc1.4D4020";"vp09.00.40.08","av01.0.08M.08"  (尽量使用avc和av1，1080p及以下不使用vp9)
"resolution": "1280x720", (大于"854x480")
"vbr": 3506.341,
"format": "311 - 1280x720"

### audio_format
"format_id": "233",
"format_note": "Default","low","medium", (无", DRC")
"language": "en",
"ext": "mp4","m4a", "webm",
"resolution": "audio only",
"tbr": 30.291015625,
"acodec": "mp4a.40.5",
"abr": 30.291015625,
"format": "599 - audio only (ultralow)"
