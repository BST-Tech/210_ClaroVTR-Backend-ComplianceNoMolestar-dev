import boto3
import json

def get_value_secret():
    client = boto3.client('secretsmanager') 
    credentials = client.get_secret_value(
        SecretId = "prod/claroVtrNoMolestar"
    )
    return  json.loads( credentials['SecretString'] )