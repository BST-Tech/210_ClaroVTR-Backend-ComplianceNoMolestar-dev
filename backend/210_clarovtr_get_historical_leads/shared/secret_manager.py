import boto3
import json
 
 
def get_value_secret():
    """
    The function `get_value_secret` retrieves a secret value from AWS Secrets Manager and returns it as
    a JSON object.
    :return: the value of the secret stored in AWS Secrets Manager with the SecretId
    "dev/claroVtrNoMolestar". The value is returned as a JSON object.
    """
    client = boto3.client('secretsmanager') 
    credentials = client.get_secret_value(
        SecretId = "dev/claroVtrNoMolestar"
    )
    return  json.loads( credentials['SecretString'] )