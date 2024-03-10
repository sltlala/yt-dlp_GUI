# 格式选择

默认情况下，如果您**不**通过任何选项，yt-dlp 会尝试下载现有的最佳质量。
这通常等同于使用 `-f bestvideo*+bestaudio/best`。不过，如果启用了多音频流 (`--audio-multistreams`)，默认格式将变为 `-f bestvideo+bestaudio/best`。
同样，如果 ffmpeg 不可用，或使用 yt-dlp 将视频流传输到 `stdout` (`-o -`)，默认格式将变为 `-f best/bestvideo+bestaudio`。

**停用警告**: 最新版本的 yt-dlp 可以使用 ffmpeg 将多种格式同时流式传输到 stdout。
因此，在未来的版本中，默认设置将与普通下载类似，设置为 `-f bv*+ba/b` 。如果要保留 `-f b/bv+ba` 设置，建议在配置选项中明确指定。

格式选择的一般语法是 `-f FORMAT`（或 `--format FORMAT`），其中 `FORMAT` 是*选择表达式*，即描述您希望下载的一种或多种格式的表达式。

<!-- MANPAGE: BEGIN EXCLUDED SECTION -->
**tl;dr:** [引导我查看示例](#格式选择示例).
<!-- MANPAGE: END EXCLUDED SECTION -->

最简单的情况是请求特定格式；例如，使用 `-f 22` 可以下载格式代码等于 22 的格式。
您可以使用 `--list-formats` 或 `-F` 获取特定视频的可用格式代码列表。请注意，这些格式代码是特定于提取器的。

您还可以使用文件扩展名（目前支持 `3gp`、`aac`、`flv`、`m4a`、`mp3`、`mp4`、`ogg`、`wav` 和 `webm`）
来下载作为单个文件提供的特定文件扩展名的最佳质量格式，例如，`-f webm` 将下载作为单个文件提供的具有 `webm` 扩展名的最佳质量格式。

您可以使用 `-f -` 以交互方式为*每个视频*提供格式选择器。

您还可以使用特殊名称来选择特定的边缘格式：

- `all`: 分别选择**所有格式**
- `mergeall`: 选择并**合并所有格式**（必须与"--audio-multistreams"、"--video-multistreams"或两者一起使用）
- `b*`, `best*`: 选择质量最好的格式，**包含**视频或音频，或两者都包含 (即; `vcodec!=none or acodec!=none`)
- `b`, `best`: 选择质量最好的格式，**同时包含**视频和音频。相当于 `best*[vcodec!=none][acodec!=none]`
- `bv`, `bestvideo`: 选择质量最好的**纯视频**格式。等同于 `best*[acodec=none]`
- `bv*`, `bestvideo*`: 选择**包含视频**的最佳质量格式。也可能包含音频。等同于`best*[vcodec!=none]`。
- `ba`, `bestaudio`: 选择质量最好的**纯音频**格式。等同于`best*[vcodec=none]`。
- `ba*`, `bestaudio*`: 选择**包含音频**的最佳质量格式。也可能包含视频。等同于`best*[acodec!=none]`。 ([Do not use!](https://github.com/yt-dlp/yt-dlp/issues/979#issuecomment-919629354))
- `w*`, `worst*`: 选择包含视频或音频的质量最差的格式
- `w`, `worst`: 选择包含视频和音频的质量最差的格式。等同于`worst*[vcodec!=none][acodec!=none]`。
- `wv`, `worstvideo`: 选择质量最差的纯视频格式。等同于 `worst*[acodec=none]`
- `wv*`, `worstvideo*`: 选择包含视频的质量最差的格式。也可能包含音频。等同于`worst*[vcodec!=none]`。
- `wa`, `worstaudio`: 选择质量最差的纯音频格式。等同于 `worst*[vcodec=none]`
- `wa*`, `worstaudio*`: 选择质量最差的音频格式。也可能包含视频。等同于`worst*[acodec!=none]`。

例如，要下载质量最差的纯视频格式，可以使用 `-f worstvideo`。但建议不要使用 `worst` 和相关选项。当格式选择器为 "worst "时，将选择各方面都最差的格式。
大多数情况下，您需要的实际上是文件最小的视频。因此，通常最好使用 `-S +size` 或更严格的 `-S +size,+br,+res,+fps` 而不是 `-f worst`。详见 [排序格式](#排序格式)。

您可以使用 `best<type>.<n>`，选择某一类型的第 n 个最佳格式。例如，`best.2` 将选择第 2 个最佳组合格式。同样，`bv*.3` 将选择包含视频流的第 3 种最佳格式。

如果您想下载多个视频，但它们的可用格式不尽相同，您可以使用斜线指定优先顺序。请注意，左手边的格式优先；
例如，`-f 22/17/18` 如果有可用的格式，将下载格式 22，否则将下载格式 17，否则将下载格式 18，否则将抱怨没有合适的格式可供下载。

如果要下载同一视频的几种格式，请使用逗号作为分隔符，例如，`-f 22,17,18` 将下载所有这三种格式，当然前提是它们可用。
或者一个更复杂的例子，结合优先级功能：`-f 136/137/mp4/bestvideo,140/m4a/bestaudio`。

您可以使用 `-f <format1>+<format2>+...` 将多种格式的视频和音频合并到一个文件中（需要安装 ffmpeg）；例如，`-f bestvideo+bestaudio` 将下载最佳纯视频格式和最佳纯音频格式，并用 ffmpeg 将它们混合在一起。

**停用警告**: 由于*下面*描述的行为既复杂又违反直觉，因此将删除该操作符，并在未来默认启用多数据流。此外，还将添加一个新的操作符，将格式限制为单一音频/视频

除非使用"--video-multistreams"（视频多流），否则除第一个视频流外，所有视频流格式都将被忽略。同样，除非使用"--audio-multistreams"，否则除第一个格式外，所有带有音频流的格式都会被忽略。
例如，`-f bestvideo+best+bestaudio --video-multistreams --audio-multistreams` 将下载并合并所有给定的 3 种格式。生成的文件将有 2 个视频流和 2 个音频流。
而 `-f bestvideo+best+bestaudio --no-video-multistreams` 将只下载和合并 `bestvideo` 和 `bestaudio`。best "会被忽略，因为另一种包含视频流的格式（"bestvideo"）已被选中。
因此，格式的顺序很重要。`-f best+bestaudio --noaudio-multistreams` 只下载`best`，而 `-f bestaudio+best --noaudio-multistreams` 则忽略`best`，只下载`bestaudio`。

## 过滤格式

您还可以通过在括号中加入条件来筛选视频格式，如 `-f "best[height=720]"（或 `-f "[文件大小>10M]"，因为没有选择器的筛选器会被解释为 "best"）。

以下数字元字段可用于比较 `<`、`<=`、`>`、`>=`、`=`（相等）、`！=`（不相等）：

- `filesize`：字节数（如果已知）
- `filesize_approx`：估计字节数
- `width`：视频的宽度（如果已知）
- `height`：视频的高度（如果已知）
- `aspect_ratio`：视频的宽高比（如果已知）
- `tbr`：音频和视频的平均比特率（KBit/s）
- `abr`：音频平均比特率（KBit/s）
- `vbr`：视频平均比特率（KBit/s）
- `asr`：音频采样率（Hz）
- `fps`：帧率
- `audio_channels`：音频通道数
- `stretched_ratio`：视频像素的`width:height`（如果不是正方形）

过滤功能还可用于比较`=`(等于)、`^=`(以...开始)、`$=`(以...结束)、`*=`(包含)、`~=`(匹配 regex) 和以下字符串元字段：

- `url`：视频 URL
- `ext`：文件扩展名
- `acodec`：使用的音频编解码器名称
- `vcodec`：使用中的视频编解码器名称
- `容器`：容器格式名称
- `protocol`：实际下载将使用的协议，小写（`http`,`https`,`rtsp`,`rtmp`,`rtmpe`,`mms`,`f4m`,`ism`,`http_dash_segments`,`m3u8`, 或`m3u8_native`)
- `语言`：语言代码
- `dynamic_range`：视频的动态范围
- `format_id`：格式的简短描述
- `format`：格式的可读描述
- `format_note`：关于格式的附加信息
- `分辨率`：宽度和高度的文字描述

任何字符串比较前都可以加上否定前缀`!`，以产生相反的比较结果，例如`!*=`（不包含）。如果字符串比较的比较对象包含空格或除 `._-` 以外的特殊字符，则需要使用双引号或单引号。

**备注**: 上述元数据字段都不能保证出现，因为这完全取决于特定提取器获得的元数据，即网站提供的元数据。提取器提供的任何其他字段也可用于过滤。

除非在运算符后加上问号 (`?`)，否则会排除未知值的格式。您可以组合格式过滤器，因此 `-f "bv[height<=?720][tbr>500]"`
最多可选择比特率至少为500KBit/s的720p视频（或高度未知的视频）。您还可以使用带有 `all` 的筛选器下载符合筛选器要求的所有格式，例如 `-f "all[vcodec=none]"` 选择所有纯音频格式。

格式选择器也可使用括号分组；例如，`-f "(mp4,webm)[height<480]"` 将下载高度低于 480 的最佳预合并 mp4 和 webm 格式。

## 排序格式

您可以使用 `-S`（`--format-sort`）来更改被视为"最佳"的标准。一般格式为 `--format-sort field1,field2...`。

可用字段有：

- `hasvid`：优先处理有视频流的格式
- `hasaud`：优先处理有音频流的格式
- `ie_pref`：格式首选项
- `lang`：语言首选项
- `quality`：格式的质量
- `source`：源的首选项
- `proto`: 下载使用的协议 (`https`/`ftps` > `http`/`ftp` > `m3u8_native`/`m3u8` > `http_dash_segments`> `websocket_frag` > `mms`/`rtsp` > `f4f`/`f4m`)
- `vcodec`: 视频编解码器 (`av01` > `vp9.2` > `vp9` > `h265` > `h264` > `vp8` > `h263` > `theora` > 其他)
- `acodec`: 音频编解码器 (`flac`/`alac` > `wav`/`aiff` > `opus` > `vorbis` > `aac` > `mp4a` > `mp3` > `ac4` > `eac3` > `ac3` > `dts` > 其他)
- `codec`: 相当于 `vcodec,acodec`
- `vext`: 视频扩展 (`mp4` > `mov` > `webm` > `flv` > other). 如果使用了 `--prefer-free-formats`，则首选 `webm`。
- `aext`: 音频扩展 (`m4a` > `aac` > `mp3` > `ogg` > `opus` > `webm` > other). 如果使用了`--prefer-free-formats`，顺序将变为`ogg` > `opus` > `webm` > `mp3` > `m4a` > `aac`
- `ext`: 相当于 `vext,aext`
- `filesize`: 如果事先知道准确的文件大小
- `fs_approx`：大致文件大小
- `size`：如果有精确文件大小，否则为近似文件大小
- `height`：视频高度
- `width`：视频宽度
- `res`：视频分辨率，以最小尺寸计算。
- `fps`：视频帧频
- `hdr`：视频的动态范围（`DV` > `HDR12` > `HDR10+` > `HDR10` > `HLG` > `SDR`）
- `channels`：音频通道的数量
- `tbr`：以 KBit/s 为单位的总平均比特率
- `vbr`：平均视频比特率（KBit/s）
- `abr`：平均音频比特率（KBit/s）
- `br`：以 KBit/s 为单位的平均比特率，`tbr`/`vbr`/`abr`
- `asr`：音频采样率（单位 Hz）

**停用警告**: 其中许多字段都有别名（目前尚未记录），这些别名可能会在未来版本中删除。建议只使用记录在案的字段名。

除非另有说明，否则所有字段都按降序排序。若要反向排序，请在字段前加上 `+`。例如，`+res`表示首选分辨率最小的格式。
此外，您还可以为字段添加一个首选值，并用`:`分隔。例如，`res:720`首选较大的视频，但不大于 720p，如果没有小于 720p 的视频，则首选最小的视频。
对于`codec`和`ext`，您可以提供两个首选值，第一个用于视频，第二个用于音频。
例如，`+codec:avc:m4a`（相当于`+vcodec:avc,+acodec:m4a`）会将视频编解码器首选项设置为 `h264` > `h265` > `vp9` > `vp9.2` > `av01` > `vp8` > `h263` > `theora`，
音频编解码器首选项为 `mp4a` > `aac` > `vorbis` > `opus`>`mp3`>`ac3`>`dts`。还可以使用 `~` 作为分隔符，使排序优先选择与所提供值最接近的值。
例如，`filesize~1G`优先选择文件大小最接近 1 GiB 的格式。

无论用户定义的顺序如何，`hasvid`和 `ie_pref`字段在排序时总是优先级最高。使用 `--format-sort-force`可以改变这种行为。
除此之外，默认使用的顺序是：`lang,quality,res,fps,hdr:12,vcodec:vp9.2,chanels,acodec,size,br,asr,proto,ext,hasaud,source,id`。提取器可以覆盖默认顺序，但不能覆盖用户提供的顺序。

请注意，默认设置为 `vcodec:vp9.2`；即不首选 `av1`。同样，hdr 的默认设置为 `hdr:12`；即不首选 dolby vision。
做出这些选择是因为 DV 和 AV1 格式尚未与大多数设备完全兼容。随着越来越多的设备能够流畅地播放这些格式，将来可能会有所改变。

如果格式选择器为 `worst`，排序后将选择最后一项。这意味着它会选择各方面都最差的格式。大多数情况下，你真正想要的是文件大小最小的视频。
因此，通常使用 `-f best -S +size,+br,+res,+fps` 会更好。

**提示**: 您可以使用 `-v -F` 查看格式的排序情况（从最差到最佳）。

## 格式选择示例

```bash
# 下载并合并最佳纯视频格式和最佳纯音频格式、
# 如果没有纯视频格式，则下载最佳组合格式
$ yt-dlp -f "bv+ba/b"

# 下载包含视频的最佳格式、
# 如果还没有音频流，则与最佳纯音频格式合并
$ yt-dlp -f "bv*+ba/b"

# 同上
$ yt-dlp

# 下载最佳纯视频格式和最佳纯音频格式，但不合并它们
# 在这种情况下，应使用输出模板，因为
# 默认情况下，bestvideo 和 bestaudio 的文件名相同。
$ yt-dlp -f "bv,ba" -o "%(title)s.f%(format_id)s.%(ext)s"

# 下载并合并有视频流的最佳格式、
# 和所有纯音频格式合并为一个文件
$ yt-dlp -f "bv*+mergeall[vcodec=none]" --audio-multistreams

# 下载并合并有视频流的最佳格式、
# 和最好的两种纯音频格式合并成一个文件
$ yt-dlp -f "bv*+ba+ba.2" --audio-multistreams

# 下面的示例展示了格式选择的老方法（不使用 -S）以及如何使用 -S 达到类似但（一般来说）更好的效果。
# 以及如何使用 -S 来实现类似但（通常）更好的结果

# 下载最差的视频（旧方法）
$ yt-dlp -f "wv*+wa/w"

# 下载最好的视频，但分辨率最小
$ yt-dlp -S "+res"

# 下载最小的视频
$ yt-dlp -S "+size,+br"

# 下载可用的最佳 mp4 视频，如果没有可用的 mp4，则下载最佳视频
$ yt-dlp -f "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4] / bv*+ba/b"

# 用最佳扩展名下载最佳视频
# 视频：mp4 > mov > webm > flv。 音频：m4a > aac > mp3 ...)
$ yt-dlp -S "ext"


# 下载最好的视频，但不超过 480p、
# 如果没有低于 480p 的视频，则下载最差的视频
$ yt-dlp -f "bv*[height<=480]+ba/b[height<=480] / wv*+ba/w"

# 下载高度最大但不超过 480p 的最佳视频、
# 如果没有分辨率低于 480p 的视频，则下载分辨率最小的最佳视频
$ yt-dlp -S "height:480"

# 下载分辨率最大但不超过 480p 的最佳视频、
# 如果没有分辨率低于 480p 的视频，则下载分辨率最小的最佳视频
# 分辨率由最小尺寸决定。
# 因此，这也适用于垂直视频
$ yt-dlp -S "res:480"


# 下载最好的视频（也有音频），但大小不超过 50 MB、
# 如果没有 50 MB 以下的视频，则下载最差的视频（也有音频）。
$ yt-dlp -f "b[filesize<50M] / w"

# 下载最大的视频（也有音频），但不超过 50 MB、
# 如果没有 50 MB 以下的视频，则下载最小的视频（也有音频）。
$ yt-dlp -f "b" -S "filesize:50M"

# 下载大小最接近 50 MB 的最佳视频（也有音频）。
$ yt-dlp -f "b" -S "filesize~50M"


# 通过 HTTP/HTTPS 协议的直接链接下载最佳视频、
# 如果没有视频，则通过任何协议下载最佳视频
$ yt-dlp -f "(bv*+ba/b)[protocol^=http][protocol!*=dash] / (bv*+ba/b)"

# 通过最佳协议下载最佳视频
# (https/ftps > http/ftp > m3u8_native > m3u8 > http_dash_segments ...)
$ yt-dlp -S "proto"


# 下载带有 h264 或 h265 编解码器的最佳视频、
# 如果没有此类视频，则下载最佳视频
$ yt-dlp -f "(bv*[vcodec~='^((he|a)vc|h26[45])']+ba) / (bv*+ba/b)"

# 下载最佳编解码器的最佳视频，不优于 h264、
# 如果没有，则下载编解码最差的最佳视频
$ yt-dlp -S "codec:h264"

# 下载最好的视频，编解码不比 h264 差、
# 如果没有，则下载最佳编解码器的最佳视频
$ yt-dlp -S "+codec:h264"


# 更复杂的例子

# 下载最好的视频，不优于 720p，帧速率大于 30、
# 如果没有这样的视频，则下载最差的视频（帧速率仍大于 30
$ yt-dlp -f "((bv*[fps>30]/bv*)[height<=720]/(wv*[fps>30]/wv*)) + ba / (b[fps>30]/b)[height<=720]/(w[fps>30]/w)"

# 下载最大分辨率不超过 720p 的视频、
# 如果没有，则下载分辨率最小的视频、
# 对于分辨率相同的格式，优先选择较大的帧率
$ yt-dlp -S "res:720,fps"


# 下载最小分辨率不低于 480p 的视频、
# 如果没有，则下载分辨率最大的视频、
# 在相同分辨率下，优先选择更好的编解码器和更高的总比特率
$ yt-dlp -S "+res:480,codec,br"
```
