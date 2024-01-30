from src.utils import compare_data, update_different_keys
from src.database import get_tipificacion_by_id


def run(event, context):
    uid = event["uid"]
    data_event = event["tipificacion"]
    tipificacion_id = data_event["id"]
    data_tipificacion = get_tipificacion_by_id(uid, tipificacion_id)
    print(f"data_event {data_event}")
    print(f"data_tipifiaccion {data_tipificacion}")
    data_updated = compare_data(data_event, data_tipificacion)
    if data_updated:
        result_update = update_different_keys(
            data_tipificacion, data_event, tipificacion_id
        )
        print(result_update)
        return {
            "statusCode": 200,
            # 'message': result_update,
            "data_updated": data_event,  # element_to_json(data_user_list)
        }
    else:
        return {"statusCode": 204, "error": "sin datos que actualizar"}


def main():
    tip = {
        "id": 168,
        "tipificacion": "TIP26B",
        "nombre_tipificacion": "asdfasdfasdfasdfasdfasf",
        "contacto": 0,
        "venta": 0,
        "id_empresa_ct": 26,
        "id_contactCenter": 4,
        "activo": 1,
    }

    data = {"uid": "1448a478-e0d1-70f9-e2d6-984ec0376f1f", "tipificacion": tip}
    print(run(data, None))


if __name__ == "__main__":
    main()
