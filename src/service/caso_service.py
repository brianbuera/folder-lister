from ..infrastructure import PowerPointClient
from ..factory import Diapositivas
from pathlib import Path
import json




class CasoService ():
    
    def __init__(self):
         self.ruta_template = self.buscar_template()


    def agregar_videos (self, videos):
            self.videos =  videos[::-1]

    def crear_nuevo_caso(self):
        aplicacion = PowerPointClient()
        presentacion = aplicacion.open_presentacion(self.ruta_template)
        for v in self.videos:
            Diapositivas.crearDiapositiva(presentacion, v)
    
    def buscar_template(self):
         with open("config.json", "r") as f:
            data = json.load(f)
            ruta = data.get("ruta_template", "")
            if Path(ruta).exists():
                return ruta
            else:
                return None



        