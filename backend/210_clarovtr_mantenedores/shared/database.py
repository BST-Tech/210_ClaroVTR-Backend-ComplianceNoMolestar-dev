import os
import sys
from sqlite3 import DatabaseError
from shared.secret_manager import get_value_secret
from shared.utils import extract_keys, extract_keys_and_values
import psycopg2

class DatabaseConnection:
	def connect(self):
		environ = get_value_secret()
		try:
			self.connection = psycopg2.connect(
				dbname=environ['DB_NAME'],
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
		if self.connection is None:
			print("No se ha establecido una conexión a la base de datos.")
			return None
		try:
			with self.connection.cursor() as cursor:
				cursor.execute(query, (params,))
				if "INSERT" in query:
					return "Insertado Correctamente"
				elif "DELETE" in query:
					return "Eliminado Correctamente" if cursor.rowcount == 1 else "Error al eliminar el registro"
				elif "UPDATE" in query:
					return "Actualizado Correctamente" if cursor.rowcount == 1 else "Error al actualizar el registro"
				else:
					result = cursor.fetchall()
					return result
		except psycopg2.Error as e:
			print(f"Error al ejecutar la consulta: {e}")
			return None

	def execute_like_query(self, query):
		if self.connection is not None:
			try:
				cursor = self.connection.cursor()
				cursor.execute(query)
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

	def close_connection(self):
		if self.connection is not None:
			self.connection.commit()
			self.connection.close()
			print("Conexión a la base de datos cerrada.")
		else:
			print("No hay una conexión activa para cerrar.")

def insert_gestiones(data):
	status = 200
	query ="""
	INSERT INTO public.gestion (
		tipificacion, 
		pcs_salida, 
		pcs_cliente,
		fecha_llamada, 
		codigo_carga, 
		canal_o_nombre_eps,
		campania,
		segundos_llamada,
		operador_id_ejecutivo,
		id_usuario)
		VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
		"""

	try:
		db = DatabaseConnection()
		if db.connect():
			results = db.execute_many_querys(query, data)
			if results:
				print(results)
				return results
			else:
				return None
	except Exception as e:
		print(f"Error general: {e}")
	finally:
		db.close_connection()
	return status

def get_element_by_upload_code(codigo_carga):
	query = '''
	select lc.codigo_carga, lc.created_at, u.nombre ||' ' ||u.apellidos as usuario, lc.pcs_cliente, lc.en_nomolestar, lc.en_cooler  from lead_carga lc
	join perfil_usuario pu on lc.id_usuario = pu.id 
	join usuario u on pu.id_usuario = u.id where lc.codigo_carga = %s;'''
	#query = "select * from lead_carga lc where lc.codigo_carga = %s;"
	try:
		db = DatabaseConnection()
		if db.connect():
			results = db.execute_query(query, codigo_carga)
			if results:
				return results
			else:
				return None
	except Exception as e:
		print(f"Error general: {e}")
	finally:
		db.close_connection()

def get_element_by_upload_code_group_by(codigo_carga):
	query = "select * from lead_carga lc where lc.codigo_carga = %s;"
	try:
		db = DatabaseConnection()
		if db.connect():
			print("conecto")
			results = db.execute_query(query, codigo_carga)
			if results:
				return results
			else:
				return None
	except Exception as e:
		print(f"Error general: {e}")
	finally:
		db.close_connection()

def get_data_user(email_user):
	status = 500
	query = "select pu.id, pu.id_empresa_ct from usuario u join perfil_usuario pu on u.id = pu.id_usuario where u.email = %s;"
	try:
		db = DatabaseConnection()
		if db.connect():
			results = db.execute_query(query, email_user)
			if results:
				return results
			else:
				return None
	except Exception as e:
		print(f"Error general: {e}")
	finally:
		db.close_connection()
	return status

def update_resumen_lead_carga(upload_code):
	status = 500
	query = "select insertar_resumen_lead_carga(%s);"
	try:
		db = DatabaseConnection()
		if db.connect():
			results = db.execute_query(query, upload_code)
			if results:
				return results
			else:
				return None
	except Exception as e:
		print(f"Error general: {e}")
	finally:
		db.close_connection()
	return status

def get_tipificaciones(value):
	data_consult = '%' + value + '%'
	query = f"select distinct t.nombre_tipificacion, id from tipificacion t where t.nombre_tipificacion like '{data_consult}';"
	try:
		db = DatabaseConnection()
		if db.connect():
			results = db.execute_like_query(query)
			if results:
				return results
			else:
				return None
	except Exception as e:
		print(f"Error general: {e}")
	finally:
		db.close_connection()
		
def get_data_user(email_user):
	query = "select pu.id, pu.id_empresa_ct from usuario u join perfil_usuario pu on u.id = pu.id_usuario where u.email = %s;"
	try:
		db = DatabaseConnection()
		if db.connect():
			results = db.execute_query(query, email_user)
			if results:
				return results
			else:
				return None
	except Exception as e:
		print(f"Error general: {e}")
	finally:
		db.close_connection()
		
############
def get_data(entidad, fields):
	keys = ",".join(extract_keys(fields))
	query = f"select {keys} from {entidad};"
	try:
		db = DatabaseConnection()
		if db.connect():
			results = db.execute_query(query)
			if results:
				return results
			else:
				return None
	except Exception as e:
		print(f"Error general: {e}")
	finally:
		db.close_connection()
		
def insert_data(data, entidad, fields):
	keys = ",".join(extract_keys(fields))
	print(keys)

	query = f"INSERT INTO {entidad} ({keys}) VALUES {data};"
	print(f"query {query}")
	try:
		db = DatabaseConnection()
		if db.connect():
			results = db.execute_query(query)
			print(f"Resultado {results}")
			if results:
				return results
			else:
				return None
	except Exception as e:
		print(f"Error general: {e}")
	finally:
		db.close_connection()
		
		
def delete_data(id, entidad):
	query = f"DELETE FROM {entidad} WHERE id = {id};"
	try:
		db = DatabaseConnection()
		if db.connect():
			results = db.execute_query(query)
			print(f"Resultado {results}")
			if results:
				return results
			else:
				return None
	except Exception as e:
		print(f"Error general: {e}")
	finally:
		db.close_connection()
		
def soft_delete(id, entidad, fields, timestamp):
	# query = f"DELETE FROM {entidad} WHERE id = {id};"
	if entidad == "regla":
		value = ", activa = 0"
	elif entidad == "contact_center":
		value = ""
	else:
		value = ", activo = 0"

	if "deleted_at" in fields:
		query = f"UPDATE {entidad} SET updated_at = '{timestamp}', deleted_at = '{timestamp}' {value}  WHERE id = {id};"
		print(query)
	else:
		query = f"DELETE FROM {entidad} WHERE id = {id};"

	try:
		db = DatabaseConnection()
		if db.connect():
			results = db.execute_query(query)
			print(f"Resultado {results}")
			if results:
				return results
			else:
				return None
	except Exception as e:
		print(f"Error general: {e}")
	finally:
		db.close_connection()
		
def update_data(entidad, id, data, fields):
	print(data)
	print(fields)
	keys = ', '.join(extract_keys_and_values(data, fields))
	print(f"keys :{keys}")
	query = f"UPDATE {entidad} SET {keys} WHERE id = {id};"
	print(query)
	try:
		db = DatabaseConnection()
		if db.connect():
			results = db.execute_query(query)
			print(f"Resultado {results}")
			if results:
				return results
			else:
				return None
	except Exception as e:
		print(f"Error general: {e}")
	finally:
		db.close_connection()