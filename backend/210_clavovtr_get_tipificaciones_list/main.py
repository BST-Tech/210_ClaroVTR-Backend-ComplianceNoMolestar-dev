import json
from src.utils import element_to_json
from src.database import get_tipificaciones_from_api, get_id_empresa_ct

def run(event, context):
    uid = event['uid']
    contact_center_id = event['data']['contact_center_id']
    if contact_center_id is None or contact_center_id == "":
        contact_center_id = get_id_empresa_ct(uid)
        
    data_tipificaciones = get_tipificaciones_from_api(uid,contact_center_id)
    print(data_tipificaciones)
    
    if data_tipificaciones is not None:
        return {
                'statusCode': 200,
                'tipificaciones':element_to_json(data_tipificaciones)
        }
    else:
        return {
                'statusCode': 204,
                'tipificaciones':None,
                'error': 'sin datos que mostrar'
        }