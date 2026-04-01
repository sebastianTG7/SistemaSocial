from database.db_config import SessionLocal
from database.models import User
from core.security import verify_password

class AuthController:
    @staticmethod
    def login(username, password):
        """
        Valida las credenciales de un usuario.
        Retorna el objeto User si es exitoso, None si falla.
        """
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.username == username, User.activo == True).first()
            if user and verify_password(password, user.password_hash):
                # Retornamos una copia o datos necesarios (evitar problemas de sesión cerrada)
                return {
                    "id": user.id,
                    "username": user.username,
                    "nombre_completo": user.nombre_completo,
                    "rol": user.rol
                }
            return None
        finally:
            db.close()
