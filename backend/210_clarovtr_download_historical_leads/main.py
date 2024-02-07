import json
from src.database import get_data_by_upload, get_element_by_upload_code
import gzip
import base64


def data_to_json(data):
    result = []
    for value in data:
        fecha = value[6]
        result.append(
            {
                "fecha": fecha.strftime("%d-%m-%Y %H:%M"),
                "pcs": value[8],
                "usuario": value[1],
                "en_cooler": value[4],
                "en_no_molestar": value[5],
            }
        )
    return result


def data_response(data_result_upload_daily):
    results = []
    for data in data_result_upload_daily:
        validation_result = ""
        if data[4] == 0 and data[5] == 0:
            validation_result = "OK PARA LLAMAR"
        elif data[4] == 0 and data[5] == 1:
            validation_result = "NO LLAMAR - BLOQUEO TEMPORAL"
        elif data[4] == 1:
            validation_result = "NO LLAMAR - NO MOLESTAR"
        results.append(
            {"TELEFONO A VALIDAR": data[3], "RESULTADO VALIDACION": validation_result}
        )
    return results


def run(event, context):
    codigo_carga = event["codigo_carga"]
    data = get_element_by_upload_code(codigo_carga)

    if data and len(data) == 0:
        return {"statusCode": 204, "body": json.dumps("Sin contenido")}
    else:
        body = data_response(data)

        json_str = json.dumps(body)
        gzip_body = gzip.compress(json_str.encode("utf-8"))
        encoded_data = base64.b64encode(gzip_body).decode("utf-8")
        based_json = {"body": encoded_data}
        return {"statusCode": 200, "body": based_json}
