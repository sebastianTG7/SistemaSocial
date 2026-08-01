from database.db_config import SessionLocal
from database.models import User
from core.security import verify_password, hash_password

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
                return {
                    "id": user.id,
                    "username": user.username,
                    "nombre_completo": user.nombre_completo,
                    "rol": user.rol
                }
            return None
        finally:
            db.close()

    @staticmethod
    def cambiar_password(user_id: int, nueva_password: str) -> bool:
        """Actualiza el hash de la contrasena de un usuario. Retorna True si tuvo exito."""
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return False
            user.password_hash = hash_password(nueva_password)
            db.commit()
            return True
        except Exception:
            db.rollback()
            return False
        finally:
            db.close()
