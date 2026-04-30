from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
from typing import Optional
import os

@dataclass
class VideoInfo:
    nombre: str
    ruta_inicial: Path
    hora_fecha: datetime
    ruta_screenshot: Optional[Path] = None
    observacion: Optional[str] = ""


    def __str__(self):
        base = (
            f"CAMARA: {self.nombre} -> {self.hora_fecha.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"RUTA: {self.ruta_inicial}"
        )
        if self.ruta_screenshot:
            base += f"\nSCREEN: {self.ruta_screenshot}"
            print(os.path.exists(self.ruta_screenshot))

        if self.observacion:
            base += f"\nObservacion: {self.observacion}"
        return base
    
    def agregar_screen(self, screen: Path) -> None:
        self.ruta_screenshot = screen
        print(self)
    
    def agregar_obs(self, obs: str) -> None:
        self.observacion = obs
