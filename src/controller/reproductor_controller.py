
from ..service.vlc_player import VlcPlayer


class PlayerController:

    def __init__(self, view, video_service):
        self.view = view
        self.video_service = video_service
        self.player = VlcPlayer(self.view.video_area)
        self.current_video = None
        self._connect_signals()

    def _connect_signals(self):
        self.view.sig_ver_video.connect(self.load_video)
        self.view.sig_play.connect(self.play)
        self.view.sig_pause.connect(self.pause)
        self.view.sig_stop.connect(self.stop)
        self.view.sig_seek.connect(self.seek)
        self.view.sig_volume.connect(self.set_volume)
        self.view.sig_speed_change.connect(self.set_speed)

    def load_video(self, row: int):
        video = self.video_service.search_video_by_id(row)

        self.current_video = video

        self.player.load(video.ruta)
        self.player.play()

        self.view.set_video_title(video.nombre)
        self.view.set_progress(0)
        self.view.set_current_time("00:00:00")

    def play(self):
        if self.current_video:
            self.player.play()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()
        self.view.set_progress(0)
        self.view.set_current_time("00:00:00")

    def seek(self, value: int):
        self.player.set_position_percent(value)

    def set_volume(self, value: int):
        self.player.set_volume(value)


    def set_speed(self, value: str):
        speed = float(value[:-1])
        self.player.set_speed(speed)
