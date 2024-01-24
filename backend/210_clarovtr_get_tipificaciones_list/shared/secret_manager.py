import boto3
import json
import os


def get_value_secret():
    dev = False
    if not os.environ.get("AWS_LAMBDA_FUNCTION_NAME") and not dev:
        session = boto3.Session(profile_name="uw2prod", region_name="us-west-2")
        client = session.client("secretsmanager")
        secret_id = "dev/claroVtrNoMolestar"
        secret_id = "prod/claroVtrNoMolestar"
    else:
        client = boto3.client("secretsmanager")
        secret_id = os.environ.get("SECRET_NAME", "dev/claroVtrNoMolestar")

    credentials = client.get_secret_value(SecretId=secret_id)
    credentials = json.loads(credentials["SecretString"])

    return credentials
