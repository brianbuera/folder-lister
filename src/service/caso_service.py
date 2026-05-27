from ..infrastructure.powerpoint_client import PowerPointClient
from ..factory.crear_slide import Diapositivas

class CasoService ():



    def crear_nuevo_caso(self, videos, ruta_template):
        aplicacion = PowerPointClient()
        caso_abierto = aplicacion.connect_presentation()
        if not caso_abierto:
            aplicacion.close_powerpoint_client()
            return False
        template = aplicacion.open_presentacion(ruta_template, False)
        for v in videos:
            if v.diapositivas:
                Diapositivas.crearDiapositiva(template, caso_abierto, v)
        aplicacion.close_presentation(template)

        return True
        
 



        