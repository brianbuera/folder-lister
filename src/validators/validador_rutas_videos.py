class ValidadorRutasVideos:

    def __init__(self, rules):
        self.rules = rules

    def validar(self, rutas_videos):
        errores = []

        for ruta in rutas_videos:

            carpeta_actual = ruta.parent
            carpeta_padre = carpeta_actual.parent

            if not carpeta_padre:
                errores.append(f"Estructura incompleta: {ruta}")
                continue

            if not (
                self.rules.es_carpeta_valida(carpeta_actual.name)
                and self.rules.es_video_valido(ruta.name)
                and self.rules.es_padre_valido(carpeta_padre.name)
            ):
                errores.append(f"No cumple formato: {ruta}")

        return errores