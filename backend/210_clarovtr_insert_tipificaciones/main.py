import json
from src.utils import make_data_to_insert
from src.database import get_id_ct, insert_new_tipificaciones

def run(event, context):
    uid = event['uid']
    data_to_process = event['data']
    empresa_ct_id = get_id_ct(uid)[0][0]
    data_to_insert = make_data_to_insert(data_to_process, empresa_ct_id)
    result_insert = insert_new_tipificaciones(data_to_insert)
    print(f"result_insert {result_insert}")
    if result_insert is None:
        return {
                'statusCode': 200,
                'message': "Insertado correctamente",
                'data_updated': data_to_process
        }
    else:
        if "Error" in result_insert:
            return {
                    'statusCode': 204,
                    'error': result_insert
            }