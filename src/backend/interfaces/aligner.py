from abc import ABC, abstractmethod
from typing import Any, Callable


class Aligner(ABC):
    """两段指纹序列对齐的统一接口；返回值是按 sequence1 下标索引、已消歧的唯一对应列表。"""

    @abstractmethod
    def align(self, sequence1: list, sequence2: list, dist_fn: Callable[[Any, Any], float]) -> list:
        raise NotImplementedError
