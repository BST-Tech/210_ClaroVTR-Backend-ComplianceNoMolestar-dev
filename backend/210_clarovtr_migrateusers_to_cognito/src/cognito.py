import os
import boto3
import botocore
import json

def authentication(username, password, secret_value):
    client = boto3.client('cognito-idp', region_name=secret_value['aws_region'])
    try:
        response = client.initiate_auth(
        ClientId=os.getenv('COGNITO_USER_CLIENT_ID'),
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': username,
            'PASSWORD': password
            
        })
        tokens ={
        'statusCode': response['ResponseMetadata']['HTTPStatusCode'],
        'IdToken': response['AuthenticationResult']['IdToken']
        }
    except client.exceptions.NotAuthorizedException as e:
        tokens = {
        'statusCode': 401,
        'error': 'Unauthorized'
        }
        
        return tokens
        
    return tokens

def create_user_on_userpool(username, password, name , family_name, secret_value):
    client = boto3.client('cognito-idp', region_name=secret_value['aws_region'])
    try:
        response = client.admin_create_user(
        UserPoolId=secret_value['user_pool_id'],
        Username=username,
        TemporaryPassword=password,
        UserAttributes=[
            {'Name': 'email', 'Value': username},
            {'Name': 'email_verified', 'Value': 'true'},
            {'Name': 'name', 'Value': name},
            {'Name': 'family_name', 'Value': family_name}
        ])
        print(response)
        # Establecer la contraseña permanente y confirmar al usuario
        auth_response = client.admin_initiate_auth(
            UserPoolId=secret_value['user_pool_id'],
            ClientId=secret_value['client_id'],
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            }
        )
        print(auth_response)
        if auth_response['ChallengeName'] == 'NEW_PASSWORD_REQUIRED':
            client.admin_respond_to_auth_challenge(
                UserPoolId=secret_value['user_pool_id'],
                ClientId=secret_value['client_id'],
                ChallengeName='NEW_PASSWORD_REQUIRED',
                ChallengeResponses={
                    'USERNAME': username,
                    'NEW_PASSWORD': password
                },
                Session=auth_response['Session']
            )
            return True
    except Exception as e:
        print("Se ha producido un error:", str(e))
        raise e  



def validate_exist_on_cognito(username, secret_value):
    client = boto3.client('cognito-idp', region_name=secret_value['aws_region'])
    try:
        response = client.admin_get_user(
            UserPoolId=secret_value['user_pool_id'],
            Username=username
        )
        print(response)
        print("El usuario existe en el grupo de usuarios, así que no hay migración:", username)
        return True
    except client.exceptions.UserNotFoundException:
        print("El usuario no existe en el pool de usuarios, intentando migración:", username)
        return False
    except Exception as e:
        # Manejar otras excepciones según sea necesario
        print("Se ha producido un error:", str(e))
        raise e    
    
    
    