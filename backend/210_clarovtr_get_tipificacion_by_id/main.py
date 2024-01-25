import json
from src.utils import element_to_json
from src.database import get_tipificacion_by_id


def run(event, context):
    uid = event["uid"]
    tipificacion_id = event["id"]
    data_tipificaciones = get_tipificacion_by_id(uid, tipificacion_id)
    print(f"data_tipificaciones {data_tipificaciones}")
    if data_tipificaciones and len(data_tipificaciones) > 0:
        return {
            "statusCode": 200,
            "tipificaciones": element_to_json(data_tipificaciones),
        }
    else:
        return {
            "statusCode": 204,
            "tipificaciones": json.dumps("Sin contenido"),
            "error": "sin datos que mostrar",
        }
