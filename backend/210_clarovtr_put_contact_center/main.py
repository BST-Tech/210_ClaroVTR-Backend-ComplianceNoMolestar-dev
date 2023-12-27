import json
from shared.cognito import get_user_by_id
from shared.secret_manager import get_value_secret
from src.database import get_rol_user, put_empresa_contact_center

def run(event, context):
    uid = event['uid']
    id_ct = event.get('data').get('id')
    data_to_process = event['data']
    email_user = get_user_by_id(uid)
    rol = get_rol_user(email_user)
    secret_value = get_value_secret()
    roles_admin = secret_value.get('USERS_ADMIN')
    if rol in roles_admin:
        empresa_updated = put_empresa_contact_center(data_to_process, id_ct, email_user)
        if empresa_updated == "Actualizado correctamente":
            return {
                'statusCode': 200,
                'message': f"Empresa Contact center {data_to_process.get('nombre')}, actualizada Correctamente",
                'data':data_to_process
            }
        else:
            return {
                        'statusCode': 204,
                        'error': empresa_updated
            }