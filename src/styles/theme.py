"""
styles/theme.py
───────────────
Token de diseño: fuente única de verdad para todos los colores,
tipografías y dimensiones del sistema Folder Lister CCTV.

Los archivos .qss importan estos valores mediante el loader (styles/loader.py).
Los widgets los consumen directamente al importar esta clase.
"""


class Theme:
    # ── Fondos ──────────────────────────────────────────────────────────
    BG_DARK    = "#0d0d0d"
    BG_PANEL   = "#111111"
    BG_TABLE   = "#131313"
    BG_ROW_ALT = "#161616"
    BG_ROW_SEL = "#1a3a6e"
    BG_HEADER  = "#0d0d0d"
    BG_TOOLBAR = "#0d0d0d"
    BG_CARD    = "#1a1a1a"
    BG_VIDEO   = "#0a0f1a"
    BG_THUMB   = "#1c2a3a"

    # ── Acentos ─────────────────────────────────────────────────────────
    ACCENT_BLUE  = "#2563eb"
    ACCENT_HOVER = "#1d4ed8"
    ACCENT_PRESS = "#1e40af"

    # ── Bordes ──────────────────────────────────────────────────────────
    BORDER_BLUE = "#2563eb"
    BORDER_DIM  = "#2a2a2a"

    # ── Texto ───────────────────────────────────────────────────────────
    TEXT_PRIMARY = "#e5e5e5"
    TEXT_SECOND  = "#9ca3af"
    TEXT_ACCENT  = "#3b82f6"
    TEXT_HEADER  = "#6b7280"
    TEXT_WHITE   = "#ffffff"

    # ── Slider ──────────────────────────────────────────────────────────
    SLIDER_TRACK  = "#2563eb"
    SLIDER_BG     = "#374151"
    SLIDER_HANDLE = "#ffffff"
    SCROLLBAR_HDL = "#374151"

    # ── Estado ──────────────────────────────────────────────────────────
    STATUS_DOT = "#3b82f6"

    # ── Tipografía ──────────────────────────────────────────────────────
    FONT_UI   = "'Segoe UI', 'Inter', sans-serif"
    FONT_MONO = "'Consolas', 'Courier New', monospace"
    SIZE_BASE = "13px"
    SIZE_SM   = "12px"
    SIZE_XS   = "11px"
    SIZE_HDR  = "11px"

    # ── Dimensiones ─────────────────────────────────────────────────────
    RADIUS_SM = "4px"
    RADIUS_MD = "6px"
    RADIUS_LG = "8px"
    BORDER_W  = "1px"
