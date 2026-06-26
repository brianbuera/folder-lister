
from PySide6.QtWidgets import (QVBoxLayout, QWidget)
from ...styles import load_qss

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout)
from ..widgets import (ReproductorWidget, VideosTable, CapturesPanel, TableHeader, BottomBar)



class VideosPage(QWidget):
    
    
        def __init__(self):
            super().__init__()
            self.tabla_header = TableHeader()
            self.videos_table = VideosTable()
            self.bottom_bar = BottomBar()
            self.reproductor = ReproductorWidget()
            self.captures_panel = CapturesPanel()
            self._build()

        # ════════════════ PAGINA VIDEOS (Columna izq +  Columna der) ═════════════════════════════════
        def _build(self) -> QWidget:
            h = QHBoxLayout(self)
            h.setContentsMargins(16, 16, 16, 16)
            h.setSpacing(16)

            h.addWidget(self._build_left_column(), stretch=5)
            h.addWidget(self._build_right_column(), stretch=4)

        # ════════════════ COLUMNA IZQUIERDA ═════════════════════════════════

        def _build_left_column(self) -> QWidget:
            col = QWidget()
            col.setProperty("panel", "true")
            col.setStyleSheet(load_qss("panels"))

            layout = QVBoxLayout(col)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)

            layout.addWidget(self.tabla_header)
            layout.addWidget(self.videos_table, stretch=1)
            layout.addWidget(self.bottom_bar)

            return col

    # ════════════════ COLUMNA DERECHA ═══════════════════════════════════

        def _build_right_column(self) -> QWidget:
            col = QWidget()
            col.setStyleSheet("background: transparent;")
            layout = QVBoxLayout(col)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(12)
            layout.addWidget(self.reproductor,   stretch=3)
            layout.addWidget(self.captures_panel, stretch=2)
            return col
        








