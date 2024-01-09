import json
from src.database import get_empresa_ct, delete_data_tipificaciones

def run(event, context):
    uid = event['uid']
    data_event = event['data']
    print(f"data_event {data_event}")
    tipificacion_id = data_event['id']
    id_contact_center = get_empresa_ct(uid)[0][0]
    print(tipificacion_id)
    print(f"id_contact_center {id_contact_center}" )
    # data_updated = compare_data(data_event, data_user_list)
    
    
    if id_contact_center:
        result_update = delete_data_tipificaciones(tipificacion_id, id_contact_center)
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