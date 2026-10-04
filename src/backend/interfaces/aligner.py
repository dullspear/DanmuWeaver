from abc import ABC, abstractmethod
from typing import Any, Callable


class Aligner(ABC):
    """两段指纹序列对齐的统一接口，对指纹的具体表示和距离函数完全通用。"""

    @abstractmethod
    def align(self, sequence1: list, sequence2: list, dist_fn: Callable[[Any, Any], float]) -> list:
        raise NotImplementedError
