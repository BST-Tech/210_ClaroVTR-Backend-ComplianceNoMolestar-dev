def element_to_json(data):
    new_data = []
    for element in data:
        new_data.append(
            {
                "id": element[0],
                "nombre": element[1],
                "apellidos": element[2],
                "email": element[3],
                "contact_center_id": element[4],
                "estado": element[5],
                "id_rol": element[6],
                "rol": element[7],
                "nombre_contact_center": element[8],
                "nombre_empresa": element[9],
                "id_empresa_ct": element[10],
            }
        )
    return new_data
