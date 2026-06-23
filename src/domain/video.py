from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime



@dataclass
class Video:
    nombre: str
    hora_fecha: datetime
    ruta: Path

    @property
    def hora_fecha_str(self)-> str:
        return self.hora_fecha.strftime('%H:%M:%S %d-%m-%M')
    
    @property
    def hora(self):
        return self.hora_fecha.strftime('%H:%M')
    
    @property
    def fecha(self):
        return self.hora_fecha.strftime('%d-%m-%M')

    def __str__(self):
        contenido = (
            f"\n==================================================\n"
            f"🎬 VIDEO\n"
            f"==================================================\n"
            f"📁 Nombre:          {self.nombre}\n"
            f"🕒 Fecha y Hora:    {self.hora_fecha_str}\n"
            f"📂 Ruta:   {self.ruta_inicial}\n"
            f"==================================================\n"
        )

        return contenido


    
    
    
  
    