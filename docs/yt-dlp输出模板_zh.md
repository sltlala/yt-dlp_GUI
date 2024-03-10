# 输出模板

选项 `-o` 用于指定输出文件名的模板，而选项 `-P` 则用于指定每类文件应保存的路径。

<!-- MANPAGE: BEGIN EXCLUDED SECTION -->
**tl;dr:** [引导我查看示例](#输出模板示例).
<!-- MANPAGE: END EXCLUDED SECTION -->

`-o` 的最简单用法是在下载单个文件时不设置任何模板参数，如 `yt-dlp -o funny_video.flv "https://some/video"` （不建议硬编码文件扩展名，这样可能会破坏某些后处理）。

不过，它也可能包含一些特殊序列，这些序列将在下载每个视频时被替换。特殊序列可以根据 [Python 字符串格式化操作](https://docs.python.org/3/library/stdtypes.html#printf-style-string-formatting) 进行格式化，
例如 `%(NAME)s` 或 `%(NAME)05d`。说明一下，这是一个百分号，后面是括号中的名称，后面是格式化操作。

字段名本身（括号内的部分）也可以有一些特殊格式：

1.**对象遍历**：使用点`.`分隔符可以遍历元数据中的字典和列表，例如`%(tags.0)s`, `%(subtitles.en.-1.ext)s`。
可以用冒号 `:` 进行Python分割；例如 `%(id.3:7:-1)s`, `%(formats.:.format_id)s`.大括号 `{}` 可以用来建立只有特定键的字典；
例如 `%(format.:.{format_id,height})#j`。空字段名`%()s`指的是整个信息字典；例如`%(.{id,title})s`。请注意，下面没有列出使用此方法可获得的所有字段。使用 `-j` 查看这些字段

2.**算术**：可以使用 `+`、`-` 和 `*` 对数字字段进行简单运算。例如，`%(playlist_index+10)03d`，`%(n_entries+1-playlist_index)d`。

3.**日期/时间格式化**：日期/时间字段可根据 [strftime格式化](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes) 格式化，
具体方法是使用`>`将其与字段名分隔开来。例如：`%(持续时间>%H-%M-%S)s`, `%(上传日期>%Y-%m-%d)s`, `%(纪元-3600>%H-%M-%S)s`。

4.**替代字段**：可以用`,`分隔指定备用字段。例如 `%(release_date>%Y,upload_date>%Y|Unknown)s`.

5.**替换**：可根据 [`str.format`迷你语言](https://docs.python.org/3/library/string.html#format-specification-mini-language) 使用`&`分隔符指定替换值。
如果字段*非*空，则将使用该替换值代替实际字段内容。这是在考虑了备选字段之后进行的；因此，如果**个备选字段**不是空的，就会使用替换值。例如，`%(chapters&has chapters|no chapters)s`, `%(title&TITLE={:>20}|NO TITLE)s`

6.**默认**：当字段为空时，可使用分隔符 `|` 指定字面默认值。这将覆盖 `--output-na-placeholder`。例如，`%(上传者|未知)s`。

7.**更多转换**：除了正常的格式类型 `diouxeEfFgGcrs` 之外，yt-dlp 还支持转换为 `B` = **B**ytes, `j` = **j**son （标志`#`用于漂亮打印，`+`用于 Unicode）,
`h`= HTML转义、`l`= 以逗号分隔的 **l**ist (标志`#`用于`\n`换行分隔), `q` = 字符串 **q**uoted for the terminal (标志 `#` 用于将列表分割成不同的参数),
`D` = 添加 **D**ecimal 后缀 (e. g. 10M) (标志 `#` 用于添加 **D**ecimal 后缀).例如 10M）（标志 `#` 使用 1024 作为因子），以及 `S` = **S*** 量化为文件名（标志 `#` 表示受限）。

8.**Unicode 规范化**：格式类型 `U` 可用于 NFC[统一编码规范化](https://docs.python.org/3/library/unicodedata.html#unicodedata.normalize)。
备用形式标志 (`#`) 可将规范化改为 NFD，转换标志 `+` 可用于 NFKC/NFKD 兼容等效规范化。例如，`%(标题)+.100U` 是 NFKC

概括地说，字段的一般语法是
```
%(name[.keys][addition][>strf][,alternate][&replacement][|default])[flags][width][.precision][length]type
```

此外，您还可以为不同的元数据文件分别设置不同的输出模板，方法是指定文件类型，然后用冒号`:`分隔模板。
支持的不同文件类型包括：`subtitle`、`thumbnail`、`description`、`annotation`（已废弃）、`infojson`、`link`、`pl_thumbnail`、`pl_description`、`pl_infojson`、`chapter`、`pl_video`。
例如，`-o "%(title)s.%(ext)s" -o "thumbnail:%(title)s\%(title)s.%(ext)s"` 将把缩略图放到与视频同名的文件夹中。如果任何模板为空，则不会写入该类型的文件。
例如，`--write-thumbnail -o "thumbnail:"` 将只写入播放列表的缩略图，而不写入视频的缩略图。

<a id="outtmpl后处理说明"/>

**备注**: 由于后期处理（如合并等），实际输出文件名可能会有所不同。使用 `--print after_move:filepath`，可以获得所有后处理完成后的文件名。

可用字段有

- `id` (string)：视频标识符
- `title` (string)：视频标题
- `fulltitle` (string)：忽略实时时间戳和通用标题的视频标题
- `ext` (string)：视频文件扩展名
- `alt_title` (string)：视频的二级标题
- `description` (string)：视频的描述
- `display_id` (string)：视频的替代标识符
- `uploader` (string)：视频上传者的全名
- `uploader_id` (string)：视频上传者的昵称或 ID
- `uploader_url` (string)：视频上传者个人资料的 URL
- `license` (string)：视频的许可证名称
- `creators` (list)：视频的创作者
- `creator` (string)：视频的创作者；以逗号分隔
- `timestamp`(numeric)：视频可用时间的 UNIX 时间戳
- `upload_date` (string)：视频上传日期，以 UTC (YYYYMMDD) 为单位
- `release_timestamp`(numeric)：视频发布时刻的 UNIX 时间戳
- `release_date` (string)：视频发布的日期 (YYYYMMDD)，以 UTC 为单位
- `release_year`(numeric)：视频或专辑发布的年份 (YYYY)
- `modified_timestamp`(numeric)：视频最后一次修改的 UNIX 时间戳
- `modified_date`(string)：视频最后一次修改的日期 (YYYYMMDD)，以 UTC 为单位
- `频道` (string)）：视频上传渠道的全称
- `channel_id` (string)：频道的 ID
- `channel_url` (string)：频道的 URL
- `channel_follower_count` (numeric)：频道的关注者数量
- `channel_is_verified` (string)：频道是否已通过平台验证
- `location` (string)：视频拍摄的实际地点
- `duration` (numeric)：视频长度（秒）
- `duration_string` (string)：视频长度（时：分：秒）
- `view_count` (numeric)：有多少用户在平台上观看了视频
- `concurrent_view_count` (numeric)：当前有多少用户正在平台上观看视频。
- `like_count` (numeric)：视频获得好评的数量
- `dislike_count` (numeric)：视频的负面评分数
- `reost_count` (numeric)：视频被转贴的次数
- `average_rating` (numeric)：用户给出的平均评分，评分标准取决于网页
- `comment_count` (numeric)：视频评论的数量（对于某些提取器，评论只在最后下载，因此无法使用此字段）
- `age_limit` (numeric)：视频的年龄限制（岁）
- `live_status` (string)：not_live"、"is_live"、"is_upcoming"、"was_live"、"post_live"（已直播，但尚未处理点播）中的一个
- `is_live` (string)：该视频是直播流还是固定长度的视频
- `was_live` (string)：该视频最初是否为直播流媒体
- `playable_in_embed` (string)：是否允许在其他网站的嵌入式播放器中播放此视频
- `availability` (string)：视频是 "私人"、"仅限高级"、"仅限订阅者"、"需要验证"、"未列出 "还是 "公开"
- `media_type` (string)：网站划分的媒体类型，例如 "插曲"、"片段"、"预告片"
- `start_time` (numeric)：URL 中指定的重现开始时间（以秒为单位）
- `end_time` (numeric)：URL 中指定的重放结束时间（以秒为单位）
- `extractor` (string)：提取器的名称
- `extractor_key` (string)：提取器的键名
- `epoch` (numeric)：信息提取完成时的 Unix 纪元
- `autonumber` (numeric)：每次下载都会增加的数字，从 `--autonumber-start`开始，用前零填充为 5 位数
- `video_autonumber` (numeric)：每下载一段视频都会增加的数字
- `n_entries` (numeric)：播放列表中已提取项目的总数
- `playlist_id` (string)）：包含视频的播放列表的标识符
- `playlist_title` (string)：包含视频的播放列表的名称
- `playlist` (string)：`playlist_id` 或 `playlist_title`
- `playlist_count` (numeric)：播放列表中项目的总数。如果未提取整个播放列表，则可能不知道
- `playlist_index` (numeric)）：播放列表中视频的索引，根据最终索引用前导零填充
- `playlist_autonumber` (numeric)： 视频在播放列表中的位置：视频在播放列表下载队列中的位置，根据播放列表的总长度用前导零填充
- `playlist_uploader` (string)：播放列表上传者的全名
- `playlist_uploader_id` (string)：播放列表上传者的昵称或 ID
- `webpage_url` (string)：视频网页的 URL，如果提供给 yt-dlp，可以再次获得相同的结果
- `webpage_url_basename` (string)：网页 URL 的基名
- `webpage_url_domain` (string)：网页 URL 的域名
- `original_url` (string)：用户提供的 URL（或与播放列表条目的 `webpage_url` 相同）
- `categories` (list)：视频所属类别列表
- `tags` (list)：分配给视频的标签列表
- `cast` (list)：演员列表

[过滤格式](#过滤格式)中的所有字段也可以使用

适用于属于某个逻辑章节或部分的视频：

- `chapter` (string)：视频所属章节的名称或标题
- `chapter_number` (numeric)：视频所属章节的编号
- `chapter_id` (string)：视频所属章节的 ID

适用于某些系列或节目的一集视频：

- `series` (string)：该集视频所属系列或节目的标题
- `series_id` (string)：该集视频所属系列或节目的 ID
- `season` (string)：该集视频所属季节的标题
- `season_number` (numeric)：该集视频所属季节的编号
- `season_id` (string)：该集视频所属季节的 ID
- `episode` (string)：视频集的标题
- `episode_number` (numeric)：视频集在一季中的编号
- `episode_id` (string)：视频集的 ID

适用于音轨或音乐专辑部分的媒体：

- `track` (string)：曲目标题
- `track_number` (numeric)：音轨在专辑或光盘中的编号
- `track_id`(string)：音轨的 ID
- `艺术家` (list)：音轨的艺术家
- `artist` (string)：音轨的艺术家；以逗号分隔
- `genres` (list)：音轨的流派
- `genre` (string)：音轨的流派；逗号分隔
- `composers` (list)：作品的作曲家
- `composer` (string)：作品的作曲家；逗号分隔
- `album` (string)：曲目所属专辑的标题
- `album_type` (string)：专辑类型
- `album_artists` (list)：专辑中出现的所有艺术家
- `album_artist` (string)：专辑中出现的所有艺术家；以逗号分隔
- `disc_number` (numeric)：音轨所属光盘或其他物理介质的编号

仅在使用`--download-sections`时可用，在使用`--split-chapters`时，`chapter:`前缀可用于有内部章节的视频：

- `section_title` (string)：章节标题
- `section_number` (numeric)：文件中章节的编号
- `section_start` (numeric)：章节的开始时间，以秒为单位
- `section_end` (numeric)：以秒为单位的章节结束时间

仅在 `--print` 中使用时可用：

- `urls` (string)：所有请求格式的 URL，每行一个
- `filename` (string)：视频文件的名称。注意[实际文件名可能不同](#outtmpl后处理说明)
- `formats_table` (table)：由 `--list-formats` 打印的视频格式表
- `thumbnails_table` (table)：由`--list-thumbnails`打印的缩略图格式表
- `subtitles_table` (table)：由 `--list-subs` 打印的字幕格式表
- `automatic_captions_table` (table)：由`--list-subs`打印的自动字幕格式表

仅在下载视频后可用（`post_process`/`after_move`）：

- `filepath`：下载视频文件的实际路径

仅在 `--sponsorblock-chapter-title` 中可用：

- `start_time` (numeric)：以秒为单位的章节开始时间
- `end_time` (numeric)：章节的结束时间，以秒为单位
- `categories` (list)：该章节所属的[赞助商区块类别](https://wiki.sponsor.ajay.app/w/Types#Category)
- `category` (string)：该章节所属的最小赞助商区块类别
- `category_names` (list)：类别的友好名称
- `name` (string)：最小分类的友好名称
- `type` (string)：章节的[赞助商区块动作类型](https://wiki.sponsor.ajay.app/w/Types#Action_Type)

在输出模板中引用上述序列时，每个序列都将被序列名称对应的实际值替换。例如，对于 `-o %(标题)s-%(id)s.%(ext)s`和标题为`yt-dlp test video`
和id为 `BaW_jenozKc` 的mp4视频，这将导致在当前目录下创建一个 `yt-dlp test video-BaW_jenozKc.mp4` 文件。

**注意**：某些序列不保证存在，因为它们取决于特定提取器获得的元数据。这些序列将被用 `--output-na-placeholder`（默认为 `NA`）提供的占位符值替换。

**提示**：查看 `-j` 输出以确定特定 URL 的可用字段

对于数字序列，可以使用[数字相关格式化](https://docs.python.org/3/library/stdtypes.html#printf-style-string-formatting)；
例如，`%(view_count)05d` 将生成一个字符串，其中的查看次数用 0 填充，最多 5 个字符，如`00042`。

输出模板也可以包含任意分层路径，例如 `-o "%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s"`
将导致下载与该路径模板相对应的目录中的每个视频。任何缺失的目录都将自动为您创建。

要在输出模板中使用百分数文字，请使用 `%%`。要输出到 stdout，使用 `-o -`。

当前的默认模板是 `%(title)s [%(id)s].%(ext)s`.

在某些情况下，你不需要中、空格或 & 等特殊字符，例如将下载的文件名传输到 Windows 系统或通过 8 位不安全通道传输文件名时。
在这种情况下，添加"--restrict-filenames "标记可获得更短的标题。

#### 输出模板示例

```bash
$ yt-dlp --print filename -o "test video.%(ext)s" BaW_jenozKc
test video.webm    # 带有正确扩展名的直译名称

$ yt-dlp --print filename -o "%(title)s.%(ext)s" BaW_jenozKc
youtube-dl test video ''_ä↭𝕐.webm    # 各种奇怪的字符

$ yt-dlp --print filename -o "%(title)s.%(ext)s" BaW_jenozKc --restrict-filenames
youtube-dl_test_video_.webm    # 受限制的文件名

# 在单独目录中下载 YouTube 播放列表视频，并按播放列表中的视频顺序编制索引
$ yt-dlp -o "%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s" "https://www.youtube.com/playlist?list=PLwiyx1dc3P2JR9N8gQaQN_BCvlSlap7re"

# 根据上传年份在不同目录中下载 YouTube 播放列表视频
$ yt-dlp -o "%(upload_date>%Y)s/%(title)s.%(ext)s" "https://www.youtube.com/playlist?list=PLwiyx1dc3P2JR9N8gQaQN_BCvlSlap7re"

# 在播放列表索引前加上"-"分隔符，但仅限于可用时
$ yt-dlp -o "%(playlist_index&{} - |)s%(title)s.%(ext)s" BaW_jenozKc "https://www.youtube.com/user/TheLinuxFoundation/playlists"

# 下载 YouTube 频道/用户的所有播放列表，将每个播放列表保存在单独的目录中：
$ yt-dlp -o "%(uploader)s/%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s" "https://www.youtube.com/user/TheLinuxFoundation/playlists"

# 下载 Udemy 课程，将每章内容保存在主页 MyVideos 目录下的单独目录中
$ yt-dlp -u user -p password -P "~/MyVideos" -o "%(playlist)s/%(chapter_number)s - %(chapter)s/%(title)s.%(ext)s" "https://www.udemy.com/java-tutorial"

# 下载整个系列的每一季，将每个系列和每一季保存在 C:/MyVideos 下的单独目录中
$ yt-dlp -P "C:/MyVideos" -o "%(series)s/%(season_number)s - %(season)s/%(episode_number)s - %(episode)s.%(ext)s" "https://videomore.ru/kino_v_detalayah/5_sezon/367617"

# 下载视频为 "C:\MyVideos\uploader\title.ext", 字幕为 "C:\MyVideos\subs\uploader\title.ext"
# 并把所有临时文件放到 "C:/MyVideos\tmp"
$ yt-dlp -P "C:/MyVideos" -P "temp:tmp" -P "subtitle:subs" -o "%(uploader)s/%(title)s.%(ext)s" BaW_jenoz --write-subs

# 下载视频为 "C:\MyVideos\uploader\title.ext" 以及字幕为 "C:\MyVideos\uploader\subs\title.ext"
$ yt-dlp -P "C:/MyVideos" -o "%(uploader)s/%(title)s.%(ext)s" -o "subtitle:%(uploader)s/subs/%(title)s.%(ext)s" BaW_jenozKc --write-subs

# 将下载的视频输出到 stdout
$ yt-dlp -o - BaW_jenozKc
```
