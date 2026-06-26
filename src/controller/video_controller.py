
from src.controller.player_controller import PlayerController


class VideoController:

    
    def __init__(self, video_service, view):

        self.video_service = video_service
        self.view = view
        self.videos_table=self.view.page_videos.videos_table
        self.player_controller = PlayerController(self.view, self.video_service)
        self._connect_signal()


    def _connect_signal(self):
        self.view.sig_importar_videos.connect(self.seleccionar_directorio)
        self.videos_table.sig_eliminar_video.connect(self.delete_video)
        self.videos_table.sig_ordenar_por_hora.connect(self.ordenar_por_horario)
        self.videos_table.sig_ver_video.connect(self.player_controller.load_video)



    def seleccionar_directorio(self, directorio : str):
        print(f"Carpeta recibida: {directorio}")
        videos_creados, videos_duplicados = self.video_service.create_videos(directorio)
        videos = self.video_service.get_videos()
        self.videos_table.update_table_data(videos)
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
        self.videos_table.update_table_data(videos)
        if was_current:
            self.player_controller.reset_player()
    

    def ordenar_por_horario(self):
        videos = self.video_service.sort_by_time()
        self.videos_table.update_table_data(videos)


        

    