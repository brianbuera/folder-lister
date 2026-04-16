from ..factory.videofactory import VideoFactory
from ..repository.videosrepository import VideoRepository
from .sort_strategy import strategies

class VideoService:
    def __init__(self, repo: VideoRepository):
        self._repo = repo

    @property
    def repo(self):
        return self._repo
    
    def cargarVideos(self, directorio):
        rutas = directorio.rglob("*.mkv")
        for ruta in rutas:
            self._repo.agregar_video(VideoFactory.crear(ruta))

    def obtenerVideos(self):
        return self._repo.videos
    
    def agregarVideo(self, ruta): 
        self._repo.agregar_video(ruta)

                
    def ordenar(self, estrategia):
        return strategies[estrategia](self._repo.videos)
        
    
    def actualizarLista(self, Videos):
        self.repo.videos = Videos
    
    def limpiarRepo(self):
        self.repo.limpiar()

