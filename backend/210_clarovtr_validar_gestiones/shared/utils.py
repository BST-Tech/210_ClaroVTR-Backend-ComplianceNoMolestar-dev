import uuid
from datetime import datetime


def generate_load_code_id():
    return uuid.uuid4().hex

def convert_date(value):
    return datetime.strptime(value, '%d-%m-%Y').strftime('%d-%m-%Y %H:%M:%S')

def format_date(date):
    fecha_obj = datetime.strptime(date, '%d-%m-%Y')
    return fecha_obj.strftime('%Y-%m-%d')





