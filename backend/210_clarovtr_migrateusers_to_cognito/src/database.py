import os
import sys
from sqlite3 import DatabaseError
import psycopg2

class DatabaseConnection:
	def connect(self):
		try:
			self.connection = psycopg2.connect(
                dbname=os.environ['DB_NAME'],
                user=os.environ['DB_USERNAME'],
                password=os.environ['DB_PASSWORD'],
				host=os.environ['DB_HOST'])
			return self.connection
		except Exception as e:
			print(f"Error al conectar a la base de datos: {e}")
			return None

	def execute_query(self, query, params=None):
		if self.connection is not None:
			try:
				cursor = self.connection.cursor()
				cursor.execute(query, params)
				result = cursor.fetchall()
				cursor.close()
				return result
			except Exception as e:
				print(f"Error al ejecutar la consulta: {e}")
				return None
		else:
			print("No se ha establecido una conexión a la base de datos.")
			return None

	def close_connection(self):
		if self.connection is not None:
			self.connection.close()
			print("Conexión a la base de datos cerrada.")
		else:
			print("No hay una conexión activa para cerrar.")

def get_element_by_email(username, password):   
	query = 'select first_name, last_name from users where username = %s and password = %s;'
	params = (username, password)
	try:
		db = DatabaseConnection()
		if db.connect():
			results = db.execute_query(query, params)
			if results:
				print(results)
				return results
			else:
				return None
	except Exception as e:
		print(f"Error general: {e}")
	finally:
		db.close_connection()