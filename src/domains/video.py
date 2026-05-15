from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime
from .diapositiva import Diapositiva
from typing import Optional


@dataclass
class Video:
    nombre: str
    hora_fecha: datetime
    ruta_inicial: Path
    ruta_enumerada: Optional[Path] = None
    diapositivas: list[Diapositiva] = field(default_factory=list)

    def __str__(self):
        base = (
            f"CAMARA: {self.nombre} -> {self.hora_fecha.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"RUTA: {self.ruta_inicial}"
        )

        return base

    
    #Agregar nueva_ruta
    def set_ruta_enumerada(self, ruta : Path):
        self.ruta_enumerada = ruta
    
    #Agregar lista de diapositivas
    def set_diapositivas(self, diapositivas : list[Diapositiva]):
        self.diapositivas = diapositivas

    def crear_nueva_diapositiva(self):
        self.diapositivas.append(Diapositiva())
    
    def agregar_screenshot(self, captura):
        self.diapositivas[len(self.diapositivas)-1].agregar_captura(captura)

    
    
    
  
    