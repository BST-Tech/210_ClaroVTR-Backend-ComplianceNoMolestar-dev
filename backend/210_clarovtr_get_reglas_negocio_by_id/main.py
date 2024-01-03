from src.database import get_regla_by_id
from src.utils import element_to_json, modify_element

def run(event, context):
    uid = event['uid']
    regla_id = event['regla']['id']
    
    result_reglas = get_regla_by_id(uid, regla_id)
    
    if len(result_reglas) > 0:
        existing_element = element_to_json(result_reglas)[0]

        # Modificar el elemento existente sin proporcionar nuevos datos
        modified_element = modify_element(existing_element, {})

        return {
            'statusCode': 200,
            'regla': modified_element,
        }
    else:
        return {
            'statusCode': 204,
            'error': 'sin datos que mostrar'
        }