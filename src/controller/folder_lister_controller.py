
from ..config.config_manager import config
from pathlib import Path


class FolderListerController:

    config_manager = config
    
    def __init__(self, video_service, view):

        self.video_service = video_service
        self.view = view
        self.view.controller = self

        self.view.sig_importar_videos.connect(self.seleccionar_directorio)
        self.view.sig_eliminar_video.connect(self.delete_video)
        


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
        



    
    