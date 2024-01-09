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

	def close_connection(self):
		if self.connection is not None:
			self.connection.commit()
			self.connection.close()
			print("Conexión a la base de datos cerrada.")
		else:
			print("No hay una conexión activa para cerrar.")
        
def list_tipo_evento(uid):
    # email = get_user_by_id(uid)
#     query=f"""select distinct tcc.id, tcc.tipo_operador from perfil_usuario pu join empresa_contact_center ecc on pu.id_empresa_ct = ecc.id
# join contact_center cc on ecc.id_contact_center = cc.id
# join tipo_contact_center tcc ON cc.id_tipo = tcc.id
# where ecc.id_empresa = (select distinct ecc.id_empresa  from empresa_contact_center ecc
# join perfil_usuario pu on ecc.id = pu.id_empresa_ct
# join usuario u on pu.id_usuario = u.id 
# where u.email ='{email}');"""
    query="""select te.id, te.tipo_evento from tipo_evento te;"""
    try:
        db = DatabaseConnection()
        if db.connect():
            return db.execute_query(query)
    except Exception as e:
        return f"Error general: {e}"
    finally:
        db.close_connection()
    
    
    
    
    
    


