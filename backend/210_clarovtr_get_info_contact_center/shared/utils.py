import pandas as pd
from datetime import datetime


def data_to_dataframe(data_to):
    """
    The function "data_to_dataframe" takes a list of data and converts it into a pandas DataFrame with
    specified column names.
    
    :param data_to: The parameter "data_to" is a list of lists or a 2D array. Each inner list represents
    a row of data, and the elements of the inner list represent the values of each column in that row
    :return: a pandas DataFrame object.
    """
    cabeceras = ["id", "nombre", "apellidos", "last_login", "validaciones", "contact_center", "cc_activo", "last_load"]
    return pd.DataFrame(data_to,columns =cabeceras)

def get_data_users_by_contact_center_to_json(data_contact_center):
    """
    The function `get_data_users_by_contact_center_to_json` takes in data from a contact center,
    converts it to a dataframe, and returns a JSON object with information about the last connection,
    number of validated leads, and last upload of management.
    
    :param data_contact_center: The parameter "data_contact_center" is assumed to be a dataset or data
    structure containing information about users in a contact center
    :return: a dictionary with the following keys and values:
    - "last_conection": the latest login date and time in the format "YYYY-MM-DD HH:MM:SS"
    - "leads_validados": the sum of the "validaciones" column (assuming it contains numeric values)
    - "last_upload_gestion": the latest load date and time in the format "YYYY-MM-DD
    """
    df = data_to_dataframe(data_contact_center)
    df['last_login'] = pd.to_datetime(df['last_login'], errors='coerce')
    df['last_load'] = pd.to_datetime(df['last_load'], errors='coerce')
    
    ultimo_last_login = df['last_login'].dropna().max().strftime("%Y-%m-%d %H:%M:%S")
    ultimo_last_load = df['last_load'].dropna().max().strftime("%Y-%m-%d %H:%M:%S")
    
    suma_validaciones = int(df['validaciones'].dropna().sum())
    return {
    "last_conection" : ultimo_last_login,
    "leads_validados": suma_validaciones,
    "last_upload_gestion": ultimo_last_load
    }