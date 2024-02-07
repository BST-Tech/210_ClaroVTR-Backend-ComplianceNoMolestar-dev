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
				return result if cursor.rowcount >= 1 else "Error al insertar el registro"
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
			print("Conexión a la base de datos cerrada.")
		else:
			print("No hay una conexión activa para cerrar.")

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
        
def get_list_contact_center(uid, id):
    email = get_user_by_id(uid)
    query = f"""select distinct ecc.id,
	cc.nombre,
	tcc.tipo_operador,
	cc.rut,
	cc.razon_social,
	cc.activo
from empresa_contact_center ecc
join contact_center cc on ecc.id_contact_center = cc.id
join tipo_contact_center tcc on cc.id_tipo = tcc.id
where ecc.id_empresa = (select ecc.id_empresa from empresa_contact_center ecc
	join perfil_usuario pu on ecc.id = pu.id_empresa_ct
	join usuario u on pu.id_usuario = u.id
	where u.email = '{email}' ) and ecc.id = {id};"""
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
