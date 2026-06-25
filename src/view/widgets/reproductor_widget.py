from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QSlider, QComboBox, QSizePolicy
)
from PySide6.QtCore import Qt, Signal

from ...styles import Theme, load_qss
from .player_control_btn import PlayerControlBtn
from .section_label import SectionLabel


class ReproductorWidget(QWidget):

    sig_play = Signal()
    sig_pause = Signal()
    sig_stop = Signal()
    sig_captura = Signal()
    sig_fullscreen = Signal()
    sig_speed_change = Signal(str)
    sig_seek = Signal(int)
    sig_volume = Signal(int)

    def __init__(self):
        super().__init__()

        self.setProperty("panel", "true")
        self.setStyleSheet(load_qss("panels"))

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(8)

        layout.addLayout(self._build_header())

        self.video_area = self._build_video_area()
        layout.addWidget(self.video_area)

        self.slider_progress = self._build_progress_slider()
        layout.addWidget(self.slider_progress)

        layout.addLayout(self._build_time_labels())
        layout.addWidget(self._build_player_controls())

    def _build_header(self) -> QHBoxLayout:
        hdr = QHBoxLayout()

        hdr.addWidget(SectionLabel("▶", "REPRODUCTOR"))
        hdr.addStretch()

        self.lbl_cam_active = QLabel("Sin video seleccionado")
        self.lbl_cam_active.setProperty("cam_active_label", "true")
        self.lbl_cam_active.setStyleSheet(load_qss("panels"))

        hdr.addWidget(self.lbl_cam_active)

        return hdr

    def _build_video_area(self) -> QFrame:
        video_area = QFrame()
        video_area.setObjectName("video_area")
        video_area.setMinimumHeight(230)
        video_area.setStyleSheet(load_qss("panels"))
        video_area.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        return video_area

    def _build_progress_slider(self) -> QSlider:
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(0, 100)
        slider.setValue(0)
        slider.valueChanged.connect(self.sig_seek.emit)

        return slider

    def _build_time_labels(self) -> QHBoxLayout:
        times = QHBoxLayout()

        self.lbl_current = QLabel("00:00:00")
        self.lbl_current.setProperty("time_label", "true")
        self.lbl_current.setStyleSheet(load_qss("panels"))

        self.lbl_duration = QLabel("00:00:00")
        self.lbl_duration.setProperty("time_label", "true")
        self.lbl_duration.setStyleSheet(load_qss("panels"))

        times.addWidget(self.lbl_current)
        times.addStretch()
        times.addWidget(self.lbl_duration)

        return times

    def _build_player_controls(self) -> QWidget:
        bar = QWidget()
        bar.setStyleSheet("background: transparent;")

        layout = QHBoxLayout(bar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        self.btn_play = PlayerControlBtn("▶")
        self.btn_pause = PlayerControlBtn("⏸")
        self.btn_stop = PlayerControlBtn("⏹")

        self.btn_play.clicked.connect(self.sig_play.emit)
        self.btn_pause.clicked.connect(self.sig_pause.emit)
        self.btn_stop.clicked.connect(self.sig_stop.emit)

        layout.addWidget(self.btn_play)
        layout.addWidget(self.btn_pause)
        layout.addWidget(self.btn_stop)

        self.cmb_speed = QComboBox()
        self.cmb_speed.setObjectName("cmb_speed")
        self.cmb_speed.addItems(["0.5x", "1.00x", "4.0x", "8.0x", "16.0x"])
        self.cmb_speed.setCurrentIndex(1)
        self.cmb_speed.setFixedWidth(72)
        self.cmb_speed.setStyleSheet(load_qss("player"))
        self.cmb_speed.currentTextChanged.connect(self.sig_speed_change.emit)

        layout.addWidget(self.cmb_speed)
        layout.addStretch()

        self.btn_screenshot = PlayerControlBtn("📷")
        self.btn_fullscreen = PlayerControlBtn("⤢")

        self.btn_screenshot.clicked.connect(self.sig_captura.emit)
        self.btn_fullscreen.clicked.connect(self.sig_fullscreen.emit)

        layout.addWidget(self.btn_screenshot)
        layout.addWidget(self.btn_fullscreen)

        lbl_vol = QLabel("🔊")
        lbl_vol.setStyleSheet(f"color: {Theme.TEXT_SECOND}; font-size: 14px;")

        self.slider_vol = QSlider(Qt.Orientation.Horizontal)
        self.slider_vol.setRange(0, 100)
        self.slider_vol.setValue(70)
        self.slider_vol.setFixedWidth(70)
        self.slider_vol.valueChanged.connect(self.sig_volume.emit)

        layout.addWidget(lbl_vol)
        layout.addWidget(self.slider_vol)

        return bar

    # API pública del widget

    def reset_player_view(self):
        self.lbl_cam_active.setText("Sin video seleccionado")

        self.slider_progress.blockSignals(True)
        self.slider_progress.setValue(0)
        self.slider_progress.blockSignals(False)

        self.lbl_current.setText("00:00:00")
        self.lbl_duration.setText("00:00:00")

    def set_camera_label(self, text: str):
        self.lbl_cam_active.setText(text)

    def set_progress(self, value: int):
        value = max(0, min(value, 100))

        self.slider_progress.blockSignals(True)
        self.slider_progress.setValue(value)
        self.slider_progress.blockSignals(False)

    def set_current_time(self, time_str: str):
        self.lbl_current.setText(time_str)

    def set_duration(self, time_str: str):
        self.lbl_duration.setText(time_str)