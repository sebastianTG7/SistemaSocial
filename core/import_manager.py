import os
import shutil
import sqlite3
from datetime import datetime
from database.db_config import DB_PATH as _DB_PATH_REL

# ── Rutas base ────────────────────────────────────────────────────────────────
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH   = os.path.join(_BASE_DIR, _DB_PATH_REL)

# Tablas mínimas que debe tener una BD válida del sistema
TABLAS_REQUERIDAS = {
    "personas",
    "atenciones",
    "cat_facultades",
    "cat_escuelas",
    "cat_modalidades",
    "cat_casos_sociales",
    "cat_tipos_usuario",
}


class ImportManager:

    @staticmethod
    def validar_bd(ruta_db: str) -> tuple[bool, str]:
        """
        Verifica que el archivo .db seleccionado es una BD SQLite
        compatible con el sistema (contiene las tablas requeridas).

        Retorna (True, "OK") si es válida, o (False, mensaje_error) si no.
        """
        if not os.path.isfile(ruta_db):
            return False, "El archivo no existe o la ruta es inválida."

        if os.path.getsize(ruta_db) == 0:
            return False, "El archivo está vacío."

        try:
            conn = sqlite3.connect(ruta_db)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tablas_encontradas = {row[0] for row in cursor.fetchall()}
            conn.close()
        except sqlite3.DatabaseError:
            return False, "El archivo seleccionado no es una base de datos SQLite válida."

        faltantes = TABLAS_REQUERIDAS - tablas_encontradas
        if faltantes:
            return False, (
                f"El archivo no es compatible con este sistema.\n"
                f"Tablas faltantes: {', '.join(sorted(faltantes))}"
            )

        return True, "OK"

    @staticmethod
    def obtener_resumen(ruta_db: str) -> dict:
        """
        Lee estadísticas básicas de la BD a importar para mostrar
        al usuario antes de confirmar (cantidad de personas, atenciones).
        """
        resumen = {"personas": 0, "atenciones": 0, "error": None}
        try:
            conn = sqlite3.connect(ruta_db)
            cursor = conn.cursor()
            resumen["personas"]   = cursor.execute("SELECT COUNT(*) FROM personas").fetchone()[0]
            resumen["atenciones"] = cursor.execute("SELECT COUNT(*) FROM atenciones").fetchone()[0]
            conn.close()
        except Exception as ex:
            resumen["error"] = str(ex)
        return resumen

    @staticmethod
    def importar_bd(ruta_db: str) -> tuple[bool, str]:
        """
        Proceso de importación:
          1. Hace backup automático de la BD actual (protección).
          2. Reemplaza database/servicio_social.db con el archivo importado.
          3. Retorna (True, ruta_backup) si ok, o (False, mensaje_error).
        """
        # 1. Backup automático de la BD actual
        backup_dir = os.path.join(_BASE_DIR, "backups")
        os.makedirs(backup_dir, exist_ok=True)

        timestamp   = datetime.now().strftime("%Y%m%d_%H%M%S")
        ruta_backup = os.path.join(backup_dir, f"pre_import_backup_{timestamp}.db")

        try:
            if os.path.exists(DB_PATH):
                shutil.copy2(DB_PATH, ruta_backup)
        except Exception as ex:
            return False, f"No se pudo crear el respaldo automático antes de importar:\n{ex}"

        # 2. Reemplazar la BD actual con la importada
        try:
            os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
            shutil.copy2(ruta_db, DB_PATH)
        except PermissionError:
            # Intentar restaurar el backup si falla
            if os.path.exists(ruta_backup):
                shutil.copy2(ruta_backup, DB_PATH)
            return False, (
                "No se pudo reemplazar la base de datos porque está en uso.\n"
                "Cierra cualquier otra instancia del sistema e intenta nuevamente."
            )
        except Exception as ex:
            if os.path.exists(ruta_backup):
                shutil.copy2(ruta_backup, DB_PATH)
            return False, f"Error al importar la base de datos:\n{ex}"

        return True, ruta_backup
