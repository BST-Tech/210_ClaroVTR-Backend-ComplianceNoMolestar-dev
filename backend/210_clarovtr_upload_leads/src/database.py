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

def insert_leads(data):
    status = 200
    query ="""
    INSERT INTO public.lead_carga (
        id_empresa_ct,
        id_canal,
        id_usuario,
        pcs_cliente,
        codigo_carga)
        VALUES (%s,%s,%s,%s,%s);"""

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
    return 500

def get_codigo_carga():
    query = """SELECT lc.codigo_carga
    FROM lead_carga lc
    WHERE lc.created_at >= CURRENT_DATE
    AND lc.created_at < CURRENT_DATE + INTERVAL '1 day'ORDER BY lc.created_at  DESC
    LIMIT 1;"""
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
    return 500
    
    
    
    