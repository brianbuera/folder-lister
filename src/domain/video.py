from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime, timedelta
from .screenshot import Screenshot


@dataclass
class Video:
    nombre: str
    hora_fecha: datetime
    ruta: Path

    @property
    def hora_fecha_str(self)-> str:
        return self.hora_fecha.strftime('%H:%M:%S %d-%m-%M')
    
    def __str__(self):
        contenido = (
            f"\n==================================================\n"
            f"🎬 VIDEO\n"
            f"==================================================\n"
            f"📁 Nombre:          {self.nombre}\n"
            f"🕒 Fecha y Hora:    {self.hora_fecha_str}\n"
            f"📂 Ruta Original:   {self.ruta_inicial}\n"
            f"📦 Ruta Enumerada:  {self.ruta_enumerada or 'Sin enumerar'}\n"
            f"🖼️  Diapositivas:    {len(self.diapositivas)}\n"
            f"📸 Capturas Totales: {self.total_capturas}\n"
            f"==================================================\n"
        )

        for idx, s in enumerate(self.screenshots, 1):
            contenido += (
                f"\n\n########## SCREENSHOT {idx} ##########\n"
                f"{s}"
            )

        return contenido


    
    
    
  
    