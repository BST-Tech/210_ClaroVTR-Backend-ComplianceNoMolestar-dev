import json
from src.utils import element_to_json, compare_data,update_different_keys
from src.database import get_user_data

def run(event, context):
    uid = event['uid']
    data_event = event['data']
    print(f"data_event {data_event}")
    perfil_user_id = data_event['id']
    data_user_list = get_user_data(uid,perfil_user_id)
    id_contact_center = data_user_list[0][2]
    user_id = data_user_list[0][1]
    print(user_id)
    print(f"id_contact_center {id_contact_center}" )
    print(f"data_user_list {data_user_list}")
    data_updated = compare_data(data_event, data_user_list)
    
    
    if data_updated:
        result_update = update_different_keys(data_user_list, data_event, user_id, id_contact_center)
        print(result_update)
        return {
                'statusCode': 200,
                'message': result_update,
                'data_updated': data_event #element_to_json(data_user_list)
            
        }
    else:
        return {
                'statusCode': 204,
                'error': 'sin datos que actualizar'
        }