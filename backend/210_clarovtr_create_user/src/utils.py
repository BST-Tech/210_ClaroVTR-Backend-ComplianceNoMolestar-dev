import time
import datetime

def make_data_to_insert(data_list, empresa_ct_id):
    """
    The function "make_data_to_insert" takes a list of data dictionaries and an "empresa_ct_id" as
    input, and returns a list of tuples with the extracted data from the dictionaries along with
    additional information.
    
    :param data_list: A list of dictionaries containing data to be inserted into a database. Each
    dictionary represents a row of data and contains the following keys:
    :param empresa_ct_id: The parameter "empresa_ct_id" is an identifier for a company or organization.
    It is used to associate the data with a specific company in the database
    :return: a list of tuples. Each tuple contains the values extracted from the `data_list` dictionary,
    along with the `empresa_ct_id`, `timestamp`, and `estado` values.
    """
    data_list_to_db = []
    timestamp = datetime.datetime.fromtimestamp(
        time.time()).strftime('%Y-%m-%d %H:%M:%S')
    for data in data_list:
        data_list_to_db.append((
            data.get('tipificacion'),
            data.get('contacto'),
            data.get('venta'),
            empresa_ct_id,
            data.get('nombre_tipificacion'),
            timestamp,
            timestamp,
            data.get('estado')
        ))
    return data_list_to_db

def get_numeric_value(tupla):
    """
    The function `get_numeric_value` takes a tuple as input and returns the numeric value inside the
    tuple if it exists, otherwise it returns False.
    
    :param tupla: The parameter `tupla` is a tuple or a list containing a tuple
    :return: either the numeric value found in the tuple or False if no numeric value is found.
    """
    if isinstance(tupla,list) and len(tupla) == 1:
        tupla = tupla[0]
        if isinstance(tupla, tuple) and len(tupla) == 1:
            elemento = tupla[0]
            if isinstance(elemento, (int, float)):
                return elemento
            elif isinstance(elemento, str) and elemento.isdigit():
                return int(elemento)
    
    # Retornar None si no se encuentra un valor numérico
    return False