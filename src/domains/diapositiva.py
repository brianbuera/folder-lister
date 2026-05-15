from typing import Optional
from dataclasses import dataclass, field
from .screenshot import Screenshot



@dataclass
class Diapositiva:
    screenshots: list[Screenshot] = field(default_factory=list)
    observacion: Optional[str] = "Observaciones de la imagen:\n"


    def __init__(self, observacion = ""):
        self.screenshots = []
        self.observacion = self.observacion

    def agregar_captura (self, captura):
        self.screenshots.append(captura)

    def agregar_observacion(self, obs : str):
        self.observacion += obs