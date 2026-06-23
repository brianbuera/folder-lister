import sys
import vlc

from PySide6.QtWidgets import QApplication, QMainWindow, QFrame, QVBoxLayout, QWidget, QPushButton, QFileDialog


class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("VLC en PySide6")
        self.resize(900, 600)

        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

        central = QWidget()
        layout = QVBoxLayout(central)

        self.video_frame = QFrame()
        self.video_frame.setStyleSheet("background: black;")
        layout.addWidget(self.video_frame)

        btn = QPushButton("Abrir video")
        btn.clicked.connect(self.abrir_video)
        layout.addWidget(btn)

        self.setCentralWidget(central)

    def abrir_video(self):
        ruta, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar video",
            "",
            "Videos (*.mp4 *.avi *.mkv *.mov)"
        )

        if ruta:
            media = self.instance.media_new(ruta)
            self.player.set_media(media)

            self.player.set_hwnd(int(self.video_frame.winId()))  # Windows

            self.player.play()


app = QApplication(sys.argv)
window = VideoPlayer()
window.show()
sys.exit(app.exec())