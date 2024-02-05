import json
from src.utils import element_to_json
from src.database import get_users_list


def run(event, context):
    uid = event["uid"]
    email = event.get("email")

    data_user_list = get_users_list(uid, email)
    if data_user_list and len(data_user_list) > 0:
        return {"statusCode": 200, "data": element_to_json(data_user_list)}
    else:
        return {
            "statusCode": 204,
            "data": json.dumps("Sin contenido"),
            "error": "sin datos que mostrar",
        }


def main():
    run({"uid": ""}, None)


if __name__ == "__main__":
    main()
