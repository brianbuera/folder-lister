from dataclasses import dataclass
from pathlib import Path


@dataclass
class Screenshot:
    ruta: Path
    x: float = 0.0
    y: float = 0.0
    ancho: float = 0.0
    alto: float = 0.0

    @property
    def posicion(self) -> tuple[float, float]:
        return self.x, self.y
    

    def __str__(self):
        return (
            f"      📸 Screenshot\n"
            f"         Ruta: {self.ruta.name}\n"
            f"         Posición: ({self.x:.2f}, {self.y:.2f})\n"
            f"         Tamaño: {self.ancho:.2f} x {self.alto:.2f}"
        )
    