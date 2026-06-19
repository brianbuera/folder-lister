
from .styles import *
from ...domain.screenshot import Screenshot
from tkinter import messagebox
import tkinter as tk



from .canvas import CropCanvas


# ══════════════════════════════════════════════════════════════════════════════
class ImagePanel(tk.Frame):
    """Panel con canvas + controles de zoom para un Screenshot."""

    def __init__(self, master, screenshot: Screenshot, label: str, **kw):
        super().__init__(master, bg=PANEL, bd=0,
                         highlightthickness=1, highlightbackground=BORDER, **kw)
        self.screenshot = screenshot
        self._label     = label
        self._zoom_var  = tk.IntVar(value=100)
        # dimensiones desde el objeto Screenshot
        self._fw = int(screenshot.ancho)
        self._fh = int(screenshot.alto)
        self._build()

    def _build(self):
        hdr = tk.Frame(self, bg=PANEL, height=40)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text=self._label, bg=PANEL, fg=T_PRI,
                 font=("Helvetica", 10, "bold")).pack(side="left", padx=12, pady=8)
        self._dim_lbl = tk.Label(hdr, text="cargando...", bg=PANEL, fg=T_MUTED,
                                 font=("Helvetica", 9))
        self._dim_lbl.pack(side="right", padx=12)
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x")

        self.canvas = CropCanvas(self, self._fw, self._fh,
                                 on_zoom_change=self._on_zoom_change)
        self.canvas.pack()
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x")

        ctrl = tk.Frame(self, bg=PANEL)
        ctrl.pack(fill="x", padx=12, pady=8)
        zoom_row = tk.Frame(ctrl, bg=PANEL)
        zoom_row.pack(fill="x", pady=(0, 6))
        tk.Label(zoom_row, text="Zoom", bg=PANEL, fg=T_SEC,
                 font=("Helvetica", 10), width=5, anchor="w").pack(side="left")
        self._slider = tk.Scale(zoom_row, from_=100, to=400, orient="horizontal",
                                variable=self._zoom_var, command=self._on_slider,
                                bg=PANEL, fg=T_PRI, troughcolor=BORDER2,
                                activebackground=ACCENT, highlightthickness=0,
                                sliderrelief="flat", bd=0, showvalue=False, length=1)
        self._slider.pack(side="left", fill="x", expand=True, padx=8)
        self._zoom_lbl = tk.Label(zoom_row, text="100%", bg=PANEL, fg=T_SEC,
                                  font=("Helvetica", 10), width=5, anchor="e")
        self._zoom_lbl.pack(side="left")
        btn_row = tk.Frame(ctrl, bg=PANEL)
        btn_row.pack(fill="x")
        tk.Button(btn_row, text="Reset", command=self._reset,
                  bg=SURFACE, fg=T_PRI, activebackground=BORDER2,
                  relief="flat", bd=0, padx=10, pady=4,
                  font=("Helvetica", 10), cursor="hand2").pack(side="left")

    def load(self):
        ok = self.canvas.load_path(self.screenshot.ruta)
        if ok:
            w, h = self.canvas._pil_img.width, self.canvas._pil_img.height
            self._dim_lbl.config(text=f"{w} × {h} px")
            self._slider.config(from_=self.canvas.min_zoom_pct)
            self._sync_zoom(self.canvas.zoom_pct)

    def _on_zoom_change(self, z):
        pct = int(z * 100)
        self._zoom_var.set(pct)
        self._zoom_lbl.config(text=f"{pct}%")

    def _on_slider(self, val):
        pct = int(float(val))
        self.canvas.set_zoom(pct)
        self._zoom_lbl.config(text=f"{pct}%")

    def _sync_zoom(self, pct: int):
        self._zoom_var.set(pct)
        self._zoom_lbl.config(text=f"{pct}%")

    def _reset(self):
        z = self.canvas.reset_view()
        if z:
            self._slider.config(from_=self.canvas.min_zoom_pct)
            self._sync_zoom(int(z * 100))

    def save_crop(self) -> bool:
        img = self.canvas.get_crop_image()
        if not img: return False
        img.save(str(self.screenshot.ruta))
        return True
