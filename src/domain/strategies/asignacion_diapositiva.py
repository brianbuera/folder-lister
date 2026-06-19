# src/strategies/asignacion_diapositiva.py
from abc import ABC, abstractmethod
from ..video import Video
from ..screenshot import Screenshot
from ..diapositiva import Diapositiva
from datetime import time

class AsignacionDiapositiva(ABC):
    @abstractmethod
    def asignar(self, video: Video, screenshot: Screenshot, hora_captura : time):
        pass

class NuevaDiapositiva(AsignacionDiapositiva):
    def asignar(self, video: Video, screenshot: Screenshot, hora_captura : time):
        diapositiva = Diapositiva()
        screenshot.hora = hora_captura
        diapositiva.agregar_captura(screenshot)
        video.agregar_diapositiva(diapositiva)

class MismaDiapositiva(AsignacionDiapositiva):
    def asignar(self, video: Video, screenshot: Screenshot, hora_captura : time):
        screenshot.hora = hora_captura
        video.diapositivas[-1].agregar_captura(screenshot)
