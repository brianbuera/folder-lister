from ..domains.video import Video
from ..utils import obtenerHorario, cortar_desde_primera_letra

class VideoFactory:
    @staticmethod
    def crear(ruta):
        return Video(
            nombre= cortar_desde_primera_letra(str(ruta.parent.name)),
            ruta_inicial=ruta,
            hora_fecha=obtenerHorario(ruta.name))