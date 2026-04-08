import sqlite3
import os

DB_PATH = "database/servicio_social.db"

def diagnostico():
    print(f"📂 Verificando base de datos: {DB_PATH}")
    if not os.path.exists(DB_PATH):
        print("❌ Error: ¡No se encontró el archivo de la base de datos!")
        return
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Ver todas las tablas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"📊 Tablas encontradas: {[t[0] for t in tables]}")
    
    # 2. Ver esquema de personas
    cursor.execute("SELECT sql FROM sqlite_master WHERE name='personas'")
    schema = cursor.fetchone()
    print(f"📝 Esquema de 'personas':\n{schema[0] if schema else 'NO ENCONTRADO'}")
    
    # 3. Ver indices
    cursor.execute("PRAGMA index_list(personas)")
    indices = cursor.fetchall()
    print("📋 REPORTE DE ÍNDICES:")
    if not indices:
        print("   (No hay índices específicos en esta tabla)")
    for idx in indices:
        name = idx[1]
        is_unique = idx[2]
        
        cursor.execute(f"PRAGMA index_info({name})")
        info = cursor.fetchall()
        cols = [i[2] for i in info]
        
        print(f"   -> Índice: '{name}' | Columnas: {cols} | Es Único?: {'SÍ' if is_unique else 'NO'}")
    
    conn.close()

if __name__ == "__main__":
    diagnostico()
