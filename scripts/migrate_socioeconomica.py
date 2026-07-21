import sqlite3
import shutil
import os
from datetime import datetime
import sys

# Agregar el directorio raíz al path para importar database.db_config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

DB_PATH = 'database/servicio_social.db'
BACKUP_PATH = f'database/servicio_social_backup_socioeconomica_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'

def run_migration():
    if not os.path.exists(DB_PATH):
        print(f"Error: Base de datos no encontrada en {DB_PATH}")
        return

    # 1. Crear Backup
    print("1. Creando backup de seguridad...")
    shutil.copy2(DB_PATH, BACKUP_PATH)
    print(f"   Backup creado en: {BACKUP_PATH}")

    # 2. Renombrar tabla antigua
    print("2. Renombrando tabla antigua...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("DROP INDEX IF EXISTS ix_fichas_socioeconomicas_id")
        cursor.execute("ALTER TABLE fichas_socioeconomicas RENAME TO fichas_socioeconomicas_old")
        conn.commit()
    except sqlite3.OperationalError as e:
        print(f"   Nota: La tabla podría estar ya renombrada o no existe. Detalle: {e}")
    conn.close()

    # 3. Crear las nuevas tablas usando SQLAlchemy
    print("3. Creando el nuevo esquema de la tabla fichas_socioeconomicas...")
    from database.db_config import engine, Base
    from database.models import FichaSocioeconomica
    Base.metadata.create_all(bind=engine)
    print("   Nueva tabla creada correctamente.")

    # 4. Migrar los Datos (Consultas SQL)
    print("4. Migrando datos a la nueva tabla...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO fichas_socioeconomicas (
                id, persona_id, motivo_evaluacion, sisfoh_condicion, 
                tiene_discapacidad, tipo_discapacidad, nivel_de_discapacidad, 
                tipo_seguro, estructura_familiar, dinamica_familiar,
                ingreso_economico_miembros, ingreso_becas, ingreso_otros,
                egreso_agua, egreso_luz, egreso_educacion_pasajes,
                egreso_alimentacion, egreso_alquiler,
                estudiante_trabaja, lugar_trabajo, remuneracion_estudiante,
                tipo_vivienda, material_paredes, material_techo,
                tiene_agua_red, tiene_desague_red, tiene_energia_electrica
            )
            SELECT 
                id, persona_id, motivo_evaluacion, sisfoh_condicion, 
                tiene_discapacidad, tipo_discapacidad, nivel_de_discapacidad, 
                tipo_seguro, estructura_familiar, dinamica_familiar,
                ingreso_familiar_total, ingreso_becas_bonos, 0.0,
                0.0, egreso_servicios, egreso_educacion_otros,
                egreso_alimentacion, egreso_alquiler,
                'No', '', 0.0,
                tipo_vivienda, material_paredes, material_techo,
                tiene_agua_red, tiene_desague_red, tiene_energia_electrica
            FROM fichas_socioeconomicas_old;
        """)
        print(f"      {cursor.rowcount} fichas socioeconómicas migradas exitosamente.")

        # 5. Limpieza Final
        print("5. Borrando tabla temporal (_old)...")
        cursor.execute("DROP TABLE fichas_socioeconomicas_old")

        conn.commit()
        print("\nMIGRACION COMPLETADA EXITOSAMENTE!")

    except Exception as e:
        print(f"\nError durante la migracion: {e}")
        conn.rollback()
        print("Se han revertido los cambios en la base de datos (Rollback).")
    finally:
        conn.close()

if __name__ == "__main__":
    run_migration()
