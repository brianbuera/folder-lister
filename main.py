from src.service import VideoService
from src.repository import VideoRepository
from src.ui import ListaDeCamaras

if __name__ == "__main__":

    repositorio = VideoRepository()
    service = VideoService(repositorio)
    root = ListaDeCamaras(service)
    root.mainloop()

    





















