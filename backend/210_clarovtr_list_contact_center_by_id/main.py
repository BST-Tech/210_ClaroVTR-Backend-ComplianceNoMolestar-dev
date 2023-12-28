from shared.cognito import get_user_by_id
from shared.secret_manager import get_value_secret
from src.database import get_rol_user,get_list_contact_center
from src.utils import data_to_json

def run(event, context):
    uid = event['uid']
    email_user = get_user_by_id(uid)
    rol = get_rol_user(email_user)
    secret_value = get_value_secret()
    roles_admin = secret_value.get('USERS_ADMIN')
    id_ct = event['data']['id']
    
    if rol in roles_admin:
        list_data_contact_center = get_list_contact_center(uid, id_ct)
        print(f"list_data_contact_center {list_data_contact_center}")
        if len(list_data_contact_center) > 0:
            return {
                'uid': uid,
                'statusCode': 200,
                'data': data_to_json(list_data_contact_center)
            }
        else:
            return {
                        'statusCode': 204,
                        'error': "No existen datos que obtener"
                }
