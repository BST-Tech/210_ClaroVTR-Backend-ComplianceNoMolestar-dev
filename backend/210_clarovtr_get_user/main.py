import json
import re
import time
import datetime
from shared.database import get_users
from shared.utils import format_date_crud

def return_data(data):
    data = data[0]
    print(data)
    return {
        "id": data[0],
        "nombre": data[1],
        "apellidos": data[2],
        "email": data[3],
        "empresa": data[4],
        "estado": data[5],
        "perfil": data[6]}


def run(event, context):
    id_value = event['id']
    try:
        if id_value:
            results = get_users(id_value)
            return {
                'statusCode': 200,
                'message': "Datos obtenidos correctamente",
                'data': return_data(results)
            }
    except Exception:
        print("ha ocurrido un error")
