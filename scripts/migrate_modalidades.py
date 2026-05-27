import sqlite3
import os

def run_migration():
    print("Iniciando migracion para incorporar Modalidades de Ingreso...")
    db_path = "database/servicio_social.db"
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. Crear tabla cat_modalidades si no existe
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cat_modalidades (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nombre VARCHAR(50) NOT NULL UNIQUE,
        activo BOOLEAN DEFAULT 1
    )
    """)
    print("  [OK] Tabla 'cat_modalidades' creada o verificada.")
    
    # 2. Insertar las 7 modalidades por defecto si la tabla está vacía
    cursor.execute("SELECT COUNT(*) FROM cat_modalidades")
    if cursor.fetchone()[0] == 0:
        modalidades = [
            "General",
            "CEPREVAL",
            "Discapacidad",
            "Violencia Politica",
            "Hijos de Campesinos",
            "Primeros Puestos",
            "Deportista Calificado"
        ]
        for m in modalidades:
            cursor.execute("INSERT INTO cat_modalidades (nombre, activo) VALUES (?, 1)", (m,))
        conn.commit()
        print("  [OK] Modalidades iniciales insertadas.")
    
    # Obtener el ID de la modalidad 'General'
    cursor.execute("SELECT id FROM cat_modalidades WHERE nombre = 'General'")
    general_id = cursor.fetchone()[0]

    # 3. Alterar tabla personas para agregar columnas 'modalidad_id' y 'registro_modalidad'
    # Agregamos modalidad_id
    try:
        cursor.execute("ALTER TABLE personas ADD COLUMN modalidad_id INTEGER REFERENCES cat_modalidades(id)")
        print("  [OK] Columna 'modalidad_id' agregada a la tabla 'personas'.")
    except sqlite3.OperationalError:
        print("  [INFO] La columna 'modalidad_id' ya existe en la tabla 'personas'.")

    # Agregamos registro_modalidad
    try:
        cursor.execute("ALTER TABLE personas ADD COLUMN registro_modalidad TEXT")
        print("  [OK] Columna 'registro_modalidad' agregada a la tabla 'personas'.")
    except sqlite3.OperationalError:
        print("  [INFO] La columna 'registro_modalidad' ya existe en la tabla 'personas'.")
        
    # 4. Actualizar todos los registros existentes que tengan modalidad_id NULL a general_id
    cursor.execute("UPDATE personas SET modalidad_id = ? WHERE modalidad_id IS NULL", (general_id,))
    conn.commit()
    print(f"  [OK] Todos los registros previos actualizados por defecto a la modalidad 'General' (ID: {general_id}).")
    
    conn.close()
    print("Migracion completada con exito.")

if __name__ == "__main__":
    run_migration()
