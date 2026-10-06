from typing import Any, Callable

import numpy as np
from dtaidistance import dtw

from src.backend.interfaces.aligner import Aligner


class DtwAligner(Aligner):
    """窗口限制的精确DTW(C加速)，核心对齐步骤要求 dist_fn 等价于 squared euclidean(比如0/1向量上的hamming距离)，消歧步骤仍用 dist_fn 本身。"""

    def __init__(self, window: int = 300):
        self.window = window

    def align(self, sequence1: list, sequence2: list, dist_fn: Callable[[Any, Any], float]) -> list:
        seq1_np = np.array(sequence1, dtype=np.double)
        seq2_np = np.array(sequence2, dtype=np.double)
        path = dtw.warping_path(seq1_np, seq2_np, use_ndim=True, window=self.window, use_c=True)

        grouped = {}
        for i, j in path:
            grouped.setdefault(i, []).append(j)

        return [min(grouped[i], key=lambda j: dist_fn(sequence1[i], sequence2[j])) for i in range(len(sequence1))]
