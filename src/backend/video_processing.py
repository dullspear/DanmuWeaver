import cv2
from src.backend.interfaces.fingerprinter import Fingerprinter


# 获取视频的指纹序列
def get_fingerprint_sequence(video: cv2.VideoCapture, frame_interval: int, fingerprinter: Fingerprinter,
                       name: str = "None", signals=None,
                       progress_bar_index=1) -> list:
    sequence = []
    if not video.isOpened():
        # print("Failed to open video")
        return []
    # print(name)
    fps = video.get(cv2.CAP_PROP_FPS)
    # print(name+str(fps))
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_duration = total_frames / fps *1000

    processed_frames = 0
    last_processed_time = -frame_interval * 1000


    retval, frame = video.read()
    retval, frame = video.read() # 先读两帧，有些视频首帧有bug
    while True:
        current_time = video.get(cv2.CAP_PROP_POS_MSEC)
        #print(name+str(current_time))
        if current_time == 0 :
            # print(name+"end")
            break





        print(name, current_time)
        if current_time >= last_processed_time + frame_interval * 1000:
            # print(name+"a")
            retval, frame = video.read()
            if not retval:
                print(name+"b")
                break

            last_processed_time = current_time // 1000 * 1000
            fingerprint = fingerprinter.fingerprint(frame)
            sequence.append(fingerprint)


            progress_value = int((current_time / frame_duration) * 100)+1
            # print(name+"d")
            # 更新进度条
            if signals:
                if progress_bar_index == 1:
                    signals.progress_video1.emit(progress_value)
                elif progress_bar_index == 2:
                    signals.progress_video2.emit(progress_value)
            # print(name + "e")
        else:
            video.grab()
            # print(name+"c")
    #


    return sequence
