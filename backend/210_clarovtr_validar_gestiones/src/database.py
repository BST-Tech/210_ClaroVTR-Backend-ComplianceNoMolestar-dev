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

	def execute_like_query(self, query):
		if self.connection is not None:
			try:
				cursor = self.connection.cursor()
				cursor.execute(query)
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

def insert_gestiones(data):
    status = 200
    query ="""
    INSERT INTO public.gestion (
        tipificacion, 
        pcs_salida, 
        pcs_cliente,
        fecha_llamada, 
        codigo_carga, 
        canal_o_nombre_eps,
        campania,
        segundos_llamada,
        operador_id_ejecutivo,
        id_usuario)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
        """

    try:
        db = DatabaseConnection()
        if db.connect():
            results = db.execute_many_querys(query, data)
            if results:
                print(results)
                return results
            else:
                return None
    except Exception as e:
        print(f"Error general: {e}")
    finally:
        db.close_connection()
    return status

def get_element_by_upload_code(codigo_carga):
    query = '''
    select lc.codigo_carga, lc.created_at, u.nombre ||' ' ||u.apellidos as usuario, lc.pcs_cliente, lc.en_nomolestar, lc.en_cooler  from lead_carga lc
    join perfil_usuario pu on lc.id_usuario = pu.id 
    join usuario u on pu.id_usuario = u.id where lc.codigo_carga = %s;'''
	#query = "select * from lead_carga lc where lc.codigo_carga = %s;"
    try:
        db = DatabaseConnection()
        if db.connect():
            results = db.execute_query(query, codigo_carga)
            if results:
                return results
            else:
                return None
    except Exception as e:
        print(f"Error general: {e}")
    finally:
        db.close_connection()

def get_element_by_upload_code_group_by(codigo_carga):
	query = "select * from lead_carga lc where lc.codigo_carga = %s;"
	try:
		db = DatabaseConnection()
		if db.connect():
			print("conecto")
			results = db.execute_query(query, codigo_carga)
			if results:
				return results
			else:
				return None
	except Exception as e:
		print(f"Error general: {e}")
	finally:
		db.close_connection()

def get_data_user(email_user):
    status = 500
    query = "select pu.id, pu.id_empresa_ct from usuario u join perfil_usuario pu on u.id = pu.id_usuario where u.email = %s;"
    try:
        db = DatabaseConnection()
        if db.connect():
            results = db.execute_query(query, email_user)
            if results:
                return results
            else:
                return None
    except Exception as e:
        print(f"Error general: {e}")
    finally:
        db.close_connection()
    return status

def update_resumen_lead_carga(upload_code):
    status = 500
    query = "select insertar_resumen_lead_carga(%s);"
    try:
        db = DatabaseConnection()
        if db.connect():
            results = db.execute_query(query, upload_code)
            if results:
                return results
            else:
                return None
    except Exception as e:
        print(f"Error general: {e}")
    finally:
        db.close_connection()
    return status

def get_tipificaciones(value):
    data_consult = '%' + value + '%'
    query = f"select distinct t.nombre_tipificacion, id from tipificacion t where t.nombre_tipificacion like '{data_consult}';"
    try:
        db = DatabaseConnection()
        if db.connect():
            results = db.execute_like_query(query)
            if results:
                return results
            else:
                return None
    except Exception as e:
        print(f"Error general: {e}")
    finally:
        db.close_connection()
        
def get_data_user(email_user):
    query = "select pu.id, pu.id_empresa_ct from usuario u join perfil_usuario pu on u.id = pu.id_usuario where u.email = %s;"
    try:
        db = DatabaseConnection()
        if db.connect():
            results = db.execute_query(query, email_user)
            if results:
                return results
            else:
                return None
    except Exception as e:
        print(f"Error general: {e}")
    finally:
        db.close_connection()