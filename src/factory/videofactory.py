from ..domains.videoinfo import VideoInfo
from ..utils.obtener_horario import obtenerHorario

class VideoFactory:
    @staticmethod
    def crear(ruta):
        return VideoInfo(
            nombre=ruta.parent.name,
            ruta_inicial=ruta,
            hora_fecha=obtenerHorario(ruta.name))