import math
import re


def format_decimal_suffix(num, fmt="%d%s", *, factor=1000):
    """Formats numbers with decimal sufixes like K, M, etc"""
    num, factor = float_or_none(num), float(factor)
    if num is None or num < 0:
        return None
    POSSIBLE_SUFFIXES = "kMGTPEZY"
    exponent = 0 if num == 0 else min(int(math.log(num, factor)), len(POSSIBLE_SUFFIXES))
    suffix = ["", *POSSIBLE_SUFFIXES][exponent]
    if factor == 1024:
        suffix = {"k": "Ki", "": ""}.get(suffix, f"{suffix}i")
    converted = num / (factor**exponent)
    return fmt % (converted, suffix)


def str_to_bool(value):
    value = value.lower()
    if value == "true":
        return True
    elif value == "false":
        return False
    else:
        raise ValueError(f"Invalid boolean value: {value}")


def format_bytes(bytes):
    return format_decimal_suffix(bytes, "%.2f%sB", factor=1024) or "N/A"


def float_or_none(v, scale=1, invscale=1, default=None):
    if v is None:
        return default
    try:
        return float(v) * invscale / scale
    except (ValueError, TypeError):
        return default


def format_filesize(f, duration_info=None):
    # f是输入的file_format数据
    if "filesize" in f and f["filesize"] is not None:
        return "  %s" % format_bytes(f["filesize"])
    elif "filesize_approx" in f and f["filesize_approx"] is not None:
        return "≈ %s" % format_bytes(f["filesize_approx"])
    else:
        try:
            # 根据tbr和时长估算文件大小
            return "~ %s" % format_bytes(int(duration_info * f["tbr"] * (1024 / 8)))
        except (TypeError, KeyError):
            print("filesize not found")


# 正则表达式验证链接格式
def is_valid_url(url):
    pattern = re.compile(
        r"^(?:https?://)?"  # 协议
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|)"  # 域名
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )
    return re.match(pattern, url) is not None
