from ..domains.rules.rules_ruta_video import RulesRutaVideo

class ValidadorRutasVideos:
        @staticmethod
        def validar(rutas_videos):
            errores = []
            carpetas = {}

            for ruta in rutas_videos:
                if not RulesRutaVideo.es_video_valido(ruta.name):
                    errores.append(f"No cumple formato: {ruta}")
                    continue

                carpeta = ruta.parent
                carpetas.setdefault(carpeta, []).append(ruta)

            for carpeta, videos in carpetas.items():
                if len(videos) > 1:
                    errores.append(f"Más de un video en carpeta: {carpeta}")

            return errores
    
