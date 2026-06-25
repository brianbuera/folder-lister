
from ..config.config_manager import config


class FolderListerController:

    config_manager = config
    
    def __init__(self, video_service, view, player_controller):

        self.video_service = video_service
        self.view = view
        self.player_controller = player_controller
        self._connect_signal()


    def _connect_signal(self):
        self.view.sig_importar_videos.connect(self.seleccionar_directorio)
        self.view.sig_eliminar_video.connect(self.delete_video)
        self.view.sig_ordenar_por_hora.connect(self.ordenar_por_horario)
        self.view.sig_ver_video.connect(self.player_controller.load_video)


    def start_app(self):
        self.view.show()


    def seleccionar_directorio(self, directorio : str):
        print(f"Carpeta recibida: {directorio}")
        videos_creados, videos_duplicados = self.video_service.create_videos(directorio)
        videos = self.video_service.get_videos()
        self.view.update_table_data(videos)
        if videos_duplicados:
            print(f"Se omitieron {len(videos_duplicados)} videos duplicados")
            self.view.show_warning_message(
                "Videos duplicados",
                f"Se omitieron {len(videos_duplicados)} videos porque ya estaban cargados."
                )


    def delete_video(self, id : int):
        video = self.video_service.search_video_by_id(id)
        was_current = self.player_controller.is_current_video(video)
        self.video_service.delete_by_id(id)
        videos = self.video_service.get_videos()
        self.view.update_table_data(videos)
        if was_current:
            self.player_controller.reset_player()
    

    def ordenar_por_horario(self):
        videos = self.video_service.sort_by_time()
        self.view.update_table_data(videos)


        

    