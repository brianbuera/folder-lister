from ..repository.videosrepository import VideoRepository
from ..domain.video import Video
from ..utils.obtener_horario import extraer_datetime
from ..exceptions.video_already_exists_error import VideoAlreadyExistsError
from pathlib import Path

class VideoService:
    
    def __init__(self, repo: VideoRepository):
        self._video_repository = repo

    @property
    def video_repository(self):
        return self._video_repository
        
    def crear_video(self, ruta) -> Video: 
        if self._video_repository.exist_video_by_ruta(ruta):
            raise VideoAlreadyExistsError(f"El video ya se encuetra cargado")
        nombre = ruta.parent.name
        hora_fecha = extraer_datetime(ruta.name)
        video = Video(nombre=nombre, hora_fecha=hora_fecha, ruta=ruta)
        self._video_repository.save(video)
        return video
            

    def crear_videos(self, rutas : Path)-> list[Path]:
        videos = [self.crear_video(r) for r in rutas]
        return videos
    
    
    def search_video_by_id(self, indice):
        return self._video_repository.find_by_id(indice)
    

    def modify_video_by_id(self, indice, video):
        self._video_repository.update_video(indice, video)


    def delete_by_id(self, indice):
        try:
            self._video_repository.delete(indice)
        except IndexError:
            print("el indice no existe")

    def ordenar(self):
        self._video_repository.ordenar_por_hora_fecha()
        
    

    



        
 


    




