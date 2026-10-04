from abc import ABC, abstractmethod


class Fingerprinter(ABC):
    """单帧画面指纹提取的统一接口，distance 必须和 fingerprint 的输出表示匹配。"""

    @abstractmethod
    def fingerprint(self, frame):
        raise NotImplementedError

    @abstractmethod
    def distance(self, a, b) -> float:
        raise NotImplementedError
