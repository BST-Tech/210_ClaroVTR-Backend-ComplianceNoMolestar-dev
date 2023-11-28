def element_to_json(data):
    new_data = []
    for element in data:
        new_data.append({
            "id": element[0],
            "nombre": element[1],
            "apellido": element[2],
            "email": element[3],
            "contactCenter": element[4],
            "estado": element[5],
            "rol": element[6],
            "nombre_empresa": element[7]
        })
    return new_data
    