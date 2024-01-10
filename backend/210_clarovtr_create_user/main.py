import json
from shared.cognito import get_user_by_id,validate_exist_on_cognito,create_user_cognito
from shared.secret_manager import get_value_secret
from src.database import create_user, create_perfil_usuario,get_rol_user
from src.utils import get_numeric_value

def run(event, context):
    """
    The function `run` processes data to create a new user, validate their existence in Cognito, and
    create the user in Cognito if they don't already exist.
    
    :param event: The `event` parameter is a dictionary that contains the data passed to the function
    when it is invoked. It is expected to have the following keys:
    :param context: The `context` parameter is an object that provides information about the runtime
    environment of the function. It includes details such as the AWS request ID, function name, and
    other contextual information. In this code snippet, the `context` parameter is not used
    :return: The code returns a dictionary with the following keys and values:
    """
    data_to_process = event['data']
    rol = get_rol_user(get_user_by_id(event['uid']))
    secret_value = get_value_secret()
    roles_admin = secret_value.get('USERS_ADMIN')
    email_new_user = data_to_process.get('email')
    if rol in roles_admin:
        user_id = create_user(data_to_process)
        user_id = get_numeric_value(user_id)
        if user_id is not False:
            if isinstance(user_id,int):
                id_ct = data_to_process.get('contactCenter')
                result = create_perfil_usuario(data_to_process, user_id, id_ct)
                if result == "Insertado correctamente":
                    result_cognito = validate_exist_on_cognito(email_new_user,secret_value)
                    if result_cognito:
                        return {"statusCode": 201,"message":"Usuario ya existe en cognito, no se puede crear"}
                    else:
                        
                        result_create = create_user_cognito(data_to_process, secret_value)
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
        elif user_id is False:
            return {
                            'statusCode': 204,
                            'error': "Usuario ya existe en la base de datos"
                    }