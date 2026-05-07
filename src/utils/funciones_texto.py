import re

def cortar_desde_primera_letra(texto: str) -> str:
    match = re.search(r"[A-Za-zÁÉÍÓÚáéíóúÑñ]", texto)
    return texto[match.start():] if match else ""