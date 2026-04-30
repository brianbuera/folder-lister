import re


medios = re.compile(r'Formato de reproductor de medios')

nombre_carpeta = re.compile(
r"(?:\d+\s*-\s+)?[\w\s\-\.\(\)]+")

nombre_video = re.compile(
    r'\d{1,2}_\d{1,2}_\d{4} \d{2}_\d{2}_\d{2} \(UTC-[0-9]{2}_[0-9]{2}\)\.(mkv|mp4)$'
)



class RulesRutaVideo:

    @staticmethod
    def es_carpeta_valida(nombre):
        return bool(nombre_carpeta.fullmatch(nombre))

    @staticmethod
    def es_video_valido(nombre):
        return bool(nombre_video.fullmatch(nombre))

    @staticmethod
    def es_padre_valido(nombre):
        return bool(medios.search(nombre))