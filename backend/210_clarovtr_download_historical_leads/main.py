import json
from src.database import get_data_by_upload

def data_to_json(data):
    result = []
    for value in data:
        fecha = value[6]
        result.append(
            {
                "fecha": fecha.strftime('%d-%m-%Y %H:%M'),
                "pcs": value[8],
                "usuario": value[1],
                "en_cooler": value[4],
                "en_no_molestar": value[5]
            }
        )
    return result

def run(event, context):
    codigo_carga = event['codigo_carga']
    data = get_data_by_upload(codigo_carga)
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
