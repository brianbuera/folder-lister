import configparser
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent.parent  # ajustá los niveles según tu estructura
CONFIG_FILE = BASE_DIR / "config.ini"
IMG_DIR = BASE_DIR / "img"
TEMPLATE_DIR = BASE_DIR / "templates"




class ConfigManager:
    def __init__(self):
        self._config = configparser.ConfigParser()
        self._path = CONFIG_FILE
        self._cargar()

    # =========================================================
    # CARGA / GUARDADO
    # =========================================================

    def _cargar(self):

        if self._path.exists():
            self._config.read(self._path)
            if self.ruta_destino:
               self.ruta_destino = "" 

        else:
            self._crear_config_default()
            self._guardar()



    def _crear_config_default(self):

        self._config["General"] = {
            "ruta_destino": "",
            "ruta_template": str(TEMPLATE_DIR / "template.pptx"),
        }

        self._config["Iconos"] = {
            "icono_next": str(IMG_DIR / "_next.png"),
            "icono_previous": str(IMG_DIR / "_previous.png"),
            "icono_video": str(IMG_DIR / "icon_video.png"),
        }

    def _guardar(self):
        try:
            with open(self._path, "w", encoding="utf-8") as file:
                self._config.write(file)
        except Exception as e:
            print(f"Error guardando configuración: {e}")

    # =========================================================
    # GETTER GENERICO
    # =========================================================

    def get(self, section: str, key: str, fallback=None):

        return self._config.get(
            section,
            key,
            fallback=fallback
        )

    # =========================================================
    # PROPIEDADES
    # =========================================================

    @property
    def ruta_destino(self) -> Path | None:
        valor = self.get("General", "ruta_destino", "")
        return Path(valor) if valor else None

    @ruta_destino.setter
    def ruta_destino(self, ruta: str | Path):

        self._config["General"]["ruta_destino"] = str(ruta)

        self._guardar()

    @property
    def ruta_template(self) -> Path:

        return Path(
            self.get(
                "General",
                "ruta_template",
                TEMPLATE_DIR / "template.pptx"
            )
        )

    @property
    def icono_next(self) -> Path:

        return Path(
            self.get(
                "Iconos",
                "icono_next",
                IMG_DIR / "_next.png"
            )
        )

    @property
    def icono_previous(self) -> Path:

        return Path(
            self.get(
                "Iconos",
                "icono_previous",
                IMG_DIR / "_previous.png"
            )
        )

    @property
    def icono_video(self) -> Path:

        return Path(
            self.get(
                "Iconos",
                "icono_video",
                IMG_DIR / "icon_video.png"
            )
        )


# =========================================================
# INSTANCIA GLOBAL
# =========================================================

config = ConfigManager()