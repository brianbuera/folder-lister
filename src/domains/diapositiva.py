# src/domain/diapositiva.py
from dataclasses import dataclass, field
from .screenshot import Screenshot
from ..utils import cm
PT_W = 960
PT_H = 540
LIMITE = cm(25.40)

@dataclass
class Diapositiva:
    id : int = 0
    observacion: str = "Observaciones de la imagen:\n"
    screenshots: list[Screenshot] = field(default_factory=list)

    def agregar_captura(self, captura: Screenshot):
        self.screenshots.append(captura)
        self.calcular_layout()

    def agregar_observacion(self, obs: str):
        self.observacion += obs

    def calcular_layout(self):
        n = len(self.screenshots)
        if n == 0:
            return
        ancho = PT_W / n
        porcentaje = LIMITE / n
        for i, screenshot in enumerate(self.screenshots):
            screenshot.x     = i * porcentaje
            screenshot.y     = 49.32
            screenshot.ancho = ancho
            screenshot.alto  = PT_H

    @property
    def cantidad_capturas(self) -> int:
        return len(self.screenshots)
 

    def __str__(self):
        contenido = (
            f"\n   ┌─────────────────────────────\n"
            f"   │ 🖼️  DIAPOSITIVA\n"
            f"   ├─────────────────────────────\n"
            f"   │ Observación: {self.observacion or 'Sin observaciones'}\n"
            f"   │ Capturas: {len(self.screenshots)}\n"
            f"   └─────────────────────────────\n"
        )

        for idx, s in enumerate(self.screenshots, 1):
            contenido += (
                f"\n      [{idx}]\n"
                f"{s}\n"
            )

        return contenido

        