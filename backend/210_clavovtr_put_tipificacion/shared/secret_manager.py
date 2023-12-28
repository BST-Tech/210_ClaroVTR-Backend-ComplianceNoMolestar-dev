import boto3
import json
 
 
def get_value_secret():
    #https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html
    client = boto3.client('secretsmanager') 
    credentials = client.get_secret_value(
        SecretId = "dev/claroVtrNoMolestar"
    )
    secretDict = json.loads( credentials['SecretString'] )
    return  secretDict