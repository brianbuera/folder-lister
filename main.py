import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QColor, QPalette
from src.styles import Theme
from src.view import FolderListerView
from src.controller.folder_lister_controller import FolderListerController
from src.service.video_service import VideoService
# ════════════════════════════════════════════════════════════════════════
#  Punto de entrada para prueba visual rápida (sin Controlador ni Modelo)
# ════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    service = VideoService()

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window,          QColor(Theme.BG_DARK))
    palette.setColor(QPalette.ColorRole.WindowText,      QColor(Theme.TEXT_PRIMARY))
    palette.setColor(QPalette.ColorRole.Base,            QColor(Theme.BG_TABLE))
    palette.setColor(QPalette.ColorRole.AlternateBase,   QColor(Theme.BG_ROW_ALT))
    palette.setColor(QPalette.ColorRole.Text,            QColor(Theme.TEXT_PRIMARY))
    palette.setColor(QPalette.ColorRole.Button,          QColor(Theme.BG_CARD))
    palette.setColor(QPalette.ColorRole.ButtonText,      QColor(Theme.TEXT_PRIMARY))
    palette.setColor(QPalette.ColorRole.Highlight,       QColor(Theme.ACCENT_BLUE))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(Theme.TEXT_WHITE))
    app.setPalette(palette)

    window = FolderListerView()
    controller = FolderListerController(service, window)
    controller.start_app()
    sys.exit(app.exec())


    

 



















