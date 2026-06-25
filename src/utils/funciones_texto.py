import re


def obtener_numero_y_nombre(texto: str) -> str:
    return re.sub(r"^\d{1,4}\s*-\s*", "", texto)
