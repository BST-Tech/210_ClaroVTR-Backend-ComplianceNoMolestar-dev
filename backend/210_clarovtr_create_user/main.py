import json
from shared.cognito import get_user_by_id,validate_exist_on_cognito,create_user_cognito
from shared.secret_manager import get_value_secret
from src.database import create_user, create_perfil_usuario, get_id_ct,get_rol_user

def run(event, context):
    uid = event['uid']
    data_to_process = event['data']
    email_user = get_user_by_id(uid)
    rol = get_rol_user(email_user)
    secret_value = get_value_secret()
    roles_admin = secret_value.get('USERS_ADMIN')
    email_new_user = data_to_process.get('email')
    if rol in roles_admin:
        user_id = create_user(data_to_process)
        id_ct = get_id_ct(uid)
        result = create_perfil_usuario(data_to_process, user_id, id_ct[0][0])
        
        
        if result == "Insertado correctamente":
            result_cognito = validate_exist_on_cognito(email_new_user,secret_value)
            if result_cognito:
                return {"statusCode": 201,"message":"Usuario ya existe en cognito, no se puede crear"}
            else:
                
                result_create = create_user_cognito(data_to_process, secret_value)
                print(result_create)
                if result_create == 200:
                    return {
                        'statusCode': 200,
                        'message': f"Usuario {email_new_user}, creado correctamente",
                        'data':data_to_process
                    }
                else:
                    return {
                'statusCode': result_create,
                'error': "Error en la creacion de usuario"
                }
        else:
            if "Error" in result:
                return {
                        'statusCode': 204,
                        'error': result
                }