from ..repository.videosrepository import VideoRepository
from ..domain.video import Video
from ..utils.features_horario import extraer_datetime
from ..exceptions.video_already_exists_error import VideoAlreadyExistsError
from pathlib import Path
from ..mapper.to_dict import _to_dict
class VideoService:
    
    def __init__(self):
        self._video_repository = VideoRepository()

    def get_videos(self):
        return _to_dict(self._video_repository.videos)
    
    #De una direccion de video crear un objeto Video
    def create_video(self, ruta) -> Video: 
        if self._video_repository.exist_video_by_ruta(ruta):
            raise VideoAlreadyExistsError(f"El video ya se encuetra cargado")
        nombre = ruta.parent.name
        hora_fecha = extraer_datetime(ruta.name)
        video = Video(nombre=nombre, hora_fecha=hora_fecha, ruta=ruta)
        self._video_repository.save(video)
        return video
            
    # De de una lista de rutas crear una lista de videos
    def create_videos(self, rutas : list[Path])-> list[Video]:
        videos = [self.create_video(r) for r in rutas]
        return _to_dict(videos)
    
    # Buscar un video por indide de ubicacion en lista 
    def search_video_by_id(self, indice) -> Video:
        try:
            return self._video_repository.find_by_id(indice)
        except IndexError:
            print("el indice no existe")
    

    def modify_video_by_id(self, indice, video):
        self._video_repository.update_video(indice, video)


    def delete_by_id(self, indice):
        try:
            self._video_repository.delete(indice)
        except IndexError:
            print("el indice no existe")

    def sort_by_time(self):
        videos = self._video_repository.videos
        return sorted(videos, key= lambda x: x.hora_fecha)

        
    

    



        
 


    




