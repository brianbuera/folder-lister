"""
view/widgets/thumbnail_widget.py
─────────────────────────────────
Miniatura de captura del video con timestamp.
Muestra un área de imagen (placeholder) y el horario de la captura.
"""

from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QSizePolicy
from PySide6.QtCore import Qt

from ...styles import load_qss


class ThumbnailWidget(QFrame):
    """
    Tarjeta de miniatura para la cuadrícula de capturas.

    Args:
        timestamp: Horario de la captura, p.ej. "08:15:32".
        active:    Si True, el borde se resalta en azul.
    """

    def __init__(self, timestamp: str, active: bool = False, parent=None):
        super().__init__(parent)
        self.setFixedSize(116, 90)
        self._qss = load_qss("panels")

        # Propiedad para selector QSS
        prop = "thumbnail_active" if active else "thumbnail"
        self.setProperty(prop, "true")
        self.setStyleSheet(self._qss)

        self._build_ui(timestamp)

    def _build_ui(self, timestamp: str):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Área de imagen simulada (será reemplazada por QPixmap real)
        self.img_area = QLabel()
        self.img_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.img_area.setText("▪")
        self.img_area.setStyleSheet("color: #4b5563; font-size: 20px; border: none; background: #1c2a3a;")
        self.img_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Timestamp
        self.lbl_ts = QLabel(timestamp)
        self.lbl_ts.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_ts.setFixedHeight(20)
        self.lbl_ts.setProperty("thumb_ts", "true")
        self.lbl_ts.setStyleSheet(self._qss)

        layout.addWidget(self.img_area)
        layout.addWidget(self.lbl_ts)

    def set_active(self, active: bool):
        """Actualiza el estado visual de selección de la miniatura."""
        self.setProperty("thumbnail", "false" if active else "true")
        self.setProperty("thumbnail_active", "true" if active else "false")
        self.setStyleSheet(self._qss)
        self.style().unpolish(self)
        self.style().polish(self)

    def set_image(self, pixmap):
        """Reemplaza el placeholder con un QPixmap real."""
        self.img_area.setPixmap(
            pixmap.scaled(
                self.img_area.width(),
                self.img_area.height(),
            )
        )
        self.img_area.setText("")
