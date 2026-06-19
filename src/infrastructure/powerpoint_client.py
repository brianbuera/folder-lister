import win32com.client
from pathlib import Path
import pythoncom
from ..utils import normalizar


class PowerPointClient:

    def __init__(self):
        try:
            # intenta conectar a instancia abierta
            self.app = win32com.client.GetActiveObject("PowerPoint.Application")

        except pythoncom.com_error:
            # si no existe, crea una nueva
            print("PowerPoint no está abierto.")
        

        self.app.Visible = True

    # Abrir presentación
    def open_presentacion(self, archivo, visible : bool = True):
        try:
            return self.app.Presentations.Open(archivo, WithWindow=visible)
        except Exception as e:
            print(f"Error abriendo archivo: {e}")
            return None

    # Conectar a presentación abierta
    def connect_presentation(self):
        try:
            pres = self.app.Presentations
            #nombre_buscado = normalizar("Presentación Análisis de Imagen.pptx")
            #for pres in self.app.Presentations:
            #    if normalizar(pres.Name) == nombre_buscado:
            #        return pres

            if len(pres)==1:
                print(f"Conectado a {pres[0].Name}")
                return pres[0]

            print("No se encontró la presentación abierta")
            return None

        except pythoncom.com_error as e:
            print(f"Error conectando: {e}")
            return None

    # Cerrar presentación
    def close_presentation(self, presentation):
        try:
            if presentation:
                presentation.Close()
        except Exception as e:
            print(f"Error cerrando presentación: {e}")

    # Guardar como
    def guardarComo(self, presentacion, destino: Path):
        try:
            presentacion.SaveAs(str(destino))
        except Exception as e:
            print(f"Error guardando: {e}")

    # Cerrar PowerPoint
    def close_powerpoint_client(self):
        try:
            self.app.Quit()
        except Exception as e:
            print(f"Error cerrando PowerPoint: {e}")




            