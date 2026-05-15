from ..factory.videofactory import VideoFactory
from ..repository.videosrepository import VideoRepository
from ..domains import strategies
from ..utils import mover_video_enumerado

class VideoService:
    def __init__(self, repo: VideoRepository):
        self._repo = repo

    @property
    def repo(self):
        return self._repo
    
    def cargarVideos(self, directorio):
        self.limpiarRepo()
        rutas = list(directorio.rglob("*.mkv"))
        for ruta in rutas:
            self._repo.agregar_video(VideoFactory.crear(ruta))

    def obtenerVideos(self):
        return self._repo.videos
    
    
    def agregarVideo(self, ruta): 
        self._repo.agregar_video(VideoFactory.crear(ruta))


    def ordenar(self, estrategia):
        self.actualizarLista(strategies[estrategia](self._repo.videos))
        

    def actualizarLista(self, videos):
        self.repo.videos = videos
    

    def limpiarRepo(self):
        self.repo.limpiar()


    def agregar_screenshot(self, video, path):
        self.repo.agregar_imagen(video, path)
    

    def agregar_observacion(self, video, observacion):
        self.repo.agregar_observacion(video, observacion)


    def eliminar_videos(self, indices):
        for i in indices:
            self._repo.eliminar_video(i)
    

    def enumerar_videos(self, destino):
        if not destino.exists():
            destino.mkdir(parents=True, exist_ok=True)
        for idx, video in enumerate(self._repo.videos):
            mover_video_enumerado(idx, video, destino)

    #OBTENER VIDEO MEDIANTE INDICE
    def obtener_video(self, indice):
        return self._repo.get_video(indice)

    def actualizar_video(self, indice, video):
        self._repo.update_video(indice, video)
        
    def guardar_diapositiva(self, indice, diapositiva):
        self._repo.videos[indice].set_diapositivas(diapositiva)


    




