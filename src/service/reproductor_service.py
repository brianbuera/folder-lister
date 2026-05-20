# src/services/reproductor_service.py
from pathlib import Path
import cv2
from ..domains.screenshot import Screenshot
from ..domains.strategies.asignacion_diapositiva import AsignacionDiapositiva
from ..utils import normalizar


class ReproductorService:

    """Lógica de negocio del reproductor: lectura de frames y capturas."""

    def __init__(self,video, config):
        self.video = video
        self.cap = cv2.VideoCapture(str(self.video.ruta_inicial))
        self.total_frames  = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.current_frame = 0
        self.is_playing = False
        self.destino = Path(config.get_ruta_destino()) / 'captures'


    # ──Video ─────────────────────────────────────────────────────────────────
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

    
    @property
    def capturas_restantes(self) -> int:
        return self.LIMITE_CAPTURAS - self.video.diapositivas[-1].cantidad_capturas

    @property
    def limite_alcanzado(self) -> bool:
        return self.video.diapositivas[-1].cantidad_capturas >= self.LIMITE_CAPTURAS


    def _guardar_frame(self, frame_id, slide_id : int) -> Path | None:
            """Guarda el frame en disco y lo registra en el servicio. Devuelve la ruta."""
            segundos = self.current_frame // self.fps
            frame = self.get_frame(frame_id)
            if frame is None:
                return None

            self.destino.mkdir(parents=True, exist_ok=True)
            slide = f"slide_{slide_id}"
            n        = self.video.total_capturas + 1
            filename = normalizar(self.video.nombre)
            path     = self.destino / f"slide {slide} - captura {n} - {filename} - {self.video.sumar_minutos(segundos)}.png"

            bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            cv2.imwrite(str(path), bgr)

            return path
    
    def guardar_captura(self, frame_id: int, estrategia: AsignacionDiapositiva, slide_id : int):
        path = self._guardar_frame(frame_id, slide_id)
        screenshot = Screenshot(ruta=path)
        estrategia.asignar(self.video, screenshot)


    def release(self):
        if self.cap:
            self.cap.release()

    
    LIMITE_CAPTURAS = 4
