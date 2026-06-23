
from ..config.config_manager import config
from pathlib import Path


class Controller:

    config_manager = config
    
    def __init__(self, service, view):
        self.service = service
        self.view = view
        

    def iniciar_app(self):
        self.view.show()

    def seleccionar_directorio(self, directorio : str):
        directorio =  list(Path(directorio).rglob("*.mkv"))
        return self.service.create_videos(directorio)


    
    