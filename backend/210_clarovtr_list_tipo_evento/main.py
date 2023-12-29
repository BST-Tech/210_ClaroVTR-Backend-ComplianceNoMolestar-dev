import json
from src.database import list_tipo_evento
from shared.utils import list_data_to_json

def run(event, context):
    uid = event['uid']
    data_tipo_evento = list_tipo_evento(uid)
    if len(data_tipo_evento) > 0:
        return {
                'statusCode': 200,
                'tipos_eventos': list_data_to_json(data_tipo_evento),
            
        }
    else:
        return {
                'statusCode': 204,
                'error': 'Sin datos que mostrar'
        }