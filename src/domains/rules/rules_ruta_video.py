import re


class RulesRutaVideo:
    _nombre_video = re.compile(
        r'\d{1,2}_\d{1,2}_\d{4} \d{2}_\d{2}_\d{2} \(UTC-[0-9]{2}_[0-9]{2}\)\.(mkv|mp4)$'
    )

    @staticmethod
    def es_video_valido(nombre):
        return bool(RulesRutaVideo._nombre_video.fullmatch(nombre))

