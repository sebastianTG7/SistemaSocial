import sys
import os
import shutil
sys.path.append(os.getcwd())

from database.db_config import SessionLocal
from sqlalchemy import text

def run_migration():
    # 1. Back up database
    db_path = os.path.join("database", "servicio_social.db")
    backup_path = os.path.join("database", "servicio_social_backup_before_cleanup.db")
    print(f"Haciendo copia de seguridad de la base de datos...")
    shutil.copyfile(db_path, backup_path)
    print(f"Copia de seguridad guardada en: {backup_path}")

    db = SessionLocal()
    try:
        # A. Reasignar estudiantes de 'Biología y Química' (ID 30) a 'Biología, Química y Ciencia del Ambiente' (ID 17)
        res = db.execute(text("UPDATE personas SET escuela_id = 17 WHERE escuela_id = 30"))
        print(f"Migrados {res.rowcount} estudiantes de 'Biología y Química' (ID 30) a 'Biología, Química y Ciencia del Ambiente' (ID 17).")

        # B. Reasignar estudiantes de Escuela ID 36 a Escuela ID 12
        res = db.execute(text("UPDATE personas SET escuela_id = 12, facultad_id = 9 WHERE escuela_id = 36"))
        print(f"Migrados {res.rowcount} estudiantes de Escuela ID 36 a Escuela ID 12.")

        # C. Reasignar estudiantes de Facultad ID 16 a Facultad ID 9
        res = db.execute(text("UPDATE personas SET facultad_id = 9 WHERE facultad_id = 16"))
        print(f"Migrados {res.rowcount} estudiantes de Facultad ID 16 a Facultad ID 9.")

        # D. Eliminar entradas obsoletas de los catálogos
        print("Eliminando registros obsoletos de catálogos...")
        
        res = db.execute(text("DELETE FROM cat_escuelas WHERE id = 30"))
        print(f"  - Escuela ID 30 eliminada ({res.rowcount} fila).")

        res = db.execute(text("DELETE FROM cat_escuelas WHERE id = 36"))
        print(f"  - Escuela ID 36 eliminada ({res.rowcount} fila).")

        res = db.execute(text("DELETE FROM cat_facultades WHERE id = 16"))
        print(f"  - Facultad ID 16 eliminada ({res.rowcount} fila).")

        db.commit()
        print("¡Limpieza de catálogos completada exitosamente!")
    except Exception as e:
        db.rollback()
        print(f"ERROR DURANTE LA MIGRACIÓN: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    run_migration()
