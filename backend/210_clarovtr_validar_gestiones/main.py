import json
from datetime import datetime
from src.database import get_tipificaciones, insert_gestiones, get_data_user, update_resumen_lead_carga
from shared.aws_cognito import get_user_by_id
from shared.utils import generate_load_gestion_code, format_date, validate_information, get_all_tipificaciones

def run(event, context):
    datas = event['data']
    data_valid = []
    data_error = []
    error_tipificacion = []
    data_user = get_user_by_id(event['uid'])
    user_data_db = get_data_user(data_user)
    id_empresa_ct = user_data_db[0][1]
    codigo_carga = generate_load_gestion_code(id_empresa_ct) #event['cod_carga']
    
    tipificaciones_list = list(get_all_tipificaciones(datas)) 
    tipificaciones = get_tipificaciones(tipificaciones_list,id_empresa_ct)
    # tipificaciones_dict = dict(tipificaciones)
    for data in datas:
        value_return = validate_information(data, tipificaciones_list)
        if value_return['status']:
            # id_tipificacion = tipificaciones_dict.get(data['cod_tipificacion']) #get_tipificaciones(data['cod_tipificacion'],id_empresa_ct)

            data_valid.append(( 
                data['cod_tipificacion'],
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
        # result_resumen = update_resumen_lead_carga(codigo_carga);
        return {
            'statusCode': 200,
            'message': "Archivo cargado correctamente",
            'body': "datos correctos"
        }