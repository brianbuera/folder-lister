import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QColor, QPalette

from src.styles import Theme
from src.view import MainView
from src.service.video_service import VideoService
from src.controller.video_controller import VideoController
from src.controller.nav_controller import NavController


def apply_theme(app: QApplication):
    """Aplica el estilo visual global de la aplicación."""

    app.setStyle("Fusion")

    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(Theme.BG_DARK))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(Theme.TEXT_PRIMARY))
    palette.setColor(QPalette.ColorRole.Base, QColor(Theme.BG_TABLE))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(Theme.BG_ROW_ALT))
    palette.setColor(QPalette.ColorRole.Text, QColor(Theme.TEXT_PRIMARY))
    palette.setColor(QPalette.ColorRole.Button, QColor(Theme.BG_CARD))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(Theme.TEXT_PRIMARY))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(Theme.ACCENT_BLUE))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(Theme.TEXT_WHITE))

    app.setPalette(palette)


def create_controllers(
    window: MainView,
    video_service: VideoService
) -> NavController:
    """Crea y conecta los controladores principales."""

    video_controller = VideoController(
        video_service=video_service,
        view=window
        )

    nav_controller = NavController(window, video_controller)

    return nav_controller


def main():
    app = QApplication(sys.argv)
    apply_theme(app)

    video_service = VideoService()
    window = MainView()

    nav_controller = create_controllers(
        window=window,
        video_service=video_service
    )

    nav_controller.start_app()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())


    

 



















