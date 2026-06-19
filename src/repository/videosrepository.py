from ..domain.video import Video
from pathlib import Path


class VideoRepository:

    def __init__(self):
        self._videos: list[Video] = []
        
    @property
    def videos(self):
        return self._videos
    

    def save(self, video):
        self._videos.append(video)
   
    def find_by_id(self, indice : int) -> Video:
        return self._videos[indice]

    def delete(self, indice):
        del self._videos[indice]

    def update(self, indice, video):
        self.videos[indice] = video

    def exist_video_by_ruta(self, ruta : Path) -> Video | None:
        return any(video.ruta == ruta for video in self._videos)
        
    def ordenar_por_hora_fecha(self):
        sorted(self._videos, key=lambda x: x.hora_fecha)



