import boto3
from shared.secret_manager import get_value_secret

def get_user_by_id(uid):
    secret_values = get_value_secret()
    client = boto3.client('cognito-idp')
    user_data = client.admin_get_user(
        UserPoolId=secret_values['user_pool_id'],
        Username=uid,
        )
    return [value['Value'] for value in user_data['UserAttributes'] if value['Name'] == 'email'][0]

def change_passowrd_cognito(username, new_password, secret_value):
    client = boto3.client('cognito-idp')
    user_pool_id = secret_value['user_pool_id']
    print("cambiar contraseña")
    try:
        response = client.admin_set_user_password(
            UserPoolId=user_pool_id,
            Username=username,
            Password=new_password,
            Permanent=False
        )
        status_code_response = response.get('ResponseMetadata').get('HTTPStatusCode')
        if status_code_response == 200:
            return {
                "statusCode": status_code_response,
                "message": "Contraseña cambiada correctamente para usuario:  "
            }
    except Exception as e:
        return {
                "statusCode": 500,
                "message":  f"No se pudo cambiar la contraseña Error {e}"
            }
   
        

def validate_exist_on_cognito(username, secret_value):
    client = boto3.client('cognito-idp', region_name=secret_value['aws_region'])
    try:
        response = client.admin_get_user(
            UserPoolId=secret_value['user_pool_id'],
            Username=username
        )
        return True
    except client.exceptions.UserNotFoundException:
        return False
    except Exception as e:
        # Manejar otras excepciones según sea necesario
        print("Se ha producido un error:", str(e))
        raise e    
