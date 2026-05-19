# src/tools/crop_tool.py
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
from typing import Optional

try:
    from PIL import Image, ImageTk, ImageDraw
except ImportError:
    raise SystemExit("Instalá Pillow: pip install Pillow")

from ..domains.video import Video
from ..domains.diapositiva import Diapositiva
from ..domains.screenshot import Screenshot

# ── Paleta ────────────────────────────────────────────────────────────────────
BG      = "#0f0f0f"
PANEL   = "#161616"
SURFACE = "#1e1e1e"
BORDER  = "#2a2a2a"
BORDER2 = "#3a3a3a"
ACCENT  = "#5b8cff"
SUCCESS = "#3ecf8e"
DANGER  = "#ff5555"
T_PRI   = "#f0f0f0"
T_SEC   = "#888888"
T_MUTED = "#555555"

CANVAS_H = 540  # alto fijo siempre


# ══════════════════════════════════════════════════════════════════════════════
class CropCanvas(tk.Canvas):
    """Canvas interactivo con zoom + pan."""

    def __init__(self, master, frame_w: int, frame_h: int, on_zoom_change=None, **kw):
        super().__init__(
            master, width=frame_w, height=frame_h,
            bg="#0a0a0a", highlightthickness=0, cursor="fleur", **kw
        )
        self.fw = frame_w
        self.fh = frame_h
        self.on_zoom_change = on_zoom_change
        self._pil_img = None
        self._tk_img  = None
        self._zoom    = 1.0
        self._min_zoom = 1.0
        self._ox = 0.0
        self._oy = 0.0
        self._drag_x = None
        self._drag_y = None
        self._draw_empty()
        self._bind_events()

    def _draw_empty(self):
        self.delete("all")
        self.create_rectangle(20, 20, self.fw-20, self.fh-20,
                              outline=BORDER2, dash=(5, 4), width=1)
        self.create_text(self.fw//2, self.fh//2,
                         text="Sin screenshot", fill=T_MUTED, font=("Helvetica", 13))

    def _redraw(self):
        if not self._pil_img:
            self._draw_empty()
            return
        iw = int(self._pil_img.width  * self._zoom)
        ih = int(self._pil_img.height * self._zoom)
        dx = int((self.fw - iw) / 2 + self._ox)
        dy = int((self.fh - ih) / 2 + self._oy)
        sx0 = max(0, -dx);  sy0 = max(0, -dy)
        sx1 = min(iw, self.fw - dx)
        sy1 = min(ih, self.fh - dy)
        dx0 = max(0, dx);   dy0 = max(0, dy)
        if sx1 - sx0 <= 0 or sy1 - sy0 <= 0:
            return
        composite = Image.new("RGB", (self.fw, self.fh), (10, 10, 10))
        scaled = self._pil_img.resize((iw, ih), Image.LANCZOS)
        composite.paste(scaled.crop((sx0, sy0, sx1, sy1)), (dx0, dy0))
        draw = ImageDraw.Draw(composite)
        draw.line([(0, self.fh//2), (self.fw, self.fh//2)], fill="#1e1e1e", width=1)
        draw.line([(self.fw//2, 0), (self.fw//2, self.fh)], fill="#1e1e1e", width=1)
        draw.rectangle([0, 0, self.fw-1, self.fh-1], outline="#3a3a3a", width=1)
        self._tk_img = ImageTk.PhotoImage(composite)
        self.delete("all")
        self.create_image(0, 0, anchor="nw", image=self._tk_img)

    def load_path(self, path: Path) -> bool:
        try:
            img = Image.open(str(path)).convert("RGB")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la imagen:\n{e}")
            return False
        self._pil_img  = img
        self._zoom     = self._fit_zoom()
        self._min_zoom = self._zoom
        self._ox = 0.0
        self._oy = 0.0
        self._redraw()
        if self.on_zoom_change:
            self.on_zoom_change(self._zoom)
        return True

    def _fit_zoom(self):
        return max(self.fw / self._pil_img.width, self.fh / self._pil_img.height)

    def _clamp(self):
        iw = self._pil_img.width  * self._zoom
        ih = self._pil_img.height * self._zoom
        ox = max(0, (iw - self.fw) / 2)
        oy = max(0, (ih - self.fh) / 2)
        self._ox = max(-ox, min(ox, self._ox))
        self._oy = max(-oy, min(oy, self._oy))

    def set_zoom(self, pct: int):
        if not self._pil_img:
            return
        self._zoom = max(self._min_zoom, min(4.0, pct / 100))
        self._clamp()
        self._redraw()

    def reset_view(self):
        if not self._pil_img:
            return None
        self._zoom = self._fit_zoom()
        self._ox = self._oy = 0.0
        self._redraw()
        return self._zoom

    @property
    def zoom_pct(self): return int(self._zoom * 100)

    @property
    def min_zoom_pct(self): return int(self._min_zoom * 100)

    def _bind_events(self):
        self.bind("<Button-1>",        self._on_click)
        self.bind("<B1-Motion>",       self._on_drag)
        self.bind("<ButtonRelease-1>", lambda e: setattr(self, '_drag_x', None))
        self.bind("<MouseWheel>",      self._on_wheel)
        self.bind("<Button-4>",        lambda e: self._zoom_by(1.06))
        self.bind("<Button-5>",        lambda e: self._zoom_by(0.94))

    def _on_click(self, e): self._drag_x = e.x; self._drag_y = e.y

    def _on_drag(self, e):
        if self._drag_x is None or not self._pil_img: return
        self._ox += e.x - self._drag_x
        self._oy += e.y - self._drag_y
        self._drag_x, self._drag_y = e.x, e.y
        self._clamp(); self._redraw()

    def _zoom_by(self, factor):
        if not self._pil_img: return
        self._zoom = max(self._min_zoom, min(4.0, self._zoom * factor))
        self._clamp(); self._redraw()
        if self.on_zoom_change: self.on_zoom_change(self._zoom)

    def _on_wheel(self, e):
        self._zoom_by(1.06 if e.delta > 0 else 0.94)

    def get_crop_image(self) -> Optional[Image.Image]:
        if not self._pil_img: return None
        iw = int(self._pil_img.width  * self._zoom)
        ih = int(self._pil_img.height * self._zoom)
        dx = int((self.fw - iw) / 2 + self._ox)
        dy = int((self.fh - ih) / 2 + self._oy)
        composite = Image.new("RGB", (self.fw, self.fh), (10, 10, 10))
        composite.paste(self._pil_img.resize((iw, ih), Image.LANCZOS), (dx, dy))
        return composite


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


# ══════════════════════════════════════════════════════════════════════════════
class CropToolWindow(tk.Toplevel):
    """
    Ventana de recorte por diapositiva para un Video.
    Navega entre diapositivas con botones anterior/siguiente.
    Guarda todos los crops al confirmar.
    """

    def __init__(self, parent, video: Video):
        super().__init__(parent)
        self._video    = video
        self._result   = False
        self._panels   = []        # panels de la diapositiva actual
        self._current  = 0         # índice de diapositiva actual

        if not video.diapositivas:
            messagebox.showwarning("Sin diapositivas",
                                   f"'{video.nombre}' no tiene diapositivas.")
            self.destroy()
            return

        self.title(f"Recorte — {video.nombre}")
        self.configure(bg=BG)
        self.resizable(False, False)

        self._build_chrome()
        self._load_diapositiva(0)
        self._center()

        self.transient(parent)
        self.grab_set()
        self.focus_set()
        self.protocol("WM_DELETE_WINDOW", self._on_cancel)

    # ── Chrome (header + nav + bottom) ───────────────────────────────────────

    def _build_chrome(self):
        # Header
        top = tk.Frame(self, bg=BG)
        top.pack(fill="x", padx=16, pady=(12, 0))
        tk.Label(top, text=f"Recorte  ·  {self._video.nombre}",
                 bg=BG, fg=T_PRI, font=("Helvetica", 14, "bold")).pack(side="left")
        tk.Label(top, text=self._video.hora_fecha.strftime('%Y-%m-%d %H:%M:%S'),
                 bg=SURFACE, fg=T_MUTED, font=("Helvetica", 9),
                 padx=10, pady=4,
                 highlightthickness=1, highlightbackground=BORDER).pack(side="right")
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", pady=(10, 0))

        # Barra de navegación
        nav = tk.Frame(self, bg=PANEL)
        nav.pack(fill="x", padx=16, pady=(10, 0))

        self._btn_prev = tk.Button(
            nav, text="◀  Anterior", command=self._prev,
            bg=SURFACE, fg=T_PRI, activebackground=BORDER2,
            relief="flat", bd=0, padx=12, pady=6,
            font=("Helvetica", 10), cursor="hand2",
            highlightthickness=1, highlightbackground=BORDER2,
        )
        self._btn_prev.pack(side="left")

        self._nav_label = tk.Label(nav, text="", bg=PANEL, fg=T_SEC,
                                   font=("Helvetica", 10))
        self._nav_label.pack(side="left", expand=True)

        self._btn_next = tk.Button(
            nav, text="Siguiente  ▶", command=self._next,
            bg=SURFACE, fg=T_PRI, activebackground=BORDER2,
            relief="flat", bd=0, padx=12, pady=6,
            font=("Helvetica", 10), cursor="hand2",
            highlightthickness=1, highlightbackground=BORDER2,
        )
        self._btn_next.pack(side="right")

        # Contenedor de paneles (se reemplaza al navegar)
        self._panels_container = tk.Frame(self, bg=BG)
        self._panels_container.pack(padx=16, pady=14)

        # Observación
        self._obs_frame = tk.Frame(self, bg=SURFACE,
                                   highlightthickness=1, highlightbackground=BORDER)
        self._obs_lbl = tk.Label(self._obs_frame, bg=SURFACE, fg=T_SEC,
                                 font=("Helvetica", 9), padx=10, pady=6, anchor="w")
        self._obs_lbl.pack(fill="x")

        # Bottom bar
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x")
        bottom = tk.Frame(self, bg=PANEL)
        bottom.pack(fill="x", padx=16, pady=10)
        tk.Button(bottom, text="✕  Cancelar", command=self._on_cancel,
                  bg=SURFACE, fg=DANGER, activebackground=BORDER2,
                  relief="flat", bd=0, padx=10, pady=5,
                  font=("Helvetica", 10), cursor="hand2",
                  highlightthickness=1, highlightbackground=DANGER).pack(side="left")
        tk.Button(bottom, text="✓  Confirmar y guardar todos los crops",
                  command=self._on_confirm,
                  bg=SUCCESS, fg="#0a0a0a", activebackground=SUCCESS,
                  relief="flat", bd=0, padx=10, pady=5,
                  font=("Helvetica", 10, "bold"), cursor="hand2").pack(side="right")

    # ── Navegación ────────────────────────────────────────────────────────────

    def _load_diapositiva(self, idx: int):
        # Destruir paneles anteriores
        for w in self._panels_container.winfo_children():
            w.destroy()
        self._panels.clear()

        self._current = idx
        diap = self._video.diapositivas[idx]
        n    = len(diap.screenshots)

        # Actualizar nav label y botones
        total = len(self._video.diapositivas)
        self._nav_label.config(text=f"Diapositiva {idx + 1} de {total}  ·  {n} captura{'s' if n > 1 else ''}")
        self._btn_prev.config(state="normal" if idx > 0 else "disabled")
        self._btn_next.config(state="normal" if idx < total - 1 else "disabled")

        # Construir paneles según screenshots de la diapositiva
        for i, screenshot in enumerate(diap.screenshots):
            label = f"Captura {i + 1}  ·  {screenshot.ruta.name}"
            panel = ImagePanel(self._panels_container, screenshot, label)
            if i > 0:
                tk.Frame(self._panels_container, bg=BG, width=12).pack(side="left")
            panel.pack(side="left")
            panel.load()
            self._panels.append(panel)

        # Observación
        if diap.observacion:
            self._obs_lbl.config(text=f"Obs: {diap.observacion}")
            self._obs_frame.pack(fill="x", padx=16, pady=(0, 8))
        else:
            self._obs_frame.pack_forget()

        self._center()

    def _prev(self):
        if self._current > 0:
            self._load_diapositiva(self._current - 1)

    def _next(self):
        if self._current < len(self._video.diapositivas) - 1:
            self._load_diapositiva(self._current + 1)

    # ── Acciones ──────────────────────────────────────────────────────────────

    def _on_confirm(self):
        errors = []
        for diap in self._video.diapositivas:
            for screen in diap.screenshots:
                try:
                    img = Image.open(str(screen.ruta)).convert("RGB")
                    img.save(str(screen.ruta))
                except Exception as e:
                    errors.append(f"{screen.ruta.name}: {e}")

        # Guardar crops del panel actual (la vista puede diferir del archivo)
        for panel in self._panels:
            if not panel.save_crop():
                errors.append(panel.screenshot.ruta.name)

        if errors:
            messagebox.showerror("Error al guardar",
                                 "No se pudieron guardar:\n" + "\n".join(errors))
            return

        self._result = True
        messagebox.showinfo("✓ Guardado", "Todos los crops fueron guardados.")
        if len(self._video.diapositivas)-1 == self._current:
            self.destroy()
        self._next()

    def _on_cancel(self):
        self._result = False
        self.destroy()

    def _center(self):
        self.update_idletasks()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        w, h   = self.winfo_reqwidth(), self.winfo_reqheight()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    @property
    def confirmed(self) -> bool:
        return self._result


# ══════════════════════════════════════════════════════════════════════════════
def realizar_recortes(parent: tk.Widget, video: Video) -> bool:
    win = CropToolWindow(parent, video)
    if not win.winfo_exists():
        return False
    parent.wait_window(win)
    return win.confirmed
 
