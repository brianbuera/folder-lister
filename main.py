from src.service.video_service import VideoService
from src.service.caso_service import  CasoService
from src.repository.videosrepository import VideoRepository
from src.ui.interfaz_principal import InterfazPrincipal


if __name__ == "__main__":

    video_repository = VideoRepository()
    video_service = VideoService(video_repository)
    caso_service =  CasoService()
    root = InterfazPrincipal(video_service, caso_service)
    root.mainloop()


    

 



















