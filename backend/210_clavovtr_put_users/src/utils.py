from src.database import get_user_data, update_data_users,update_empresa_contact_center

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

def compare_data(data_event, data_user_list):
    if all(user_value == data_event[key] for key, user_value in zip(['nombre', 'apellidos', 'email', 'contact_center', 'activo'], data_user_list[0][3:8])):
        print("Los datos son iguales.")
        return False
    else:
        print("Los datos son diferentes.")
        return True
    
def update_different_keys(data_user_list, new_data,user_id = None, id_contact_center = None ):
    contact_center = ['contact_center']
    usuario = ['nombre', 'apellidos', 'email', 'activo']
    result_contact_center = ""
    result_user = ""
    user_tuple = data_user_list[0]
    list_data = []
    list_contact_center = []
    list_user = []
    for key, user_value in zip(['nombre', 'apellidos', 'email', 'contact_center', 'activo'], user_tuple[3:8]):
        if user_value != new_data[key]:
            list_data.append({
                "key": key,
                "value":new_data[key]
            })
    for list in list_data:

        if list['key'] in usuario:
            list_user.append({
                "key": list['key'],
                "value":list['value']
            })
        elif list['key'] in contact_center:
            list_contact_center.append({
                "key": list['key'],
                "value":list['value']
            })
    
    if len(list_user) >0:
        result_user = update_data_users(list_user, user_id)
    if len(list_contact_center) > 0:
        result_contact_center = update_empresa_contact_center(list_contact_center, id_contact_center)
    
    result = ""
    if result_user:
        result = f"Tabla usuario {result_user} "
    if result_contact_center :
        if result_user:
            result = result + f"/ Tabla contact Center {result_contact_center}"
        else:
            result = f"Tabla contact Center {result_contact_center}"
        
        
    return result