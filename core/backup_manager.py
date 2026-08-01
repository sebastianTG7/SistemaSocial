import os
import shutil
import json
import sqlite3
import bcrypt
from datetime import date, datetime
from database.db_config import DB_PATH as _DB_PATH_REL

# ── Rutas base ─────────────────────────────────────────────────────────────────
# _BASE_DIR: directorio raíz del proyecto (siempre desde __file__)
_BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# DB_PATH: ruta absoluta real de la BD (igual que en db_config.py)
DB_PATH      = os.path.join(_BASE_DIR, _DB_PATH_REL)
CONFIG_PATH  = os.path.join(_BASE_DIR, "config", "backup_config.json")
DEFAULT_BACKUP_FOLDER = os.path.join(_BASE_DIR, "backups")

# ── Config por defecto ──────────────────────────────────────────────────────────
DEFAULT_CONFIG = {
    "automatico": False,
    "intervalo_dias": 7,          # 1 = diario, 7 = semanal, 30 = mensual
    "carpeta": DEFAULT_BACKUP_FOLDER,
    "ultimo_respaldo": None       # ISO date string "YYYY-MM-DD"
}


class BackupManager:

    @staticmethod
    def get_config() -> dict:
        """Lee la configuración de respaldo desde el JSON."""
        if not os.path.exists(CONFIG_PATH):
            return DEFAULT_CONFIG.copy()
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            # Rellenar claves faltantes con defaults
            for k, v in DEFAULT_CONFIG.items():
                cfg.setdefault(k, v)
            return cfg
        except Exception:
            return DEFAULT_CONFIG.copy()

    @staticmethod
    def save_config(cfg: dict):
        """Guarda la configuración de respaldo en el JSON."""
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2, ensure_ascii=False)

    @staticmethod
    def hacer_respaldo(carpeta: str = None) -> str:
        """
        Copia la BD al carpeta indicada con timestamp en el nombre.
        Retorna la ruta del archivo generado o lanza excepción.
        """
        cfg = BackupManager.get_config()
        destino = carpeta or cfg.get("carpeta") or DEFAULT_BACKUP_FOLDER
        os.makedirs(destino, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_backup = f"servicio_social_backup_{timestamp}.db"
        ruta_destino = os.path.join(destino, nombre_backup)

        if not os.path.exists(DB_PATH):
            raise FileNotFoundError(f"Base de datos no encontrada en: {DB_PATH}")

        shutil.copy2(DB_PATH, ruta_destino)

        # Resetear la contraseña del admin en la COPIA exportada.
        # La base de datos activa NO se modifica.
        # Esto garantiza que al importar en otra PC siempre se pueda
        # acceder con admin / admin123 y luego cambiar la contraseña.
        try:
            hash_defecto = bcrypt.hashpw(
                "admin123".encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")
            con = sqlite3.connect(ruta_destino)
            con.execute(
                "UPDATE usuarios SET password_hash = ? WHERE username = 'admin'",
                (hash_defecto,),
            )
            con.commit()
            con.close()
        except Exception:
            pass  # Si falla, el backup igual se guarda; solo no tiene el reset

        # Actualizar fecha de último respaldo
        cfg["ultimo_respaldo"] = date.today().isoformat()
        BackupManager.save_config(cfg)

        return ruta_destino

    @staticmethod
    def verificar_respaldo_automatico() -> str | None:
        """
        Llama al inicio de la app: si el respaldo automático está activo
        y han pasado >= intervalo_dias desde el último respaldo, lo ejecuta.
        Retorna la ruta del backup creado, o None si no correspondía hacerlo.
        """
        try:
            cfg = BackupManager.get_config()
            if not cfg.get("automatico", False):
                return None

            ultimo = cfg.get("ultimo_respaldo")
            intervalo = int(cfg.get("intervalo_dias", 7))

            if ultimo:
                try:
                    dias_desde = (date.today() - date.fromisoformat(ultimo)).days
                    if dias_desde < intervalo:
                        return None
                except ValueError:
                    pass

            return BackupManager.hacer_respaldo()
        except Exception:
            return None   # El backup falla silenciosamente; la app igual arranca

    @staticmethod
    def ultimo_respaldo_texto() -> str:
        """Devuelve un texto amigable del último respaldo."""
        cfg = BackupManager.get_config()
        ultimo = cfg.get("ultimo_respaldo")
        if not ultimo:
            return "Nunca se ha realizado un respaldo"
        try:
            d = date.fromisoformat(ultimo)
            dias = (date.today() - d).days
            if dias == 0:
                return f"Hoy ({d.strftime('%d/%m/%Y')})"
            elif dias == 1:
                return f"Ayer ({d.strftime('%d/%m/%Y')})"
            else:
                return f"Hace {dias} días ({d.strftime('%d/%m/%Y')})"
        except ValueError:
            return "Fecha desconocida"
