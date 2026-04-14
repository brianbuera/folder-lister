from dataclasses import dataclass
from pathlib import Path
from datetime import datetime

@dataclass
class VideoInfo:
    nombre: str
    ruta_inicial: Path
    hora_fecha: datetime


    def __str__(self):
        return (
            f"CAMARA: {self.nombre} -> {self.hora_fecha.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"RUTA: {self.ruta_inicial}"
        )
