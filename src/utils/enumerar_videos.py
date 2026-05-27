import shutil

def mover_video_enumerado(orden, video, destino):
    nueva_ruta = destino / f"{str(orden+1).zfill(2)} - {video.nombre}"
    nueva_ruta.mkdir()
    shutil.copy(video.ruta_inicial, nueva_ruta)
    video.ruta_enumerada = nueva_ruta / video.ruta_inicial.name
    print(video)
