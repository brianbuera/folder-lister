
from PySide6.QtWidgets import (QWidget,QHBoxLayout,QButtonGroup, QPushButton)

from ...styles import load_qss
from PySide6.QtCore import Signal
from ..widgets import (PaginationButton, ArrowButton)

"""
    Ventana principal de la aplicación CCTV Folder Lister.

    Señales (para conectar desde el Controlador):
        sig_guardar()           — botón "Guardar carpeta CCTV"
        sig_pagina(int)         — cambio de página
"""

# ── Barra inferior ────────────────────────────────────────────────────────
class BottomBar(QWidget):

    sig_pagina = Signal(int)
    sig_guardar = Signal()

    def __init__(self):
        super().__init__()
        self._build()

    def _build(self):
        self.setFixedHeight(60)
        self.setProperty("bottom_bar", "true")
        self.setStyleSheet(load_qss("panels"))

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(6)

        self.btn_prev = ArrowButton("‹")
        layout.addWidget(self.btn_prev)

        self.page_buttons: list[PaginationButton] = []
        self._page_group = QButtonGroup(self)
        self._page_group.setExclusive(True)

        for p in range(1, 6):
            pb = PaginationButton(str(p), active=(p == 1))
            self._page_group.addButton(pb)
            self.page_buttons.append(pb)
            pb.clicked.connect(lambda _, pg=p: self.sig_pagina.emit(pg))
            layout.addWidget(pb)

        self.btn_next = ArrowButton("›")
        layout.addWidget(self.btn_next)
        layout.addStretch()

        self.btn_guardar = QPushButton("  Guardar carpeta CCTV")
        self.btn_guardar.setObjectName("btn_guardar")
        self.btn_guardar.setFixedHeight(38)
        self.btn_guardar.setStyleSheet(load_qss("player"))
        self.btn_guardar.clicked.connect(self.sig_guardar.emit)
        layout.addWidget(self.btn_guardar)