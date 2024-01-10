from shared.secret_manager import get_value_secret
import psycopg2

class DatabaseConnection:
	def connect(self):
		"""
		The function connects to a PostgreSQL database using environment variables for the database name,
		username, password, and host.
		:return: The code is returning the connection object if the connection to the database is
		successful. If there is an error connecting to the database, it will print an error message and
		return None.
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
			print(f"Error al conectar a la base de datos: {e}")
			return None

	def execute_many_querys(self, query, params:list=None):
		"""
		The function `execute_many_querys` executes a query multiple times with different parameters in a
		database connection.
		
		:param query: The query parameter is a string that represents the SQL query you want to execute. It
		should be a valid SQL statement that can be executed by the database
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
				print(f"Error al ejecutar la consulta: {e}")
				return None
		else:
			return "No se ha establecido una conexión a la base de datos."

	def execute_query(self, query, params:str=None):
		"""
		The function `execute_query` executes a SQL query using a provided connection and returns the
		result, or an error message if there is a problem.
		
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

	def execute_update(self, query, params:str=None):
		"""
		The function `execute_update` executes an update query on a PostgreSQL database using the provided
		query and parameters.
		
		:param query: The query parameter is a string that represents the SQL query you want to execute. It
		should be a valid SQL statement that can be executed by the database
		:param params: The `params` parameter is a string that contains the values to be substituted into
		the query. It is used to prevent SQL injection by safely passing user input as parameters to the
		query
		:type params: str
		:return: The function `execute_update` returns a string. If the connection to the database is
		established and the query is executed successfully, it returns "actualizada correctamente" (updated
		correctly). If there is an error while executing the query, it returns an error message. If there is
		no connection to the database, it returns "No se ha establecido una conexión a la base de datos."
		(No connection
		"""
		if self.connection is not None:
			try:
				cursor = self.connection.cursor()
				cursor.execute(query, (params,))
				cursor.close()
				return "actualizada correctamente"
			# except Exception as e:
			except psycopg2.Error as e:
				return f"Error al ejecutar la consulta: {e}"
		else:
			return "No se ha establecido una conexión a la base de datos."

	def close_connection(self):
		"""
		The close_connection function closes the connection to a database if it is active, otherwise it
		prints a message indicating that there is no active connection to close.
		"""
		if self.connection is not None:
			self.connection.commit()
			self.connection.close()
			print("Conexión a la base de datos cerrada.")
		else:
			print("No hay una conexión activa para cerrar.")        

def get_data_contact_center(email, id_ct):
	"""
	The function `get_data_contact_center` retrieves contact center data for a given email and contact
	center ID from a database.
	
	:param email: The email parameter is the email address of the user for whom you want to retrieve
	contact center data
	:param id_ct: The parameter "id_ct" is the ID of the contact center. It is used to filter the data
	and retrieve information specific to a particular contact center
	:return: the results of the query executed on the database.
	"""
	query = f"""select pu.id, max(u.nombre) as nombre,
		max(u.apellidos) as apellidos, max(pu.last_login) as last_login,
		count(lc.id) as validaciones, max(cc.nombre) as contact_center,
		max(cc.activo) as cc_activo, max(g.loaded_at) as last_load
	from perfil_usuario pu
	join usuario u on pu.id_usuario = u.id
	left join lead_carga lc on lc.id_usuario = u.id
	join empresa_contact_center ecc on pu.id_empresa_ct = ecc.id
	join contact_center cc on ecc.id_contact_center = cc.id
	left join (select g.id_lead_carga , max(g.loaded_at) as loaded_at
		from gestion g group by id_lead_carga) g on g.id_lead_carga = lc.id
	where ecc.id_empresa = (select distinct ecc.id_empresa  from perfil_usuario pu join empresa_contact_center ecc
	on pu.id_empresa_ct = ecc.id join usuario u
	on pu.id_usuario = u.id where u.email = '{email}')
	and ecc.id = {id_ct}
	group by pu.id ;
	"""
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


