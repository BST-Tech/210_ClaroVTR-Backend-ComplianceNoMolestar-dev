import json
import re
from src.database import insert_leads, get_data_user,get_element_by_upload_code,update_resumen_lead_carga
from shared.aws_cognito import get_user_by_id
from shared.utils import generate_load_code_id

def validate_pcs(pcs):
    pattern = r'^\d{8,}$'
    if re.match(pattern, pcs):
        return True
    else:
        return False

def data_response(data_result_upload_daily):
    results = []
    for data in data_result_upload_daily:
        validation_result = ""
        if data[4] == 0 and data[5] == 0:
            validation_result = "OK PARA LLAMAR"
        elif data[4] == 1 and data[5] == 0:
            validation_result = "NO LLAMAR - NO MOLESTAR"
        elif data[4] == 0 and data[5] == 1:
            validation_result = "NO LLAMAR - BLOQUEO TEMPORAL"
        results.append({
            "TELEFONO A VALIDAR": data[3],
            "RESULTADO VALIDACION": validation_result
        }
        )
    return results

def run(event, context):
    data_from_event = event['TELEFONO A VALIDAR']
    data_user = get_user_by_id(event['uid'])
    id_canal = event['id_canal']
    id_code_uploads = generate_load_code_id()
    pcs_data_to_storage = []
    user_data_db = get_data_user(data_user)
    print(user_data_db)
    print(f"user_data_db {user_data_db}")
    error = False
    errors = []
    for pcs in data_from_event:
        if validate_pcs(pcs):
            pcs_data_to_storage.append((user_data_db[0][1],int(id_canal),user_data_db[0][0],pcs[-9:], id_code_uploads))
        else:
            error = True
            errors.append({
                "pcs": pcs,
                "error": "PCS no cumple con las reglas de negocio"
            })
            print("PCS con error")
    insert_leads(pcs_data_to_storage)
    update_resumen_lead_carga(id_code_uploads)
    
    data_result_upload_daily= get_element_by_upload_code(id_code_uploads)
    if not error:
        return {
            'statusCode': 200,
            'upload_code': id_code_uploads,
            'message': "Archivo cargado correctamente",
            'body': data_response(data_result_upload_daily)
        }
    else:
        return {
            'statusCode': 500,
            'errors': errors
        }


