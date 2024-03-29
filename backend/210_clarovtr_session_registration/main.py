import json
from src.database import get_data_contact_center
from shared.cognito import get_user_by_id

def run(event, context):
    uid = event['uid']
    id_ct = event['data']['id']
    email = get_user_by_id(uid)
    
    result = get_data_contact_center(email, id_ct)
    if result is not None:
        if len(result) > 0:
            data_result = {
                    'statusCode': 200,
                    'data': {
                        "last_conection" : result[3],
                        "leads_validados": result[4],
                        "last_upload_gestion": result[5]

                    }            }
            return data_result

        else:
            return {
                    'statusCode': 204,
                    'error': 'sin datos que mostrar'
            }
    else:
        return {
                'statusCode': 204,
                'error': 'sin datos que mostrar'
        }