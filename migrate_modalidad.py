import sqlite3
import shutil
import os
import sys
from datetime import datetime

# Añadir el directorio raíz al path para poder importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Definir rutas
DB_PATH = 'database/servicio_social.db'
BACKUP_PATH = f'database/servicio_social_backup_modalidad_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'

def run_migration():
    if not os.path.exists(DB_PATH):
        print(f"Error: Base de datos no encontrada en {DB_PATH}")
        return

    # 1. Crear Backup
    print("1. Creando backup de seguridad...")
    shutil.copy2(DB_PATH, BACKUP_PATH)
    print(f"   Backup creado en: {BACKUP_PATH}")

    # 2. Renombrar tablas antiguas
    print("2. Renombrando tablas antiguas...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Eliminar índices viejos si existen para evitar conflictos con SQLAlchemy
        cursor.execute("DROP INDEX IF EXISTS ix_personas_dni")
        cursor.execute("DROP INDEX IF EXISTS ix_personas_id")
        cursor.execute("DROP INDEX IF EXISTS ix_atenciones_id")
        
        cursor.execute("ALTER TABLE personas RENAME TO personas_old_mod")
        cursor.execute("ALTER TABLE atenciones RENAME TO atenciones_old_mod")
        conn.commit()
    except sqlite3.OperationalError as e:
        print(f"   Nota: Las tablas podrían estar ya renombradas o no existen. Detalle: {e}")
    conn.close()

    # 3. Crear las nuevas tablas usando SQLAlchemy
    print("3. Creando el nuevo esquema de la base de datos mediante SQLAlchemy...")
    from database.db_config import engine, Base
    from database.models import Persona, Atencion
    Base.metadata.create_all(bind=engine)
    print("   Nuevas tablas (personas y atenciones) creadas correctamente.")

    # 4. Migrar los Datos (Consultas SQL)
    print("4. Migrando datos a las nuevas tablas...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # A. Migrar Personas recuperando modalidad_id y registro_modalidad de la última atención
        print("   -> Insertando Personas y recuperando Modalidad de sus atenciones previas...")
        cursor.execute("""
            INSERT INTO personas (id, dni, nombres, apellidos, fecha_nacimiento, edad, sexo, codigo_estudiante, año_estudio, tipo_usuario_id, facultad_id, escuela_id, modalidad_id, registro_modalidad, celular, correo, direccion, activo, fecha_registro)
            SELECT 
                p.id, p.dni, p.nombres, p.apellidos, p.fecha_nacimiento, p.edad, p.sexo, p.codigo_estudiante, p.año_estudio, p.tipo_usuario_id, p.facultad_id, p.escuela_id,
                (SELECT a.modalidad_id FROM atenciones_old_mod a WHERE a.persona_id = p.id ORDER BY a.id DESC LIMIT 1) as modalidad_id,
                (SELECT a.registro_modalidad FROM atenciones_old_mod a WHERE a.persona_id = p.id ORDER BY a.id DESC LIMIT 1) as registro_modalidad,
                p.celular, p.correo, p.direccion, p.activo, p.fecha_registro
            FROM personas_old_mod p;
        """)
        print(f"      {cursor.rowcount} personas insertadas exitosamente.")

        # B. Migrar Atenciones (ya sin los campos de modalidad)
        print("   -> Migrando historial de Atenciones...")
        cursor.execute("""
            INSERT INTO atenciones (id, persona_id, fecha_atencion, caso_social_id, observaciones, activo, fecha_registro)
            SELECT 
                id, persona_id, fecha_atencion, caso_social_id, observaciones, activo, fecha_registro
            FROM atenciones_old_mod;
        """)
        print(f"      {cursor.rowcount} atenciones insertadas exitosamente.")

        # 5. Limpieza Final
        print("5. Borrando tablas temporales (_old_mod)...")
        cursor.execute("DROP TABLE personas_old_mod")
        cursor.execute("DROP TABLE atenciones_old_mod")

        conn.commit()
        print("\n¡MIGRACIÓN DE MODALIDAD COMPLETADA EXITOSAMENTE! 🎉")

    except Exception as e:
        print(f"\n❌ Error durante la migración: {e}")
        conn.rollback()
        print("Se han revertido los cambios en la base de datos (Rollback).")
    finally:
        conn.close()

if __name__ == "__main__":
    run_migration()
