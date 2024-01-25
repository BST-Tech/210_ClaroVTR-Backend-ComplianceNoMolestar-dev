def element_to_json(data):
    new_data = []
    for element in data:
        new_data.append(
            {
                "id": element[0],
                "tipificacion": element[1],
                "nombre_tipificacion": element[2],
                "contacto": element[3],
                "venta": element[4],
                "id_empresa_ct": element[5],
                "id_contactCenter": element[6],
            }
        )
    return new_data
