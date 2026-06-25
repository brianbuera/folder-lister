
from ..service.vlc_player import VlcPlayer


class PlayerController:

    def __init__(self, view, video_service):
        self.view = view
        self.reproductor = self.view.reproductor
        self.video_service = video_service
        self.player = VlcPlayer(self.reproductor.video_area)
        self.current_video = None
        self._connect_signals()

    def _connect_signals(self):
        self.reproductor.sig_play.connect(self.play)
        self.reproductor.sig_pause.connect(self.pause)
        self.reproductor.sig_stop.connect(self.stop)
        self.reproductor.sig_seek.connect(self.seek)
        self.reproductor.sig_volume.connect(self.set_volume)
        self.reproductor.sig_speed_change.connect(self.set_speed)
        self.view.sig_nav_videos.connect(self.view.show_videos_page)
        self.view.sig_nav_diapositivas.connect(self.view.show_diapositivas_page)


    def load_video(self, row: int):
        video = self.video_service.search_video_by_id(row)

        self.current_video = video

        self.player.load(video.ruta)

        self.reproductor.set_camera_label(video.nombre)
        self.reproductor.set_progress(0)
        self.reproductor.set_current_time("00:00:00")

        self.play()

    def is_current_video(self, video) -> bool:
        if self.current_video is None:
            return False

        return self.current_video.ruta == video.ruta
    
    def play(self):
        if self.current_video:
            self.player.play()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()
        self.reproductor.set_progress(0)
        self.reproductor.set_current_time("00:00:00")

    def seek(self, value: int):
        self.player.set_position_percent(value)

    def set_volume(self, value: int):
        self.player.set_volume(value)


    def set_speed(self, value: str):
        speed = float(value[:-1])
        self.player.set_speed(speed)


    def reset_player(self):
        self.player.stop()
        self.current_video = None
        self.reproductor.reset_player_view()