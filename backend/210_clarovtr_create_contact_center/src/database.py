import os
import sys
import time
import datetime
from sqlite3 import DatabaseError
from shared.secret_manager import get_value_secret
from shared.cognito import get_user_by_id
import psycopg2

class DatabaseConnection:
	def connect(self):
		environ = get_value_secret()
		try:
			self.connection = psycopg2.connect(
                dbname= environ['DB_NAME'],
                user=environ['DB_USERNAME'],
                password=environ['DB_PASSWORD'],
				host=environ['DB_HOST'])
			return self.connection
		except Exception as e:
			return f"Error al conectar a la base de datos: {e}"

	def execute_many_querys(self, query, params:list=None):
		if self.connection is not None:
			try:
				cursor = self.connection.cursor()
				cursor.executemany(query, params)
				cursor.close()
			except Exception as e:
				return f"Error al ejecutar la consulta: {e}"
		else:
			return "No se ha establecido una conexión a la base de datos."

	def execute_query(self, query, params:str=None):
		if self.connection is not None:
			try:
				cursor = self.connection.cursor()
				cursor.execute(query, (params,))
				result = cursor.fetchall()
				cursor.close()
				return result
			# except Exception as e:
			except psycopg2.Error as e:
				return f"Error al ejecutar la consulta: {e}"
		else:
			print("No se ha establecido una conexión a la base de datos.")
			return None

	def execute_without_return(self, query, params:str=None):
		if self.connection is not None:
			try:
				cursor = self.connection.cursor()
				cursor.execute(query, (params,))
				cursor.close()
				return "Insertado correctamente"
			# except Exception as e:
			except psycopg2.Error as e:
				return f"Error al ejecutar la consulta: {e}"
		else:
			print("No se ha establecido una conexión a la base de datos.")
			return None

	def close_connection(self):
		if self.connection is not None:
			self.connection.commit()
			self.connection.close()
			# print("Conexión a la base de datos cerrada.")
		else:
			print("No hay una conexión activa para cerrar.")

def get_id_ct(uid):
    email = get_user_by_id(uid)
    query = f'''
	select pu.id_empresa_ct from perfil_usuario pu 
	join empresa_contact_center ecc on pu.id_empresa_ct = ecc.id
	join usuario u on u.id = pu.id_usuario
	where u.email = '{email}';'''
    try:
        db = DatabaseConnection()
        if db.connect():
            results = db.execute_query(query)
            if results:
                return results
            else:
                return "Sin datos para esta empresa contact center"
    except Exception as e:
        return f"Error general: {e}"
    finally:
        db.close_connection()

        
def get_rol_user(email):
    query = f"""select r.nombre from perfil_usuario pu join usuario u on pu.id_usuario = u.id 
    join rol r on pu.id_rol = r.id where u.email = '{email}';"""
    try:
        db = DatabaseConnection()
        if db.connect():
            results = db.execute_query(query)
            if results:
                return results[0][0]
            else:
                return None
    except Exception as e:
        print(f"Error general: {e}")
    finally:
        db.close_connection()
        
def get_user_data_email(user_id):
    query = f'''select u.email from perfil_usuario pu join usuario u 
    on pu.id_usuario = u.id where pu.id = '{user_id}';'''
    try:
        db = DatabaseConnection()
        if db.connect():
            results = db.execute_query(query)
            if results:
                return results[0][0]
            else:
                return None
    except Exception as e:
        print(f"Error general: {e}")
    finally:
        db.close_connection()

def create_contact_center(new_data):
    nombre = new_data.get('nombre')
    razon_social = new_data.get('razon_social')
    rut = new_data.get('rut')
    tipo = int(new_data.get('tipo'))
    activo = int(new_data.get('activo'))
    print(type(activo), type(activo))
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    query_user = f"""INSERT INTO public.contact_center (id_tipo, rut, nombre, razon_social, created_at, updated_at, activo)
    VALUES('{tipo}', '{rut}', '{nombre}', '{razon_social}','{timestamp}','{timestamp}', '{activo}') returning id;
    """

    try:
        db = DatabaseConnection()
        if db.connect():
            result =db.execute_query(query_user)
            return result[0][0]
    except Exception as e:
        return f"Error general: {e}"
    finally:
        db.close_connection()
        
def get_exist_contactcenter(new_data):
    rut = new_data.get('rut')
    query_user = f"""select cc.id from contact_center cc where cc.rut = '{rut}';"""
    try:
        db = DatabaseConnection()
        if db.connect():
            return db.execute_query(query_user)
    except Exception as e:
        return f"Error general: {e}"
    finally:
        db.close_connection()
    return None

def create_empresa_contact_center(id_contact_center,new_data, email_user):
    activo = new_data.get('activo')
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    query_user = f"""INSERT INTO public.empresa_contact_center 
    (id_empresa, id_contact_center, activo, created_at)
    VALUES((select e.id from perfil_usuario pu join usuario u on pu.id_usuario = u.id
    join empresa_contact_center ecc on pu.id_empresa_ct = ecc.id
    join empresa e on ecc.id_empresa = e.id
    where u.email = '{email_user}'), {int(id_contact_center)}, {int(activo)}, '{timestamp}');
    """
    try:
        db = DatabaseConnection()
        if db.connect():
            return db.execute_without_return(query_user)
    except Exception as e:
        return f"Error general: {e}"
    finally:
        db.close_connection()
    

