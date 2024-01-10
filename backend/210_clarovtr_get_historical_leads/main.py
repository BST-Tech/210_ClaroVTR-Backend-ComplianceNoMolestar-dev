import json
from src.database import get_data_resume
from datetime import datetime, timedelta, timezone

def data_to_json(data):
    result = []
    for value in data:
        fecha_utc =  datetime.strptime(value[0], "%d-%m-%Y %H:%M") 
        fecha_utc.replace(tzinfo=timezone.utc)
        local_time_chile = timezone(timedelta(hours=-3))
        fecha_chile = fecha_utc.astimezone(local_time_chile).strftime("%d-%m-%Y %H:%M")

        print(fecha_chile)
        
        result.append(
            {
                "fecha": fecha_chile,
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
    if not data or len(data) == 0:
        return {
        'statusCode': 204,
        'body': json.dumps('Sin contenido')
        }
    else:
        return {
            'statusCode': 200,
            'body': data_to_json(data)
        }
