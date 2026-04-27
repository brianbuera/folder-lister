
from tkinter import filedialog
from pathlib import Path
from .mensajes import *
from ..validators import ValidadorRutasVideos
from ..domains import RulesRutaVideo

def seleccionarDirectorio():
    directorio : Path = Path(filedialog.askdirectory())
    validador = ValidadorRutasVideos(RulesRutaVideo)

    if not directorio != Path("."):
        show_error(NO_SELECCIONADO)
        return

    if not any(directorio.iterdir()):
        show_error(VACIO)
        return

    validado = validador.validar(directorio.rglob("*.mkv"))
    if validado:
        print(validado)
        return 
    
    return directorio