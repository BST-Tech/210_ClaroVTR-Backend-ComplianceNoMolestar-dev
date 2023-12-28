import json
from src.database import get_data_resume

def data_to_json(data):
    result = []
    for value in data:
        result.append(
            {
                "fecha": value[0],
                "usuario": value[1],
                "leads_validados": value[2],
                "leads_no_molestar": value[3],
                "leads_en_cooler": value[4],
                "leads_para_llamado": value[5],
                "codigo_carga": value[7],
                "id_empresa_ct": value[6]
            }
        )
    return result

def run(event, context):
    data = get_data_resume()
    if len(data) == 0:
        return {
        'statusCode': 204,
        'body': json.dumps('Sin contenido')
        }
    else:
        return {
            'statusCode': 200,
            'body': data_to_json(data)
        }
