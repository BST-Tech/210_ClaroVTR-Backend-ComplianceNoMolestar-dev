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
			print(f"Error al conectar a la base de datos: {e}")
			return None

	def execute_many_querys(self, query, params:list=None):
		if self.connection is not None:
			try:
				cursor = self.connection.cursor()
				cursor.executemany(query, params)
				cursor.close()
			except Exception as e:
				print(f"Error al ejecutar la consulta: {e}")
				return None
		else:
			print("No se ha establecido una conexión a la base de datos.")
			return None

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
				print(f"Error al ejecutar la consulta: {e}")
				return None
		else:
			print("No se ha establecido una conexión a la base de datos.")
			return None

	def execute_update(self, query, params:str=None):
		if self.connection is not None:
			try:
				cursor = self.connection.cursor()
				cursor.execute(query, (params,))
				cursor.close()
				return "actualizada correctamente"
			# except Exception as e:
			except psycopg2.Error as e:
				print(f"Error al ejecutar la consulta: {e}")
				return None
		else:
			print("No se ha establecido una conexión a la base de datos.")
			return None

	def close_connection(self):
		if self.connection is not None:
			self.connection.commit()
			self.connection.close()
			print("Conexión a la base de datos cerrada.")
		else:
			print("No hay una conexión activa para cerrar.")

def update_last_login_user(uid):
    # Actualizar el ultimo login de un usuario a la hora actual
    email = get_user_by_id(uid)
    # current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    current_time = datetime.datetime.fromtimestamp(
        time.time()).strftime('%Y-%m-%d %H:%M:%S')
    query=f"""
    UPDATE public.perfil_usuario set last_login='{current_time}'
		WHERE id = (select pu.id from perfil_usuario pu join usuario u on pu.id_usuario = u.id where u.email = '{email}' LIMIT 1 );"""
    try:
        db = DatabaseConnection()
        if db.connect():
            return db.execute_update(query)
    except Exception as e:
        return f"Error general: {e}"
    finally:
        db.close_connection()
        
        
def list_data_contact_center(uid):
	# Actualizar el ultimo login de un usuario a la hora actual
    email = get_user_by_id(uid)
    # current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    current_time = datetime.datetime.fromtimestamp(
        time.time()).strftime('%Y-%m-%d %H:%M:%S')
    query=f"""
    UPDATE public.perfil_usuario set last_login='{current_time}'
		WHERE id = (select pu.id from perfil_usuario pu join usuario u on pu.id_usuario = u.id where u.email = '{email}' LIMIT 1 );"""
    try:
        db = DatabaseConnection()
        if db.connect():
            return db.execute_update(query)
    except Exception as e:
        return f"Error general: {e}"
    finally:
        db.close_connection()