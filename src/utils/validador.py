import re

'''
pattern = re.compile(
    r'^.*[\\/]'                                  # cualquier ruta previa
    r'Exportar \d{1,2}-\d{1,2}-\d{4} \d{2}-\d{2}-\d{2}'
    r'[\\/]Formato de reproductor de medios'
    r'[\\/][^\\/]+'                              # carpeta de cámara
    r'[\\/]\d{1,2}_\d{1,2}_\d{4} '               # fecha del archivo
    r'\d{2}_\d{2}_\d{2} '
    r'\(UTC-[0-9]{2}_[0-9]{2}\)'
    r'\.(mkv|mp4)$'
)
'''

medios = re.compile(r'Formato de reproductor de medios')

nombre_carpeta = re.compile(
    r"(?:\d+\s*-\s+)?[A-Za-z0-9](?:[A-Za-z0-9 _-]*[A-Za-z0-9])?"
)

nombre_video = re.compile(
    r'\d{1,2}_\d{1,2}_\d{4} \d{2}_\d{2}_\d{2} \(UTC-[0-9]{2}_[0-9]{2}\)\.(mkv|mp4)$'
)


def validar_recien_exportados(directorio):

    rutas_videos = list(directorio.rglob("*.mkv"))

    if not rutas_videos:
        return "❌ No se encontraron videos .mkv en el directorio."

    errores = []

    for ruta_video in rutas_videos:

        carpeta_actual = ruta_video.parent
        carpeta_padre = carpeta_actual.parent if carpeta_actual.parent else None

        if not carpeta_padre:
            errores.append(f"Estructura incompleta: {ruta_video}")
            continue

        if not (
            nombre_carpeta.fullmatch(carpeta_actual.name)
            and nombre_video.fullmatch(ruta_video.name)
            and medios.search(carpeta_padre.name)
        ):
            errores.append(f"No cumple formato: {ruta_video}")

    if errores:
        return "\n".join(errores)

    return None




