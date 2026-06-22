import sqlite3

def run_migration():
    print("Iniciando migración para incorporar Nivel de Discapacidad...")
    db_path = "database/servicio_social.db"
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Agregar columna nivel_de_discapacidad a la tabla fichas_socioeconomicas
    try:
        cursor.execute("ALTER TABLE fichas_socioeconomicas ADD COLUMN nivel_de_discapacidad VARCHAR(50)")
        conn.commit()
        print("  [OK] Columna 'nivel_de_discapacidad' agregada a 'fichas_socioeconomicas'.")
    except sqlite3.OperationalError:
        print("  [INFO] La columna 'nivel_de_discapacidad' ya existe en 'fichas_socioeconomicas'.")
        
    # Inicializar con 'Ninguno' para los registros existentes que no tengan valor
    cursor.execute("UPDATE fichas_socioeconomicas SET nivel_de_discapacidad = 'Ninguno' WHERE nivel_de_discapacidad IS NULL")
    conn.commit()
    print("  [OK] Registros existentes actualizados por defecto a 'Ninguno'.")
    
    conn.close()
    print("Migración completada con éxito.")

if __name__ == "__main__":
    run_migration()
