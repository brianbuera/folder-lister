"""
view/widgets/nav_button.py
──────────────────────────
Botón de navegación superior con dos estados: activo / inactivo.
Se usa en la toolbar para VIDEOS y DIAPOSITIVAS.

El estilo se carga desde styles/nav_button.qss a través de
la propiedad Qt `nav_active` para que el selector QSS funcione.
"""

from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Property

from ...styles import load_qss


class NavButton(QPushButton):
    """
    Botón toggle de navegación de la toolbar.

    Args:
        text:      Texto visible en el botón.
        icon_char: Carácter unicode/emoji opcional que precede al texto.
        active:    Estado inicial (True = seleccionado).
    """

    def __init__(self, text: str, icon_char: str = "", active: bool = False, parent=None):
        super().__init__(parent)
        label = f"  {icon_char}  {text}" if icon_char else text
        self.setText(label)
        self.setCheckable(True)
        self.setChecked(active)
        self.setFixedHeight(36)
        self.setMinimumWidth(150)

        # Carga el QSS del botón de navegación una sola vez
        self._qss = load_qss("nav_button")
        self._refresh_style()

        self.toggled.connect(self._refresh_style)

    # ── Propiedad Qt para el selector QSS [nav_active="true"] ──────────
    def _get_nav_active(self) -> str:
        return "true" if self.isChecked() else "false"

    nav_active = Property(str, _get_nav_active)

    # ── Aplicar estilo según estado ──────────────────────────────────────
    def _refresh_style(self):
        self.setProperty("nav_active", "true" if self.isChecked() else "false")
        self.setStyleSheet(self._qss)
        # Forzar re-evaluación del estilo por el motor QSS
        self.style().unpolish(self)
        self.style().polish(self)
