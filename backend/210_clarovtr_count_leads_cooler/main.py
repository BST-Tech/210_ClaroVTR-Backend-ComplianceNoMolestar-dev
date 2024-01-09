import json
from src.utils import element_to_json
from src.database import get_leads_by_count

def run(event, context):
    try:
        uid = event['uid']
    except KeyError:
        return {
            'statusCode': 400,
            'error': 'El campo "uid" es obligatorio en la solicitud.'
        }

    data_leads_list = get_leads_by_count(uid)
    if len(data_leads_list) > 0:
        return {
            'statusCode': 200,
            'leads': element_to_json(data_leads_list)
        }
    else:
        return {
            'statusCode': 204,
            'leads': json.dumps('Sin contenido'),
            'error': 'sin datos que mostrar'
        }