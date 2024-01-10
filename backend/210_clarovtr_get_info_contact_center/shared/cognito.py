import boto3
from shared.secret_manager import get_value_secret

def get_user_by_id(uid):
    """
    The function `get_user_by_id` retrieves the email of a user given their user ID using the AWS
    Cognito service.
    
    :param uid: The `uid` parameter is the unique identifier of the user you want to retrieve
    :return: The email value of the user with the given ID.
    """
    secret_values = get_value_secret()
    client = boto3.client('cognito-idp')
    user_data = client.admin_get_user(
        UserPoolId=secret_values['user_pool_id'],
        Username=uid,
        )
    return [value['Value'] for value in user_data['UserAttributes'] if value['Name'] == 'email'][0]