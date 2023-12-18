import json
from src.database import update_last_login_user

def run(event, context):
    uid = event['uid']
    data_updated = update_last_login_user(uid)
    if data_updated:
        return {
                'statusCode': 200,
                'message': "Ultimo inicio de sesion registrado",
            
        }
    else:
        return {
                'statusCode': 204,
                'error': 'sin datos que actualizar'
        }