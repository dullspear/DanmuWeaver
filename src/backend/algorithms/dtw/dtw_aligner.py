from typing import Any, Callable

from fastdtw import fastdtw

from src.backend.interfaces.aligner import Aligner


class DtwAligner(Aligner):
    """DTW 对齐实现，对距离函数完全通用，不绑定任何具体指纹算法。"""

    def align(self, sequence1: list, sequence2: list, dist_fn: Callable[[Any, Any], float]) -> list:
        distance, path = fastdtw(sequence1, sequence2, dist=dist_fn)

        grouped = {}
        for i, j in path:
            grouped.setdefault(i, []).append(j)

        return [min(grouped[i], key=lambda j: dist_fn(sequence1[i], sequence2[j])) for i in range(len(sequence1))]
