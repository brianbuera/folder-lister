#!/usr/bin/env python3
"""
crop_tool.py — Tkinter + Pillow
Uso integrado:
    from crop_tool import realizar_recortes
    realizar_recortes(parent_tk_widget, video_info)
 
Dimensiones dinámicas según cantidad de screenshots en VideoInfo:
    1 screenshot  → 1 panel  960×540 px
    2 screenshots → 2 paneles 480×540 px c/u  (side by side)
 
Los crops reemplazan los archivos originales en ruta_screenshot.
"""
 
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
from typing import Optional
 
try:
    from PIL import Image, ImageTk, ImageDraw
except ImportError:
    raise SystemExit("Instalá Pillow: pip install Pillow")
 
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
 
# ── Dimensiones por modo ──────────────────────────────────────────────────────
#   1 imagen: panel ancho completo
SINGLE_W, SINGLE_H = 960, 540
#   2 imágenes: paneles mitad de ancho
DUAL_W,   DUAL_H   = 480, 540
 
PT_W, PT_H = 360.14, 202.3
 
 
# ══════════════════════════════════════════════════════════════════════════════
class CropCanvas(tk.Canvas):
    """Canvas interactivo con zoom + pan. frame_w/frame_h definen el recorte."""
 
    def __init__(self, master, frame_w: int, frame_h: int,
                 on_zoom_change=None, **kw):
        super().__init__(
            master,
            width=frame_w, height=frame_h,
            bg="#0a0a0a", highlightthickness=0,
            cursor="fleur", **kw
        )
        self.fw = frame_w
        self.fh = frame_h
        self.on_zoom_change = on_zoom_change
 
        self._pil_img  = None
        self._tk_img   = None
        self._zoom     = 1.0
        self._min_zoom = 1.0
        self._ox = 0.0
        self._oy = 0.0
        self._drag_x = None
        self._drag_y = None
 
        self._draw_empty()
        self._bind_events()
 
    # ── Dibujo ────────────────────────────────────────────────────────────────
    def _draw_empty(self):
        self.delete("all")
        self.create_rectangle(
            20, 20, self.fw - 20, self.fh - 20,
            outline=BORDER2, dash=(5, 4), width=1
        )
        self.create_text(
            self.fw // 2, self.fh // 2,
            text="Sin screenshot", fill=T_MUTED,
            font=("Helvetica", 13)
        )
 
    def _redraw(self):
        if not self._pil_img:
            self._draw_empty()
            return
 
        iw = int(self._pil_img.width  * self._zoom)
        ih = int(self._pil_img.height * self._zoom)
        dx = int((self.fw - iw) / 2 + self._ox)
        dy = int((self.fh - ih) / 2 + self._oy)
 
        src_x0 = max(0, -dx);    src_y0 = max(0, -dy)
        src_x1 = min(iw, self.fw - dx)
        src_y1 = min(ih, self.fh - dy)
        dst_x0 = max(0, dx);     dst_y0 = max(0, dy)
 
        if src_x1 - src_x0 <= 0 or src_y1 - src_y0 <= 0:
            return
 
        composite = Image.new("RGB", (self.fw, self.fh), (10, 10, 10))
        scaled  = self._pil_img.resize((iw, ih), Image.LANCZOS)
        region  = scaled.crop((src_x0, src_y0, src_x1, src_y1))
        composite.paste(region, (dst_x0, dst_y0))
 
        draw = ImageDraw.Draw(composite)
        draw.line([(0, self.fh//2), (self.fw, self.fh//2)], fill="#1e1e1e", width=1)
        draw.line([(self.fw//2, 0), (self.fw//2, self.fh)], fill="#1e1e1e", width=1)
        draw.rectangle([0, 0, self.fw-1, self.fh-1], outline="#3a3a3a", width=1)
 
        self._tk_img = ImageTk.PhotoImage(composite)
        self.delete("all")
        self.create_image(0, 0, anchor="nw", image=self._tk_img)
 
    # ── Carga ─────────────────────────────────────────────────────────────────
    def load_path(self, path):
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
 
    # ── Zoom / Pan ────────────────────────────────────────────────────────────
    def _fit_zoom(self):
        return max(self.fw / self._pil_img.width,
                   self.fh / self._pil_img.height)
 
    def _clamp(self):
        iw = self._pil_img.width  * self._zoom
        ih = self._pil_img.height * self._zoom
        max_ox = max(0, (iw - self.fw) / 2)
        max_oy = max(0, (ih - self.fh) / 2)
        self._ox = max(-max_ox, min(max_ox, self._ox))
        self._oy = max(-max_oy, min(max_oy, self._oy))
 
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
        self._ox = 0.0
        self._oy = 0.0
        self._redraw()
        return self._zoom
 
    @property
    def zoom_pct(self):
        return int(self._zoom * 100)
 
    @property
    def min_zoom_pct(self):
        return int(self._min_zoom * 100)
 
    # ── Eventos ───────────────────────────────────────────────────────────────
    def _bind_events(self):
        self.bind("<Button-1>",        self._on_click)
        self.bind("<B1-Motion>",       self._on_drag)
        self.bind("<ButtonRelease-1>", self._on_release)
        self.bind("<MouseWheel>",      self._on_wheel)
        self.bind("<Button-4>",        self._on_wheel_up)
        self.bind("<Button-5>",        self._on_wheel_down)
 
    def _on_click(self, e):
        self._drag_x = e.x
        self._drag_y = e.y
 
    def _on_drag(self, e):
        if self._drag_x is None or not self._pil_img:
            return
        self._ox += e.x - self._drag_x
        self._oy += e.y - self._drag_y
        self._drag_x = e.x
        self._drag_y = e.y
        self._clamp()
        self._redraw()
 
    def _on_release(self, e):
        self._drag_x = None
        self._drag_y = None
 
    def _zoom_by(self, factor):
        if not self._pil_img:
            return
        self._zoom = max(self._min_zoom, min(4.0, self._zoom * factor))
        self._clamp()
        self._redraw()
        if self.on_zoom_change:
            self.on_zoom_change(self._zoom)
 
    def _on_wheel(self, e):
        self._zoom_by(1.06 if e.delta > 0 else 0.94)
 
    def _on_wheel_up(self, e):
        self._zoom_by(1.06)
 
    def _on_wheel_down(self, e):
        self._zoom_by(0.94)
 
    # ── Export ────────────────────────────────────────────────────────────────
    def get_crop_image(self) -> Optional[Image.Image]:
        if not self._pil_img:
            return None
        iw = int(self._pil_img.width  * self._zoom)
        ih = int(self._pil_img.height * self._zoom)
        dx = int((self.fw - iw) / 2 + self._ox)
        dy = int((self.fh - ih) / 2 + self._oy)
        composite = Image.new("RGB", (self.fw, self.fh), (10, 10, 10))
        scaled = self._pil_img.resize((iw, ih), Image.LANCZOS)
        composite.paste(scaled, (dx, dy))
        return composite
 
 
# ══════════════════════════════════════════════════════════════════════════════
def _make_btn(parent, text, command, style="normal", width=None):
    colors = {
        "normal":  (SURFACE, T_PRI,    BORDER2),
        "accent":  (ACCENT,  "#ffffff", ACCENT),
        "success": (SUCCESS, "#0a0a0a", SUCCESS),
        "danger":  (SURFACE, DANGER,   DANGER),
    }
    bg, fg, bd = colors.get(style, colors["normal"])
    kw = dict(
        text=text, command=command, bg=bg, fg=fg,
        activebackground=BORDER2, activeforeground=fg,
        relief="flat", bd=0, padx=10, pady=5,
        font=("Helvetica", 10),
        highlightthickness=1, highlightbackground=bd,
        cursor="hand2"
    )
    if width:
        kw["width"] = width
    return tk.Button(parent, **kw)
 
 
# ══════════════════════════════════════════════════════════════════════════════
class ImagePanel(tk.Frame):
    """Panel: header con nombre de cámara + canvas + controles de zoom."""
 
    def __init__(self, master, label: str, frame_w: int, frame_h: int, **kw):
        super().__init__(
            master, bg=PANEL, bd=0,
            highlightthickness=1, highlightbackground=BORDER, **kw
        )
        self._label   = label
        self._frame_w = frame_w
        self._frame_h = frame_h
        self._zoom_var = tk.IntVar(value=100)
        self._build()
 
    def _build(self):
        # Header
        hdr = tk.Frame(self, bg=PANEL, height=40)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
 
        tk.Label(
            hdr, text=self._label,
            bg=PANEL, fg=T_PRI,
            font=("Helvetica", 11, "bold")
        ).pack(side="left", padx=12, pady=8)
 
        self._dim_lbl = tk.Label(
            hdr, text="cargando...",
            bg=PANEL, fg=T_MUTED, font=("Helvetica", 9)
        )
        self._dim_lbl.pack(side="right", padx=12)
 
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x")
 
        # Canvas
        self.canvas = CropCanvas(
            self, self._frame_w, self._frame_h,
            on_zoom_change=self._on_zoom_change
        )
        self.canvas.pack()
 
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x")
 
        # Controles
        ctrl = tk.Frame(self, bg=PANEL)
        ctrl.pack(fill="x", padx=12, pady=10)
 
        zoom_row = tk.Frame(ctrl, bg=PANEL)
        zoom_row.pack(fill="x", pady=(0, 8))
 
        tk.Label(
            zoom_row, text="Zoom", bg=PANEL, fg=T_SEC,
            font=("Helvetica", 10), width=5, anchor="w"
        ).pack(side="left")
 
        self._slider = tk.Scale(
            zoom_row, from_=100, to=400,
            orient="horizontal", variable=self._zoom_var,
            command=self._on_slider,
            bg=PANEL, fg=T_PRI, troughcolor=BORDER2,
            activebackground=ACCENT, highlightthickness=0,
            sliderrelief="flat", bd=0, showvalue=False, length=1
        )
        self._slider.pack(side="left", fill="x", expand=True, padx=8)
 
        self._zoom_lbl = tk.Label(
            zoom_row, text="100%", bg=PANEL, fg=T_SEC,
            font=("Helvetica", 10), width=5, anchor="e"
        )
        self._zoom_lbl.pack(side="left")
 
        btn_row = tk.Frame(ctrl, bg=PANEL)
        btn_row.pack(fill="x")
 
        _make_btn(btn_row, "Reset", self._reset).pack(side="left")
 
    # ── Carga ─────────────────────────────────────────────────────────────────
    def load(self, path: Path):
        ok = self.canvas.load_path(path)
        if ok:
            img_w = self.canvas._pil_img.width
            img_h = self.canvas._pil_img.height
            self._dim_lbl.config(text=f"{img_w} × {img_h} px")
            min_pct = self.canvas.min_zoom_pct
            self._slider.config(from_=min_pct)
            self._sync_zoom_label(self.canvas.zoom_pct)
 
    # ── Zoom sync ─────────────────────────────────────────────────────────────
    def _on_zoom_change(self, zoom_float):
        pct = int(zoom_float * 100)
        self._zoom_var.set(pct)
        self._zoom_lbl.config(text=f"{pct}%")
 
    def _on_slider(self, val):
        pct = int(float(val))
        self.canvas.set_zoom(pct)
        self._zoom_lbl.config(text=f"{pct}%")
 
    def _sync_zoom_label(self, pct: int):
        self._zoom_var.set(pct)
        self._zoom_lbl.config(text=f"{pct}%")
 
    def _reset(self):
        zoom = self.canvas.reset_view()
        if zoom:
            pct = int(zoom * 100)
            self._slider.config(from_=self.canvas.min_zoom_pct)
            self._sync_zoom_label(pct)
 
    # ── Export ────────────────────────────────────────────────────────────────
    def save_to(self, path: Path) -> bool:
        img = self.canvas.get_crop_image()
        if not img:
            return False
        img.save(str(path))
        return True
 
 
# ══════════════════════════════════════════════════════════════════════════════
class CropToolWindow(tk.Toplevel):
    """
    Ventana modal de recorte.
    Recibe un VideoInfo, carga sus screenshots y al confirmar
    sobreescribe los archivos originales con los crops.
    """
 
    def __init__(self, parent, video_info):
        super().__init__(parent)
        self.video   = video_info
        self._panels = []
        self._result = False   # True si el usuario confirmó
 
        screens = list(video_info.ruta_screenshot)
        n = len(screens)
        if n == 0:
            messagebox.showwarning(
                "Sin screenshots",
                f"El video '{video_info.nombre}' no tiene screenshots cargados."
            )
            self.destroy()
            return
 
        # Dimensiones según cantidad
        if n == 1:
            fw, fh = SINGLE_W, SINGLE_H
        else:
            fw, fh = DUAL_W, DUAL_H
 
        self._screens = screens
        self._fw = fw
        self._fh = fh
 
        self._build(n, fw, fh)
        self._load_screens()
        self._center()
 
        # Modal
        self.transient(parent)
        self.grab_set()
        self.focus_set()
        self.protocol("WM_DELETE_WINDOW", self._on_cancel)
 
    # ── UI ────────────────────────────────────────────────────────────────────
    def _build(self, n_screens: int, fw: int, fh: int):
        self.title(f"Recorte — {self.video.nombre}")
        self.configure(bg=BG)
        self.resizable(False, False)
 
        # Top bar
        top = tk.Frame(self, bg=BG)
        top.pack(fill="x", padx=16, pady=(12, 0))
 
        tk.Label(
            top,
            text=f"Recorte manual  ·  {self.video.nombre}",
            bg=BG, fg=T_PRI, font=("Helvetica", 14, "bold")
        ).pack(side="left")
 
        dim_txt = (
            f"{SINGLE_W}×{SINGLE_H} px" if n_screens == 1
            else f"2 × {DUAL_W}×{DUAL_H} px"
        )
        tk.Label(
            top,
            text=f"{dim_txt}  ·  {self.video.hora_fecha.strftime('%Y-%m-%d %H:%M:%S')}",
            bg=SURFACE, fg=T_MUTED, font=("Helvetica", 9),
            padx=10, pady=4,
            highlightthickness=1, highlightbackground=BORDER
        ).pack(side="right")
 
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", pady=(10, 0))
 
        # Paneles
        panels_frame = tk.Frame(self, bg=BG)
        panels_frame.pack(padx=16, pady=14)
 
        for i, screen_path in enumerate(self._screens):
            label = f"Screenshot {i+1}  ·  {Path(screen_path).name}"
            panel = ImagePanel(panels_frame, label, fw, fh)
            if i == 0:
                panel.pack(side="left")
            else:
                tk.Frame(panels_frame, bg=BG, width=12).pack(side="left")
                panel.pack(side="left")
            self._panels.append(panel)
 
        # Observación (si tiene)
        if self.video.observacion:
            obs_frame = tk.Frame(self, bg=SURFACE,
                                 highlightthickness=1, highlightbackground=BORDER)
            obs_frame.pack(fill="x", padx=16, pady=(0, 8))
            tk.Label(
                obs_frame,
                text=f"Obs: {self.video.observacion}",
                bg=SURFACE, fg=T_SEC, font=("Helvetica", 9),
                padx=10, pady=6, anchor="w"
            ).pack(fill="x")
 
        # Bottom bar
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x")
        bottom = tk.Frame(self, bg=PANEL)
        bottom.pack(fill="x", padx=16, pady=10)
 
        _make_btn(bottom, "✕  Cancelar", self._on_cancel, "danger"
                  ).pack(side="left")
        _make_btn(
            bottom,
            "✓  Confirmar y guardar crops",
            self._on_confirm, "success"
        ).pack(side="right")
 
    def _load_screens(self):
        for panel, path in zip(self._panels, self._screens):
            panel.load(Path(path))
 
    def _center(self):
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        w  = self.winfo_reqwidth()
        h  = self.winfo_reqheight()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
 
    # ── Acciones ──────────────────────────────────────────────────────────────
    def _on_confirm(self):
        saved = []
        errors = []
        for panel, path in zip(self._panels, self._screens):
            dest = Path(path)
            ok = panel.save_to(dest)
            if ok:
                saved.append(dest.name)
            else:
                errors.append(dest.name)
 
        if errors:
            messagebox.showerror(
                "Error al guardar",
                f"No se pudieron guardar:\n" + "\n".join(errors)
            )
            return
 
        self._result = True
        messagebox.showinfo(
            "✓ Guardado",
            f"Crops guardados ({len(saved)}):\n" + "\n".join(saved)
        )
        self.destroy()
 
    def _on_cancel(self):
        self._result = False
        self.destroy()

 
    @property
    def confirmed(self) -> bool:
        return self._result
 
 
# ══════════════════════════════════════════════════════════════════════════════
def realizar_recortes(parent: tk.Widget, video_info) -> bool:
    """
    Abre la ventana modal de recorte para un VideoInfo.
    Bloquea hasta que el usuario confirme o cancele.
 
    Returns:
        True  → el usuario confirmó y los crops se guardaron.
        False → cancelado o sin screenshots.
 
    Uso:
        confirmado = realizar_recortes(self.root, video)
    """
    win = CropToolWindow(parent, video_info)
    if not win.winfo_exists():
        return False          # se destruyó inmediatamente (sin screenshots)
    parent.wait_window(win)
    return win.confirmed
 
 
