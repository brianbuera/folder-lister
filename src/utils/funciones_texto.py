import re
def cortar_desde_primera_letra(texto: str) -> str:
    match = re.search(r"[A-Za-zÁÉÍÓÚáéíóúÑñ]", texto)
    return texto[match.start():] if match else ""

import re

def obtener_numero_y_nombre(texto: str) -> str:
    return re.sub(r"^\d{1,2}\s*-\s*", "", texto)
