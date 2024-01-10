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
			return "No se ha establecido una conexión a la base de datos."

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
			return "No se ha establecido una conexión a la base de datos."

	def close_connection(self):
		if self.connection is not None:
			self.connection.commit()
			self.connection.close()
		else:
			print("No hay una conexión activa para cerrar.")

def get_id_ct(uid):
    """
    The function `get_id_ct` retrieves the ID of a company in a contact center system based on a user's
    ID.
    
    :param uid: The parameter "uid" is the user ID. It is used to retrieve the email associated with the
    user ID and then query the database to get the ID of the company contact center that the user
    belongs to
    :return: the results of the query, which could be the ID of the empresa_contact_center associated
    with the given user ID. If there are no results, it will return the string "Sin datos para esta
    empresa contact center". If there is an error, it will return a string indicating the general error.
    """
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
    """
    The `create_user` function creates a new user in a database with the provided data.
    
    :param new_data: The `new_data` parameter is a dictionary that contains the information of a new
    user. It should have the following keys:
    :return: the result of the `db.execute_query(query_user)` method call.
    """
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
    """
    The function `create_perfil_usuario` creates a new user profile in a database table called
    `perfil_usuario` with the provided data.
    
    :param new_data: The `new_data` parameter is a dictionary that contains the new data for creating a
    user profile. It should have the following keys:
    :param id_user: The `id_user` parameter is the ID of the user for whom the profile is being created.
    It is used to associate the profile with the corresponding user in the database
    :param id_ct: The parameter `id_ct` represents the ID of the company or organization associated with
    the user's profile
    :return: the result of the `db.execute_query_usuario()` method call.
    """
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
    """
    The function `get_rol_user` retrieves the role name of a user based on their email from a database.
    
    :param email: The email parameter is the email address of the user for whom you want to retrieve the
    role
    :return: the name of the role associated with the given email.
    """
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
    """
    The function `get_user_data_email` retrieves the email of a user based on their user ID from a
    database.
    
    :param user_id: The user_id parameter is the unique identifier of the user whose email we want to
    retrieve from the database
    :return: the email of the user with the given user_id.
    """
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
    