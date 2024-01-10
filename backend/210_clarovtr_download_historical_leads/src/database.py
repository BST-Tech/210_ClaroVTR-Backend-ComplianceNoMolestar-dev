from sqlite3 import DatabaseError
from shared.secret_manager import get_value_secret
import psycopg2

class DatabaseConnection:
	def connect(self):
		"""
		The function connects to a PostgreSQL database using environment variables for the database name,
		username, password, and host.
		:return: The code is returning either the connection object if the connection is successful, or an
		error message if there is an exception while connecting to the database.
		"""
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
		"""
		The function `execute_many_querys` executes a query multiple times with different parameters in a
		database connection.
		
		:param query: The query parameter is a string that represents the SQL query you want to execute. It
		should be a valid SQL statement
		:param params: The `params` parameter is a list of tuples or lists containing the values to be used
		in the query. Each tuple or list represents a set of values for a single execution of the query. The
		number of values in each tuple or list should match the number of placeholders in the query
		:type params: list
		:return: If the connection to the database is established and the query is executed successfully,
		nothing is returned. If there is an error while executing the query, an error message is returned.
		If there is no connection established to the database, a message indicating that no connection has
		been established is returned.
		"""
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
		"""
		The function `execute_query` executes a SQL query using a provided connection and returns the
		result, or an error message if there is an issue with the query or connection.
		
		:param query: The query parameter is a string that represents the SQL query you want to execute. It
		can be any valid SQL statement, such as SELECT, INSERT, UPDATE, DELETE, etc
		:param params: The "params" parameter is a string that represents the parameters to be passed to the
		query. It is used to prevent SQL injection by passing user input as parameters instead of directly
		concatenating them into the query string
		:type params: str
		:return: the result of the query execution if the connection to the database is established. If
		there is an error during the execution of the query, it returns an error message. If there is no
		connection to the database, it returns a message indicating that no connection has been established.
		"""
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

	def close_connection(self):
		"""
		The close_connection function closes the active connection and commits any pending changes.
		"""
		if self.connection is not None:
			self.connection.commit()
			self.connection.close()
		else:
			print("No hay una conexión activa para cerrar.")

def get_data_by_upload(codigo_carga):
	"""
	The function `get_data_by_upload` retrieves data from a database based on a given `codigo_carga`
	parameter.
	
	:param codigo_carga: The parameter "codigo_carga" is a unique identifier for a data upload. It is
	used in the SQL query to retrieve data related to that specific upload
	:return: the results of the query if there are any, otherwise it returns None.
	"""
	query = """select 
	lc.id, lc.id_lead, lc.id_empresa_ct, lc.id_canal, lc.en_cooler, lc.en_nomolestar, lc.created_at, u.nombre||' '||u.apellidos as usuario, lc.pcs_cliente from lead_carga lc join perfil_usuario pu 
	on lc.id_usuario = pu.id join usuario u
	on pu.id_usuario = u.id
	where lc.codigo_carga = %s;
	"""
	try:
		db = DatabaseConnection()
		if db.connect():
			results = db.execute_query(query, codigo_carga)
			if results:
				return results
			else:
				return None
	except Exception as e:
		return f"Error general: {e}"
	finally:
		db.close_connection()

def get_element_by_upload_code(codigo_carga):
	"""
	The function `get_element_by_upload_code` retrieves information from a database based on a given
	upload code.
	
	:param codigo_carga: The parameter "codigo_carga" is a code used to identify a specific load in the
	database. It is used in the query to retrieve information about that particular load
	:return: the results of the query if there are any, or None if there are no results.
	"""
	query = '''
    select lc.codigo_carga, lc.created_at, u.nombre ||' ' ||u.apellidos as usuario, lc.pcs_cliente, lc.en_nomolestar, lc.en_cooler  from lead_carga lc
    join perfil_usuario pu on lc.id_usuario = pu.id 
    join usuario u on pu.id_usuario = u.id where lc.codigo_carga = %s;'''
	try:
		db = DatabaseConnection()
		if db.connect():
			results = db.execute_query(query, codigo_carga)
			if results:
				return results
			else:
				return None
	except Exception as e:
		return f"Error general: {e}"
	finally:
		db.close_connection()