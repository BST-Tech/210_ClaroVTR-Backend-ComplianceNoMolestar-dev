import boto3
import json
import os


def get_value_secret():
    is_deployed = bool(os.environ.get("AWS_LAMBDA_FUNCTION_NAME"))
    testing_for_prod = True
    if is_deployed:
        client = boto3.client("secretsmanager")
        secret_id = os.environ.get("SECRET_NAME", "prod/claroVtrNoMolestar")
    elif testing_for_prod:
        session = boto3.Session(profile_name="uw2prod", region_name="us-west-2")
        client = session.client("secretsmanager")
        secret_id = "prod/claroVtrNoMolestar"
    else:
        client = boto3.client("secretsmanager")
        secret_id = "dev/claroVtrNoMolestar"

    credentials = client.get_secret_value(SecretId=secret_id)
    credentials = json.loads(credentials["SecretString"])

    return credentials
