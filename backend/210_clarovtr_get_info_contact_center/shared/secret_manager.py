import boto3
import json
import os


def get_value_secret():
    client = boto3.client("secretsmanager")
    secret_id = os.environ.get("SECRET_NAME", "dev/claroVtrNoMolestar")
    credentials = client.get_secret_value(SecretId=secret_id)
    return json.loads(credentials["SecretString"])
