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

	def close_connection(self):
		if self.connection is not None:
			self.connection.commit()
			self.connection.close()
		else:
			print("No hay una conexión activa para cerrar.")

def list_reglas(uid):
    email = get_user_by_id(uid)
    # query=f"""
    # select r.id, r.nombre, r.dias_rango, r.numero_incidencias, r.dias_permanencia, r.activa from regla r where r.id_empresa = (select ecc.id_empresa from empresa_contact_center ecc
    #     join perfil_usuario pu on ecc.id = pu.id_empresa_ct
    #     join usuario u on pu.id_usuario = u.id
    #     where u.email = '{email}');"""
    query=f"""
		select r.id, r.nombre, r.dias_rango, r.numero_incidencias, r.dias_permanencia, r.activa, te.tipo_evento, te.descripcion from regla r 
		join tipo_evento te on r.id_tipo_evento  = te.id 
		where r.id_empresa = (select ecc.id_empresa from empresa_contact_center ecc
				join perfil_usuario pu on ecc.id = pu.id_empresa_ct
				join usuario u on pu.id_usuario = u.id
				where u.email = '{email}');"""
    try:
        db = DatabaseConnection()
        if db.connect():
            return db.execute_query(query)
    except Exception as e:
        return f"Error general: {e}"
    finally:
        db.close_connection()
        
        
