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