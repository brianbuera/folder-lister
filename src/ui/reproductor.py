import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from pathlib import Path
import re


def cortar_desde_primera_letra(texto: str) -> str:
    match = re.search(r"[A-Za-zÁÉÍÓÚáéíóúÑñ]", texto)
    return texto[match.start():] if match else ""

# ── Paleta de colores ────────────────────────────────────────────────────────
BG_DARK      = "#0F1117"   # fondo principal
BG_CARD      = "#1A1D27"   # tarjeta / panel inferior
BG_SURFACE   = "#22263A"   # superficie de inputs
ACCENT       = "#4F8EF7"   # azul principal
ACCENT_HOVER = "#6EA6FF"
TEXT_PRIMARY = "#E8EAF0"
TEXT_MUTED   = "#7A7F99"
BORDER       = "#2E3249"
SUCCESS      = "#3DDC84"


def _hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def _lerp_color(c1, c2, t):
    r = int(c1[0] + (c2[0] - c1[0]) * t)
    g = int(c1[1] + (c2[1] - c1[1]) * t)
    b = int(c1[2] + (c2[2] - c1[2]) * t)
    return f"#{r:02x}{g:02x}{b:02x}"


class Reproductor(tk.Toplevel):
    def __init__(self, parent, video, destino: Path, service):
        super().__init__(parent)
        self.video   = video
        self.destino = destino / "captures"
        self.service = service
        self.titulo = cortar_desde_primera_letra(video.nombre)
        # ── Video setup ───────────────────────────────────────────────────────
        self.cap          = cv2.VideoCapture(str(video.ruta_inicial))
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.current_frame = 0

        # ── Dimensiones de visualización ──────────────────────────────────────
        screen_w = self.winfo_screenwidth()  * 0.80
        screen_h = self.winfo_screenheight() * 0.55   # reservar ~45% para controles
        self.v_width  = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.v_height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        scale = min(screen_w / self.v_width, screen_h / self.v_height)
        self.display_w = int(self.v_width  * scale)
        self.display_h = int(self.v_height * scale)

        # ── Ventana ───────────────────────────────────────────────────────────
        self.title("Reproductor")
        self.configure(bg=BG_DARK)
        self.resizable(False, False)

        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.show_frame(0)

        # Centrar ventana en pantalla tras buildear
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        x = (self.winfo_screenwidth()  - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"+{x}+{y}")

    # ── Construcción de la UI ─────────────────────────────────────────────────

    def _build_ui(self):
        PANEL_W = self.display_w + 32  # padding horizontal total

        # ── Header ────────────────────────────────────────────────────────────
        header = tk.Frame(self, bg=BG_DARK)
        header.pack(fill="x", padx=16, pady=(16, 8))

        tk.Label(
            header, text="●", font=("Courier", 10),
            fg=ACCENT, bg=BG_DARK
        ).pack(side="left")
        tk.Label(
            header, text=f"  {self.titulo}",
            font=("Courier", 11, "bold"),
            fg=TEXT_PRIMARY, bg=BG_DARK
        ).pack(side="left")

        # nombre del archivo (derecha)
        name = getattr(self.video.ruta_inicial, "name", "")[:32]
        tk.Label(
            header, text=name,
            font=("Courier", 9), fg=TEXT_MUTED, bg=BG_DARK
        ).pack(side="right")

        # ── Separador ─────────────────────────────────────────────────────────
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=16)

        # ── Canvas de video ───────────────────────────────────────────────────
        video_frame = tk.Frame(self, bg=BG_DARK)
        video_frame.pack(padx=16, pady=(12, 0))

        # borde decorativo
        border_frame = tk.Frame(
            video_frame,
            bg=BORDER,
            padx=2, pady=2
        )
        border_frame.pack()

        self.label = tk.Label(border_frame, bg=BG_DARK, cursor="crosshair")
        self.label.pack()

        # ── Slider + frame counter ────────────────────────────────────────────
        slider_area = tk.Frame(self, bg=BG_DARK)
        slider_area.pack(fill="x", padx=16, pady=(10, 4))

        # frame counter
        counter_row = tk.Frame(slider_area, bg=BG_DARK)
        counter_row.pack(fill="x")

        tk.Label(
            counter_row, text="FRAME",
            font=("Courier", 8), fg=TEXT_MUTED, bg=BG_DARK
        ).pack(side="left")

        self.frame_label = tk.Label(
            counter_row,
            text=f"0 / {self.total_frames - 1}",
            font=("Courier", 9, "bold"), fg=ACCENT, bg=BG_DARK
        )
        self.frame_label.pack(side="left", padx=(6, 0))

        # ttk slider estilizado
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(
            "FP.Horizontal.TScale",
            background=BG_DARK,
            troughcolor=BG_SURFACE,
            sliderlength=18,
            sliderrelief="flat",
        )
        style.map("FP.Horizontal.TScale", background=[("active", ACCENT)])

        self.slider = ttk.Scale(
            slider_area,
            from_=0, to=self.total_frames - 1,
            orient="horizontal",
            command=self.on_slider,
            style="FP.Horizontal.TScale",
            length=self.display_w
        )
        self.slider.pack(pady=(2, 0))

        # ── Panel inferior (observación + captura) ────────────────────────────
        card = tk.Frame(self, bg=BG_CARD, padx=16, pady=14)
        card.pack(fill="x", padx=16, pady=(10, 16))

        # Título sección
        top_row = tk.Frame(card, bg=BG_CARD)
        top_row.pack(fill="x", pady=(0, 8))

        tk.Label(
            top_row, text="OBSERVACIÓN",
            font=("Courier", 9, "bold"), fg=TEXT_MUTED, bg=BG_CARD
        ).pack(side="left")

        self.conteo = tk.Label(
            top_row, text="0 / 219",
            font=("Courier", 9), fg=TEXT_MUTED, bg=BG_CARD
        )
        self.conteo.pack(side="right")

        # Textarea
        text_frame = tk.Frame(card, bg=BORDER, padx=1, pady=1)
        text_frame.pack(fill="x", pady=(0, 12))

        self.text_input = tk.Text(
            text_frame,
            height=5,
            font=("Courier", 11),
            bg=BG_SURFACE,
            fg=TEXT_PRIMARY,
            insertbackground=ACCENT,
            relief="flat",
            wrap="word",
            padx=10, pady=8,
            undo=True,
            selectbackground=ACCENT,
            selectforeground=TEXT_PRIMARY,
        )
        self.text_input.pack(fill="x")
        self.text_input.bind("<KeyPress>", self.verificar_limite)

        # Scrollbar discreta para el textarea
        sb = tk.Scrollbar(text_frame, command=self.text_input.yview, width=6, bg=BG_SURFACE, troughcolor=BG_SURFACE, relief="flat")
        # (omitimos yscrollcommand para no complicar el layout, el usuario puede scrollear con teclado)

        # ── Botón capturar ────────────────────────────────────────────────────
        self.btn = _FlatButton(
            card,
            text="⬤  Capturar frame  (calidad original)",
            command=self.capture,
            bg=ACCENT, fg="white",
            hover_bg=ACCENT_HOVER,
            font=("Courier", 10, "bold"),
            padx=18, pady=10,
            width=PANEL_W - 32
        )
        self.btn.pack(fill="x")

    # ── Lógica (sin cambios) ──────────────────────────────────────────────────

    def show_frame(self, frame_id):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
        ret, frame = self.cap.read()
        if ret:
            frame_resized = cv2.resize(frame, (self.display_w, self.display_h))
            frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
            img   = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(img)
            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)

    def on_slider(self, val):
        self.current_frame = int(float(val))
        self.frame_label.config(text=f"{self.current_frame} / {self.total_frames - 1}")
        self.show_frame(self.current_frame)

    def capture(self):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)
        ret, frame = self.cap.read()
        if ret:
            if not self.destino.exists():
                self.destino.mkdir(parents=True, exist_ok=True)
            filename = self.video.ruta_inicial.name[:18]
            path = self.destino / f"{filename}.png"
            cv2.imwrite(str(path), frame)
            print(f"Guardado frame original en: {path}")
            self.service.agregar_screenshot(self.video, path)
            self.service.agregar_observacion(self.video, self.text_input.get("1.0", "end-1c"))
        self.close()

    def close(self):
        if self.cap:
            self.cap.release()
        self.destroy()

    def verificar_limite(self, event):
        contenido = self.text_input.get("1.0", "end-1c")
        n = len(contenido)
        # Color del contador según proximidad al límite
        if n >= 219:
            color = "#FF5A5A"
        elif n >= 180:
            color = "#FFB347"
        else:
            color = TEXT_MUTED
        self.conteo.config(text=f"{n} / 219", fg=color)
        if n >= 219 and event.keysym not in ("BackSpace", "Delete", "Left", "Right", "Up", "Down"):
            return "break"


# ── Widget auxiliar: botón flat con hover ────────────────────────────────────

class _FlatButton(tk.Canvas):
    """Botón rectangular sin relieve, con transición de color al hover."""

    def __init__(self, parent, text, command, bg, fg, hover_bg,
                 font, padx=12, pady=8, width=200, **kwargs):
        h = pady * 2 + 22
        super().__init__(parent, bg=parent["bg"], bd=0, highlightthickness=0,
                         height=h, width=width)
        self._bg       = bg
        self._hover_bg = hover_bg
        self._fg       = fg
        self._font     = font
        self._text     = text
        self._cmd      = command
        self._width    = width
        self._height   = h
        self._padx     = padx
        self._pady     = pady

        self._rect = self.create_rectangle(0, 0, width, h, fill=bg, outline="", tags="btn")
        self._lbl  = self.create_text(
            width // 2, h // 2,
            text=text, fill=fg,
            font=font, tags="btn"
        )

        self.tag_bind("btn", "<Enter>",   self._on_enter)
        self.tag_bind("btn", "<Leave>",   self._on_leave)
        self.tag_bind("btn", "<Button-1>", self._on_click)

    def _on_enter(self, _):
        if not getattr(self, '_disabled', False):
            self.itemconfig(self._rect, fill=self._hover_bg)

    def _on_leave(self, _):
        if not getattr(self, '_disabled', False):
            self.itemconfig(self._rect, fill=self._bg)
        else:
            self.itemconfig(self._rect, fill=BORDER)

    def _on_click(self, _):
        if not getattr(self, '_disabled', False):
            self._cmd()

    def set_state(self, state):
        """'normal' o 'disabled'. Cambia apariencia y bloquea clicks."""
        self._disabled = (state == "disabled")
        alpha = TEXT_MUTED if self._disabled else self._fg
        fill  = BORDER     if self._disabled else self._bg
        self.itemconfig(self._rect, fill=fill)
        self.itemconfig(self._lbl,  fill=alpha)

