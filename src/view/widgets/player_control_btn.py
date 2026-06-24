"""
view/widgets/player_control_btn.py
───────────────────────────────────
Botón cuadrado de control del reproductor (▶ ⏸ ⏹ 📷 ⏺ ⤢).
"""

from PySide6.QtWidgets import QPushButton

from ...styles import load_qss


class PlayerControlBtn(QPushButton):
    """
    Botón de control del reproductor de video.

    Args:
        symbol: Carácter unicode/emoji que representa la acción.
        size:   Tamaño fijo del botón en píxeles (ancho y alto).
    """

    def __init__(self, symbol: str, size: int = 36, parent=None):
        super().__init__(symbol, parent)
        self.setFixedSize(size, size)
        self.setProperty("player_ctrl", "true")
        self.setStyleSheet(load_qss("player"))
