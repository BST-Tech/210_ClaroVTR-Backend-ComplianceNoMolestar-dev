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

def get_leads_by_count(uid):
    query_count_leads = """
    SELECT
        COUNT(*) AS total_leads,
        COUNT(CASE WHEN l.en_nomolestar = 1 THEN 1 END) AS en_nomolestar,
        (SELECT COUNT(1) FROM lead_cooler lc WHERE lc.activo = 1) AS leads_en_cooler,
        (SELECT COUNT(1) FROM lead_cooler lc WHERE lc.activo = 0) AS leads_liberados,
        (SELECT COUNT(1) FROM gestion g) AS total_gestiones
    FROM lead l;
    """

    try:
        db = DatabaseConnection()
        if db.connect():

            # Devolver el resultado
            return db.execute_query(query_count_leads)
    except Exception as e:
        return f"Error general: {e}"
    finally:
        db.close_connection()
