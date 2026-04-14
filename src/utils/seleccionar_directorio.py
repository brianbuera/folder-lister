
from tkinter import filedialog
from pathlib import Path
from .mensajes import *
from .validador import validar_recien_exportados

def seleccionarDirectorio():
    directorio : Path = Path(filedialog.askdirectory())

    if not directorio != Path("."):
        show_error(NO_SELECCIONADO)
        return

    if not any(directorio.iterdir()):
        show_error(VACIO)
        return
    
    validado = validar_recien_exportados(directorio)
    if validado:
        show_error(validado)
        return 
    
    return directorio