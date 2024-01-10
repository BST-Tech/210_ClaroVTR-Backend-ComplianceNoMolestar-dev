import json
from shared.cognito import get_user_by_id,validate_exist_on_cognito,create_user_cognito
from shared.secret_manager import get_value_secret
from src.database import create_user, create_perfil_usuario, get_id_ct,get_rol_user

def run(event, context):
    """
    The function `run` processes data, checks user roles, creates a user and profile, and creates a user
    in Cognito if the user does not already exist.
    
    :param event: The `event` parameter is a dictionary that contains the data passed to the function
    when it is invoked. It is assumed to have the following structure:
    :param context: The `context` parameter is an object that provides information about the runtime
    environment of the function. It includes details such as the AWS request ID, function name, and
    function version. This parameter is typically not used in the code you provided, but it can be
    useful for accessing additional information about the execution
    :return: The code is returning a dictionary with different key-value pairs depending on the
    conditions met in the code.
    """
    data_to_process = event['data']
    rol = get_rol_user(get_user_by_id(event['uid']))
    secret_value = get_value_secret()
    roles_admin = secret_value.get('USERS_ADMIN')
    email_new_user = data_to_process.get('email')
    if rol in roles_admin:
        user_id = create_user(data_to_process)
        result = create_perfil_usuario(data_to_process, user_id, data_to_process.get('contactCenter'))
        if result == "Insertado correctamente":
            if validate_exist_on_cognito(email_new_user,secret_value):
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