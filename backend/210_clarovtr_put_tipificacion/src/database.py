from shared.secret_manager import get_value_secret
import psycopg2

import time
import datetime


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

    def execute_update(self, query, params: str = None):
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


def get_tipificacion_by_id(uid, tipificacion_id):
    # email = get_user_by_id(uid)
    #    query = f"""
    # select t.id, t.tipificacion, t.nombre_tipificacion, t.contacto, t.venta, t.activo, ecc.id_contact_center from tipificacion t join empresa_contact_center ecc
    # on ecc.id = t.id_empresa_ct join perfil_usuario pu
    # on pu.id_empresa_ct = ecc.id join usuario u
    # on u.id = pu.id_usuario
    # where u.email ='{email}' and t.id = {tipificacion_id}"""
    query = f"""
	select t.id, t.tipificacion, t.nombre_tipificacion, t.contacto, t.venta, t.activo, ecc.id_contact_center from tipificacion t join empresa_contact_center ecc
	on ecc.id = t.id_empresa_ct 
	where t.id = {tipificacion_id};"""
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


def update_data_tipificaciones(data, id):
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    values = create_query_set(data)
    query = (
        "UPDATE tipificacion SET "
        + values
        + f",updated_at = '{timestamp}' WHERE id = {id};"
    )
    print(query)
    try:
        db = DatabaseConnection()
        if db.connect():
            return db.execute_update(query)
    except Exception as e:
        return f"Error general: {e}"
    finally:
        db.close_connection()


def create_query_set(data_users):
    values = ""
    for data in data_users:
        values = f"{data['key']} = '{data['value']}' ," + values
    return values.rstrip(",")
