import time
import datetime

def make_data_to_insert(data_list, empresa_ct_id):
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