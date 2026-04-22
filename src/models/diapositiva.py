
class Diapositivas:
    @staticmethod
    def crearDiapositiva(presentacion, rutas_imagenes):
        # diapositiva original
        slide = presentacion.Slides(6)

        for i in rutas_imagenes:
            # crear duplicado
            duplicated = slide.Duplicate()

            # normalmente Duplicate devuelve una colección → agarramos la primera
            new_slide = duplicated.Item(1)


            shape = new_slide.Shapes.AddPicture(
                FileName=i,
                LinkToFile=False,
                SaveWithDocument=True,
                Left=0.57,   # posición horizontal
                Top=49.33,    # posición vertical
                Width=719.52,  # ancho
                Height=404.60 # alto
            )
            shape.ZOrder(1)