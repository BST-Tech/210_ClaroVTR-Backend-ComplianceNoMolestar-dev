import json
from src.database import get_data_contact_center
from shared.cognito import get_user_by_id
from shared.utils import get_data_users_by_contact_center_to_json

def run(event, context):
    """
    The function takes an event and context as input, retrieves user data based on the provided ID, and
    returns the data in JSON format if it exists, otherwise it returns an error message.
    
    :param event: The `event` parameter is a dictionary that contains the data passed to the function
    when it is triggered. It is used to pass information to the function
    :param context: The `context` parameter is an object that provides information about the runtime
    environment of the function. It includes details such as the AWS request ID, the function name, and
    the function version
    :return: The code is returning a dictionary with a 'statusCode' key and a 'data' key. If the length
    of the 'result' list is greater than 0, the 'data' key will contain the result of the
    'get_data_users_by_contact_center_to_json' function. If the length of the 'result' list is 0, the
    code will return a dictionary with a 'statusCode
    """
    email = get_user_by_id(event['uid'])
    result = get_data_contact_center(email, event['data']['id'])
    if len(result) > 0:
        data ={
                'statusCode': 200,
                'data':  get_data_users_by_contact_center_to_json(result)
            
        }
        return data
    else:
        return {
                'statusCode': 204,
                'error': 'sin datos que mostrar'
        }