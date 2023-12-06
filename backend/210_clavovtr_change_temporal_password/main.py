import json
from src.database import get_rol_user, get_user_data_email
from shared.cognito import get_user_by_id, change_passowrd_cognito, validate_exist_on_cognito
from shared.secret_manager import get_value_secret
from src.utils import validate_password


def run(event, context):
    roles_admin = ['ADMIN_TELCOM']
    uid = event['uid']
    data_event = event['data']
    print(f"data_event {data_event}")
    email_user = get_user_by_id(uid)
    rol = get_rol_user(email_user)
    user_id = data_event['id']
    secret_value = get_value_secret()
    new_password = data_event['new_password']
    validate_pass = validate_password(new_password)
    print(validate_pass)
    if validate_pass:
        if rol in roles_admin:
            print("si puede cambiar la clave")
            email_to_change = get_user_data_email(user_id)
            print(email_to_change)
            if email_to_change:
                result_cognito = validate_exist_on_cognito(email_to_change,secret_value)
                if result_cognito:
                    print("usuario existe en cognito")
                    result = change_passowrd_cognito(email_to_change,new_password, secret_value)
                    if result.get('statusCode') == 200:
                        return {
                            'statusCode': 200,
                            'message': f"{result.get('message')}{email_to_change}",
                            'data':data_event
                        }
                    else:
                        return {
                    'statusCode': result.get('statusCode'),
                    'error': result.get('message')
            }
                else:
                    return {
                    'statusCode': 204,
                    'error': 'Usuario no existe en cognito'
            }
            else:
                return {
                    'statusCode': 204,
                    'error': 'Correo de usuario no existe en la base de datos'
            }
        else:
            return {
                    'statusCode': 204,
                    'error': 'Usuario no autorizado'
            }
    else:
        return {
                    'statusCode': 204,
                    'error': 'Contraseña no cumple con los requisitos minimos requeridos'
            }

