
from PySide6.QtWidgets import (QVBoxLayout, QWidget)
from ...styles import load_qss
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,QFrame, QScrollArea, QGridLayout)
from PySide6.QtCore import Qt
from ..widgets import (SectionLabel, ThumbnailWidget)


# ── Capturas ────────────────────────────────────────────────────────
class CapturesPanel(QWidget):

    def __init__(self):
        super().__init__()
        self._build()

    def _build(self):
        self.setProperty("panel", "true")
        self.setStyleSheet(load_qss("panels"))

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(10)

        hdr = QHBoxLayout()
        hdr.addWidget(SectionLabel("📷", "CAPTURAS DEL VIDEO"))
        hdr.addStretch()
        layout.addLayout(hdr)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("background: transparent;")

        container = QWidget()
        container.setStyleSheet("background: transparent;")
        grid = QGridLayout(container)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(8)

        timestamps = [
            "08:15:32", "08:15:40", "08:15:48", "08:16:02", "08:16:15",
            "08:16:28", "08:16:40", "08:16:55", "08:17:05", "08:17:20",
        ]
        self.thumbnails: list[ThumbnailWidget] = []
        for idx, ts in enumerate(timestamps):
            thumb = ThumbnailWidget(ts, active=(idx == 0))
            self.thumbnails.append(thumb)
            grid.addWidget(thumb, idx // 5, idx % 5)

        scroll.setWidget(container)
        layout.addWidget(scroll)