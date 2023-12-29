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
			print("No se ha establecido una conexión a la base de datos.")
			return None

	def execute_without_return(self, query, params:str=None):
		if self.connection is not None:
			try:
				cursor = self.connection.cursor()
				cursor.execute(query, (params,))
				cursor.close()
				return "Actualizado correctamente"
			# except Exception as e:
			except psycopg2.Error as e:
				print(e)
                
				return f"Error al ejecutar la consulta: {e}"
		else:
			print("No se ha establecido una conexión a la base de datos.")
			return None

	def close_connection(self):
		if self.connection is not None:
			self.connection.commit()
			self.connection.close()
			# print("Conexión a la base de datos cerrada.")
		else:
			print("No hay una conexión activa para cerrar.")

def get_id_ct(uid):
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
        
def get_user_data_email(user_id):
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
    
def put_empresa_contact_center(data_updated, id, email):
    activo = data_updated.get('activo')
    nombre = data_updated.get('nombre')
    razon_social = data_updated.get('razon_social')
    tipo = data_updated.get('tipo')
    
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    query_ct = f"""UPDATE public.contact_center
    SET id_tipo={tipo}, nombre='{nombre}', razon_social='{razon_social}', updated_at='{timestamp}', activo={activo} WHERE id = (select cc.id from empresa_contact_center ecc
    join contact_center cc on ecc.id_contact_center = cc.id where ecc.id_empresa = (select ecc.id_empresa from empresa_contact_center ecc
	join perfil_usuario pu on ecc.id = pu.id_empresa_ct
	join usuario u on pu.id_usuario = u.id
	where u.email = '{email}' ) and ecc.id = {id});
    """
    print(query_ct)
    try:
        db = DatabaseConnection()
        if db.connect():
            return db.execute_without_return(query_ct)
    except Exception as e:
        return f"Error general: {e}"
    finally:
        db.close_connection()


