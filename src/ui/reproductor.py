import cv2
import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path

class Reproductor(tk.Toplevel):
    def __init__(self, parent, video_path: Path, destino: Path): 
        super().__init__(parent)
        self.video_path = video_path
        self.title("Frame Picker")
        self.destino : Path = destino / "captures"
        
        # 1. Configuración de Video
        self.cap = cv2.VideoCapture(str(video_path))
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.current_frame = 0

        # 2. Obtener dimensiones de la pantalla para el reescalado
        # Usamos el 80% del ancho/alto de la pantalla como máximo
        self.screen_w = self.winfo_screenwidth() * 0.8
        self.screen_h = self.winfo_screenheight() * 0.8
        
        # Obtener dimensiones originales del video
        self.v_width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.v_height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        # Calcular el factor de escala manteniendo la proporción
        scaling_factor = min(self.screen_w / self.v_width, self.screen_h / self.v_height)
        self.display_w = int(self.v_width * scaling_factor)
        self.display_h = int(self.v_height * scaling_factor)

        # 3. Interfaz
        self.slider = tk.Scale(
            self,
            from_=0,
            to=self.total_frames - 1,
            orient="horizontal",
            command=self.on_slider,
            length=self.display_w # El slider mide lo mismo que la imagen
        )
        self.slider.pack(pady=5)
      
        self.label = tk.Label(self)
        self.label.pack()

        self.btn = tk.Button(self, text="Capturar frame (Calidad Original)", command=self.capture, bg="#4CAF50", fg="white")
        self.btn.pack(pady=10)

        # Manejar el cierre de la ventana con la "X"
        self.protocol("WM_DELETE_WINDOW", self.close)

        # Mostrar primer frame
        self.show_frame(0)

    def show_frame(self, frame_id):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
        ret, frame = self.cap.read()
        if ret:
            # Redimensionar solo para la visualización
            frame_resized = cv2.resize(frame, (self.display_w, self.display_h))
            
            frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(img)

            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)

    def on_slider(self, val):
        self.current_frame = int(val)
        self.show_frame(self.current_frame)

    def capture(self):
        # Para capturar, volvemos a leer el frame en tamaño original
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)
        ret, frame = self.cap.read()
        if ret:
            if not self.destino.exists():
                self.destino.mkdir(parents=True, exist_ok=True)
            
            # Nombre de archivo seguro
            filename = self.video_path.name[:18]
            path = self.destino / f"{filename}.png"
            
            cv2.imwrite(path, frame)
            print(f"Guardado frame original en: {path}")
        self.close()

    def close(self):
        if self.cap:
            self.cap.release()
        self.destroy()


