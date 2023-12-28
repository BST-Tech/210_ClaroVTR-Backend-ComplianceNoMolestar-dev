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

	def execute_query_usuario(self, query, params:str=None):
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
        
def create_user(new_data):
    nombre = new_data.get('nombre')
    apellidos = new_data.get('apellido')
    email = new_data.get('email')
    activo = new_data.get('activo')
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    query_user = f"""INSERT INTO public.usuario 
    (nombre, apellidos, email, activo, created_at, updated_at)
    VALUES('{nombre}', '{apellidos}', '{email}', {activo},'{timestamp}','{timestamp}') returning id;
    """
    try:
        db = DatabaseConnection()
        if db.connect():
            return db.execute_query(query_user)
    except Exception as e:
        return f"Error general: {e}"
    finally:
        db.close_connection()
    

def create_perfil_usuario(new_data, id_user, id_ct):
    rol = new_data.get('rol')
    activo = new_data.get('activo')
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    
    query_perfil_usuario = f"""INSERT INTO public.perfil_usuario
    (id_usuario, id_empresa_ct, id_rol, activo, created_at, updated_at)
    VALUES({id_user}, {id_ct}, {rol}, {activo}, '{timestamp}', '{timestamp}');
    """
    try:
        db = DatabaseConnection()
        if db.connect():
            return db.execute_query_usuario(query_perfil_usuario)
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
    