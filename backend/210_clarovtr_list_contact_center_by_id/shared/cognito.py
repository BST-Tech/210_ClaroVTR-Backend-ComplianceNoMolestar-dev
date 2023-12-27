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


def create_user_cognito(data,secret_value):
# def create_user_on_userpool(username, password, name , family_name, secret_value):
    name = data.get('nombre')
    email = data.get('email')
    family_name = data.get('apellido')
    password = secret_value.get('PASSWORD_TEMPORAL')
    client = boto3.client('cognito-idp', region_name=secret_value['aws_region'])
    try:
        response = client.admin_create_user(
        UserPoolId=secret_value['user_pool_id'],
        Username=email,
        TemporaryPassword=password,
        UserAttributes=[
            {'Name': 'email', 'Value': email},
            {'Name': 'email_verified', 'Value': 'true'},
            {'Name': 'name', 'Value': name},
            {'Name': 'family_name', 'Value': family_name}
        ])
        print("usuario creado")
        auth_response = client.admin_initiate_auth(
            UserPoolId=secret_value['user_pool_id'],
            ClientId= secret_value['CREATE_CLIENT_ID'],
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': email,
                'PASSWORD': password,
            }
        )
        if auth_response['ChallengeName'] == 'NEW_PASSWORD_REQUIRED':
            result = client.admin_respond_to_auth_challenge(
                UserPoolId=secret_value['user_pool_id'],
                ClientId= secret_value['CREATE_CLIENT_ID'],
                ChallengeName='NEW_PASSWORD_REQUIRED',
                ChallengeResponses={
                    'USERNAME': email,
                    'NEW_PASSWORD': password
                },
                Session=auth_response['Session']
            )
            
            return result.get('ResponseMetadata').get('HTTPStatusCode')
    except Exception as e:
        print("Se ha producido un error:", str(e))
        raise e  