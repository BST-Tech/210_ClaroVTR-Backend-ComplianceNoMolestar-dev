import json
from src.database import get_data_contact_center
from shared.cognito import get_user_by_id
from shared.utils import get_data_users_by_contact_center_to_json

def run(event, context):
    uid = event['uid']
    id_ct = event['data']['id']
    email = get_user_by_id(uid)
    
    result = get_data_contact_center(email, id_ct)
    
    if len(result) > 0:
        data ={
                'statusCode': 200,
                'data':  get_data_users_by_contact_center_to_json(result)
            
        }
        print(data)
        return data
    else:
        return {
                'statusCode': 204,
                'error': 'sin datos que mostrar'
        }