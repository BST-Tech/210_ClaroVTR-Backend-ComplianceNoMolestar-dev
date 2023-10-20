import uuid
import bcrypt
from datetime import datetime


def generate_load_code_id():
    return uuid.uuid4().hex

def convert_date(value):
    return datetime.strptime(value, '%d-%m-%Y').strftime('%d-%m-%Y %H:%M:%S')

def format_date(date):
    fecha_obj = datetime.strptime(date, '%d-%m-%Y')
    return fecha_obj.strftime('%Y-%m-%d')

def format_date_crud(date):
    if date != None:
        return date.strftime('%d-%m-%Y %H:%M:%S')
    else:
        return None

def extract_keys(dictionary):
    return [key for key in dictionary]

def encript_password(password):
    password_bytes = password.encode("utf-8")
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode("utf-8")

def validate_password_hash(password):
    password_bytes = password.encode("utf-8")
    return bcrypt.checkpw(password_bytes,  bcrypt.hashpw(password_bytes, bcrypt.gensalt()))

def extract_keys_and_values(data, fields):
    return [f"{key} = '{data[key]}'" for key in fields]
