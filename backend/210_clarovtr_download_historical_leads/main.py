import json
from src.database import get_element_by_upload_code

def data_to_json(data):
    """
    The function `data_to_json` converts a list of data into a JSON format, extracting specific values
    from each element of the list.
    
    :param data: The parameter "data" is a list of values. Each value is expected to be a tuple with at
    least 9 elements. The elements in each tuple are expected to be in the following order:
    :return: a list of dictionaries. Each dictionary contains the following keys: "fecha", "pcs",
    "usuario", "en_cooler", and "en_no_molestar". The values for these keys are extracted from the input
    data.
    """
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

def data_response(data_result_upload_daily):
    """
    The function `data_response` takes a list of data results and returns a list of dictionaries
    containing the phone number to validate and the corresponding validation result.
    
    :param data_result_upload_daily: The parameter `data_result_upload_daily` is a list of lists. Each
    inner list represents a data result for a daily upload. The inner list contains the following
    elements:
    :return: a list of dictionaries. Each dictionary contains two key-value pairs: "TELEFONO A VALIDAR"
    which corresponds to the phone number being validated, and "RESULTADO VALIDACION" which corresponds
    to the result of the validation.
    """
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
    """
    The function checks if there is data associated with a given upload code and returns a response
    accordingly.
    
    :param event: The `event` parameter is a dictionary that contains the input data for the function.
    In this case, it is expected to have a key called `'codigo_carga'` which represents the upload code
    :param context: The `context` parameter is an object that provides information about the runtime
    environment of the function. It includes details such as the AWS request ID, function name, and
    other contextual information. In this code snippet, the `context` parameter is not used
    :return: The code is returning a JSON response with a status code and a body. If the length of the
    data is 0, it returns a status code of 204 and a body indicating "Sin contenido" (no content).
    Otherwise, it returns a status code of 200 and the response body is the result of the
    `data_response` function applied to the `data` variable.
    """
    data = get_element_by_upload_code(event['codigo_carga'])
    if len(data) == 0:
        return {
        'statusCode': 204,
        'body': json.dumps('Sin contenido')
        }
    else:
        return {
            'statusCode': 200,
            'body': data_response(data)
        }
