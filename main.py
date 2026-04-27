from src.service import VideoService, CasoService
from src.repository import VideoRepository
from src.ui import ListaDeCamaras

if __name__ == "__main__":

    repositorio = VideoRepository()
    service = VideoService(repositorio)
    caso_service =  CasoService()
    root = ListaDeCamaras(service, caso_service)
    root.mainloop()

    





















