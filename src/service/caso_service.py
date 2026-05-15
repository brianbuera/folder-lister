from ..infrastructure import PowerPointClient
from ..factory import Diapositivas
from ..domains import Diapositiva
from pathlib import Path

class CasoService ():



    def crear_nuevo_caso(self, videos, ruta_template):
        aplicacion = PowerPointClient()
        caso_abierto = aplicacion.connect_presentation()
        if not caso_abierto:
            return
        template = aplicacion.open_presentacion(ruta_template)

        for v in videos:
            if v.ruta_screenshot:
                Diapositivas.crearDiapositiva(template, caso_abierto, v)
        aplicacion.close_presentation(template)
        
 



        