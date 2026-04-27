import win32com.client
from pathlib import Path


class PowerPointClient:

    def __init__(self):
        try:
            self.app = win32com.client.Dispatch("PowerPoint.Application")
            self.app.Visible = True
        except Exception as e:
            print(f"Error iniciando PowerPoint: {e}")

    #Abrir un proyecto pptx
    def open_presentacion(self, archivo):
        try:
            return self.app.Presentations.Open(
                archivo,
                WithWindow=True
            )
        except Exception as e:
            print(f"Error abriendo archivo: {e}")

    #cerrar proyecto pptx
    def close_presentation(self, presentation):
        try:
            if presentation:
                presentation.Close()
        except Exception as e:
            print(f"Error cerrando presentación: {e}")

    #Guardar proyecto
    def guardarComo(presentacion, destino : Path):
        presentacion.SaveAs(destino)
    
    #Cerrar Aplicacion
    def close_powerpoint_client(self):
        try:
            self.app.Quit()
            print("\nAplicación cerrada")
        except Exception as e:
            print(f"Error cerrando PowerPoint: {e}")

    def diapositiva_detalles(self, slide):
        for shape in slide.Shapes:
            print("-----")
            print("Nombre:", shape.Name)
            print("Tipo:", shape.Type)

            # TEXTO normal
            if shape.HasTextFrame:
                if shape.TextFrame.HasText:
                    print("Texto:", shape.TextFrame.TextRange.Text)

            # TABLA
            if shape.Type == 19:  # Tabla
                tabla = shape.Table
                
                filas = tabla.Rows.Count
                columnas = tabla.Columns.Count
                
                print(f"Tabla: {filas} filas x {columnas} columnas")

                for i in range(1, filas + 1):
                    for j in range(1, columnas + 1):
                        celda = tabla.Cell(i, j)
                        
                        texto = ""
                        if celda.Shape.HasTextFrame:
                            if celda.Shape.TextFrame.HasText:
                                texto = celda.Shape.TextFrame.TextRange.Text.strip()
                        
                        print(f"Fila {i}, Col {j}: {texto}")



            