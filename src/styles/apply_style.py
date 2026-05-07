from .colors import *
from tkinter import ttk

def _apply_styles(root):
    """Configura los estilos ttk globales para toda la app."""
    style = ttk.Style(root)
    style.theme_use("clam")

    # ── Treeview ──────────────────────────────────────────────────────────────
    style.configure(
        "FP.Treeview",
        background=BG_CARD,
        foreground=TEXT_PRIMARY,
        fieldbackground=BG_CARD,
        rowheight=28,
        font=("Courier", 10),
        borderwidth=0,
        relief="flat",
    )
    style.configure(
        "FP.Treeview.Heading",
        background=BG_SURFACE,
        foreground=TEXT_MUTED,
        font=("Courier", 9, "bold"),
        relief="flat",
        borderwidth=0,
        padding=(8, 6),
    )
    style.map(
        "FP.Treeview",
        background=[("selected", ACCENT)],
        foreground=[("selected", "#FFFFFF")],
    )
    style.map(
        "FP.Treeview.Heading",
        background=[("active", BORDER)],
        foreground=[("active", TEXT_PRIMARY)],
    )

    # ── Scrollbar ─────────────────────────────────────────────────────────────
    style.configure(
        "FP.Vertical.TScrollbar",
        background=BG_SURFACE,
        troughcolor=BG_CARD,
        bordercolor=BG_CARD,
        arrowcolor=TEXT_MUTED,
        relief="flat",
        width=8,
    )
    style.map("FP.Vertical.TScrollbar", background=[("active", BORDER)])

    # ── Entry (ruta destino) ──────────────────────────────────────────────────
    style.configure(
        "FP.TEntry",
        fieldbackground=BG_SURFACE,
        foreground=TEXT_MUTED,
        insertcolor=ACCENT,
        bordercolor=BORDER,
        relief="flat",
        font=("Courier", 10),
        padding=(8, 5),
    )