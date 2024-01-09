import json
from src.secret_manager import get_value_secret
from src.cognito import create_user_on_userpool, validate_exist_on_cognito,authentication
from src.database import get_element_by_email

# def simple_hash(password):
#     return hashlib.md5(password.encode()).hexdigest()

def run(event, context):

    secret_value = get_value_secret()
    username = event['username']
    password = event['password']
    ### Verificar que los datos existan en la base de datos

    data = get_element_by_email(username, password)

    if data:
        print(data[0][0])
        print(data[0][1])

        name = data[0][0]
        family_name = data[0][1]
        result_cognito = validate_exist_on_cognito(username,secret_value)
        print(result_cognito)
        if result_cognito:
            return authentication(username, password, secret_value)
        else:
            try:
                create_user_on_userpool(username, password, name , family_name, secret_value)
            except Exception as e:
                print("No se ha podido crear el usuario de migración en el grupo de usuarios: " + username)
                print(str(e))
            return authentication(username, password,secret_value)
    else:
        return f"Usuario y/o contraseña erroneos o no esta autorizado"

