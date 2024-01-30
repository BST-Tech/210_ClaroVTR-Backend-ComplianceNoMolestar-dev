import re
from shared.timeit import timeit
from src.database import (
    insert_leads,
    get_data_user,
    get_element_by_upload_code,
    insert_leads_alt,
    update_resumen_lead_carga,
)
from shared.aws_cognito import get_user_by_id
from shared.utils import generate_load_code_id


def validate_pcs(pcs):
    pattern = r"^\d{8,}$"
    return re.match(pattern, pcs)


@timeit
def data_response(data_result_upload_daily):
    results = []
    for data in data_result_upload_daily:
        validation_result = ""
        if data[4] == 0 and data[5] == 0:
            validation_result = "OK PARA LLAMAR"
        elif data[4] == 1 and data[5] == 0:
            validation_result = "NO LLAMAR - NO MOLESTAR"
        elif data[4] == 0 and data[5] == 1:
            validation_result = "NO LLAMAR - BLOQUEO TEMPORAL"
        results.append(
            {"TELEFONO A VALIDAR": data[3], "RESULTADO VALIDACION": validation_result}
        )
    return results


@timeit
def data_response_alt(data_result_upload_daily):
    results = []
    for data in data_result_upload_daily:
        validation_result = ""
        if data[1] == 0 and data[2] == 0:
            validation_result = "OK PARA LLAMAR"
        elif data[1] == 1 and data[2] == 0:
            validation_result = "NO LLAMAR - NO MOLESTAR"
        elif data[1] == 0 and data[2] == 1:
            validation_result = "NO LLAMAR - BLOQUEO TEMPORAL"
        results.append(
            {"TELEFONO A VALIDAR": data[0], "RESULTADO VALIDACION": validation_result}
        )
    return results


@timeit
def run(event, context):
    print(event.keys())
    data_from_event = event["TELEFONO A VALIDAR"]
    data_user = get_user_by_id(event["uid"])
    id_canal = event["id_canal"]
    pcs_data_to_storage = []
    user_data_db = get_data_user(data_user)
    id_empresa_ct = user_data_db[0][1]
    id_code_uploads = generate_load_code_id(id_empresa_ct)
    print(f" id_code_uploads {id_code_uploads}")

    error = False
    errors = []
    for pcs in data_from_event:
        if validate_pcs(pcs):
            pcs_data_to_storage.append(
                (
                    user_data_db[0][1],
                    int(id_canal),
                    user_data_db[0][0],
                    pcs[-9:],
                    id_code_uploads,
                )
            )
        else:
            error = True
            errors.append(
                {"pcs": pcs, "error": "PCS no cumple con las reglas de negocio"}
            )
            print("PCS con error")
    result_insert = insert_leads(pcs_data_to_storage)
    # result_insert = insert_leads_alt(pcs_data_to_storage)
    result_update_lc = update_resumen_lead_carga(id_code_uploads)
    print(result_insert, result_update_lc)

    data_result_upload_daily = get_element_by_upload_code(id_code_uploads)

    if not error:
        return {
            "statusCode": 200,
            "message": "Archivo cargado correctamente",
            "body": data_response(data_result_upload_daily),
            # "body": data_response_alt(data_result_upload_daily_alt),
        }
    else:
        return {"statusCode": 500, "errors": errors}


def main():
    import json

    # from dotenv import load_dotenv
    # load_dotenv()

    with open("test_cases.json", "r") as f:
        data = json.load(f)

    test_cases = data["cases"]
    for test in test_cases:
        print(test["name"])
        if "Big" in test["name"]:
            result = run(test["data"], {})
            print(result["statusCode"])
            # print(json.dumps(result, indent=2))
            print("*" * 25)


if __name__ == "__main__":
    main()