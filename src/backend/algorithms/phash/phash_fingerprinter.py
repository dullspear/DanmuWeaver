from scipy.spatial.distance import hamming

from src.backend.algorithms.phash.phash import pHash
from src.backend.interfaces.fingerprinter import Fingerprinter


class PhashFingerprinter(Fingerprinter):
    """感知哈希（pHash）指纹实现，配套 hamming 距离。"""

    def fingerprint(self, frame):
        return pHash(frame)

    def distance(self, a, b) -> float:
        return hamming(a, b)
