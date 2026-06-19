import tkinter as tk
from tkinter import ttk
from ..domain.video import Video


def mostrar_info_video(video: Video, parent: tk.Misc | None = None) -> tk.Toplevel:
    """Abre un Toplevel con toda la información del video."""
    win = tk.Toplevel(parent)
    win.title(f"Info — {video.nombre}")
    win.resizable(False, False)
    win.geometry("560x520")
    win.configure(padx=16, pady=16)

    _construir_contenido(win, video)
    _centrar_ventana(win)
    return win


# ── Construcción ────────────────────────────────────────────────────────────

def _construir_contenido(win: tk.Toplevel, video: Video) -> None:
    # ── Encabezado
    header = ttk.Frame(win)
    header.pack(fill="x", pady=(0, 12))

    ttk.Label(
        header,
        text="🎬  Info del video",
        font=("TkDefaultFont", 13, "bold"),
    ).pack(side="left")

    ttk.Label(
        header,
        text=video.nombre,
        foreground="gray",
        font=("TkDefaultFont", 11),
    ).pack(side="right")

    ttk.Separator(win, orient="horizontal").pack(fill="x", pady=(0, 12))

    # ── Campos principales
    campos = ttk.LabelFrame(win, text="General", padding=10)
    campos.pack(fill="x", pady=(0, 10))

    _fila(campos, "📁  Nombre",          video.nombre)
    _fila(campos, "🕒  Fecha y hora",     video.hora_fecha.strftime("%Y-%m-%d %H:%M:%S"))
    _fila(campos, "📂  Ruta original",    str(video.ruta_inicial))
    _fila(campos, "📦  Ruta enumerada",   str(video.ruta_enumerada) if video.ruta_enumerada else "Sin enumerar")

    # ── Stats
    stats = ttk.Frame(win)
    stats.pack(fill="x", pady=(0, 10))

    _stat_card(stats, "Diapositivas",    str(len(video.diapositivas))).pack(side="left", expand=True, fill="x", padx=(0, 6))
    _stat_card(stats, "Capturas totales", str(video.total_capturas)).pack(side="left", expand=True, fill="x", padx=(0, 6))
    _stat_card(stats, "Tiene capturas",  "Sí" if video.tiene_capturas else "No").pack(side="left", expand=True, fill="x")

    # ── Diapositivas
    if video.diapositivas:
        diapo_frame = ttk.LabelFrame(win, text="Diapositivas", padding=10)
        diapo_frame.pack(fill="both", expand=True, pady=(0, 10))
        _lista_diapositivas(diapo_frame, video)

    # ── Botón cerrar
    ttk.Button(win, text="Cerrar", command=win.destroy).pack(anchor="e")


def _fila(parent: ttk.Frame, etiqueta: str, valor: str) -> None:
    fila = ttk.Frame(parent)
    fila.pack(fill="x", pady=2)
    ttk.Label(fila, text=etiqueta, width=20, anchor="w", foreground="gray").pack(side="left")
    ttk.Label(fila, text=valor, anchor="w", wraplength=340).pack(side="left", fill="x", expand=True)


def _stat_card(parent: ttk.Frame, titulo: str, valor: str) -> ttk.Frame:
    card = ttk.LabelFrame(parent, text=titulo, padding=8)
    ttk.Label(card, text=valor, font=("TkDefaultFont", 16, "bold")).pack()
    return card


def _lista_diapositivas(parent: ttk.LabelFrame, video: Video) -> None:
    cols = ("n", "capturas")
    tree = ttk.Treeview(parent, columns=cols, show="headings", height=min(len(video.diapositivas), 6))
    tree.heading("n",        text="#")
    tree.heading("capturas", text="Capturas")
    tree.column("n",        width=40,  anchor="center")
    tree.column("capturas", width=100, anchor="center")

    for idx, d in enumerate(video.diapositivas, 1):
        tree.insert("", "end", values=(idx, d.cantidad_capturas))

    scrollbar = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")


# ── Utilidad ─────────────────────────────────────────────────────────────────

def _centrar_ventana(win: tk.Toplevel) -> None:
    win.update_idletasks()
    w, h   = win.winfo_width(), win.winfo_height()
    sw, sh = win.winfo_screenwidth(), win.winfo_screenheight()
    win.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")