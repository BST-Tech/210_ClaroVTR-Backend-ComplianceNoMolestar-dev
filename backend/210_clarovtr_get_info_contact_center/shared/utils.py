import pandas as pd
from datetime import datetime


def data_to_dataframe(data_to):
    cabeceras = [
        "id",
        "nombre",
        "apellidos",
        "last_login",
        "validaciones",
        "contact_center",
        "cc_activo",
        "last_load",
    ]
    return pd.DataFrame(data_to, columns=cabeceras)


def get_data_users_by_contact_center_to_json(data_contact_center):
    df = data_to_dataframe(data_contact_center)
    df["last_login"] = pd.to_datetime(df["last_login"], errors="coerce")
    df["last_load"] = pd.to_datetime(df["last_load"], errors="coerce")

    ultimo_last_login = None
    ultimo_last_load = None
    logins = df["last_login"].dropna()
    if not logins.empty:
        ultimo_last_login = logins.max().strftime("%Y-%m-%d %H:%M:%S")

    loads = df["last_load"].dropna()
    if not loads.empty:
        ultimo_last_load = loads.max().strftime("%Y-%m-%d %H:%M:%S")

    suma_validaciones = int(df["validaciones"].dropna().sum())
    return {
        "last_conection": ultimo_last_login,
        "leads_validados": suma_validaciones,
        "last_upload_gestion": ultimo_last_load,
    }
