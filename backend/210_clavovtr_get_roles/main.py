import json
from src.utils import element_to_json
from src.database import get_rol_user
from shared.cognito import get_user_by_id

def run(event, context):
    uid = event['uid']
    email = get_user_by_id(uid)
    rol = get_rol_user(email)
    
    if rol:
        return {
                'statusCode': 200,
                'data': element_to_json(rol)
            
        }
    else:
        return {
                'statusCode': 204,
                'error': 'sin datos que actualizar'
        }