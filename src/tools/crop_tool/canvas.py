from pathlib import Path
from typing import Optional
try:
    from PIL import Image, ImageTk, ImageDraw
except ImportError:
    raise SystemExit("Instalá Pillow: pip install Pillow")

from .styles import *
from tkinter import messagebox
import tkinter as tk






#══════════════════════════════════════════════════════════════════════════════
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