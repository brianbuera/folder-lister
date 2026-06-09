# src/ui/reproductor.py
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from ..styles.colors import *
from ..utils import obtener_numero_y_nombre
from ..service.reproductor_service import ReproductorService
from .widgets.flat_button import _FlatButton
from ..domains.strategies import NuevaDiapositiva, MismaDiapositiva
class Reproductor(tk.Toplevel):

    LIMITE_OBSERVACION = 219

    def __init__(self, parent , video, config):
        super().__init__(parent)
        self.parent = parent
        self.service = ReproductorService(video = video, config = config)
        self.titulo = obtener_numero_y_nombre(self.service.video.nombre)

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
        self.bind('<space>', lambda e: self.toggle_play())
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self._show_frame(0)
        self._center_window()
        if not config.ruta_destino:
            self.btn_capturar.set_state('disabled')
        

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

        name = self.service.video.get_hora_fecha_str
        tk.Label(header, text=name, font=("Courier", 9),
                 fg=TEXT_MUTED, bg=BG_DARK).pack(side="right")

    def _build_video_canvas(self):
        video_frame = tk.Frame(self, bg=BG_DARK)
        video_frame.pack(padx=16, pady=(12, 0))

        border = tk.Frame(video_frame, bg=BORDER, padx=2, pady=2)
        border.pack()

        self.label = tk.Label(border, bg=BG_DARK, cursor="crosshair")
        self.label.pack()

    def _build_slider(self):
        slider_area = tk.Frame(self, bg=BG_DARK)
        slider_area.pack(fill="x", padx=16, pady=(10, 4))

        counter_row = tk.Frame(slider_area, bg=BG_DARK)
        counter_row.pack(fill="x")

        # ▶️ botón play/pause
        self.btn = tk.Button(slider_area, text="▶", bg=BG_DARK, fg=ACCENT, height=2, width=4, command=self.toggle_play)
        self.btn.pack()

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
  
        # Botón capturar
        self.btn_capturar = _FlatButton(
            card,
            text="⬤  Sacar Captura",
            command=self.sacar_captura,
            bg=ACCENT, fg="white",
            hover_bg=ACCENT_HOVER,
            font=("Courier", 10, "bold"),
            padx=18, pady=10,
            width=PANEL_W - 32,
        )
        self.btn_capturar.pack(fill="x")
        
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
            return False
        imgtk = ImageTk.PhotoImage(Image.fromarray(img))
        self.label.imgtk = imgtk
        self.label.configure(image=imgtk)
        return True
    

    def _actualizar_estado_boton(self):
            state = "disabled" if self.service.limite_alcanzado else "normal"
            self.btn_capturar.set_state(state)


    # ── Eventos ───────────────────────────────────────────────────────────────

    def _on_slider(self, val):
        frame_id = int(float(val))
        self.service.current_frame = frame_id
        self.frame_label.config(text=f"{frame_id} / {self.service.total_frames - 1}")
        self._show_frame(frame_id)

        
    def _on_close(self):
        self.service.release()
        self.destroy()
        self.parent.deiconify()






      # ▶️⏸ toggle
    def toggle_play(self):
        self.service.is_playing = not self.service.is_playing

        if self.service.is_playing:
            self.btn.config(text="❚❚")
            self.update_frame()
        else:
            self.btn.config(text="▶")


    def update_frame(self):
        if self.service.is_playing:
            self.slider.set(self.service.current_frame) 
            self.frame_label.config(text=f"{self.service.current_frame} / {self.service.total_frames - 1}")
            self.service.current_frame += 1
            if self.service.current_frame < self.service.total_frames:
                self.after(30, self.update_frame)
            else:
                self.service.is_playing = False
                self.btn.config(text="▶")


    def sacar_captura(self):
        if not self.service.video.diapositivas:
            estrategia = NuevaDiapositiva()
        else:
            if self.service.limite_alcanzado:
                nueva = messagebox.askokcancel("Limite de capturas en diapositiva", "Deberá crear una nueva")
                if nueva:
                    estrategia = NuevaDiapositiva()
                else:
                    self._on_close()
            else:
                self.btn_capturar.set_state('disabled')
                misma = messagebox.askyesno("Diapositiva", "¿Misma diapositiva?")
                self.btn_capturar.set_state('normal')

                estrategia = MismaDiapositiva() if misma else NuevaDiapositiva()

        self.service.guardar_captura(self.service.current_frame, estrategia, len(self.service.video.diapositivas))
        messagebox.showinfo("Captura guardada", "La captura se guardó con exito")