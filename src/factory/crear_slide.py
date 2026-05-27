from ..utils import cortar_desde_primera_letra
from ..utils import cm
from ..config.config_manager import config

from os.path import relpath
from pathlib import Path


from pathlib import Path

def archivo_dentro_de_directorio(archivo, directorio):
    archivo = Path(archivo).resolve()
    directorio = Path(directorio).resolve()

    try:
        archivo.relative_to(directorio)
        return True
    except ValueError:
        return False


class Diapositivas:

    @staticmethod                     
    def crearDiapositiva(template, caso_abierto, video):
        ruta_ppt = Path(caso_abierto.FullName)

        # diapositiva original
        slide = template.Slides(6)
        # copiar slide
        slide.Copy() 
        
          
        for diapositiva in video.diapositivas:

            valores = {
                "[hora]":diapositiva.screenshots[0].hora.strftime("%H:%M"),
                "[ubicacion]": cortar_desde_primera_letra(video.nombre),
                "[observacion]": f"{diapositiva.observacion}"
            }

     

            new_slide = caso_abierto.Slides.Paste(Index=caso_abierto.Slides.Count)

            for idx, screenshot in enumerate(diapositiva.screenshots, 1):
                shape = new_slide.Shapes.AddPicture(
                    FileName=str(screenshot.ruta),
                    LinkToFile=False,
                    SaveWithDocument=True,
                    Left=screenshot.x,   # posición horizontal
                    Top=screenshot.y,    # posición vertical

                )
                shape.LockAspectRatio = True
                shape.ZOrder(1)


                Diapositivas.crear_cuadro_hora(new_slide,screenshot)
                #Agregar numero de screenshots cuando la diapositiva tenga varias capturas
                if diapositiva.cantidad_capturas > 1:
                    Diapositivas.crear_numero_captura(new_slide, screenshot, idx)

            #Agregar icono de video    
            if diapositiva == video.diapositivas[-1]:
                icon_video = Diapositivas.agregar_imagen(new_slide,config.icono_video,cm(23.13),cm(13.9))
                ruta_video = video.ruta_enumerada or video.ruta_inicial
                if archivo_dentro_de_directorio(ruta_video, ruta_ppt.parent):
                    ruta_relativa = relpath(ruta_video, ruta_ppt.parent)
                    # Hipervínculo al video MKV
                    icon_video.ActionSettings(1).Action = 7
                    icon_video.ActionSettings(1).Hyperlink.Address = str(ruta_relativa)


                
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
                diapositiva.id = new_slide.SlideID
        Diapositivas.agregar_flechas(caso_abierto, video)


    @staticmethod
    def crear_cuadro_hora(slide, screenshot):
        # Crear textbox
        shape = slide.Shapes.AddTextbox(
            Orientation=1,
            Left=screenshot.x + cm(0.26),
            Top=screenshot.y + cm(12.90),
            Width=cm(2.04),
            Height=cm(1.03)
        )
        shape.Fill.Visible = True
        shape.Fill.Solid()
        # Blanco, Fondo 1
        shape.Fill.ForeColor.ObjectThemeColor = 14
        
        horario = screenshot.hora_str()

        # Texto
        text_range = shape.TextFrame.TextRange
        text_range.Text = horario

        # Fuente
        font = text_range.Font
        font.Name = "Calibri"
        font.Size = 18
        font.Color.RGB = 0


    @staticmethod
    def crear_numero_captura(slide, screenshot, idx):
        # Crear textbox
        shape = slide.Shapes.AddTextbox(
            Orientation=1,
            Left=screenshot.x + cm(0.26),
            Top=screenshot.y,
            Width=cm(0.5),
            Height=cm(0.5)
        )
        shape.Fill.Visible = True
        shape.Fill.Solid()
        # Blanco, Fondo 1
        shape.Fill.ForeColor.ObjectThemeColor = 14
        shape.Line.Visible = True
        shape.Line.ForeColor.RGB = 0
        shape.Line.Weight = 1.5

        # Texto
        text_range = shape.TextFrame.TextRange
        text_range.Text = str(idx)
        # Centrar horizontal
        text_range.ParagraphFormat.Alignment = 2

        # Centrar vertical
        shape.TextFrame.VerticalAnchor = 3

        # Fuente
        font = text_range.Font
        font.Name = "Calibri"
        font.Size = 10
        font.Color.RGB = 0
        font.Bold = True
            



    @staticmethod
    def agregar_imagen(new_slide, path, x, y):

        shape = new_slide.Shapes.AddPicture(
                    FileName=str(path),
                    LinkToFile=False,
                    SaveWithDocument=True,
                    Left=x,   # posición horizontal
                    Top=y,    # posición vertical

                )
        shape.LockAspectRatio = True
        shape.ZOrder(4)

        return shape
    
    
    
    @staticmethod
    def agregar_flechas(caso_abierto, video):

        for idx, diapositiva in enumerate(video.diapositivas):

            if idx < video.total_diapositivas - 1:

                slide_actual = caso_abierto.Slides.FindBySlideID(diapositiva.id)
                slide_siguiente = caso_abierto.Slides.FindBySlideID(video.diapositivas[idx+1].id)
                icon_next = Diapositivas.agregar_imagen(slide_actual, config.icono_next, cm(23), cm(16.49))
                sub_address = f"{slide_siguiente.SlideID},{slide_siguiente.SlideIndex},{slide_siguiente.Name}"
                icon_next.ActionSettings(1).Hyperlink.SubAddress = sub_address
            
            if idx > 0:
                slide_actual = caso_abierto.Slides.FindBySlideID(diapositiva.id)
                slide_anterior = caso_abierto.Slides.FindBySlideID(video.diapositivas[idx-1].id)
                icon_next = Diapositivas.agregar_imagen(slide_actual, config.icono_previous, cm(21), cm(16.49))
                sub_address = f"{slide_anterior.SlideID},{slide_anterior.SlideIndex},{slide_anterior.Name}"
                icon_next.ActionSettings(1).Hyperlink.SubAddress = sub_address