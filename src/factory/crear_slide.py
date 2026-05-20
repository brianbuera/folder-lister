from ..utils import cortar_desde_primera_letra
from ..utils import cm


class Diapositivas:

    @staticmethod
    
    def crearDiapositiva(template, caso_abierto, video):
        # diapositiva original
        slide = template.Slides(6)
        # copiar slide
        slide.Copy() 
        
          
        for diapositiva in video.diapositivas:

            valores = {
                "[hora]":video.hora_fecha.time().strftime("%H:%M"),
                "[ubicacion]": cortar_desde_primera_letra(video.nombre),
                "[observacion]": f"{diapositiva.observacion}"
            }

     

            new_slide = caso_abierto.Slides.Paste(Index=caso_abierto.Slides.Count)

            for screenshot in diapositiva.screenshots:
                shape = new_slide.Shapes.AddPicture(
                    FileName=screenshot.ruta,
                    LinkToFile=False,
                    SaveWithDocument=True,
                    Left=screenshot.x,   # posición horizontal
                    Top=screenshot.y,    # posición vertical

                )
                shape.LockAspectRatio = True
                shape.ZOrder(1)

            for shape in new_slide.Shapes:
                if shape.Type == 17:
                    if shape.TextFrame.TextRange.Text == "[hora]":
                        shape.TextFrame.TextRange.Text = valores["[hora]"]

                    elif shape.TextFrame.TextRange.Text == "[observacion]":
                            tf = shape.TextFrame
                            tr = tf.TextRange
                            tr.Text = tr.Text.replace("[observacion]", f"{diapositiva.observacion}")
                            # Usar TextRange con Start y Length en lugar de Characters
                            label_range = tf.TextRange.Characters(0, len("Observaciones de la imagen:"))
                            label_range.Font.Bold = True
                            print(label_range.Text)



                if shape.Type == 19:
                    tabla = shape.Table
                    for i in range(1, tabla.Rows.Count + 1):
                        for j in range(1, tabla.Columns.Count + 1):
                            celda = tabla.Cell(i, j)
                            if not (celda.Shape.HasTextFrame and celda.Shape.TextFrame.HasText):
                                continue

                            texto = celda.Shape.TextFrame.TextRange.Text
                            
                            # Si el texto está vacío, es celda secundaria de un merge → saltar
                            if not texto.strip():
                                continue

                            # Reemplazar placeholders simples
                            for key in ("[hora]", "[ubicacion]"):
                                texto = texto.replace(key, str(valores[key]))
                            celda.Shape.TextFrame.TextRange.Text = texto

            

    def crear_cuadro_hora(self, slide, hora: str, posicion: dict):
        # Crear textbox
        shape = slide.Shapes.AddTextbox(
            Orientation=1,
            Left=posicion["x"],
            Top=posicion["y"],
            Width=cm(2.04),
            Height=cm(1.03)
        )

        # Texto
        text_range = shape.TextFrame.TextRange
        text_range.Text = hora

        # Fuente
        font = text_range.Font
        font.Name = "Calibri"
        font.Size = 18
        font.Bold = True
        font.Color.ObjectThemeColor = 14

            




