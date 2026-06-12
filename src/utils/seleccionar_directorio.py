from tkinter import Tk, filedialog, messagebox
from pathlib import Path
from ..validators.validador_rutas_videos import ValidadorRutasVideos




def seleccionarDirectorio():

    # Ventana temporal
    root = Tk()
    root.withdraw()

    # Siempre al frente
    root.attributes("-topmost", True)

    # Escritorio
    escritorio = Path.home() / "Desktop"

    directorio = filedialog.askdirectory(
        initialdir=escritorio,
        parent=root
    )

    root.destroy()

    if not directorio:
        return

    directorio = Path(directorio)


    return directorio




def seleccionarDirectorioVideos():
    directorio = seleccionarDirectorio()

    if not any(directorio.iterdir()):
        messagebox.showerror(
            "Directorio vacío",
            "El directorio se encuentra vacío"
        )
        return

    videos = list(directorio.rglob("*.mkv")) 
    if not videos:
        messagebox.showerror(
            "No hay videos",
            "El directorio no contiene videos"
        )
        return

    validado = ValidadorRutasVideos.validar(videos)

    if validado:
        messagebox.showerror(
            "Videos inválidos",
            "Ocurrió un problema al seleccionar el directorio:\n"
            + "\n".join(validado)
        )
        return

    return directorio



