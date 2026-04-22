import shutil
from pathlib import Path


RUTA_TEMPLATE = Path("templates/template.pptx").resolve()

class CasoFactory:
    @staticmethod
    def crearCaso(destino):
        shutil.copy(RUTA_TEMPLATE, destino)





