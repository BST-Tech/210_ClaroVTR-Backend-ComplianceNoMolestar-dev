
def list_data_to_json(tipo_contact_center):
    data_result = []
    for tipo in tipo_contact_center:
        data_result.append({
            "id": int(tipo[0]),
            "tipo_operador":tipo[1]
        })
        
    return data_result