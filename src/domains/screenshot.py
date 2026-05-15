
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Screenshot:
    ruta: Path
    x: float
    y: float
    ancho: float
    alto: float

    def __init__(self, ruta : Path):
        self.ruta = ruta

    
    def get_posicion(self):
        return self.x, self.y