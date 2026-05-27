from ..domains.video import Video
from ..utils import obtenerHorario, obtener_numero_y_nombre

class VideoFactory:
    @staticmethod
    def crear(ruta):
        return Video(
            nombre= obtener_numero_y_nombre(str(ruta.parent.name)),
            ruta_inicial=ruta,
            hora_fecha=obtenerHorario(ruta.name))