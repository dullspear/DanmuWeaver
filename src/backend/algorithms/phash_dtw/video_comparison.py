import cv2
from concurrent.futures import ThreadPoolExecutor
from fastdtw import fastdtw
from scipy.spatial.distance import hamming
from src.backend.algorithms.phash_dtw.video_processing import get_phash_sequence


# 比较两个视频帧
def compare_video(src_video, dst_video, frame_interval=1,signals=None):
    """
    比较两个视频的帧，并计算最优路径。

    :param src_video: 源视频路径
    :param dst_video: 目标视频路径
    :param frame_interval: 每隔多少秒处理一帧
    :return: 最优路径
    """
    video1 = cv2.VideoCapture(src_video)
    video2 = cv2.VideoCapture(dst_video)
    print(int(video1.get(cv2.CAP_PROP_FRAME_COUNT)))
    print(int(video2.get(cv2.CAP_PROP_FRAME_COUNT)))

    with ThreadPoolExecutor() as executor:
        future1 = executor.submit(get_phash_sequence, video1, frame_interval, "short", signals,1)
        future2 = executor.submit(get_phash_sequence, video2, frame_interval, "long", signals,2)

        sequence1 = future1.result()
        sequence2 = future2.result()

        print("sequence1.len:", len(sequence1))
        print("sequence2.len:", len(sequence2))

    distance, path = fastdtw(sequence1, sequence2, dist=hamming)
    return path
