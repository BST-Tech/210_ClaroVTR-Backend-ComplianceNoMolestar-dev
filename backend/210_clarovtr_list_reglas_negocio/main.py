from src.database import list_reglas
from src.utils import element_to_json

def run(event, context):
    uid = event['uid']
    result_reglas = list_reglas(uid)
    if len(result_reglas) > 0:
        return {
                'statusCode': 200,
                'reglas': element_to_json(result_reglas),
            
        }
    else:
        return {
                'statusCode': 204,
                'error': 'sin datos que mostrar'
        }