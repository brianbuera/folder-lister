from ..domain.rules import RulesRutaVideo

class ValidadorRutasVideos:
        @staticmethod

        def validar(directorio):
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
        

        def empty(self, directorio):
            if not any(directorio.iterdir()):
                return False
            return True

        def get_path_videos(self, directorio):
            return list(directorio.rglob("*.mkv")) 
             
            
             
    
