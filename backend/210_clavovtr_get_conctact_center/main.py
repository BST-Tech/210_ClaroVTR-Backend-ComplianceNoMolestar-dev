import json
from src.utils import element_to_json
from src.database import get_contact_cernter_list

def run(event, context):
    uid = event['uid']
    data_user_list = get_contact_cernter_list(uid)
    if len(data_user_list) > 0:
        return {
                'statusCode': 200,
                'conctactCenters':element_to_json(data_user_list)
            
        }
    else:
        return {
                'statusCode': 204,
                'tipificaciones':json.dumps('Sin contenido'),
                'error': 'sin datos que mostrar'
        }