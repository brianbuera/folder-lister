from datetime import datetime

#Obtiene por parametro el nombre de un video en (ejemplo: 29_10_2025 14_31_20 (UTC-03_00).mp4)
#Devuelve un datetime a partir del nombre del video
def obtenerHorario(video):
    fecha_hora = video.split(" (")[0]
    dt = datetime.strptime(fecha_hora, "%d_%m_%Y %H_%M_%S") 
    return dt