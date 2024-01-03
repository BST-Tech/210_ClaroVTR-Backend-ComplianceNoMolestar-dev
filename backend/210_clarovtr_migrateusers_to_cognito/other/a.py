import json
import boto3
import hashlib
import os
from src.secret_manager import get_value_secret

# Configura las credenciales de AWS
aws_region = 'us-east-1'
user_pool_id = 'us-west-2_SnKj7iUB0'
client_id = 'pbpv36ke75ve7ckd4tf158haf'



def create_user_on_userpool(client, username, password, name , family_name):

    response = client.admin_create_user(
    UserPoolId=user_pool_id,
    Username=username,
    TemporaryPassword=password,
    UserAttributes=[
        {'Name': 'email', 'Value': username},
        {'Name': 'email_verified', 'Value': 'true'},
        {'Name': 'name', 'Value': name},
        {'Name': 'family_name', 'Value': family_name}
    ])
    # Establecer la contraseña permanente y confirmar al usuario
    auth_response = client.admin_initiate_auth(
        UserPoolId=user_pool_id,
        ClientId=client_id,
        AuthFlow='ADMIN_NO_SRP_AUTH',
        AuthParameters={
            'USERNAME': username,
            'PASSWORD': password
        }
    )
    print(auth_response)
    if auth_response['ChallengeName'] == 'NEW_PASSWORD_REQUIRED':
        client.admin_respond_to_auth_challenge(
            UserPoolId=user_pool_id,
            ClientId=client_id,
            ChallengeName='NEW_PASSWORD_REQUIRED',
            ChallengeResponses={
                'USERNAME': username,
                'NEW_PASSWORD': password
            },
            Session=auth_response['Session']
        )

    return {
                'statusCode': 200,
                'body': json.dumps('User migrated and password set: ' + username)
            }



def simple_hash(password):
    # Supongamos que la función simpleHash utiliza MD5 como en tu ejemplo de JavaScript
    hashed_password = hashlib.md5(password.encode()).hexdigest()
    return hashed_password


def lambda_handler(event, context):
    #secretValue = get_value_secret()
    #print(secretValue)
    client = boto3.client('cognito-idp', region_name=os.getenv('COGNITO_REGION_NAME'))
    username = event['username']
    password = event['password']
    family_name = event['family_name']
    name = event['name']

    try:
        # Comprueba si el usuario existe en el User Pool usando admin_get_user
        response = client.admin_get_user(
            UserPoolId=user_pool_id,
            Username=username
        )
        print(response)
       # El usuario existe en el User Pool, por lo que indicamos que no se debe volver a intentar el inicio de sesión
        print("User exists in User Pool so no migration:", username)
        return "NO_RETRY"

    except client.exceptions.UserNotFoundException:
        # El usuario no existe en el User Pool, intenta la migración
        print("User does not exist in User Pool, attempting migration:", username)
        try:
            create_user_on_userpool(client, username, password, name , family_name)
        except Exception as e:
            print("Failed to create migrating user in User Pool: " + username)
            return {
                'statusCode': 500,
                'body': json.dumps('Failed to create migrating user: ' + str(e))
            }

    except Exception as e:
        # Manejar otras excepciones según sea necesario
        print("An error occurred:", str(e))
        raise e
