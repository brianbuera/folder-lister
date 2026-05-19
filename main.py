from src.service import VideoService, CasoService
from src.repository import VideoRepository
from src.ui import ListaDeCamaras

if __name__ == "__main__":

    video_repository = VideoRepository()
    video_service = VideoService(video_repository)
    caso_service =  CasoService()
    root = ListaDeCamaras(video_service, caso_service)
    root.mainloop()

    

 



















