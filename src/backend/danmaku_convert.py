import re

DIALOGUE_RE = re.compile(r"^Dialogue:\s*\d+,([^,]+),([^,]+),[^,]*,[^,]*,[^,]*,[^,]*,[^,]*,[^,]*,(.*)$")
OVERRIDE_TAG_RE = re.compile(r"\{[^}]*\}")


def ass_to_danmaku_json(ass_path: str) -> list:
    """简化版转换：只取文字和起始时间，颜色/位置统一按滚动弹幕处理。"""
    comments = []
    with open(ass_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.startswith("Dialogue:"):
                continue
            match = DIALOGUE_RE.match(line.strip())
            if not match:
                continue
            start_str, _end_str, raw_text = match.groups()
            text = OVERRIDE_TAG_RE.sub("", raw_text).strip()
            if not text:
                continue
            h, m, s = start_str.split(":")
            time_sec = int(h) * 3600 + int(m) * 60 + float(s)
            comments.append({"time": round(time_sec, 1), "type": 0, "color": 16777215, "author": "", "text": text})
    return comments
