
from PySide6.QtWidgets import (QWidget,QHBoxLayout, QLabel)
from ...styles import load_qss


# ── Encabezado de la tabla ────────────────────────────────────────────────────────

class TableHeader(QWidget):
    
    def __init__(self):
        super().__init__()
        self._build()

    def _build(self):
        self.setFixedHeight(44)
        self.setProperty("panel_header", "true")
        self.setStyleSheet(load_qss("panels"))

        h = QHBoxLayout(self)
        h.setContentsMargins(16, 0, 16, 0)

        dot = QLabel("●")
        dot.setObjectName("status_dot")
        dot.setStyleSheet(load_qss("panels"))

        title = QLabel("FOLDER LISTER")
        title.setObjectName("lbl_title")
        title.setStyleSheet(load_qss("panels"))

        h.addWidget(dot)
        h.addSpacing(6)
        h.addWidget(title)
        h.addStretch()
        return self