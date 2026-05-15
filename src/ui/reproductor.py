# src/ui/reproductor.py
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from pathlib import Path
from ..styles.colors import *
from ..utils import cortar_desde_primera_letra
from ..service import ReproductorService
from .widgets.flat_button import _FlatButton
from ..domains import Screenshot, Diapositiva

class Reproductor(tk.Toplevel):

    LIMITE_OBSERVACION = 219

    def __init__(self, parent, indice, destino: Path, video_service):
        super().__init__(parent)
        self.parent = parent

        self.service = ReproductorService(
            i_video = indice,
            destino      = destino,
            video_service = video_service,
        )
        self.titulo = cortar_desde_primera_letra(self.service.video.nombre)

        # ── Dimensiones de visualización ──────────────────────────────────────
        screen_w = self.winfo_screenwidth()  * 0.80
        screen_h = self.winfo_screenheight() * 0.55
        v_w, v_h= self.service.dimensiones_video
        scale = min(screen_w / v_w, screen_h / v_h)
        self.display_w = int(v_w * scale)
        self.display_h = int(v_h * scale)

        self.title("Reproductor")
        self.configure(bg=BG_DARK)
        self.resizable(False, False)

        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self._show_frame(0)
        self._center_window()

    # ── Construcción de la UI ─────────────────────────────────────────────────

    def _build_ui(self):
        self._build_header()
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=16)
        self._build_video_canvas()
        self._build_slider()
        self._build_bottom_panel()

    def _build_header(self):
        header = tk.Frame(self, bg=BG_DARK)
        header.pack(fill="x", padx=16, pady=(16, 8))

        tk.Label(header, text="●", font=("Courier", 10), fg=ACCENT, bg=BG_DARK).pack(side="left")
        tk.Label(header, text=f"  {self.titulo}", font=("Courier", 11, "bold"),
                 fg=TEXT_PRIMARY, bg=BG_DARK).pack(side="left")

        name = self.service.video.ruta_inicial.name[:32]
        tk.Label(header, text=name, font=("Courier", 9),
                 fg=TEXT_MUTED, bg=BG_DARK).pack(side="right")

    def _build_video_canvas(self):
        video_frame = tk.Frame(self, bg=BG_DARK)
        video_frame.pack(padx=16, pady=(12, 0))

        border = tk.Frame(video_frame, bg=BORDER, padx=2, pady=2)
        border.pack()

        self.label = tk.Label(border, bg=BG_DARK, cursor="crosshair")
        self.label.pack()
        self.label.bind("<Double-Button-1>", lambda e: self._abrir_fullscreen())

    def _build_slider(self):
        slider_area = tk.Frame(self, bg=BG_DARK)
        slider_area.pack(fill="x", padx=16, pady=(10, 4))

        counter_row = tk.Frame(slider_area, bg=BG_DARK)
        counter_row.pack(fill="x")

        tk.Label(counter_row, text="FRAME", font=("Courier", 8),
                 fg=TEXT_MUTED, bg=BG_DARK).pack(side="left")

        self.frame_label = tk.Label(
            counter_row,
            text=f"0 / {self.service.total_frames - 1}",
            font=("Courier", 9, "bold"), fg=ACCENT, bg=BG_DARK,
        )
        self.frame_label.pack(side="left", padx=(6, 0))

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("FP.Horizontal.TScale",
                        background=BG_DARK, troughcolor=BG_SURFACE,
                        sliderlength=18, sliderrelief="flat")
        style.map("FP.Horizontal.TScale", background=[("active", ACCENT)])

        self.slider = ttk.Scale(
            slider_area,
            from_=0, to=self.service.total_frames - 1,
            orient="horizontal",
            command=self._on_slider,
            style="FP.Horizontal.TScale",
            length=self.display_w,
        )
        self.slider.pack(pady=(2, 0))

    def _build_bottom_panel(self):
        PANEL_W = self.display_w + 32

        card = tk.Frame(self, bg=BG_CARD, padx=16, pady=14)
        card.pack(fill="x", padx=16, pady=(10, 16))

        # Encabezado con contador
        top_row = tk.Frame(card, bg=BG_CARD)
        top_row.pack(fill="x", pady=(0, 8))

        tk.Label(top_row, text="OBSERVACIÓN", font=("Courier", 9, "bold"),
                 fg=TEXT_MUTED, bg=BG_CARD).pack(side="left")

        self.conteo = tk.Label(top_row, text=f"0 / {self.LIMITE_OBSERVACION}",
                               font=("Courier", 9), fg=TEXT_MUTED, bg=BG_CARD)
        self.conteo.pack(side="right")

        # Textarea
        text_frame = tk.Frame(card, bg=BORDER, padx=1, pady=1)
        text_frame.pack(fill="x", pady=(0, 12))

        self.text_input = tk.Text(
            text_frame, height=5,
            font=("Courier", 11), bg=BG_SURFACE, fg=TEXT_PRIMARY,
            insertbackground=ACCENT, relief="flat", wrap="word",
            padx=10, pady=8, undo=True,
            selectbackground=ACCENT, selectforeground=TEXT_PRIMARY,
        )
        self.text_input.pack(side="left", fill="x", expand=True)

        sb = tk.Scrollbar(text_frame, command=self.text_input.yview,
                          width=6, bg=BG_SURFACE, troughcolor=BG_SURFACE, relief="flat")
        self.text_input.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")

        self.text_input.bind("<KeyPress>", self._verificar_limite)

        # Botón capturar
        self.btn_capturar = _FlatButton(
            card,
            text="⬤  Capturar frame  (calidad original)",
            command=self._on_capture,
            bg=ACCENT, fg="white",
            hover_bg=ACCENT_HOVER,
            font=("Courier", 10, "bold"),
            padx=18, pady=10,
            width=PANEL_W - 32,
        )
        self.btn_capturar.pack(fill="x")
        self._actualizar_estado_boton()

    # ── Helpers privados ──────────────────────────────────────────────────────

    def _center_window(self):
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        x = (self.winfo_screenwidth()  - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"+{x}+{y}")

    def _show_frame(self, frame_id: int):
        img = self.service.get_frame_scaled(frame_id, self.display_w, self.display_h)
        if img is None:
            return
        imgtk = ImageTk.PhotoImage(Image.fromarray(img))
        self.label.imgtk = imgtk
        self.label.configure(image=imgtk)

    def _actualizar_estado_boton(self):
        state = "disabled" if self.service.limite_alcanzado else "normal"
        self.btn_capturar.set_state(state)

    # ── Eventos ───────────────────────────────────────────────────────────────

    def _on_slider(self, val):
        frame_id = int(float(val))
        self.service.current_frame = frame_id
        self.frame_label.config(text=f"{frame_id} / {self.service.total_frames - 1}")
        self._show_frame(frame_id)

    def _on_capture(self):

        
        if not messagebox.askokcancel("Confirmación", "¿Seguro que querés guardar la captura?"):
            return
        
        path = self.service.guardar_captura(self.service.current_frame)
        screenshot = Screenshot(path)

        if not path:
            return
        
        cantidad_diapositiva = self.service.obtener_cantidad_diapositivas()

        if not cantidad_diapositiva:
            self.service.agregar_nueva_diapositiva()
            self.service.agregar_screenshot(cantidad_diapositiva-1, screenshot)









        








    def _on_close(self):
        self.service.release()
        self.destroy()
        self.parent.deiconify()
        self.service.video_service.guardar_diapositivas(self.diapositivas)

    def _verificar_limite(self, event):
        n = len(self.text_input.get("1.0", "end-1c"))
        if n >= self.LIMITE_OBSERVACION:
            color = "#FF5A5A"
        elif n >= 180:
            color = "#FFB347"
        else:
            color = TEXT_MUTED
        self.conteo.config(text=f"{n} / {self.LIMITE_OBSERVACION}", fg=color)
        if n >= self.LIMITE_OBSERVACION and event.keysym not in (
            "BackSpace", "Delete", "Left", "Right", "Up", "Down"
        ):
            return "break"

    def _abrir_fullscreen(self):
        fs = tk.Toplevel(self)
        fs.attributes("-fullscreen", True)
        fs.configure(bg="black")

        lbl = tk.Label(fs, bg="black")
        lbl.pack(expand=True)

        w, h  = fs.winfo_screenwidth(), fs.winfo_screenheight()
        img   = self.service.get_frame_scaled(self.service.current_frame, w, h)
        if img:
            imgtk    = ImageTk.PhotoImage(Image.fromarray(img))
            lbl.imgtk = imgtk
            lbl.config(image=imgtk)

        fs.bind("<Escape>", lambda e: fs.destroy())



