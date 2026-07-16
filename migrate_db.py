import sqlite3
import shutil
import os
from datetime import datetime

# Definir rutas
DB_PATH = 'database/servicio_social.db'
BACKUP_PATH = f'database/servicio_social_backup_migration_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'

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
    
    # Manejar caso si el script falla y se vuelve a correr
    try:
        # Drop old indexes so SQLAlchemy can recreate them without conflict
        cursor.execute("DROP INDEX IF EXISTS ix_personas_dni")
        cursor.execute("DROP INDEX IF EXISTS ix_personas_id")
        cursor.execute("DROP INDEX IF EXISTS ix_fichas_derivacion_id")
        
        cursor.execute("ALTER TABLE personas RENAME TO personas_old")
        cursor.execute("ALTER TABLE fichas_derivacion RENAME TO fichas_derivacion_old")
        conn.commit()
    except sqlite3.OperationalError as e:
        print(f"   Nota: Las tablas podrían estar ya renombradas o no existen. Detalle: {e}")
    conn.close()

    # 3. Crear las nuevas tablas usando SQLAlchemy
    print("3. Creando el nuevo esquema de la base de datos mediante SQLAlchemy...")
    from database.db_config import engine, Base
    from database.models import Persona, Atencion, FichaDerivacion
    # Esto creará las tablas personas, atenciones, y fichas_derivacion con sus nuevas estructuras
    Base.metadata.create_all(bind=engine)
    print("   Nuevas tablas creadas correctamente.")

    # 4. Migrar los Datos (Consultas SQL)
    print("4. Migrando datos a las nuevas tablas...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # A. Migrar Personas Únicas (manteniendo el último registro por DNI)
        print("   -> Insertando Personas Únicas...")
        cursor.execute("""
            INSERT INTO personas (id, dni, nombres, apellidos, edad, sexo, codigo_estudiante, año_estudio, tipo_usuario_id, facultad_id, escuela_id, celular, correo, direccion, activo, fecha_registro)
            SELECT id, dni, nombres, apellidos, edad, sexo, codigo_estudiante, año_estudio, tipo_usuario_id, facultad_id, escuela_id, celular, correo, direccion, activo, fecha_registro
            FROM personas_old p1
            WHERE id = (SELECT MAX(id) FROM personas_old p2 WHERE p2.dni = p1.dni);
        """)
        print(f"      {cursor.rowcount} personas insertadas exitosamente.")

        # B. Migrar Atenciones
        print("   -> Generando historial de Atenciones...")
        cursor.execute("""
            INSERT INTO atenciones (id, persona_id, fecha_atencion, caso_social_id, modalidad_id, registro_modalidad, observaciones, activo, fecha_registro)
            SELECT 
                p1.id as id, 
                (SELECT MAX(p2.id) FROM personas_old p2 WHERE p2.dni = p1.dni) as persona_id,
                p1.fecha_atencion, 
                p1.caso_social_id, 
                p1.modalidad_id, 
                p1.registro_modalidad, 
                p1.observaciones, 
                p1.activo, 
                p1.fecha_registro
            FROM personas_old p1;
        """)
        print(f"      {cursor.rowcount} atenciones insertadas exitosamente.")

        # C. Migrar Fichas de Derivación (ahora vinculadas a la atención)
        print("   -> Migrando Fichas de Derivación...")
        cursor.execute("""
            INSERT INTO fichas_derivacion (id, atencion_id, lugar_nacimiento, ocupacion, vive_con, telefono_familiares, area_deriva, area_derivada, fecha_derivacion, motivo_consulta, tiene_derivaciones_previas, detalle_derivaciones_previas, condicion, impacto_academico, impacto_social, impacto_familiar, impacto_personal, diagnostico, observaciones)
            SELECT id, persona_id, lugar_nacimiento, ocupacion, vive_con, telefono_familiares, area_deriva, area_derivada, fecha_derivacion, motivo_consulta, tiene_derivaciones_previas, detalle_derivaciones_previas, condicion, impacto_academico, impacto_social, impacto_familiar, impacto_personal, diagnostico, observaciones
            FROM fichas_derivacion_old;
        """)
        print(f"      {cursor.rowcount} fichas de derivación insertadas exitosamente.")

        # D. Recuperar fecha_nacimiento hacia la tabla de personas
        print("   -> Rescatando fecha de nacimiento a la tabla personas...")
        cursor.execute("""
            UPDATE personas
            SET fecha_nacimiento = (
                SELECT f.fecha_nacimiento 
                FROM fichas_derivacion_old f 
                JOIN atenciones a ON a.id = f.persona_id
                WHERE a.persona_id = personas.id
                AND f.fecha_nacimiento IS NOT NULL
                LIMIT 1
            );
        """)
        print(f"      Fechas de nacimiento recuperadas.")
        
        # E. Ajustar Fichas Socioeconómicas al nuevo persona_id unificado
        print("   -> Ajustando IDs en Fichas Socioeconómicas...")
        cursor.execute("""
            UPDATE fichas_socioeconomicas
            SET persona_id = (
                SELECT MAX(p2.id) 
                FROM personas_old p2 
                WHERE p2.dni = (
                    SELECT dni FROM personas_old p1 WHERE p1.id = fichas_socioeconomicas.persona_id
                )
            );
        """)
        print(f"      Fichas Socioeconómicas conectadas a la Persona única.")

        # 5. Limpieza Final
        print("5. Borrando tablas temporales (_old)...")
        cursor.execute("DROP TABLE personas_old")
        cursor.execute("DROP TABLE fichas_derivacion_old")

        conn.commit()
        print("\n¡MIGRACIÓN COMPLETADA EXITOSAMENTE! 🎉")

    except Exception as e:
        print(f"\n❌ Error durante la migración: {e}")
        conn.rollback()
        print("Se han revertido los cambios en la base de datos (Rollback).")
    finally:
        conn.close()


if __name__ == "__main__":
    run_migration()
