# src/strategies/asignacion_diapositiva.py
from abc import ABC, abstractmethod
from ..video import Video
from ..screenshot import Screenshot
from ..diapositiva import Diapositiva

class AsignacionDiapositiva(ABC):
    @abstractmethod
    def asignar(self, video: Video, screenshot: Screenshot):
        pass

class NuevaDiapositiva(AsignacionDiapositiva):
    def asignar(self, video: Video, screenshot: Screenshot):
        diapositiva = Diapositiva()
        diapositiva.agregar_captura(screenshot)
        video.agregar_diapositiva(diapositiva)

class MismaDiapositiva(AsignacionDiapositiva):
    def asignar(self, video: Video, screenshot: Screenshot):
        video.diapositivas[-1].agregar_captura(screenshot)
