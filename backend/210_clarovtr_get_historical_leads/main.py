import json
from src.database import get_data_resume
from datetime import datetime, timedelta, timezone

def data_to_json(data):
    """
    The function `data_to_json` converts a list of data into a JSON format, with specific formatting for
    the date and time values.
    
    :param data: The `data` parameter is a list of lists. Each inner list represents a row of data and
    contains the following elements:
    :return: a list of dictionaries. Each dictionary contains the following keys: "fecha", "usuario",
    "leads_validados", "leads_no_molestar", "leads_en_cooler", "leads_para_llamado", "codigo_carga", and
    "id_empresa_ct". The values for these keys are extracted from the input data and formatted
    accordingly.
    """
    result = []
    for value in data:
        fecha_utc =  datetime.strptime(value[0], "%d-%m-%Y %H:%M") 
        fecha_utc.replace(tzinfo=timezone.utc)
        local_time_chile = timezone(timedelta(hours=-3))
        fecha_chile = fecha_utc.astimezone(local_time_chile).strftime("%d-%m-%Y %H:%M")
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
    """
    The function checks if there is any data in the resume and returns a response with the appropriate
    status code and body.
    
    :param event: The `event` parameter is typically used to pass information about the triggering event
    to the function. It can contain various details such as the request headers, request body, path
    parameters, query parameters, etc. In this code snippet, the `event` parameter is not used, so it
    can be ignored
    :param context: The `context` parameter is an object that provides information about the runtime
    environment of the function. It includes details such as the AWS request ID, function name, and
    other metadata
    :return: The code is returning a dictionary with a 'statusCode' key and a 'body' key. The value of
    the 'statusCode' key is either 204 or 200, depending on the length of the data. The value of the
    'body' key is either a string 'Sin contenido' or the result of converting the data to JSON format.
    """
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
