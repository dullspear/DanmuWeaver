import cv2
from concurrent.futures import ThreadPoolExecutor
from src.backend.algorithms.dtw.dtw_aligner import DtwAligner
from src.backend.algorithms.phash.phash_fingerprinter import PhashFingerprinter
from src.backend.interfaces.aligner import Aligner
from src.backend.interfaces.fingerprinter import Fingerprinter
from src.backend.video_processing import get_fingerprint_sequence


# 比较两个视频
def compare_video(src_video, dst_video, frame_interval=1, signals=None,
                   fingerprinter: Fingerprinter = None, aligner: Aligner = None):
    """
    比较两个视频的帧，并计算最优路径。

    :param src_video: 源视频路径
    :param dst_video: 目标视频路径
    :param frame_interval: 每隔多少秒处理一帧
    :param fingerprinter: 单帧指纹实现，默认使用 pHash
    :param aligner: 序列对齐实现，默认使用 DTW
    :return: 按 src_video 采样下标索引的对应关系列表
    """
    if fingerprinter is None:
        fingerprinter = PhashFingerprinter()
    if aligner is None:
        aligner = DtwAligner()

    video1 = cv2.VideoCapture(src_video)
    video2 = cv2.VideoCapture(dst_video)
    print(int(video1.get(cv2.CAP_PROP_FRAME_COUNT)))
    print(int(video2.get(cv2.CAP_PROP_FRAME_COUNT)))

    with ThreadPoolExecutor() as executor:
        future1 = executor.submit(get_fingerprint_sequence, video1, frame_interval, fingerprinter, "short", signals, 1)
        future2 = executor.submit(get_fingerprint_sequence, video2, frame_interval, fingerprinter, "long", signals, 2)

        sequence1 = future1.result()
        sequence2 = future2.result()

        print("sequence1.len:", len(sequence1))
        print("sequence2.len:", len(sequence2))

    path = aligner.align(sequence1, sequence2, fingerprinter.distance)
    return path
