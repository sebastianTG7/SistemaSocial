"""
Script de migración: Elimina la restricción UNIQUE del campo DNI en la tabla personas.
En SQLite no se puede ALTER una restricción, así que se recrea la tabla completa.
"""
import sqlite3
import os

DB_PATH = "database/servicio_social.db"

def migrar():
    print("🔧 Iniciando migración segura...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Verificar si ya existe la restricción UNIQUE en DNI
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='personas'")
    schema_actual = cursor.fetchone()[0]
    print(f"📋 Schema actual:\n{schema_actual}\n")
    
    if "UNIQUE" not in schema_actual.upper() or "dni" not in schema_actual.lower():
        print("✅ No se encontró restricción UNIQUE en dni. No se necesita migración.")
        conn.close()
        return
    
    print("⚠️  Restricción UNIQUE detectada en dni. Procediendo a migrar...")
    
    try:
        conn.execute("BEGIN")
        
        # 2. Crear tabla temporal con el schema correcto (sin UNIQUE en dni)
        cursor.execute("""
            CREATE TABLE personas_nueva (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dni VARCHAR(20) NOT NULL,
                nombres VARCHAR(100) NOT NULL,
                apellidos VARCHAR(100) NOT NULL,
                edad INTEGER,
                sexo VARCHAR(1),
                fecha_atencion DATETIME NOT NULL,
                codigo_estudiante VARCHAR(20),
                año_estudio VARCHAR(10),
                tipo_usuario_id INTEGER REFERENCES cat_tipos_usuario(id),
                facultad_id INTEGER REFERENCES cat_facultades(id),
                escuela_id INTEGER REFERENCES cat_escuelas(id),
                caso_social_id INTEGER REFERENCES cat_casos_sociales(id),
                celular VARCHAR(20),
                correo VARCHAR(100),
                direccion VARCHAR(200),
                observaciones TEXT,
                activo BOOLEAN DEFAULT 1,
                fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 3. Copiar TODOS los datos de la tabla vieja a la nueva
        cursor.execute("""
            INSERT INTO personas_nueva 
            SELECT id, dni, nombres, apellidos, edad, sexo, fecha_atencion,
                   codigo_estudiante, año_estudio, tipo_usuario_id, facultad_id,
                   escuela_id, caso_social_id, celular, correo, direccion,
                   observaciones, activo, fecha_registro
            FROM personas
        """)
        
        filas_copiadas = cursor.rowcount
        print(f"📊 Registros copiados: {filas_copiadas}")
        
        # 4. Eliminar tabla vieja y renombrar la nueva
        cursor.execute("DROP TABLE personas")
        cursor.execute("ALTER TABLE personas_nueva RENAME TO personas")
        
        # 5. Recrear el índice normal en dni (sin UNIQUE)
        cursor.execute("CREATE INDEX IF NOT EXISTS ix_personas_dni ON personas (dni)")
        
        conn.commit()
        print("✅ Migración completada exitosamente.")
        print("✅ Ahora puedes registrar múltiples atenciones para el mismo DNI.")
        
    except Exception as ex:
        conn.rollback()
        print(f"❌ Error durante la migración: {ex}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrar()
