from ..domains.video import Video
from ..utils import obtenerHorario

class VideoFactory:
    @staticmethod
    def crear(ruta):
        return Video(
            nombre= str(ruta.parent.name),
            ruta_inicial=ruta,
            hora_fecha=obtenerHorario(ruta.name))