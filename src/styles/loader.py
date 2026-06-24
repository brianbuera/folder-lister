"""
styles/loader.py
────────────────
Carga archivos .qss desde la carpeta styles/ e inyecta los tokens
del Theme para que los archivos QSS usen variables en lugar de
valores hardcodeados.

Uso:
    from styles.loader import load_qss
    app.setStyleSheet(load_qss("global"))
    widget.setStyleSheet(load_qss("nav_button_active"))
"""

from __future__ import annotations
import os
from .theme import Theme

# Carpeta donde viven los .qss (misma que este módulo)
_QSS_DIR = os.path.dirname(__file__)


def load_qss(name: str) -> str:
    """
    Lee <name>.qss desde styles/ y sustituye los placeholders
    {{TOKEN}} por el valor correspondiente en Theme.

    Los placeholders tienen la forma: {{BG_DARK}}, {{ACCENT_BLUE}}, etc.
    (dobles llaves para no colisionar con la sintaxis f-string de Python).
    """
    path = os.path.join(_QSS_DIR, f"{name}.qss")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Archivo QSS no encontrado: {path}")

    with open(path, encoding="utf-8") as fh:
        raw = fh.read()

    # Sustituir cada atributo público de Theme
    tokens = {k: v for k, v in vars(Theme).items() if not k.startswith("_")}
    for token, value in tokens.items():
        raw = raw.replace(f"{{{{{token}}}}}", value)

    return raw
