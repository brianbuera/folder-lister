# src/strategies/asignacion_diapositiva.py
from abc import ABC, abstractmethod
from ..video import Video
from ..screenshot import Screenshot
from ..diapositiva import Diapositiva

class AsignacionDiapositiva(ABC):
    @abstractmethod
    def asignar(self, video: Video, screenshot: Screenshot, observacion: str):
        pass

class NuevaDiapositiva(AsignacionDiapositiva):
    def asignar(self, video: Video, screenshot: Screenshot, observacion: str):
        diapositiva = Diapositiva()
        diapositiva.agregar_captura(screenshot)
        if observacion:
            diapositiva.agregar_observacion(observacion)
        video.agregar_diapositiva(diapositiva)

class MismaDiapositiva(AsignacionDiapositiva):
    def asignar(self, video: Video, screenshot: Screenshot, observacion: str):
        video.diapositivas[-1].agregar_captura(screenshot)
        if observacion:
            video.diapositivas[-1].agregar_observacion(observacion)