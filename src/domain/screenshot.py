from dataclasses import dataclass
from pathlib import Path
from datetime import time

@dataclass
class Screenshot:
    ruta: Path
    hora: time | None = None 
    ruta_video = Path | None = None


    def __str__(self):
        return (
            f"      📸 Screenshot\n"
            f"         Ruta: {self.ruta.name}\n"
        )
    
    def hora_str(self):
        return self.hora.strftime("%H:%M")