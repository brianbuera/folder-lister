from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional
from .diapositiva import Diapositiva


@dataclass
class Video:
    nombre: str
    hora_fecha: datetime
    ruta_inicial: Path
    ruta_enumerada: Optional[Path] = None
    diapositivas: list[Diapositiva] = field(default_factory=list)

    def agregar_diapositiva(self, diapositiva: Diapositiva):
        self.diapositivas.append(diapositiva)
    
    @property
    def ruta_hypervinculo(self) -> Path:
        return self.ruta_enumerada or self.ruta_inicial

    @property
    def tiene_capturas(self) -> bool:
        return any(d.cantidad_capturas > 0 for d in self.diapositivas)

    @property
    def total_capturas(self) -> int:
        return sum(d.cantidad_capturas for d in self.diapositivas) if len(self.diapositivas) > 0 else 0
        
    def sumar_minutos(self, seg):
        hora = self.hora_fecha + timedelta(seconds=seg)
        return hora.strftime('%H_%M_%S')


    def __str__(self):
        contenido = (
            f"\n==================================================\n"
            f"🎬 VIDEO\n"
            f"==================================================\n"
            f"📁 Nombre:          {self.nombre}\n"
            f"🕒 Fecha y Hora:    {self.hora_fecha.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"📂 Ruta Original:   {self.ruta_inicial}\n"
            f"📦 Ruta Enumerada:  {self.ruta_enumerada or 'Sin enumerar'}\n"
            f"🖼️  Diapositivas:    {len(self.diapositivas)}\n"
            f"📸 Capturas Totales: {self.total_capturas}\n"
            f"==================================================\n"
        )

        for idx, d in enumerate(self.diapositivas, 1):
            contenido += (
                f"\n\n########## DIAPOSITIVA {idx} ##########\n"
                f"{d}"
            )

        return contenido


    
    
    
  
    