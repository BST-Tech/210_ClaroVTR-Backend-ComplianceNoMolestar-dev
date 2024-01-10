from shared.secret_manager import get_value_secret
import psycopg2

# The `DatabaseConnection` class provides methods to establish a connection to a PostgreSQL database,
# execute SQL queries, and close the connection.
class DatabaseConnection:
	def connect(self):
		"""
		The function `connect` establishes a connection to a PostgreSQL database using environment variables
		for the database name, username, password, and host.
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
		can be any valid SQL statement, such as SELECT, INSERT, UPDATE, DELETE, etc
		:param params: The `params` parameter is a list of tuples or lists containing the values to be used
		in the query. Each tuple or list represents a set of values for a single execution of the query. The
		number of values in each tuple or list should match the number of placeholders in the query
		:type params: list
		:return: If the connection to the database is not established, the function will return the string
		"No se ha establecido una conexión a la base de datos." If there is an error executing the query,
		the function will print an error message and return None.
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
		The function `execute_query` executes a SQL query using a cursor and returns the result, or returns
		an error message if there is a problem with the query or the database connection.
		
		:param query: The query parameter is a string that represents the SQL query you want to execute. It
		can be any valid SQL statement, such as SELECT, INSERT, UPDATE, DELETE, etc. This query will be
		executed on the database
		:param params: The `params` parameter is a string that represents the parameters to be passed to the
		query. It is used to prevent SQL injection by safely passing user input as parameters to the query.
		The `params` value is passed as a tuple to the `execute` method of the cursor object
		:type params: str
		:return: the result of the query execution if the connection to the database is established. If
		there is an error during the execution of the query, it prints the error message and returns None.
		If there is no connection to the database, it returns the string "No se ha establecido una conexión
		a la base de datos" (which means "No connection to the database has been established" in
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
		The close_connection function checks if there is an active connection and if so, commits any pending
		changes and closes the connection; otherwise, it prints a message indicating that there is no active
		connection to close.
		"""
		if self.connection is not None:
			self.connection.commit()
			self.connection.close()
		else:
			print("No hay una conexión activa para cerrar.")

def get_data_resume():
	"""
	The function `get_data_resume` retrieves data from a database table called `resumen_lead_carga` for
	the past month.
	:return: the results of the query executed on the database.
	"""
	query = "select rl.fecha_carga, rl.usuario, rl.cnt_leads, rl.en_nomolestar, rl.en_cooler, rl.validos_llamada, rl.id_empresa_ct, rl.codigo_carga from resumen_lead_carga rl where TO_DATE(fecha_carga, 'DD-MM-YYYY') >= (NOW() - INTERVAL '1 month') AND TO_DATE(fecha_carga, 'DD-MM-YYYY') < NOW();"
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
		raise e
	finally:
		db.close_connection()