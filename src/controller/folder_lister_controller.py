
from ..config.config_manager import config
from pathlib import Path
from ..service.vlc_player import VlcPlayer


class FolderListerController:

    config_manager = config
    
    def __init__(self, video_service, view):

        self.video_service = video_service
        self.view = view
        self.view.sig_importar_videos.connect(self.seleccionar_directorio)
        self.view.sig_eliminar_video.connect(self.delete_video)
        self.view.sig_ordenar_por_hora.connect(self.ordenar_por_horario)


    def start_app(self):
        self.view.show()


    def seleccionar_directorio(self, directorio : str):
        print(f"Carpeta recibida: {directorio}")
        directorio =  list(Path(directorio).rglob("*.mkv"))
        videos = self.video_service.create_videos(directorio)
        self.view.update_table_data(videos)


    def delete_video(self, id : int):
        self.video_service.delete_by_id(id)
        videos = self.video_service.get_videos()
        self.view.update_table_data(videos)
    

    def ordenar_por_horario(self):
        videos = self.video_service.sort_by_time()
        self.view.update_table_data(videos)


        

    