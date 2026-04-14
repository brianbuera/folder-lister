
def sort_by_name(videos):
    return sorted(videos, key=lambda x: x.nombre)

def sort_by_time(videos):
    return sorted(videos, key=lambda x: x.hora_fecha)
    
    
strategies = {
    "nombre": sort_by_name,
    "horario": sort_by_time
}