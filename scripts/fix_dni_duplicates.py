import sqlite3

DB_PATH = "database/servicio_social.db"

def reparar_indices():
    print(f"🔧 Reparando índices en: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # 1. Borrar el índice único que bloquea todo
        print("🗑️  Borrando índice único de DNI...")
        cursor.execute("DROP INDEX IF EXISTS ix_personas_dni")
        
        # 2. Crear el nuevo índice que permite duplicados (para el historial)
        print("🏗️  Creando nuevo índice de DNI (permitiendo duplicados)...")
        cursor.execute("CREATE INDEX ix_personas_dni ON personas (dni)")
        
        conn.commit()
        print("✅ ¡ÉXITO! La base de datos ahora permite registrar a la misma persona varias veces.")
        
    except Exception as ex:
        conn.rollback()
        print(f"❌ Error al reparar los índices: {ex}")
    finally:
        conn.close()

if __name__ == "__main__":
    reparar_indices()
