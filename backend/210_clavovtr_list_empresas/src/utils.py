import re

def validate_password(new_password):    
    return bool(re.match(r'^(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>])(?=.*[A-Z])(?=.*[a-z]).{8,}$', new_password))

