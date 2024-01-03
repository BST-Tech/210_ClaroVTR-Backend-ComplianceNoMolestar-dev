from src.database import update_data_tipificaciones

def compare_data(data_event, data_tipificacion_list):

    if all(user_value == data_event[key] for key, user_value in zip(['id', 'tipificacion', 'nombre_tipificacion', 'contacto', 'venta', 'activo'], data_tipificacion_list[0][:7])):
        print("Los datos son iguales.")
        return False
    else:
        print("Los datos son diferentes.")
        return True
    
def update_different_keys(data_tipificacion_list, new_data,tipificaciones_id):
    print("update_different_keys")
    tipificacion_tuple = data_tipificacion_list[0]
    list_data = []
    for key, user_value in zip(['id', 'tipificacion', 'nombre_tipificacion', 'contacto', 'venta', 'activo'], tipificacion_tuple[:7]):
        if user_value != new_data[key]:
            list_data.append({
                "key": key,
                "value":new_data[key]
            })
    
    if len(list_data) >0:
        result = update_data_tipificaciones(list_data, tipificaciones_id)
    
    return result