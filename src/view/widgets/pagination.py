"""
view/widgets/pagination.py
──────────────────────────
Widgets de paginación:
    PaginationButton — número de página, toggle activo/inactivo.
    ArrowButton      — flecha anterior / siguiente.
"""

from PySide6.QtWidgets import QPushButton

from ...styles import load_qss


class PaginationButton(QPushButton):
    """
    Botón numérico de página.

    Args:
        text:   Número de página como string.
        active: Estado inicial seleccionado.
    """

    def __init__(self, text: str, active: bool = False, parent=None):
        super().__init__(text, parent)
        self.setFixedSize(32, 32)
        self.setCheckable(True)
        self.setChecked(active)
        self._qss = load_qss("pagination")
        self._refresh_style()
        self.toggled.connect(self._refresh_style)

    def _refresh_style(self):
        self.setProperty("page_active", "true" if self.isChecked() else "false")
        self.setProperty("arrow", "false")
        self.setStyleSheet(self._qss)
        self.style().unpolish(self)
        self.style().polish(self)


class ArrowButton(QPushButton):
    """
    Botón de flecha para avanzar / retroceder páginas.

    Args:
        symbol: Carácter de flecha, p.ej. "‹" o "›".
    """

    def __init__(self, symbol: str, parent=None):
        super().__init__(symbol, parent)
        self.setFixedSize(32, 32)
        self._qss = load_qss("pagination")
        self.setProperty("arrow", "true")
        self.setProperty("page_active", "false")
        self.setStyleSheet(self._qss)
