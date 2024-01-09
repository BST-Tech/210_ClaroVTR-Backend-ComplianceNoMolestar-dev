from src.database import get_rol_user, put_regla_negocio
from shared.cognito import get_user_by_id
from shared.secret_manager import get_value_secret

def run(event, context):
    uid = event['uid']
    regla_id = event['regla']['id']
    data_to_process = event['regla']
    email_user = get_user_by_id(uid)
    rol = get_rol_user(email_user)
    secret_value = get_value_secret()
    roles_admin = secret_value.get('USERS_ADMIN')
    
    if rol in roles_admin:
        regla_updated = put_regla_negocio(data_to_process, regla_id, email_user)
        if len(regla_updated) > 0:
            return {
                    'statusCode': 200,
                    'message': "Regla Actualizada correctamente",
                    'regla': data_to_process,
                
            }
        else:
            return {
                    'statusCode': 204,
                    'error': 'Error al actualizar los datos'
            }