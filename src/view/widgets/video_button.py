"""
view/widgets/video_button.py
────────────────────────────
Botón "Ver video" que aparece en cada fila de la tabla de cámaras.
Tiene dos variantes visuales: activo (fila seleccionada) e inactivo.
"""

from PySide6.QtWidgets import QPushButton

from ...styles import load_qss


class VideoButton(QPushButton):
    """
    Botón de acción para reproducir el video de una cámara.

    Args:
        active: Si True, se renderiza con fondo sólido (azul).
                Si False, con borde y fondo transparente.
    """

    def __init__(self, active: bool = False, parent=None):
        super().__init__("Ver video", parent)
        self.setFixedSize(90, 28)
        self._qss = load_qss("video_button")
        self.set_active(active)

    def set_active(self, active: bool):
        """Cambia el estado visual del botón en tiempo de ejecución."""
        self.setProperty("video_active", "true" if active else "false")
        self.setStyleSheet(self._qss)
        self.style().unpolish(self)
        self.style().polish(self)
