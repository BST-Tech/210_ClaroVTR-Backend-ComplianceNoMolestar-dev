import json
import re
import time
import datetime
from shared.database import get_users
from shared.utils import format_date_crud

def return_data(data):
    print(data)
    data = data[0]
    return {
        "id": data[0],
        "nombre": data[1],
        "apellidos": data[2],
        "empresa": data[3],
        "email": data[4],
        "activo": data[5],
        "perfil": data[6],
        "created_at": format_date_crud(data[7]),
        "updated_at": format_date_crud(data[8])}


def run(event, context):
    id_value = event['id']
    try:
        if id_value:
            results = get_users(id_value)
            print(results)
            return {
                'statusCode': 200,
                'message': "Datos obtenidos correctamente",
                'data': return_data(results)
            }
    except Exception:
        print("ha ocurrido un error")
