import json
from src.utils import element_to_json
from src.database import get_tipificaciones_from_api

def run(event, context):
    uid = event['uid']
    data_tipificaciones = get_tipificaciones_from_api(uid)
    if len(data_tipificaciones) > 0:
        return {
                'statusCode': 200,
                'tipificaciones':element_to_json(data_tipificaciones)
            
        }
    else:
        return {
                'statusCode': 204,
                'tipificaciones':json.dumps('Sin contenido'),
                'error': 'sin datos que mostrar'
        }