from src.infrastructure.powerpoint_client import PowerPointClient
from src.utils.cm_point import cm


def rgb(r, g, b):
    return r + (g << 8) + (b << 16)


def crear_cuadro_hora(slide, _left, _top, hora):
        # Crear textbox
        shape = slide.Shapes.AddTextbox(
            Orientation=1,
            Left = cm(_left),
            Top = cm(_top),
            Width=cm(2.04),
            Height=cm(1.03)
        )
        shape.Fill.Visible = True
        shape.Fill.Solid()
        # Blanco, Fondo 1
        shape.Fill.ForeColor.ObjectThemeColor = 14
        
        horario = hora

        # Texto
        text_range = shape.TextFrame.TextRange
        text_range.Text = horario

        # Fuente
        font = text_range.Font
        font.Name = "Calibri"
        font.Size = 18
        font.Color.RGB = 0


def crear_btn_volver_mapa(slide, texto, mapa = None):
        # Crear textbox
        shape = slide.Shapes.AddShape(
            34,
            cm(21.1),
            cm(16.5),
            cm(2.33),
            cm(1.97)
        )
        shape.Fill.Visible = True
        shape.Fill.Solid()

        shape.Fill.ForeColor.RGB = 65535
        shape.Line.ForeColor.RGB = 0
        shape.Line.Weight = 2

        # Texto
        text_range = shape.TextFrame.TextRange
        text_range.Text = texto

        # Fuente
        font = text_range.Font
        font.Name = "Calibri"
        font.Size = 12
        font.Color.RGB = 0
        font.Bold = True

        if mapa:
             sub_address = f"{mapa.SlideID},{mapa.SlideIndex},{mapa.Name}"
             shape.ActionSettings(1).Hyperlink.SubAddress = sub_address
             


def agregar_encabezado(slide, caso, caratula, fecha, ubicacion):

    shape = slide.Shapes.AddTable(
    NumRows=2,
    NumColumns=2,
    Left=cm(0.01),
    Top=cm(-0.08),
    Width=cm(25.39),
    Height=cm(1.82)
)
    shape.Left = cm(0.01)
    shape.Top = cm(-0.08)
    shape.Width = cm(25.39)
    shape.Height = cm(1.82)
    tabla = shape.Table

    tabla.Cell(1, 1).Shape.TextFrame.TextRange.Text = f"Caso Nº:{caso}"
    tabla.Cell(1, 2).Shape.TextFrame.TextRange.Text = f"Nombre del Caso: {caratula}"
    tabla.Cell(2, 1).Shape.TextFrame.TextRange.Text = f"Fecha: {fecha}"
    tabla.Cell(2, 2).Shape.TextFrame.TextRange.Text = f"Lugar del Hecho: {ubicacion}"
    tabla.Columns(1).Width = cm(6)
    tabla.Columns(2).Width = cm(19.39)

    for i in range(1, tabla.Rows.Count + 1):
        for j in range(1, tabla.Columns.Count + 1):
            celda = tabla.Cell(i, j)
            celda.Shape.Fill.Visible = True

            if i == 1:
                celda.Shape.fill.TwoColorGradient(1, 2)
                celda.Shape.fill.ForeColor.RGB = rgb(208,216,232)
                celda.Shape.fill.BackColor.RGB = rgb(150, 171, 148)

            else:
                celda.Shape.Fill.Solid()
                celda.Shape.Fill.ForeColor.RGB = rgb(208,216,232)
            for borde in range(1, 5):
                borde_actual = celda.Borders(borde)
                borde_actual.ForeColor.RGB = 0
                borde_actual.Weight = 1
            tf = celda.Shape.TextFrame
            tf.MarginLeft = cm(0.25)
            tf.MarginRight = cm(0.25)
            tf.MarginTop = cm(0.13)
            tf.MarginBottom = cm(0.13)

            # Ajustes de texto
            font = celda.Shape.TextFrame.TextRange.Font
            font.Name = "Calibri"
            font.Size = 15.5
            font.Bold = True
            font.Color.RGB = 0      # Negro





if __name__ == "__main__":
    print("App corriendo ...")

    pptx = PowerPointClient()
    presentacion = pptx.connect_presentation()

    slide = presentacion.Slides(7)
    mapa1 = presentacion.Slides(5)
    crear_cuadro_hora(slide, 0.26, 14.64, "01:08")
    crear_btn_volver_mapa(slide, "Mapa 1", mapa1)
    agregar_encabezado(slide, "4263", "Robo de motevehículo", "18/06/2026", "Chapearouge y Jujuy")
