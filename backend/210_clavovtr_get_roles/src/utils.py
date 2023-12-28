def element_to_json(data):
    new_data = []
    for element in data:
        new_data.append({
            "id": element[0],
            "rol": element[1]
        })
    return new_data