import configparser
from pathlib import Path

CONFIG_FILE = "config.ini"

class ConfigManager:
    def __init__(self):
        self._config = configparser.ConfigParser()
        self._path = Path(CONFIG_FILE)
        self._cargar()

    def _cargar(self):
        if self._path.exists():
            self._config.read(self._path)
        else:
            # valores por defecto
            self._config["General"] = {
                "ruta_destino": str(Path.home() / "Desktop"),
                "ruta_template" : str(Path.cwd()/"templates"/"template.pptx")
            }

    def get_ruta_destino(self) -> str:
        return self._config.get("General", "ruta_destino", fallback=str(Path.home() / "Desktop"))
    
    def get_ruta_template(self) -> str:
        return self._config.get("General", "ruta_template")

    def set_ruta_destino(self, ruta: str):
        self._config["General"]["ruta_destino"] = ruta
        self._guardar()

    def _guardar(self):
        with open(self._path, "w") as f:
            self._config.write(f)