import sys
from PySide6.QtWidgets import QApplication
from src.views.main_view import MainView
from src.controller.controller import Controller
from src.service.video_service import VideoService


def main():
    app = QApplication(sys.argv)
    service = VideoService()
    view = MainView(video_service=service)
    controller = Controller(service=service,view=view)
    view.controller = controller
    controller.iniciar_app()
    sys.exit(app.exec())



if __name__ == "__main__":

    print("App iniciando...")
    main()


    

 



















