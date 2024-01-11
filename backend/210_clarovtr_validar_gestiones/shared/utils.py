import uuid
import re

from datetime import datetime
from src.database import get_codigo_carga_gestion, get_tipificaciones, get_last_codigo_carga_lead

# def generate_load_code_id():
#     return uuid.uuid4().hex
def generate_load_gestion_code():
    #debo verificar si existe alguna carga anterior en el dia, si no existe.. creo el id..
    #si existe, rescatarlo y mantener ese como codigo.
    codigo_carga_getion = get_codigo_carga_gestion()
    if codigo_carga_getion and len(codigo_carga_getion) > 0:
        return codigo_carga_getion
    else:
        # codigo_gestion = get_last_codigo_carga_lead()
        # print(f" codigo_gestion {codigo_gestion}")
        # # return uuid.uuid4().hex
        return get_last_codigo_carga_lead()

def convert_date(value):
    return datetime.strptime(value, '%d-%m-%Y').strftime('%d-%m-%Y %H:%M:%S')

def format_date(date):
    fecha_obj = datetime.strptime(date, '%d-%m-%Y %H:%M:%S')
    return fecha_obj.strftime('%Y-%m-%d %H:%M:%S')



def validate_pcs(pcs):
    pattern = r'^\d{8,}$'
    if re.match(pattern, pcs):
        return True
    else:
        return False
    
def validate_format_date(date):
    pattern = r'\d{2}-\d{2}-\d{4}'
    if re.match(pattern, date):
        return True
    else:
        return False
    
def validar_numero(value):
    pattern = r'^\d+$'
    if re.match(pattern, str(value)):
        return True
    else:
        return False
    
def validate_tipificaciones(value, empresa_ct):
    result = get_tipificaciones(value, empresa_ct)
    if result is not None:
        return result[0][0]
    else:
        return None

def validate_information(row_value, tipificaciones):
    invalid_rules = []
    # tipificaciones = []
    # tipificaciones = tipificaciones_dict.get(row_value['cod_tipificacion'])#validate_tipificaciones(row_value['cod_tipificacion'], empresa_ct)
    if row_value['canal_o_nombre_EPS'] == "":
        invalid_rules.append("Canal o nombre EPS no presente")
    if not validate_pcs(row_value['pcs_salida']):
        invalid_rules.append("PCS Salida no cumple con los 8 caracteres minimos")
    if not validate_pcs(row_value['pcs_cliente']):
        invalid_rules.append("PCS Cliente no cumple con los 8 caracteres minimos")
    if not validate_format_date(row_value['fechallamada']):
        invalid_rules.append("Fecha llamada no coincide con formato establecido")
    if row_value['campania'] in ('', None):
        invalid_rules.append("Campaña vacia y/o con datos nulos")
    if len(tipificaciones) == 0 or row_value['cod_tipificacion'] not in tipificaciones:
        invalid_rules.append("Tipificacion no existe o no encontrada")
    if not validar_numero(row_value['duracion_en_segundos']):
        invalid_rules.append("Duracion en segundos no es numerico")
    
    if invalid_rules:
        return {
            "status": False,
            "errors": ' y '.join([rule for rule in invalid_rules])
        } 
    else: 
        return {
            "status": True
            }
        
def get_all_tipificaciones(datas):
    return set([item['cod_tipificacion'] for item in datas])
    