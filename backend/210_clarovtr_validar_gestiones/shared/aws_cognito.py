import os

import boto3

from shared.secret_manager import get_value_secret
from shared.timeit import timeit


@timeit
def get_user_by_id(uid):
    testing_for_prod = True
    secret_values = get_value_secret()
    is_deployed = bool(os.environ.get("AWS_LAMBDA_FUNCTION_NAME"))
    if testing_for_prod and not is_deployed:
        session = boto3.Session(profile_name="uw2prod", region_name="us-west-2")
        client = session.client("cognito-idp")
    else:
        client = boto3.client("cognito-idp")

    user_data = client.admin_get_user(
        UserPoolId=secret_values["user_pool_id"],
        Username=uid,
    )
    return [
        value["Value"]
        for value in user_data["UserAttributes"]
        if value["Name"] == "email"
    ][0]
