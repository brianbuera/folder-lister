import re

def cortar_desde_primera_letra(texto: str) -> str:
    match = re.search(r"[A-Za-zÁÉÍÓÚáéíóúÑñ]", texto)
    return texto[match.start():] if match else ""


class Diapositivas:

    @staticmethod
    
    def crearDiapositiva(presentacion, video):
        
        label = "Observaciones de la imagen:"

        valores = {
            "[hora]":video.hora_fecha.time().strftime("%H:%M"),
            "[ubicacion]": cortar_desde_primera_letra(video.nombre),
            "[observacion]": f"{label}\n{video.observacion}"
        }

        # diapositiva original
        slide = presentacion.Slides(6)
        # crear duplicado
        duplicated = slide.Duplicate()
        # normalmente Duplicate devuelve una colección → agarramos la primera
        new_slide = duplicated.Item(1)

        shape = new_slide.Shapes.AddPicture(
            FileName=video.ruta_screenshot,
            LinkToFile=False,
            SaveWithDocument=True,
            Left=0.28,   # posición horizontal
            Top=49.32,    # posición vertical
            Width=720.28,  # ancho
            Height=403.65 # alto
        )
        shape.ZOrder(1)

        for shape in new_slide.Shapes:
            if shape.Type == 17:
                if shape.TextFrame.TextRange.Text == "[hora]":
                    shape.TextFrame.TextRange.Text = valores["[hora]"]

                elif shape.TextFrame.TextRange.Text == "[observacion]":
                        tf = shape.TextFrame
                        tr = tf.TextRange
                        tr.Text = tr.Text.replace("[observacion]", f"{label}\n{video.observacion}")
                        # Usar TextRange con Start y Length en lugar de Characters
                        label_range = tf.TextRange.Characters(0, len(label))
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








