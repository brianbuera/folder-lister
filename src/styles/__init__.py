"""
styles/
───────
Paquete de estilos del sistema Folder Lister CCTV.

Exporta:
    Theme   — tokens de diseño (colores, fuentes, dimensiones)
    load_qss(name) — carga un archivo .qss e inyecta los tokens
"""

from .theme import Theme
from .loader import load_qss

__all__ = ["Theme", "load_qss"]
