from src.database import delete_data_tipificaciones


def run(event, context):
    uid = event["uid"]
    data_event = event["data"]
    print(f"data_event {data_event}")
    tipificacion_id = data_event["id"]
    # id_contact_center = get_empresa_ct(uid)[0][0]
    print(tipificacion_id)
    # print(f"id_contact_center {id_contact_center}" )
    # data_updated = compare_data(data_event, data_user_list)

    result_update = delete_data_tipificaciones(tipificacion_id)
    if result_update and result_update.get("ok"):
        return {
            "statusCode": 200,
            "message": result_update.get("msg", "Ok"),
            "data_updated": data_event,
        }
    elif result_update:
        return {
            "statusCode": 204,
            "message": result_update.get("msg", "No se elimino"),
            "data_updated": data_event,
        }
    return {
        "statusCode": 500,
        "message": "Ocurrio un error al intentar eliminar la tipificacion.",
        "data_updated": None,
    }
