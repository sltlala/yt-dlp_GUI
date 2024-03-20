import math


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


def format_bytes(bytes):
    return format_decimal_suffix(bytes, "%.2f%sB", factor=1024) or "N/A"


def float_or_none(v, scale=1, invscale=1, default=None):
    if v is None:
        return default
    try:
        return float(v) * invscale / scale
    except (ValueError, TypeError):
        return default


def format_filesize(file_format, duration_info=None):
    if "filesize" in file_format and file_format["filesize"] is not None:
        return "  %s" % format_bytes(file_format["filesize"])
    elif "filesize_approx" in file_format and file_format["filesize_approx"] is not None:
        return "≈ %s" % format_bytes(file_format["filesize_approx"])
    else:
        try:
            return "~ %s" % format_bytes(int(duration_info * file_format["tbr"] * (1024 / 8)))
        except (TypeError, KeyError):
            print("filesize not found")
