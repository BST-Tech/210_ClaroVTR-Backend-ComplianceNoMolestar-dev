import json
import re
from datetime import datetime
from src.database import get_tipificaciones, insert_gestiones, get_data_user
from shared.aws_cognito import get_user_by_id
from shared.utils import generate_load_code_id, format_date

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

def validate_information(row_value, empresa_ct):
    invalid_rules = []
    tipificaciones = []
    tipificaciones = validate_tipificaciones(row_value['cod_tipificacion'], empresa_ct)
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

def run(event, context):
    datas = event['data']
    codigo_carga = event['cod_carga']
    data_valid = []
    data_error = []
    error_tipificacion = []
    data_user = get_user_by_id(event['uid'])
    user_data_db = get_data_user(data_user)
    id_empresa_ct = user_data_db[0][1]
    data_null = None
    id_canal = event['id_canal']
    
    for data in datas:
        value_return = validate_information(data,id_empresa_ct )
        if value_return['status']:
            tipificacion = get_tipificaciones(data['cod_tipificacion'],id_empresa_ct)
            id_tipificacion = tipificacion[0][1]

            data_valid.append(( 
                id_tipificacion,
                data['pcs_salida'][-9:],
                data['pcs_cliente'][-9:], 
                format_date(data['fechallamada']), 
                codigo_carga,
                data['canal_o_nombre_EPS'],
                data['campania'],
                data['duracion_en_segundos'],
                data['operador_id_ejecutivo'],
                user_data_db[0][0]))
            
        elif not value_return['status']:
            if "Tipificacion no existe o no encontrada" in value_return['errors']:
                error_tipificacion.append({
                    "pcs": data['pcs_cliente'],
                    "tipificacion": data['cod_tipificacion']
                })
            
            data_error.append(                    {
                        "canal_o_nombre_EPS": data['canal_o_nombre_EPS'],
                        "operador_id_ejecutivo": data['operador_id_ejecutivo'],
                        "pcs_salida": data['pcs_salida'],
                        "pcs_cliente": data['pcs_cliente'],
                        "fechallamada": data['fechallamada'],
                        "campania": data['campania'],
                        "cod_tipificacion": data['cod_tipificacion'],
                        "duracion_en_segundos":data['duracion_en_segundos'],
                        "error": value_return['errors']
                    })
    if len(data_error) > 0:
        if len(error_tipificacion) > 0:
            return {
                'statusCode': 402 ,
                'data': error_tipificacion
            }
        else:
            return {
                'statusCode': 400 ,
                'data': data_error
            }
    elif len(data_error) == 0:
        result = insert_gestiones(data_valid)
        print(result)
        return {
            'statusCode': 200,
            'message': "Archivo cargado correctamente",
            'body': "datos correctos"
        }
