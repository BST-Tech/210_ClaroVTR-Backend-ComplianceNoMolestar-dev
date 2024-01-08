import boto3
from shared.secret_manager import get_value_secret


def get_user_by_id(uid):
    secret_values = get_value_secret()
    client = boto3.client("cognito-idp")
    try:
        user_data = client.admin_get_user(
            UserPoolId=secret_values["user_pool_id"],
            Username=uid,
        )
        return [
            value["Value"]
            for value in user_data["UserAttributes"]
            if value["Name"] == "email"
        ][0]

    except client.exceptions.UserNotFoundException:
        return None
    except Exception as e:
        # Manejar otras excepciones según sea necesario
        print("Se ha producido un error:", str(e))
        raise e
