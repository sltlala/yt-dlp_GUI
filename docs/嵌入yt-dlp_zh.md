# 嵌入 YT-DLP

yt-dlp 尽最大努力成为一个优秀的命令行程序，因此可以从任何编程语言中调用。

你的程序应该避免解析正常的 stdout，因为它们在未来的版本中可能会改变。
相反，它们应该使用 `-J`、`--print`、`--progress-template`、`--exec` 等选项来创建你可以可靠地复制和解析的控制台输出。

在 Python 程序中，你可以用更强大的方式嵌入 yt-dlp，就像这样：

```python
from yt_dlp import YoutubeDL

URLS = ['https://www.youtube.com/watch?v=BaW_jenozKc']
with YoutubeDL() as ydl:
    ydl.download(URLS)
```

大多数情况下，你需要使用各种选项。有关可用选项的列表，请参阅 [`yt_dlp/YoutubeDL.py`](yt_dlp/YoutubeDL.py#L183) 或 Python shell 中的 `help(yt_dlp.YoutubeDL)` 。
如果你已经熟悉 CLI，可以使用 [`devscripts/cli_too_api.py`](https://github.com/yt-dlp/yt-dlp/blob/master/devscripts/cli_to_api.py) 将任何 CLI 开关转换为 `YoutubeDL` 参数。

**提示**: 如果您要将代码从 youtube-dl 移植到 yt-dlp，需要注意的一个要点是，我们并不保证 `YoutubeDL.extract_info` 的返回值是 json 序列化的，或者甚至是一个字典。
它将类似于字典，但如果你想确保它是一个可序列化的字典，请将它通过 `YoutubeDL.sanitize_info` 传递，如 [下面的示例](#提取信息) 所示

## 嵌入示例

#### 提取信息

```python
import json
import yt_dlp

URL = 'https://www.youtube.com/watch?v=BaW_jenozKc'

# ℹ️ 有关可用选项和公共函数的列表，请参阅 help(yt_dlp.YoutubeDL)
ydl_opts = {}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(URL, download=False)

    # ℹ️ ydl.sanitize_info 使信息可 json 序列化
    print(json.dumps(ydl.sanitize_info(info)))
```
#### 使用 info-json 下载

```python
import yt_dlp

INFO_FILE = 'path/to/video.info.json'

with yt_dlp.YoutubeDL() as ydl:
    error_code = ydl.download_with_info_file(INFO_FILE)

print('某些视频下载失败' if error_code
      else '成功下载所有视频')
```

#### 提取音频

```python
import yt_dlp

URLS = ['https://www.youtube.com/watch?v=BaW_jenozKc']

ydl_opts = {
    'format': 'm4a/bestaudio/best',
    # ℹ️ 请参阅 help(yt_dlp.postprocessor) 获取可用后处理器及其参数的列表
    'postprocessors': [{  # 使用 ffmpeg 提取音频
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'm4a',
    }]
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    error_code = ydl.download(URLS)
```

#### 筛选视频

```python
import yt_dlp

URLS = ['https://www.youtube.com/watch?v=BaW_jenozKc']

def longer_than_a_minute(info, *, incomplete):
    """只下载超过一分钟的视频（或时长未知的视频）"""
    duration = info.get('duration')
    if duration and duration < 60:
        return 'The video is too short'

ydl_opts = {
    'match_filter': longer_than_a_minute,
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    error_code = ydl.download(URLS)
```

#### 添加日志记录器和进度钩子

```python
import yt_dlp

URLS = ['https://www.youtube.com/watch?v=BaW_jenozKc']

class MyLogger:
    def debug(self, msg):
        # 为了与 youtube-dl 兼容，调试和信息都会传入调试程序
        # 您可以通过前缀"[debug]"来区分它们。
        if msg.startswith('[debug] '):
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
    if d['status'] == 'finished':
        print('Done downloading, now post-processing ...')


ydl_opts = {
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(URLS)
```

#### 添加自定义 PostProcessor

```python
import yt_dlp

URLS = ['https://www.youtube.com/watch?v=BaW_jenozKc']

# ℹ️ 请参阅 help(yt_dlp.postprocessor) 获取可用后处理器及其参数的列表
class MyCustomPP(yt_dlp.postprocessor.PostProcessor):
    def run(self, info):
        self.to_screen('Doing stuff')
        return [], info


with yt_dlp.YoutubeDL() as ydl:
    # ℹ️ "when "可以取 yt_dlp.utils.POSTPROCESS_WHEN 中的任意值。
    ydl.add_post_processor(MyCustomPP(), when='pre_process')
    ydl.download(URLS)
```


#### 使用自定义格式选择器

```python
import yt_dlp

URLS = ['https://www.youtube.com/watch?v=BaW_jenozKc']

def format_selector(ctx):
    """选择不会生成 mkv 的最佳视频和最佳音频。
    注意：这只是一个示例，并不能处理所有情况 """

    # 格式已从最差到最佳排序
    formats = ctx.get('formats')[::-1]

    # acodec='none' 表示没有音频
    best_video = next(f for f in formats
                      if f['vcodec'] != 'none' and f['acodec'] == 'none')

    # 查找兼容的音频扩展
    audio_ext = {'mp4': 'm4a', 'webm': 'webm'}[best_video['ext']]
    # vcodec='none'表示没有视频
    best_audio = next(f for f in formats if (
        f['acodec'] != 'none' and f['vcodec'] == 'none' and f['ext'] == audio_ext))

    # 这些是合并格式的最低必填字段
    yield {
        'format_id': f'{best_video["format_id"]}+{best_audio["format_id"]}',
        'ext': best_video['ext'],
        'requested_formats': [best_video, best_audio],
        # 必须是 + 分隔的协议列表
        'protocol': f'{best_video["protocol"]}+{best_audio["protocol"]}'
    }


ydl_opts = {
    'format': format_selector,
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(URLS)
```

<!-- MANPAGE: MOVE "NEW FEATURES" SECTION HERE -->
