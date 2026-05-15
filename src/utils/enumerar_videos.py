import shutil
from pathlib import Path
from ..domains import Video

def mover_video_enumerado(orden, video : Video, destino):
    nueva_ruta = destino / f"{str(orden).zfill(2)} - {video.nombre}"
    nueva_ruta.mkdir()
    shutil.copy(video.ruta_inicial, nueva_ruta)
