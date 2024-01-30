import uuid
from src.database import get_codigo_carga

def generate_load_code_id(id_empresa_ct):
    #debo verificar si existe alguna carga anterior en el dia, si no existe.. creo el id..
    #si existe, rescatarlo y mantener ese como codigo.
    search_codigo_carga = get_codigo_carga(id_empresa_ct)
    if search_codigo_carga and len(search_codigo_carga) > 0:
        return search_codigo_carga
    else:
        return uuid.uuid4().hex