import unicodedata

def normalizar(texto):
    # elimina tildes y pasa a minúsculas
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return texto.lower()