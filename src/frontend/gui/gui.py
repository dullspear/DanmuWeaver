import os

import cv2
from PySide6.QtCore import Qt, Signal, QThread, QObject
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QApplication, QFileDialog, QVBoxLayout, QHBoxLayout
)
from qfluentwidgets import (
    FluentWidget, CardWidget, IconWidget, BodyLabel, CaptionLabel, TitleLabel, SubtitleLabel,
    PushButton, PrimaryPushButton, ProgressBar, StateToolTip, InfoBar,
    InfoBarPosition, FluentIcon, setTheme, Theme
)

from src.backend.segments import find_missing_segments
from src.backend.video_comparison import compare_video
from src.backend.switch import switch
from src.frontend.gui.player.danmaku_convert import ass_to_danmaku_json
from src.frontend.gui.player.web_server import launch as launch_player

ICON_PATH = os.path.join(os.path.dirname(__file__), "logo.ico")


# 定义一个信号类，用于线程间通信
class ProgressSignals(QObject):
    progress_video1 = Signal(int)
    progress_video2 = Signal(int)
    finished = Signal()
    error = Signal(str)


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

            comments = ass_to_danmaku_json(output_ass_path)
            video = cv2.VideoCapture(self.output_video_path)
            fps = video.get(cv2.CAP_PROP_FPS)
            total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
            long_duration = total_frames / fps if fps else 0
            missing_segments = find_missing_segments(path, int(long_duration))

            launch_player(self.output_video_path, {
                "comments": comments,
                "missing_segments": missing_segments,
                "long_duration": long_duration,
            })
        except Exception as e:
            self.signals.error.emit(str(e))
        finally:
            self.signals.finished.emit()  # 处理完成时发出 finished 信号


class FilePickerCard(CardWidget):
    """一张可点击/可拖拽文件进来的卡片，展示标题+已选路径+浏览按钮"""

    pathChanged = Signal(str)

    def __init__(self, icon, title, subtitle, file_filter, parent=None):
        super().__init__(parent)
        self.file_filter = file_filter
        self.path = ""
        self.setAcceptDrops(True)
        self.setFixedHeight(72)

        icon_widget = IconWidget(icon, self)
        icon_widget.setFixedSize(28, 28)

        self.title_label = BodyLabel(title, self)
        self.path_label = CaptionLabel(subtitle, self)
        self.path_label.setTextColor("#606060", "#a0a0a0")

        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)
        text_layout.addWidget(self.title_label)
        text_layout.addWidget(self.path_label)

        self.browse_button = PushButton("浏览", self, FluentIcon.FOLDER_ADD)
        self.browse_button.clicked.connect(self._browse)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 12, 16, 12)
        layout.setSpacing(16)
        layout.addWidget(icon_widget)
        layout.addLayout(text_layout, 1)
        layout.addWidget(self.browse_button)

    def _browse(self):
        path, _ = QFileDialog.getOpenFileName(self, f"选择{self.title_label.text()}", "", self.file_filter)
        if path:
            self.set_path(path)

    def set_path(self, path):
        self.path = path
        self.path_label.setText(os.path.basename(path))
        self.path_label.setToolTip(path)
        self.pathChanged.emit(path)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            self.set_path(urls[0].toLocalFile())


class MainWindow(FluentWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("弹幕编织者")
        self.setWindowIcon(QIcon(ICON_PATH))
        self.resize(640, 560)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(36, 56, 36, 32)
        layout.setSpacing(16)

        # 品牌头：logo + 标题 + 副标题
        header_layout = QHBoxLayout()
        header_layout.setSpacing(14)
        logo_pixmap = QPixmap(ICON_PATH).scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_icon_widget = IconWidget(QIcon(logo_pixmap), self)
        logo_icon_widget.setFixedSize(48, 48)

        title_layout = QVBoxLayout()
        title_layout.setSpacing(2)
        title_layout.addWidget(TitleLabel("弹幕编织者", self))
        title_layout.addWidget(SubtitleLabel("将删减版视频的弹幕，重新对齐到完整版", self))

        header_layout.addWidget(logo_icon_widget)
        header_layout.addLayout(title_layout, 1)
        layout.addLayout(header_layout)
        layout.addSpacing(8)

        # 三张文件选择卡片
        self.output_video_card = FilePickerCard(
            FluentIcon.MOVIE, "完整版视频", "未选择文件",
            "视频文件 (*.avi *.mp4 *.mov *.mkv *.wmv *.flv *.mpeg *.mpg)", self
        )
        self.input_video_card = FilePickerCard(
            FluentIcon.VIDEO, "删减版视频", "未选择文件",
            "视频文件 (*.avi *.mp4 *.mov *.mkv *.wmv *.flv *.mpeg *.mpg)", self
        )
        self.input_ass_card = FilePickerCard(
            FluentIcon.DOCUMENT, "删减版弹幕字幕", "未选择文件",
            "字幕文件 (*.ass)", self
        )
        for card in (self.output_video_card, self.input_video_card, self.input_ass_card):
            card.pathChanged.connect(self._on_path_changed)
            layout.addWidget(card)

        layout.addSpacing(8)

        # 进度条（默认隐藏，处理时显示）
        self.progress_label1 = CaptionLabel("删减版视频扫描进度", self)
        self.progress_bar1 = ProgressBar(self)
        self.progress_label2 = CaptionLabel("完整版视频扫描进度", self)
        self.progress_bar2 = ProgressBar(self)
        self.progress_widgets = [self.progress_label1, self.progress_bar1, self.progress_label2, self.progress_bar2]
        for w in self.progress_widgets:
            w.setVisible(False)
            layout.addWidget(w)

        layout.addStretch(1)

        self.confirm_button = PrimaryPushButton("开始对齐", self, FluentIcon.PLAY)
        self.confirm_button.setFixedHeight(44)
        self.confirm_button.setEnabled(False)
        self.confirm_button.clicked.connect(self.confirm)
        layout.addWidget(self.confirm_button)

        # 初始化信号对象
        self.signals = ProgressSignals()
        self.signals.progress_video1.connect(self.progress_bar1.setValue)
        self.signals.progress_video2.connect(self.progress_bar2.setValue)
        self.signals.finished.connect(self.on_processing_finished)
        self.signals.error.connect(self.on_processing_error)

        self.state_tooltip = None
        self.had_error = False

    def _on_path_changed(self, _path):
        ready = bool(
            self.input_video_path() and self.output_video_path() and self.input_ass_path()
        )
        self.confirm_button.setEnabled(ready)

    def input_video_path(self):
        return self.input_video_card.path

    def output_video_path(self):
        return self.output_video_card.path

    def input_ass_path(self):
        return self.input_ass_card.path

    # 点击确认按钮后禁用界面，显示进度条，执行操作
    def confirm(self):
        self.had_error = False
        self.confirm_button.setEnabled(False)
        self.confirm_button.setText("运行中...")
        self.titleBar.closeBtn.setEnabled(False)

        self.progress_bar1.setValue(0)
        self.progress_bar2.setValue(0)
        for w in self.progress_widgets:
            w.setVisible(True)

        self.state_tooltip = StateToolTip("正在对齐", "正在扫描视频并计算弹幕时间轴，请稍候…", self)
        self.state_tooltip.move(self.state_tooltip.getSuitablePos())
        self.state_tooltip.show()

        # 启动后台线程进行视频处理
        self.video_thread = VideoProcessingThread(
            self.input_video_path(), self.output_video_path(), self.input_ass_path(), self.signals
        )
        self.video_thread.start()

    def on_processing_error(self, message):
        self.had_error = True
        InfoBar.error(
            title="处理失败",
            content=message,
            duration=5000,
            position=InfoBarPosition.TOP,
            parent=self,
        )

    def on_processing_finished(self):
        if self.state_tooltip:
            self.state_tooltip.setContent("处理完成" if not self.had_error else "处理失败")
            self.state_tooltip.setState(True)
            self.state_tooltip = None

        for w in self.progress_widgets:
            w.setVisible(False)

        self.confirm_button.setEnabled(True)
        self.confirm_button.setText("开始对齐")
        self.titleBar.closeBtn.setEnabled(True)

        if not self.had_error:
            InfoBar.success(
                title="完成",
                content="已在浏览器中打开播放页面",
                duration=4000,
                position=InfoBarPosition.TOP,
                parent=self,
            )


if __name__ == '__main__':
    app = QApplication([])
    setTheme(Theme.AUTO)
    window = MainWindow()
    window.show()
    app.exec()
