import os
import sys
from sqlite3 import DatabaseError
from shared.secret_manager import get_value_secret
from src.cognito import get_user_by_id
import psycopg2

class DatabaseConnection:
	def connect(self):
		environ = get_value_secret()
		#print(environ)
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
				result = cursor.executemany(query, params)
				print(result)

				cursor.close()
			except Exception as e:
				print(f"Error al ejecutar la consulta: {e}")
				return None
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
				return f"Error al ejecutar la consulta: {e}"
		else:
			return "No se ha establecido una conexión a la base de datos."

	def close_connection(self):
		if self.connection is not None:
			self.connection.commit()
			self.connection.close()
		else:
			print("No hay una conexión activa para cerrar.")

# def insert_gestiones(data):
#     status = 200
#     query ="""
#     INSERT INTO public.gestion (
#         id_lead_carga,
#         id_usuario,
#         id_tipificacion,
#         operador_id_ejecutivo,
#         pcs_salida, 
#         pcs_cliente,
#         venta,
#         contacto,
#         segundos_llamada,
#         codigo_carga,
#         fecha_llamada,
#         tipificacion,
#         campania,
#         canal_o_nombre_eps,
#         loaded_at,
#         updated_at,
#         id_empresa,
#         id_canal,
#         id_empresa_ct,
#         procesada)
#         VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
#         """

#     try:
#         db = DatabaseConnection()
#         if db.connect():
#             results = db.execute_many_querys(query, data)
#             if results:
#                 print(results)
#                 return results
#             else:
#                 return None
#     except Exception as e:
#         print(f"Error general: {e}")
#     finally:
#         db.close_connection()
#     return status
def insert_gestiones(data):
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
    print(query)
    print(data)
    try:
        db = DatabaseConnection()
        if db.connect():
            db.execute_many_querys(query, data)
    except Exception as e:
        print(f"Error general: {e}")
    finally:
        db.close_connection()
        
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
    query = "select pu.id, pu.id_empresa_ct from perfil_usuario pu join usuario u on u.id = pu.id_usuario where u.email = %s;"
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

def get_tipificaciones(value, id_empresa_ct):
    data_consult = '%' + value + '%'
    query = f"select distinct t.tipificacion, t.id from tipificacion t where t.tipificacion like '{data_consult}' and t.id_empresa_ct = {id_empresa_ct};"
    try:
        db = DatabaseConnection()
        if db.connect():
            return db.execute_like_query(query)
    except Exception as e:
        return f"Error general: {e}"
    finally:
        db.close_connection()
        
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