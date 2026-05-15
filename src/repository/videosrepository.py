from ..domains.video import Video

class VideoRepository:

    def __init__(self):
        self._videos: list[Video] = []
        
    @property
    def videos(self):
        return self._videos
    
    @videos.setter
    def videos(self, videos: list[Video]):
        if not all(isinstance(v, Video) for v in videos):
            raise ValueError("Todos los elementos deben ser Video")
        self._videos = videos

    def get_video(self, indice):
        return self._videos[indice]
    
    def agregar_video(self, video):
        self._videos.append(video)

    def limpiar(self):
        self._videos.clear()    
    
    def agregar_imagen(self, video, path):
        for v in self._videos:
            if v == video: 
                v.agregar_screen(path) 

    def agregar_observacion(self, video, observacion):
        for v in self._videos:
            if v == video: 
                v.agregar_obs(observacion) 

    def eliminar_video(self, indice):
        del self._videos[indice]

    def update_video(self, indice, video):
        self.videos[indice] = video




