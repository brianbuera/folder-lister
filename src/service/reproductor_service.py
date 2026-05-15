# src/services/reproductor_service.py
from pathlib import Path
import cv2
from ..domains import Diapositiva

class ReproductorService:
    """Lógica de negocio del reproductor: lectura de frames y capturas."""

    def __init__(self,i_video, destino: Path, video_service):
        self.i_video        = i_video
        self.destino      = destino / "captures"
        self.video_service = video_service
        self.video = self.video_service.obtener_video(i_video)
        self.cap           = cv2.VideoCapture(str(self.video.ruta_inicial))
        self.total_frames  = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.current_frame = 0

    # ── Video ─────────────────────────────────────────────────────────────────
    @property
    def dimensiones_video(self) -> tuple[int, int]:
        w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return w, h
    
    def get_frame(self, frame_id: int):
        """Devuelve el frame RGB como ndarray, o None si falla."""
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
        ret, frame = self.cap.read()
        if not ret:
            return None
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def get_frame_scaled(self, frame_id: int, width: int, height: int):
        frame = self.get_frame(frame_id)
        if frame is None:
            return None
        return cv2.resize(frame, (width, height))

    # ── Capturas ──────────────────────────────────────────────────────────────

    @property
    def capturas_restantes(self) -> int:
        return self.LIMITE_CAPTURAS - len(self.video.ruta_screenshot)

    @property
    def limite_alcanzado(self) -> bool:
        return len(self.video.ruta_screenshot) >= self.LIMITE_CAPTURAS

    def guardar_captura(self, frame_id: int, tamaño) -> Path | None:
        """Guarda el frame en disco y lo registra en el servicio. Devuelve la ruta."""
        frame = self.get_frame(frame_id)
        if frame is None:
            return None

        self.destino.mkdir(parents=True, exist_ok=True)

        n        = tamaño + 1
        filename = self.video.ruta_inicial.name[:18]
        path     = self.destino / f"{n} - {filename}.png"

        bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        cv2.imwrite(str(path), bgr)

        return path

    def release(self):
        if self.cap:
            self.cap.release()


    def obtener_cantidad_diapositivas(self):
        return len(self.video.diapositivas)
    
    def agregar_nueva_diapositiva(self):
        self.video.crear_nueva_diapositiva()
    

    LIMITE_CAPTURAS = 4
