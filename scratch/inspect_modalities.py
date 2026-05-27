import os
import sys

# Añadir el directorio raíz al path de Python
sys.path.append(os.getcwd())

from database.db_config import SessionLocal
from database.models import Persona, CatModalidad

def inspect():
    db = SessionLocal()
    try:
        results = db.query(Persona.activo, CatModalidad.nombre, Persona.modalidad_id).outerjoin(CatModalidad, Persona.modalidad_id == CatModalidad.id).all()
        print(f"Total rows in Persona table: {len(results)}")
        
        counts = {}
        for activo, mod_nombre, mod_id in results:
            key = (activo, mod_nombre or "Unknown", mod_id)
            counts[key] = counts.get(key, 0) + 1
            
        print("\nActive/Inactive status by modality:")
        for (activo, mod_nombre, mod_id), count in sorted(counts.items()):
            status = "Active" if activo else "Inactive"
            print(f"Status: {status:8} | Modality: {mod_nombre:20} (ID: {mod_id}) | Count: {count}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    inspect()
