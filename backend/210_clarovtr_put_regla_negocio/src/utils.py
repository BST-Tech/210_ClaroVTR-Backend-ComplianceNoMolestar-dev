def element_to_json(data):
    new_data = []
    for element in data:
        new_data.append({
            "id": element[0],
            "nombre": element[1],
            "rango_fecha": element[2],
            "incidencias": element[3],
            "dias_cooler": element[4],
            "activo": element[5]
        })
    return new_data
    