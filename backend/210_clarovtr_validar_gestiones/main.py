import json
from datetime import datetime
from shared.timeit import timeit
import zlib
import base64

from src.database import (
    get_tipificaciones,
    insert_gestiones,
    get_data_user,
    insert_gestiones_alt,
    update_insert_resumen_lead_carga,
    update_carga_gestiones,
)
import time
from shared.aws_cognito import get_user_by_id
from shared.utils import (
    generate_load_gestion_code,
    format_date,
    validate_information,
    get_all_tipificaciones,
)


@timeit
def run(event, context):
    encoded_data = event["data"]
    decoded_data = base64.b64decode(encoded_data)
    decompressed_data = zlib.decompress(decoded_data, 16 + zlib.MAX_WBITS)
    event = json.loads(decompressed_data.decode("utf-8"))
    datas = event["data"]
    data_valid = []
    data_error = []
    error_tipificacion = []
    data_user = get_user_by_id(event["uid"])
    user_data_db = get_data_user(data_user)
    id_usuario = user_data_db[0][0]
    id_empresa_ct = user_data_db[0][1]
    id_empresa = user_data_db[0][2]
    id_canal = event.get("id_canal")
    codigo_carga = generate_load_gestion_code(id_empresa_ct)

    tipificaciones_list = list(get_all_tipificaciones(datas))
    tipificaciones = get_tipificaciones(tipificaciones_list, id_empresa_ct)

    new_tipificaciones_list = [tupla[0] for tupla in tipificaciones]
    start_time = time.perf_counter()
    for data in datas:
        value_return = validate_information(data, new_tipificaciones_list)
        if value_return["status"]:
            data_valid.append(
                (
                    data["cod_tipificacion"],
                    data["pcs_salida"][-9:],
                    data["pcs_cliente"][-9:],
                    format_date(data["fechallamada"]),
                    codigo_carga,
                    data["canal_o_nombre_EPS"],
                    data["campania"],
                    data["duracion_en_segundos"],
                    data["operador_id_ejecutivo"],
                    id_usuario,
                    id_empresa,
                    id_empresa_ct,
                    id_canal,
                )
            )

        elif not value_return["status"]:
            if "Tipificacion no existe o no encontrada" in value_return["errors"]:
                error_tipificacion.append(
                    {
                        "pcs": data["pcs_cliente"],
                        "tipificacion": data["cod_tipificacion"],
                    }
                )

            data_error.append(
                {
                    "canal_o_nombre_EPS": data["canal_o_nombre_EPS"],
                    "operador_id_ejecutivo": data["operador_id_ejecutivo"],
                    "pcs_salida": data["pcs_salida"],
                    "pcs_cliente": data["pcs_cliente"],
                    "fechallamada": data["fechallamada"],
                    "campania": data["campania"],
                    "cod_tipificacion": data["cod_tipificacion"],
                    "duracion_en_segundos": data["duracion_en_segundos"],
                    "error": value_return["errors"],
                }
            )

    end_time = time.perf_counter()
    total_time = end_time - start_time
    print(f"[timeit] {total_time:.4f}s (validate_data)")

    if len(data_error) > 0:
        if len(error_tipificacion) > 0:
            return {"statusCode": 402, "data": error_tipificacion}
        else:
            return {"statusCode": 400, "data": data_error}
    elif len(data_error) == 0:
        insert_gestiones_alt(data_valid)
        update_carga_gestiones()
        update_insert_resumen_lead_carga(codigo_carga)
        return {
            "statusCode": 200,
            "message": "Archivo cargado correctamente",
            "body": "datos correctos",
        }


def main():
    import json

    with open("gestiones_5k.json", "r") as f:
        data = json.load(f)

    result = run(data, {})
    print(result)


if __name__ == "__main__":
    main()
