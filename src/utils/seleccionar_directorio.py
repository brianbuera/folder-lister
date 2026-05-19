
from tkinter import filedialog, messagebox
from pathlib import Path
from ..validators import ValidadorRutasVideos



def seleccionarDirectorio():

    directorio : Path = Path(filedialog.askdirectory())

    if not directorio != "":
        return
           
    if not any(directorio.iterdir()):
        messagebox.showerror("Directorio vacio","El directorio se encuentra vacio")
        return
    
    videos = list(directorio.rglob("*.mkv"))

    if not videos:
        messagebox.showerror("No hay videos","El directorio no contiene videos")
        return

    validado = ValidadorRutasVideos.validar(videos)

    if validado:
        messagebox.showerror("Videos Invalidos", f"Ocurrio un problema al seleccionar el directorio: \n".join(validado))
        return 
    
    return directorio
   