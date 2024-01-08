import json
from src.database import get_data_contact_center
from shared.cognito import get_user_by_id
from shared.utils import get_data_users_by_contact_center_to_json


def run(event, context):
    uid = event["uid"]
    id_ct = event["data"]["id"]
    email = get_user_by_id(uid)
    if not email:
        return {
            "statusCode": 400,
            "error": "No se encontro un usuario con el CognitoID ingresado",
        }

    result = get_data_contact_center(email, id_ct)

    if result and len(result) > 0:
        data = {
            "statusCode": 200,
            "data": get_data_users_by_contact_center_to_json(result),
        }
        return data
    else:
        return {"statusCode": 204, "error": "sin datos que mostrar"}


def main():
    import json
    from dotenv import load_dotenv

    load_dotenv()
    with open("test_cases.json", "r") as f:
        data = json.load(f)

    test_cases = data["cases"]
    for test in test_cases:
        print(test["name"])
        result = run(test["data"], {})
        print(result["statusCode"])
        print("*" * 25)


if __name__ == "__main__":
    main()
