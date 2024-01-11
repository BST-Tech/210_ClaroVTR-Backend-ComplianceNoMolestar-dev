from src.database import get_regla_by_id
from src.utils import element_to_json

def run(event, context):
    uid = event['uid']
    regla_id = event['regla']['id']
    
    result_reglas = get_regla_by_id(uid,regla_id)
    if len(result_reglas) > 0:
        return {
                'statusCode': 200,
                'regla': element_to_json(result_reglas),
            
        }
    else:
        return {
                'statusCode': 204,
                'error': 'sin datos que mostrar'
        }