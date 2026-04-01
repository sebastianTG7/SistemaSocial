import bcrypt

def hash_password(password: str) -> str:
    """Encripta la contraseña usando bcrypt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verifica si la contraseña ingresada coincide con el hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
