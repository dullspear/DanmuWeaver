def find_missing_segments(mapping: list, long_duration_sec: int, min_gap_sec: int = 3) -> list:
    """给定 short->long 的映射列表和 long 视频总时长，找出 long 里没被 short 任何一秒覆盖到的连续区间。"""
    covered = set(mapping)
    missing = []
    start = None
    for t in range(long_duration_sec):
        if t not in covered:
            if start is None:
                start = t
        elif start is not None:
            if t - start >= min_gap_sec:
                missing.append({"start": start, "end": t})
            start = None
    if start is not None and long_duration_sec - start >= min_gap_sec:
        missing.append({"start": start, "end": long_duration_sec})
    return missing
