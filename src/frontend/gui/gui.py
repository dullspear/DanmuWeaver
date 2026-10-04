from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QLineEdit,
    QFileDialog, QMessageBox, QVBoxLayout, QWidget, QProgressBar
)
from PySide6.QtCore import Qt, Signal, QThread, QObject
from src.backend.video_comparison import compare_video
from src.backend.switch import switch
import os

# 定义一个信号类，用于线程间通信
class ProgressSignals(QObject):
    progress_video1 = Signal(int)
    progress_video2 = Signal(int)
    finished = Signal()

class VideoProcessingThread(QThread):
    def __init__(self, input_video_path, output_video_path, input_ass_path, signals):
        super().__init__()
        self.input_video_path = input_video_path
        self.output_video_path = output_video_path
        self.input_ass_path = input_ass_path
        self.signals = signals

    def run(self):
        try:
            video_file_name = os.path.basename(self.output_video_path)
            output_file_name_without_extension, _ = os.path.splitext(video_file_name)
            output_ass_path = os.path.join(os.path.dirname(self.input_ass_path), output_file_name_without_extension + ".ass")

            # 对比视频并获取路径
            path = compare_video(self.input_video_path, self.output_video_path, frame_interval=1, signals=self.signals)
            switch(self.input_ass_path, output_ass_path, path)
        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            self.signals.finished.emit()  # 处理完成时发出 finished 信号

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("弹幕编织者")
        icon = QIcon(".\logo.ico")
        self.setWindowIcon(icon)
        self.resize(300, 400)

        # 创建标签和输入框
        self.label_input_video = QLabel("删减视频路径:")
        self.label_output_video = QLabel("完整视频路径:")
        self.label_input_ass = QLabel("删减视频的字幕路径:")

        self.input_video_path = QLineEdit(self)
        self.output_video_path = QLineEdit(self)
        self.input_ass_path = QLineEdit(self)

        # 创建按钮
        self.button_input_video = QPushButton("选择删减视频文件", self)
        self.button_output_video = QPushButton("选择完整视频文件", self)
        self.button_input_ass = QPushButton("选择字幕文件", self)
        self.button_confirm = QPushButton("确定", self)

        # 创建进度条
        self.progress_bar1 = QProgressBar(self)
        self.progress_bar2 = QProgressBar(self)
        self.progress_bar1.setMaximum(100)
        self.progress_bar2.setMaximum(100)

        # 连接按钮点击事件
        self.button_input_video.clicked.connect(self.choose_input_video)
        self.button_output_video.clicked.connect(self.choose_output_video)
        self.button_input_ass.clicked.connect(self.choose_input_ass)
        self.button_confirm.clicked.connect(self.confirm)

        # 布局
        layout = QVBoxLayout()

        layout.addWidget(self.label_output_video)
        layout.addWidget(self.output_video_path)
        layout.addWidget(self.button_output_video)


        layout.addWidget(self.label_input_video)
        layout.addWidget(self.input_video_path)
        layout.addWidget(self.button_input_video)

        layout.addWidget(self.label_input_ass)
        layout.addWidget(self.input_ass_path)
        layout.addWidget(self.button_input_ass)



        layout.addWidget(self.progress_bar1)
        layout.addWidget(self.progress_bar2)

        layout.addWidget(self.button_confirm)

        # 设置主窗口的中心部件
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # 初始化信号对象
        self.signals = ProgressSignals()

        # 连接信号到进度条更新槽
        self.signals.progress_video1.connect(self.progress_bar1.setValue)
        self.signals.progress_video2.connect(self.progress_bar2.setValue)
        self.signals.finished.connect(self.on_processing_finished)

    # 选择输入视频文件
    def choose_input_video(self):
        path, _ = QFileDialog.getOpenFileName(
            None,
            "选择视频文件",
            "",
            "视频文件 (*.avi *.mp4 *.mov *.mkv *.wmv *.flv *.mpeg *.mpg)"
        )

        if path:
            self.input_video_path.setText(path)

    # 选择输出视频文件
    def choose_output_video(self):
        path, _ = QFileDialog.getOpenFileName(
            None,
            "选择视频文件",
            "",
            "视频文件 (*.avi *.mp4 *.mov *.mkv *.wmv *.flv *.mpeg *.mpg)"
        )

        if path:
            self.output_video_path.setText(path)

    # 选择字幕文件
    def choose_input_ass(self):
        path = QFileDialog.getOpenFileName(None, "选择字幕文件", "", "字幕文件 (*.ass)")[0]
        if path:
            self.input_ass_path.setText(path)

    # 点击确认按钮后禁用界面，显示进度条，执行操作
    def confirm(self):
        input_video_path = self.input_video_path.text()
        output_video_path = self.output_video_path.text()
        input_ass_path = self.input_ass_path.text()

        # 禁用按钮和关闭事件
        self.button_confirm.setEnabled(False)
        self.button_confirm.setText("运行中...")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)
        self.show()

        # 清空进度条
        self.progress_bar1.setValue(0)
        self.progress_bar2.setValue(0)

        # 启动后台线程进行视频处理
        self.video_thread = VideoProcessingThread(input_video_path, output_video_path, input_ass_path, self.signals)
        self.video_thread.start()

    def on_processing_finished(self):
        # 处理结束后恢复按钮和关闭功能
        self.button_confirm.setEnabled(True)
        self.setWindowFlags(self.windowFlags() | Qt.WindowCloseButtonHint)
        self.button_confirm.setText("确认")
        self.show()
        QMessageBox.information(self, "完成", "处理完成！")


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
