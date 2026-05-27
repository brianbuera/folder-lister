from .styles import *
from tkinter import messagebox
import tkinter as tk
try:
    from PIL import Image
except ImportError:
    raise SystemExit("Instalá Pillow: pip install Pillow")
from ...domains.video import Video
from .image_panel import ImagePanel
from .observation_sidebar import ObservationSidebar


# ══════════════════════════════════════════════════════════════════════════════
class CropToolWindow(tk.Toplevel):
    """
    Ventana de recorte por diapositiva para un Video.
    Navega entre diapositivas con botones anterior/siguiente.
    Guarda todos los crops al confirmar.
    """
    LIMITE_OBSERVACION = 219

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

        self._content = tk.Frame(self, bg=BG)
        self._content.pack(fill="both", expand=True, padx=16, pady=14)

        self._panels_container = tk.Frame(self._content, bg=BG)
        self._panels_container.pack(side="left")

        self._sidebar = ObservationSidebar(
            self._content,
            on_close=self._hide_sidebar
        )

        self._sidebar_visible = False


        
        # Bottom bar ---------------------------------------------------------------------
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
        tk.Button(
            bottom,
            text="📝 Agregar observación",
            command=self._toggle_sidebar,
        ).pack(side="left", padx=(10, 0))
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

        observacion = self._sidebar.get_text()
        if observacion:
            self._video.diapositivas[self._current].agregar_observacion(observacion)
            self._sidebar.clear()
        messagebox.showinfo("✓ Guardado", "Todos los crops fueron guardados.")
        #cerrar ventana si es la ultima diapositiva
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
    


    def _toggle_sidebar(self):

        self._sidebar_visible = not self._sidebar_visible

        if self._sidebar_visible:
            self._sidebar.pack(side="right",anchor="n",padx=(12, 0))
        else:
            self._sidebar.pack_forget()

        self._center()


    def _hide_sidebar(self):

        self._sidebar_visible = False
        self._sidebar.pack_forget()

        self._center()