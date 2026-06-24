import sys
import vlc


class VlcPlayer:
    def __init__(self, video_widget):
        self.video_widget = video_widget

        self.instance = vlc.Instance(
            "--quiet",
            "--no-video-title-show",
            "--avcodec-hw=none",
            "--verbose=-1"
        )

        self.player = self.instance.media_player_new()
        self._set_output_widget()

    def _set_output_widget(self):
        widget_id = int(self.video_widget.winId())

        if sys.platform.startswith("win"):
            self.player.set_hwnd(widget_id)
        elif sys.platform.startswith("linux"):
            self.player.set_xwindow(widget_id)
        elif sys.platform == "darwin":
            self.player.set_nsobject(widget_id)

    def load(self, path: str):
        self.stop()

        media = self.instance.media_new(path)
        self.player.set_media(media)

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def set_volume(self, value: int):
        self.player.audio_set_volume(value)

    def set_position_percent(self, value: int):
        self.player.set_position(value / 100)
    
    def set_speed(self, value: float):
        self.player.set_rate(value)