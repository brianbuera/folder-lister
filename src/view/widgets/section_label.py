"""
view/widgets/section_label.py
──────────────────────────────
Etiqueta de encabezado de sección con ícono y texto en mayúsculas.
Ejemplos: "▶  REPRODUCTOR", "📷  CAPTURAS DEL VIDEO".
"""

from PySide6.QtWidgets import QLabel

from ...styles import load_qss


class SectionLabel(QLabel):
    """
    Etiqueta de título de sección (ícono + texto).

    Args:
        icon: Carácter unicode/emoji.
        text: Texto descriptivo de la sección.
    """

    def __init__(self, icon: str, text: str, parent=None):
        super().__init__(f"  {icon}  {text}", parent)
        self.setProperty("section_label", "true")
        self.setStyleSheet(load_qss("panels"))
