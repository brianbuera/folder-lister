from ..infrastructure import PowerPointClient
from ..factory import Diapositivas
from pathlib import Path



class CasoService ():
    
    ruta_template = Path("C:/Users/u58667/Desktop/Programacion/FolderLister/templates/template.pptx")
    videos = None 

    def agregar_videos (self, videos):
        self.videos =  videos[::-1]

    def crear_nuevo_caso(self):
        aplicacion = PowerPointClient()
        presentacion = aplicacion.open_presentacion(self.ruta_template)
        for v in self.videos:
            Diapositivas.crearDiapositiva(presentacion, v)



        