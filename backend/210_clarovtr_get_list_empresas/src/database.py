import os
import sys
from sqlite3 import DatabaseError
from shared.secret_manager import get_value_secret
from shared.cognito import get_user_by_id
import psycopg2


class DatabaseConnection:
    def connect(self):
        environ = get_value_secret()
        try:
            self.connection = psycopg2.connect(
                dbname=environ["DB_NAME"],
                user=environ["DB_USERNAME"],
                password=environ["DB_PASSWORD"],
                host=environ["DB_HOST"],
            )
            return self.connection
        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None

    def execute_many_querys(self, query, params: list = None):
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

    def execute_query(self, query, params: str = None):
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


def get_users_list(uid):
    email = get_user_by_id(uid)
    query = """
	select p.id, u.nombre, u.apellidos, u.email, cc.id, u.activo as estado, p.id_rol ,r.nombre as rol, cc.nombre as nombre_contact_center, e.nombre as nombre_empresa, p.id_empresa_ct
		from perfil_usuario p
		join empresa_contact_center ecc on p.id_empresa_ct = ecc.id
		join contact_center cc on ecc.id_contact_center = cc.id
		join usuario u on p.id_usuario = u.id
		join rol r on p.id_rol = r.id 
		join empresa e on e.id = ecc.id_empresa 
		where u.email = %s"""
    try:
        db = DatabaseConnection()
        if db.connect():
            results = db.execute_query(query, email)
            if results:
                return results
            else:
                return None
    except Exception as e:
        print(f"Error general: {e}")
    finally:
        db.close_connection()

