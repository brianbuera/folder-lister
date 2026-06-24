
from ..config.config_manager import config
from pathlib import Path


class FolderListerController:

    config_manager = config
    
    def __init__(self, service, view):
        self.service = service
        self.view = view
        self.view.controller = self
        self.view.sig_importar_videos.connect(self.seleccionar_directorio)
        

    def start_app(self):
        self.view.show()

    def seleccionar_directorio(self, directorio : str):
        print(f"Carpeta recibida: {directorio}")
        directorio =  list(Path(directorio).rglob("*.mkv"))
        videos = self.service.create_videos(directorio)
        self.view.update_table_data(videos)


    
    