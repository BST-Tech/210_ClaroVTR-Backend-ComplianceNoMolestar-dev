import time
import datetime
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
	def execute_update(self, query, params:str=None):
		if self.connection is not None:
			try:
				cursor = self.connection.cursor()
				cursor.execute(query, (params,))
				cursor.close()
				return "actualizada correctamente"
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
		else:
			print("No hay una conexión activa para cerrar.")

def get_regla_by_id(uid, regla_id):
    email = get_user_by_id(uid)
    query=f"""
    select r.id, r.nombre, r.dias_rango, r.numero_incidencias, r.dias_permanencia, r.activa from regla r where r.id_empresa = (select ecc.id_empresa from empresa_contact_center ecc
        join perfil_usuario pu on ecc.id = pu.id_empresa_ct
        join usuario u on pu.id_usuario = u.id
        where u.email = '{email}') and r.id = {regla_id};"""
    try:
        db = DatabaseConnection()
        if db.connect():
            return db.execute_query(query)
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

def put_regla_negocio(data_updated, id, email):
	activo = int(data_updated.get('activo'))
	nombre = data_updated.get('nombre')
	rango_fecha = int(data_updated.get('rango_fecha'))
	incidencias = int(data_updated.get('incidencias'))
	dias_cooler = int(data_updated.get('dias_cooler'))
	tipo_evento = int(data_updated.get('tipo_evento'))
	id_canal = int(data_updated.get('id_canal'))
    
	timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
	query_regla_negocio = f"""UPDATE public.regla
	SET id_canal={id_canal}, id_empresa=(select ecc.id_empresa from empresa_contact_center ecc
	join perfil_usuario pu on ecc.id = pu.id_empresa_ct
	join usuario u on pu.id_usuario = u.id
	where u.email = '{email}' ), id_tipo_evento={tipo_evento}, nombre='{nombre}', dias_rango={rango_fecha}, numero_incidencias={incidencias}, dias_permanencia={dias_cooler},
	updated_at='{timestamp}', activa={activo}
	WHERE id={id};
	"""
	print(query_regla_negocio)
	try:
		db = DatabaseConnection()
		if db.connect():
			result = db.execute_update(query_regla_negocio)
			print(result)
			return result
	except Exception as e:
		return f"Error general: {e}"
	finally:
		db.close_connection()