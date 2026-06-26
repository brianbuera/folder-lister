from ..domain.video import Video
from pathlib import Path


class VideoRepository:

    def __init__(self):
        self._videos: list[Video] = []
        self._next_id = 1
   
    @property
    def videos(self):
        return self._videos
    
    #Agregar un nuevo video
    def save(self, video):
        video.id = self._next_id
        self._next_id += 1
        self._videos.append(video)
        print(video)
    
    #Encontrar un video por id (indice)
    def find_by_id(self, indice : int) -> Video:
        return self._videos[indice]

    #Borrar un video
    def delete(self, indice):
        del self._videos[indice]

    #Actualizar un video
    def update(self, indice, video):
        self._videos[indice] = video

    #Verificar existencia de un video con un ruta especifica
    def exist_video_by_ruta(self, ruta : Path) -> Video | None:
        return any(video.ruta == ruta for video in self._videos)
    

    def sort_by_time(self):
        self._videos.sort(key=lambda video:video.hora_fecha)



