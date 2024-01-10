import os
import sys
from sqlite3 import DatabaseError
from shared.secret_manager import get_value_secret
import psycopg2

class DatabaseConnection:
	def connect(self):
		environ = get_value_secret()
	#	print(environ)
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

	def close_connection(self):
		if self.connection is not None:
			self.connection.commit()
			self.connection.close()
			print("Conexión a la base de datos cerrada.")
		else:
			print("No hay una conexión activa para cerrar.")

def get_data_resume():
	query = "select rl.fecha_carga, rl.usuario, rl.cnt_leads, rl.en_nomolestar, rl.en_cooler, rl.validos_llamada, rl.id_empresa_ct, rl.codigo_carga from resumen_lead_carga rl where TO_DATE(fecha_carga, 'DD-MM-YYYY') >= (NOW() - INTERVAL '1 month') AND TO_DATE(fecha_carga, 'DD-MM-YYYY') < NOW();"
	try:
		db = DatabaseConnection()
		if db.connect():
			print("conecto")
			results = db.execute_query(query)
			if results:
				return results
			else:
				return None
	except Exception as e:
		print(f"Error general: {e}")
	finally:
		db.close_connection()
