from sqlite3 import DatabaseError
from shared.secret_manager import get_value_secret
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
			print("Conexión a la base de datos cerrada.")
		else:
			print("No hay una conexión activa para cerrar.")        

def get_data_contact_center(email, id_ct):
#     query = f"""select pu.id, max(u.nombre) as nombre,
# 	max(u.apellidos) as apellidos, max(pu.last_login) as last_login,
# 	count(lc.id) as validaciones, max(cc.nombre) as contact_center,
# 	max(cc.activo) as cc_activo
# from perfil_usuario pu
# join usuario u on pu.id_usuario = u.id
# join lead_carga lc on lc.id_usuario = u.id
# join empresa_contact_center ecc on pu.id_empresa_ct = ecc.id
# join contact_center cc on ecc.id_contact_center = cc.id
# where ecc.id_empresa = (
# 	select distinct ecc.id_empresa from perfil_usuario pu join empresa_contact_center ecc 
# on pu.id_empresa_ct = ecc.id join usuario u 
# on pu.id_usuario = u.id where u.email = '{email}'
# 	) and ecc.id_contact_center = {id_ct}
# 	group by pu.id limit 1;""" 
	query = f"""select pu.id, max(u.nombre) as nombre,
		max(u.apellidos) as apellidos, max(pu.last_login) as last_login,
		count(lc.id) as validaciones, max(cc.nombre) as contact_center,
		max(cc.activo) as cc_activo, max(g.loaded_at) as last_load
	from perfil_usuario pu
	join usuario u on pu.id_usuario = u.id
	left join lead_carga lc on lc.id_usuario = pu.id
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


