from ..domain.video import Video


def _to_dict(videos : list[Video])->list[dict]:
    list = []
    for v in videos:
        list.append({
                "nombre": v.nombre,
                "hora": v.hora,
                "fecha": v.fecha
                })
    return list