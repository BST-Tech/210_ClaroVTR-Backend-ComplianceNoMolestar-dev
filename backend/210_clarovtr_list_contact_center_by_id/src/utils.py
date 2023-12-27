def data_to_json(data_list):
    data_to_dict = []
    for data in data_list:
        data_to_dict.append(
            {
                "id": data[0],
                "nombre":data[1],
                "razon_social":data[4],
                "rut":data[3],
                "tipo":data[2],
                "estado":data[5]
            }
        )
    print(data_to_dict)
    return data_to_dict