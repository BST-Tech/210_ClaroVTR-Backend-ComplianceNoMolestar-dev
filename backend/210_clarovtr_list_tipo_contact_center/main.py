import json
from src.database import get_tipo_contact_center
from shared.utils import list_data_to_json

def run(event, context):
    uid = event['uid']
    list_contact_center_type = get_tipo_contact_center(uid)
    if list_contact_center_type:
        return {
                'statusCode': 200,
                'tipo_contact_center': list_data_to_json(list_contact_center_type),
            
        }
    else:
        return {
                'statusCode': 204,
                'error': 'sin datos que mostrar'
        }