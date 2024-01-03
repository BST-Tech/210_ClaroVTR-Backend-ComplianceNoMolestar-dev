import json
from shared.cognito import get_user_by_id
from shared.secret_manager import get_value_secret
from src.database import create_contact_center,get_rol_user, get_exist_contactcenter, create_empresa_contact_center

def run(event, context):
    uid = event['uid']
    data_to_process = event['data']
    email_user = get_user_by_id(uid)
    rol = get_rol_user(email_user)
    secret_value = get_value_secret()
    roles_admin = secret_value.get('USERS_ADMIN')
    if rol in roles_admin:
        valor = get_exist_contactcenter(data_to_process)
        if len(valor) > 0:
            return {
                        'statusCode': 204,
                        'error': "Rut de contact center ya existe"
                }
        id_new_contact_center = create_contact_center(data_to_process)
        new_empresa = create_empresa_contact_center(id_new_contact_center, data_to_process, email_user)
        if new_empresa == "Insertado correctamente":
            return {
                'statusCode': 200,
                'message': f"Empresa Contact center {data_to_process.get('nombre')}, creada correctamente",
                'data':data_to_process
            }
        else:
            return {
                        'statusCode': 204,
                        'error': new_empresa
            }