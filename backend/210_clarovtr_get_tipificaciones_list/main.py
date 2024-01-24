from src.utils import element_to_json
from src.database import get_tipificaciones_from_api, get_id_empresa_ct


def run(event, context):
    uid = event["uid"]
    ecc_id = event.get("data", {}).get("empresa_contact_center_id")
    if not ecc_id:
        ecc_id = get_id_empresa_ct(uid)

    data_tipificaciones = get_tipificaciones_from_api(ecc_id)

    if data_tipificaciones:
        json_data = element_to_json(data_tipificaciones)
        print(f"found {len(json_data)} results")
        return {
            "statusCode": 200,
            "tipificaciones": json_data,
        }
    return {
        "statusCode": 204,
        "tipificaciones": None,
        "error": "sin datos que mostrar",
    }


def main():
    import json

    # from dotenv import load_dotenv
    # load_dotenv()

    with open("test_cases.json", "r") as f:
        data = json.load(f)

    test_cases = data["cases"]
    for test in test_cases:
        print(test["name"])
        result = run(test["data"], {})
        print(result["statusCode"])
        print(json.dumps(result, indent=2))
        print("*" * 25)


if __name__ == "__main__":
    main()
