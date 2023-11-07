import json
import re
import time
import datetime
from shared.database import get_data, insert_data, soft_delete, update_data
from shared.utils import extract_keys, format_date_crud, encript_password

entity_definitions = {
    "tipificacion": {
        "tipificacion": str,
        "contacto": int,
        "venta": int,
        "id_empresa_ct": int,
        "nombre_tipificacion": str,
        "created_at": "timestamp",
        "updated_at": "timestamp"
    },
    "usuario": {
        "nombre": str,
        "apellidos": str,
        "email": str,
        "password": str,
        "activo": int,
        "created_at": "timestamp",
        "updated_at": "timestamp",
        "deleted_at": "timestamp",
        "id": int

    },
    "contact_center": {
        "id_tipo": int,
        "rut": str,
        "nombre": str,
        "razon_social": str,
        "created_at": "timestamp",
        "updated_at": "timestamp",
        "deleted_at": "timestamp"
    },
    "regla": {
        "id_canal": int,
        "id_empresa": int,
        "id_tipo_evento": int,
        "nombre": str,
        "dias_rango": int,
        "numero_incidencias": int,
        "dias_permanencia": int,
        "activa": int,
        "created_at": "timestamp",
        "updated_at": "timestamp",
        "deleted_at": "timestamp",
    }}


def validate_entidad(entity):
    if entity in entity_definitions:
        return entity_definitions.get(entity)
    else:
        return False

def return_entidad_get(datas, fields, entity):
    fields = extract_keys(fields)
    result = []
    if entity == "tipificacion":
        for data in datas:
            result.append({
                "tipificacion": data[0],
                "contacto": data[1],
                "venta": data[2],
                "id_empresa_ct": data[3],
                "nombre_tipificacion": data[4],
                "created_at": format_date_crud(data[5]),
                "updated_at": format_date_crud(data[6])
            })
    elif entity == "usuario":
        for data in datas:
            record = {
                "nombre": data[0],
                "apellidos": data[1],
                "email": data[2],
                "password": data[3],
                "activo": data[4],
                "created_at": format_date_crud(data[5]),
                "updated_at": format_date_crud(data[6]),
                "id": data[8]}

            if data[7] is not None:
                record["deleted_at"] = format_date_crud(data[7])
            result.append(record)
    elif entity == "contact_center":
        for data in datas:
            print(data)
            record = {
                "id_tipo": data[0],
                "rut": data[1],
                "nombre": data[2],
                "razon_social": data[3],
                "created_at": format_date_crud(data[4]),
                "updated_at": format_date_crud(data[5])}

            if data[6] is not None:
                record["deleted_at"] = format_date_crud(data[6])
            result.append(record)
    elif entity == "regla":
        for data in datas:
            print(data)
            record = {
                "id_canal": data[0],
                "id_empresa":data[1],
                "id_tipo_evento":data[2],
                "nombre":data[3],
                "dias_rango":data[4],
                "numero_incidencias":data[5],
                "dias_permanencia":data[6],
                "activa":data[7],
                "created_at": format_date_crud(data[8]),
                "updated_at": format_date_crud(data[9])
            }
            if data[10] is not None:
                record["deleted_at"] = format_date_crud(data[10])
            result.append(record)
    return result


def return_entidad_post(data, fields, entity):
    print(fields)
    fields = extract_keys(fields)
    if entity == "usuario" and "id" in fields:
        fields.remove('id')
        
    if 'deleted_at' in fields:
        fields.remove('deleted_at')
    timestamp = datetime.datetime.fromtimestamp(
        time.time()).strftime('%Y-%m-%d %H:%M:%S')
    if entity == "tipificacion":
        data_insert = (
            data['tipificacion'],
            data['contacto'],
            data['venta'],
            data['id_empresa_ct'],
            data['nombre_tipificacion'],
            timestamp,
            timestamp)
    elif entity == "usuario":
        data_insert = (
            data['nombre'],
            data['apellidos'],
            data['email'],
            encript_password(data['password']),
            data['activo'],
            timestamp,
            timestamp)
    
    elif entity == "contact_center":
        data_insert = (
            data['id_tipo'],
            data['rut'],
            data['nombre'],
            data['razon_social'],
            timestamp,
            timestamp)
    elif entity == "regla":
        data_insert = (
            data['id_canal'],
            data['id_empresa'],
            data['id_tipo_evento'],
            data['nombre'],
            data['dias_rango'],
            data['numero_incidencias'],
            data['dias_permanencia'],
            data['activa'],
            timestamp,
            timestamp)
    return insert_data(data_insert, entity, fields)


def return_deleted_data(id, entity, fields):
    timestamp = datetime.datetime.fromtimestamp(
        time.time()).strftime('%Y-%m-%d %H:%M:%S')
    try:
        resultado = soft_delete(id, entity, fields, timestamp)
        return resultado
    except Exception as e:
        print(f"Error general: {e}")
        return "Error al eliminar el registro"


def return_update_data(data, id_value, entity, fields):
    fields = extract_keys(fields)
    if 'created_at' in fields:
        fields.remove('created_at')
    timestamp = datetime.datetime.fromtimestamp(
        time.time()).strftime('%Y-%m-%d %H:%M:%S')
    if entity == "tipificacion":
        data = {
            "tipificacion": data['tipificacion'],
            "contacto": data['contacto'],
            "venta": data['venta'],
            "id_empresa_ct": data['id_empresa_ct'],
            "nombre_tipificacion": data['nombre_tipificacion'],
            "updated_at": timestamp}
    elif entity == "usuario":
        data = {
            "nombre": data['nombre'],
            "apellidos": data['apellidos'],
            "email": data['email'],
            "password": data['password'],
            "activo": data['activo'],
            "updated_at": timestamp,
            "deleted_at": None
        }
    elif entity == "contact_center":
        data = {
            "id_tipo": data['id_tipo'],
            "rut": data['rut'],
            "nombre": data['nombre'],
            "razon_social": data['razon_social'],
            "updated_at": timestamp,
            "deleted_at": None
        }
    elif entity =="regla":
        data = {
            "id_canal": data['id_canal'],
            "id_empresa": data['id_empresa'],
            "id_tipo_evento": data['id_tipo_evento'],
            "nombre": data['nombre'],
            "dias_rango": data['dias_rango'],
            "numero_incidencias": data['numero_incidencias'],
            "dias_permanencia": data['dias_permanencia'],
            "activa": data['activa'],
            "created_at": timestamp,
            "updated_at": timestamp,
            "deleted_at": None
        }
    return update_data(entity, id_value, data, fields)


def run(event, context):
    entidad = event['entity']
    method = event['method']
    data = event['data']
    data_validate = validate_entidad(entidad)
    if data_validate:
        print("entidad valida")
        if method == "GET":
            print("GET")
            return {
                'statusCode': 200,
                'message': "Datos obtenidos correctamente",
                'data': return_entidad_get(get_data(entidad, data_validate), data_validate, entidad)
            }
        elif method == "POST":
            print("POST")
            return {
                'statusCode': 200,
                'message': return_entidad_post(data, data_validate, entidad),
                'data': data
            }
        elif method == "DELETE":
            print("delete")
            id_value = data['id']
            return {
                'statusCode': 200,
                'message': return_deleted_data(id_value, entidad, data_validate),
                'data': data
            }
        elif method == "PUT":
            print("update")
            id_value = data['id']
            return {
                'statusCode': 200,
                'message': return_update_data(data, id_value, entidad, data_validate),
                'data': data
            }
