import pandas as pd
from datetime import datetime, timedelta


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

    last_load_str = None
    last_login_str = None
    logins = df["last_login"].dropna()
    delta = timedelta(hours=-3)
    if not logins.empty:
        ultimo_last_login = logins.max() + delta
        last_login_str = ultimo_last_login.strftime("%Y-%m-%d %H:%M:%S")

    loads = df["last_load"].dropna()
    if not loads.empty:
        ultimo_last_load = loads.max() + delta
        last_load_str = ultimo_last_load.strftime("%Y-%m-%d %H:%M:%S")

    suma_validaciones = int(df["validaciones"].dropna().sum())
    return {
        "last_conection": last_login_str,
        "leads_validados": suma_validaciones,
        "last_upload_gestion": last_load_str,
    }
