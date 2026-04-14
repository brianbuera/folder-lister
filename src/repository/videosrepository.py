from pathlib import Path
from ..models.videoinfo import VideoInfo

class VideoRepository:

    def __init__(self):
        self._videos: list[VideoInfo] = []
        
    @property
    def videos(self):
        return self._videos
    
    @videos.setter
    def videos(self, videos: list[VideoInfo]):
        if not all(isinstance(v, VideoInfo) for v in videos):
            raise ValueError("Todos los elementos deben ser VideoInfo")
        self._videos = videos

    def agregar_video(self, video):
        self._videos.append(video)

    def limpiar(self):
        self._videos.clear()    



